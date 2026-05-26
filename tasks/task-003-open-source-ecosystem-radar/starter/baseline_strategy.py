#!/usr/bin/env python3
"""
Baseline Strategy — Task 003: Open Source Ecosystem Radar

Simple baseline that:
  1. Loads processed aggregation files (top repos by event type, distributions)
  2. Formats them as a structured prompt
  3. Calls an LLM to produce a developer-focused analysis
  4. Writes answer.json

This baseline is more tractable than Tasks 001 and 002 because:
  - The aggregation step (prepare.py) handles the large event volume
  - Processed outputs fit easily in an LLM context window
  - The analysis question is more structured

Expected score: ~62/100 with 2-hour sample data.
Improves significantly with more data (1 week → ~78/100).

Usage:
    python baseline_strategy.py
    python baseline_strategy.py --dry-run
    python baseline_strategy.py --model claude-3-sonnet-20240229
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_INPUT_DIR = Path("data/processed/task-003-open-source-ecosystem-radar")
DEFAULT_SAMPLE_INPUT_DIR = Path("data/samples/task-003-open-source-ecosystem-radar")
DEFAULT_OUTPUT = Path("submissions/my-submission/task-003-open-source-ecosystem-radar/answer.json")

ATTRIBUTION = "Data source: GH Archive (https://www.gharchive.org/) — CC BY 4.0"


def load_json(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def load_jsonl(path: Path, n: int = None) -> List[Dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
                if n and len(records) >= n:
                    break
            except json.JSONDecodeError:
                continue
    return records


def format_top_repos(repos: List[Dict], n: int = 20) -> str:
    """Format top-N repos as a readable list."""
    lines = []
    for r in repos[:n]:
        unique_actors = r.get("unique_actors", "?")
        lines.append(
            f"  #{r['rank']:2d}  {r['repo']:<50s}  {r['count']:6,}  ({unique_actors} unique actors)"
        )
    return "\n".join(lines)


def format_event_distribution(dist: Dict) -> str:
    """Format event type distribution as a table."""
    total = dist.get("total", 1)
    lines = []
    for item in dist.get("distribution", [])[:15]:
        et = item["event_type"]
        count = item["count"]
        pct = count / total * 100
        lines.append(f"  {et:<35s}  {count:9,}  ({pct:.1f}%)")
    return "\n".join(lines)


def format_hourly_counts(hourly: Dict) -> str:
    """Format hourly event counts."""
    hours = hourly.get("hourly", [])
    if not hours:
        return "  (no data)"
    lines = [f"  {h['hour']:25s}  {h['count']:9,} events" for h in hours]
    return "\n".join(lines)


def build_prompt(
    top_stars: Dict,
    top_forks: Dict,
    top_pushes: Dict,
    top_prs: Dict,
    event_dist: Dict,
    hourly: Dict,
    repo_details: List[Dict],
    stats: Dict,
) -> str:
    """Build the analysis prompt from aggregated GH Archive data."""

    hours = stats.get("hours_covered", "?")
    time_start = stats.get("time_range_approx", {}).get("start", "?")
    time_end = stats.get("time_range_approx", {}).get("end", "?")
    total_events = stats.get("total_events", 0)
    unique_repos = stats.get("unique_repos", 0)

    # Determine caveat level based on data size
    if hours <= 2:
        trend_caveat = "CRITICAL: Only {hours} hours of data. NO trend claims are possible. This is a snapshot only.".format(hours=hours)
    elif hours <= 24:
        trend_caveat = f"CAUTION: Only {hours} hours of data. Trend claims are weak — at most 'interpretation' type."
    elif hours <= 168:
        trend_caveat = f"NOTE: {hours} hours ({hours//24} days) of data. Weak trend claims possible as 'interpretation'."
    else:
        trend_caveat = f"NOTE: {hours} hours ({hours//24} days) of data. Trend claims with appropriate confidence possible."

    prompt = f"""You are a developer ecosystem analyst. Analyze the GH Archive event data below
and produce a structured report for developers.

{ATTRIBUTION}

DATA WINDOW: {time_start} to {time_end} ({hours} hours, {total_events:,} total events, {unique_repos:,} unique repos)

{trend_caveat}

---

EVENT TYPE DISTRIBUTION:
{format_event_distribution(event_dist)}

HOURLY ACTIVITY:
{format_hourly_counts(hourly)}

TOP 20 BY STARS (WatchEvent):
  Repo                                               Stars  Unique Actors
{format_top_repos((top_stars or {}).get("repos", []))}

TOP 20 BY FORKS (ForkEvent):
  Repo                                               Forks  Unique Actors
{format_top_repos((top_forks or {}).get("repos", []))}

TOP 20 BY PUSHES (PushEvent):
  Repo                                               Pushes  Unique Actors
{format_top_repos((top_pushes or {}).get("repos", []))}

TOP 20 BY PULL REQUESTS (PullRequestEvent):
  Repo                                               PRs    Unique Actors
{format_top_repos((top_prs or {}).get("repos", []))}

---

INSTRUCTIONS:
1. Base all claims on the data above. Do not use prior knowledge about repo popularity.
2. Label every claim: "fact" (in the data), "interpretation" (inference), "uncertainty"
3. Add time_window_caveat to any trend or growth claim
4. Use correct event type names: WatchEvent, ForkEvent, PushEvent, PullRequestEvent, etc.
5. Format repos as org/repo (e.g., microsoft/vscode)
6. Stars (WatchEvent) in a short window are noisy — note this explicitly
7. A repo with many pushes + few unique actors has concentration risk — mention this

Return a JSON object matching the task-003-open-source-ecosystem-radar schema:
{{
  "task_id": "task-003-open-source-ecosystem-radar",
  "participant_id": "my-submission",
  "title": "Open Source Ecosystem Radar — {time_start}",
  "attribution": "{ATTRIBUTION}",
  "data_window": {{
    "start": "{time_start}",
    "end": "{time_end}",
    "hours_covered": {hours},
    "files_processed": {stats.get("files_processed", 0)},
    "total_events": {total_events}
  }},
  "executive_summary": "...",
  "sections": [
    {{"id": "executive-summary", "title": "Executive Summary", "content": "..."}},
    {{"id": "dataset-scope", "title": "Dataset Scope", "content": "..."}},
    {{"id": "ecosystem-trends", "title": "Ecosystem Trends", "content": "..."}},
    {{"id": "repositories-heating-up", "title": "Repositories Heating Up", "content": "..."}},
    {{"id": "repositories-cooling-down", "title": "Repositories Cooling Down", "content": "..."}},
    {{"id": "maintainer-contributor-concentration-risk", "title": "Concentration Risk", "content": "..."}},
    {{"id": "event-timeline", "title": "Event Timeline", "content": "..."}},
    {{"id": "evidence-backed-claims", "title": "Evidence-Backed Claims", "content": "..."}},
    {{"id": "caveats-and-data-limitations", "title": "Caveats", "content": "..."}},
    {{"id": "context-engineering-strategy", "title": "Context Engineering Strategy", "content": "..."}}
  ],
  "claims": [...],
  "evidence": [...],
  "top_repos": {{
    "by_stars": [...],
    "by_forks": [...],
    "by_pushes": [...]
  }},
  "event_distribution": {{...}},
  "limitations": [...]
}}
"""
    return prompt


def call_llm(prompt: str, model: str) -> str:
    """Call an LLM API."""
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic not installed. Run: uv pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    print(f"  Calling {model} (~{len(prompt)//4:,} est. tokens)...")
    start = time.time()
    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.time() - start
    print(f"  Done in {elapsed:.1f}s | in={resp.usage.input_tokens} out={resp.usage.output_tokens}")
    return resp.content[0].text


def parse_response(raw: str) -> Dict:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        raw = "\n".join(lines[start:end])
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "task_id": "task-003-open-source-ecosystem-radar",
            "title": "Parse error",
            "executive_summary": f"ERROR: {e}",
            "sections": [],
            "claims": [],
            "evidence": [],
            "top_repos": {},
            "limitations": [{"description": f"LLM parse error: {e}"}],
        }


def main():
    parser = argparse.ArgumentParser(description="Baseline strategy for Task 003")
    parser.add_argument("--input-dir", type=Path, default=None)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default="claude-3-haiku-20240307")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Auto-detect input
    if args.input_dir is None:
        if DEFAULT_SAMPLE_INPUT_DIR.exists():
            args.input_dir = DEFAULT_SAMPLE_INPUT_DIR
        elif DEFAULT_INPUT_DIR.exists():
            args.input_dir = DEFAULT_INPUT_DIR
        else:
            print("ERROR: No processed data found. Run prepare.py first.")
            sys.exit(1)

    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_file}")
    print()

    # Load data
    top_stars = load_json(args.input_dir / "top_repos_by_stars.json")
    top_forks = load_json(args.input_dir / "top_repos_by_forks.json")
    top_pushes = load_json(args.input_dir / "top_repos_by_pushes.json")
    top_prs = load_json(args.input_dir / "top_repos_by_prs.json")
    event_dist = load_json(args.input_dir / "event_type_distribution.json")
    hourly = load_json(args.input_dir / "hourly_event_counts.json")
    stats = load_json(args.input_dir / "dataset_stats.json") or {}
    repo_details = load_jsonl(args.input_dir / "repo_event_details.jsonl", 50)

    if top_stars is None:
        print("WARNING: No top_repos_by_stars.json found. Run prepare.py first.")

    prompt = build_prompt(top_stars, top_forks, top_pushes, top_prs, event_dist or {}, hourly or {}, repo_details, stats)
    print(f"  Prompt: ~{len(prompt)//4:,} tokens")

    if args.dry_run:
        print("\n--- PROMPT (first 2000 chars) ---")
        print(prompt[:2000])
        return

    raw = call_llm(prompt, args.model)
    answer = parse_response(raw)
    answer["task_id"] = "task-003-open-source-ecosystem-radar"
    answer["attribution"] = ATTRIBUTION
    answer["submitted_at"] = datetime.utcnow().isoformat() + "Z"

    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(answer, f, indent=2, ensure_ascii=False)
    print(f"\nAnswer written: {args.output_file}")
    print(f"  Claims: {len(answer.get('claims', []))}")
    print(f"  Evidence: {len(answer.get('evidence', []))}")


if __name__ == "__main__":
    main()
