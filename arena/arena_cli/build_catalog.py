"""Build the site's catalog JSON files from tasks and submissions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import (
    ContextTrace,
    DataManifest,
    Participant,
    Score,
    SubmissionCatalogEntry,
    Task,
    TaskCatalogEntry,
    LeaderboardEntry,
)
from .utils import (
    get_site_data_dir,
    get_submissions_dir,
    get_tasks_dir,
    load_json,
    load_yaml,
    participant_ids,
    task_ids,
)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_tasks() -> list[dict]:
    """Load all task.yaml files and return full task dicts for the site catalog."""
    tasks_dir = get_tasks_dir()
    results: list[dict] = []

    for tid in task_ids():
        task_path = tasks_dir / tid
        yaml_path = task_path / "task.yaml"
        if not yaml_path.exists():
            continue

        try:
            raw = load_yaml(yaml_path)
        except Exception:
            continue

        # Check for sample availability in data_manifest
        has_sample = False
        manifest_path = task_path / "data_manifest.yaml"
        if manifest_path.exists():
            try:
                raw_manifest = load_yaml(manifest_path)
                manifest = DataManifest.model_validate(raw_manifest)
                has_sample = any(s.sample_available for s in manifest.sources)
            except Exception:
                pass

        # Build full catalog entry preserving all task fields
        entry = {
            "id": raw.get("id", tid),
            "title": raw.get("title", ""),
            "short_description": raw.get("short_description", ""),
            "long_description": raw.get("long_description", ""),
            "benchmark_question": raw.get("benchmark_question", ""),
            "domain": raw.get("domain", ""),
            "difficulty": raw.get("difficulty", "medium"),
            "tags": raw.get("tags", []),
            "dataset": raw.get("dataset", {}),
            "outputs": raw.get("outputs", {}),
            "scoring": raw.get("scoring", {}),
            "safety": raw.get("safety", {}),
            "has_sample": has_sample,
            "num_submissions": 0,  # filled in by build_leaderboard
            "top_score": None,      # filled in by build_leaderboard
        }
        results.append(entry)

    return results


def load_submissions() -> list[dict]:
    """Load all answer.json + context_trace.json + optional score.json.

    Returns a list of SubmissionCatalogEntry dicts.
    """
    submissions_dir = get_submissions_dir()
    results: list[dict] = []

    for pid in participant_ids():
        participant_path = submissions_dir / pid

        # Load participant metadata
        participant_yaml = participant_path / "participant.yaml"
        display_name = pid
        participant_type = "team"
        if participant_yaml.exists():
            try:
                raw_p = load_yaml(participant_yaml)
                p = Participant.model_validate(raw_p)
                display_name = p.display_name
                participant_type = p.type
            except Exception:
                pass

        # Iterate submission sub-folders
        for sub_dir in sorted(participant_path.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name.startswith("."):
                continue

            task_id = sub_dir.name
            answer_path = sub_dir / "answer.json"
            trace_path = sub_dir / "context_trace.json"
            score_path = sub_dir / "score.json"

            if not answer_path.exists():
                continue

            # Load context trace
            raw_trace: dict = {}
            methods: dict[str, bool] = {}
            context_stats: dict[str, Any] = {}
            submitted_at: str | None = None

            if trace_path.exists():
                try:
                    raw_trace = load_json(trace_path)
                    methods = raw_trace.get("methods", {})
                    context_stats = raw_trace.get("context_stats", {})
                except Exception:
                    pass

            # Load answer
            raw_answer: dict = {}
            try:
                raw_answer = load_json(answer_path)
                submitted_at_raw = raw_answer.get("submitted_at")
                if submitted_at_raw:
                    submitted_at = str(submitted_at_raw)
            except Exception:
                pass

            # Load score if available
            overall_score: float | None = None
            raw_score: dict = {}
            if score_path.exists():
                try:
                    raw_score = load_json(score_path)
                    score_obj = Score.model_validate(raw_score)
                    overall_score = score_obj.overall_score
                except Exception:
                    pass

            entry = {
                "task_id": task_id,
                "participant_id": pid,
                "participant": {
                    "id": pid,
                    "display_name": display_name,
                    "type": participant_type,
                },
                "participant_display_name": display_name,
                "participant_type": participant_type,
                "methods": methods,
                "overall_score": overall_score,
                "rank": None,  # filled in by build_leaderboard
                "submitted_at": submitted_at,
                "context_stats": context_stats,
                "answer": raw_answer,
                "context_trace": raw_trace,
                "score": raw_score if raw_score else None,
            }
            results.append(entry)

    return results


# ---------------------------------------------------------------------------
# Leaderboard builder
# ---------------------------------------------------------------------------


def build_leaderboard(tasks: list[dict], submissions: list[dict]) -> list[dict]:
    """For each task, rank submissions by overall_score (descending).

    Submissions without a score are listed last.
    Returns a list of LeaderboardEntry dicts.
    """
    # Build a task lookup
    task_lookup: dict[str, dict] = {t["id"]: t for t in tasks}

    # Group submissions by task
    subs_by_task: dict[str, list[dict]] = {}
    for sub in submissions:
        tid = sub["task_id"]
        subs_by_task.setdefault(tid, []).append(sub)

    leaderboard: list[dict] = []

    for tid, task_dict in task_lookup.items():
        task_subs = subs_by_task.get(tid, [])

        # Sort: scored submissions first (descending), then unscored
        scored = sorted(
            [s for s in task_subs if s.get("overall_score") is not None],
            key=lambda x: x["overall_score"],
            reverse=True,
        )
        unscored = [s for s in task_subs if s.get("overall_score") is None]

        ranked: list[dict] = []
        for rank_idx, sub in enumerate(scored, start=1):
            sub_copy = dict(sub)
            sub_copy["rank"] = rank_idx
            ranked.append(sub_copy)
        for sub in unscored:
            sub_copy = dict(sub)
            sub_copy["rank"] = None
            ranked.append(sub_copy)

        entry = {
            "task_id": tid,
            "task_title": task_dict["title"],
            "domain": task_dict["domain"],
            "difficulty": task_dict["difficulty"],
            "rankings": [
                {
                    "rank": r.get("rank"),
                    "participant_id": r["participant_id"],
                    "participant_display_name": r["participant_display_name"],
                    "overall_score": r.get("overall_score"),
                    "scored_by": r.get("score", {}).get("scored_by", "manual") if r.get("score") else "manual",
                }
                for r in ranked
            ],
        }
        leaderboard.append(entry)

    # Annotate tasks with num_submissions and top_score (update the tasks list in-place)
    for task_dict in tasks:
        tid = task_dict["id"]
        task_subs = subs_by_task.get(tid, [])
        task_dict["num_submissions"] = len(task_subs)
        scored_scores = [
            s["overall_score"]
            for s in task_subs
            if s.get("overall_score") is not None
        ]
        task_dict["top_score"] = max(scored_scores) if scored_scores else None

    return leaderboard


# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str, ensure_ascii=False)


def write_site_data(
    tasks: list[dict],
    submissions: list[dict],
    leaderboard: list[dict],
) -> None:
    """Write tasks.json, submissions.json, and leaderboard.json to the site data directory."""
    out_dir = get_site_data_dir()
    _write_json(out_dir / "tasks.json", tasks)
    _write_json(out_dir / "submissions.json", submissions)
    _write_json(out_dir / "leaderboard.json", leaderboard)
    print(f"  tasks.json          -> {out_dir / 'tasks.json'}")
    print(f"  submissions.json    -> {out_dir / 'submissions.json'}")
    print(f"  leaderboard.json    -> {out_dir / 'leaderboard.json'}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def build_catalog() -> None:
    """Main entry point: load all data, build leaderboard, write JSON files."""
    tasks = load_tasks()
    submissions = load_submissions()
    leaderboard = build_leaderboard(tasks, submissions)
    write_site_data(tasks, submissions, leaderboard)
    print(f"Catalog built: {len(tasks)} tasks, {len(submissions)} submissions")
