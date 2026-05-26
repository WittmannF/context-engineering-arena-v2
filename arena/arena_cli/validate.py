"""Validation functions for tasks, participants, and submissions."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError
from rich.console import Console

from .schemas import Answer, ContextTrace, DataManifest, Participant, Task
from .utils import (
    find_repo_root,
    get_submissions_dir,
    get_tasks_dir,
    load_json,
    load_yaml,
    participant_ids,
    task_ids,
)

console = Console()

# ---------------------------------------------------------------------------
# Task validation
# ---------------------------------------------------------------------------

_TASK_REQUIRED_FILES = [
    "task.yaml",
    "README.md",
    "rubric.md",
    "data_manifest.yaml",
    "expected_answer_schema.json",
    "scripts/download.py",
    "scripts/prepare.py",
]


def validate_task(task_path: Path) -> list[str]:
    """Validate a task folder.

    Returns a list of error strings; an empty list means the task is valid.
    """
    errors: list[str] = []

    # 1. Check required files exist
    for rel in _TASK_REQUIRED_FILES:
        if not (task_path / rel).exists():
            errors.append(f"Missing required file: {rel}")

    # 2. Parse and validate task.yaml
    task_yaml_path = task_path / "task.yaml"
    if task_yaml_path.exists():
        try:
            raw = load_yaml(task_yaml_path)
        except RuntimeError as exc:
            errors.append(f"Cannot load task.yaml: {exc}")
            raw = None

        if raw is not None:
            # Validate schema
            try:
                task = Task.model_validate(raw)
            except ValidationError as exc:
                for err in exc.errors():
                    field = ".".join(str(e) for e in err["loc"])
                    errors.append(f"task.yaml validation error at '{field}': {err['msg']}")
                task = None

            if task is not None:
                # task_id must match folder name
                if task.id != task_path.name:
                    errors.append(
                        f"task.yaml id='{task.id}' does not match folder name '{task_path.name}'"
                    )

    # 3. Parse data_manifest.yaml
    manifest_path = task_path / "data_manifest.yaml"
    if manifest_path.exists():
        try:
            raw_manifest = load_yaml(manifest_path)
        except RuntimeError as exc:
            errors.append(f"Cannot load data_manifest.yaml: {exc}")
            raw_manifest = None

        if raw_manifest is not None:
            try:
                manifest = DataManifest.model_validate(raw_manifest)
            except ValidationError as exc:
                for err in exc.errors():
                    field = ".".join(str(e) for e in err["loc"])
                    errors.append(
                        f"data_manifest.yaml validation error at '{field}': {err['msg']}"
                    )
                manifest = None

            if manifest is not None and manifest.task_id != task_path.name:
                errors.append(
                    f"data_manifest.yaml task_id='{manifest.task_id}' "
                    f"does not match folder name '{task_path.name}'"
                )

    # 4. Parse expected_answer_schema.json (must be valid JSON)
    schema_path = task_path / "expected_answer_schema.json"
    if schema_path.exists():
        try:
            load_json(schema_path)
        except RuntimeError as exc:
            errors.append(f"Cannot load expected_answer_schema.json: {exc}")

    return errors


# ---------------------------------------------------------------------------
# Participant validation
# ---------------------------------------------------------------------------


def validate_participant(participant_path: Path) -> list[str]:
    """Validate a participant folder (submissions/<participant-id>/).

    Returns a list of error strings.
    """
    errors: list[str] = []
    yaml_path = participant_path / "participant.yaml"

    if not yaml_path.exists():
        errors.append("Missing required file: participant.yaml")
        return errors

    try:
        raw = load_yaml(yaml_path)
    except RuntimeError as exc:
        errors.append(f"Cannot load participant.yaml: {exc}")
        return errors

    try:
        p = Participant.model_validate(raw)
    except ValidationError as exc:
        for err in exc.errors():
            field = ".".join(str(e) for e in err["loc"])
            errors.append(f"participant.yaml validation error at '{field}': {err['msg']}")
        return errors

    if p.id != participant_path.name:
        errors.append(
            f"participant.yaml id='{p.id}' does not match folder name '{participant_path.name}'"
        )

    return errors


# ---------------------------------------------------------------------------
# Submission validation
# ---------------------------------------------------------------------------


def _collect_evidence_ids(answer: Answer) -> set[str]:
    return {e.id for e in answer.evidence}


def _check_evidence_refs(
    ids_used: list[str], valid_ids: set[str], context: str
) -> list[str]:
    errors = []
    for eid in ids_used:
        if eid not in valid_ids:
            errors.append(f"{context}: evidence_id '{eid}' not found in evidence list")
    return errors


def validate_submission(submission_path: Path) -> list[str]:
    """Validate a submission folder (submissions/<participant-id>/<task-id>/).

    Returns a list of error strings.
    """
    errors: list[str] = []

    task_id = submission_path.name
    participant_id = submission_path.parent.name

    # Required files
    for rel in ["answer.json", "context_trace.json", "strategy.md"]:
        if not (submission_path / rel).exists():
            errors.append(f"Missing required file: {rel}")

    # --- answer.json ---
    answer_path = submission_path / "answer.json"
    answer: Answer | None = None
    if answer_path.exists():
        try:
            raw = load_json(answer_path)
        except RuntimeError as exc:
            errors.append(f"Cannot load answer.json: {exc}")
            raw = None

        if raw is not None:
            try:
                answer = Answer.model_validate(raw)
            except ValidationError as exc:
                for err in exc.errors():
                    field = ".".join(str(e) for e in err["loc"])
                    errors.append(f"answer.json validation error at '{field}': {err['msg']}")
                answer = None

        if answer is not None:
            # task_id must match folder name
            if answer.task_id != task_id:
                errors.append(
                    f"answer.json task_id='{answer.task_id}' "
                    f"does not match folder name '{task_id}'"
                )
            # participant_id must match parent folder name
            if answer.participant_id != participant_id:
                errors.append(
                    f"answer.json participant_id='{answer.participant_id}' "
                    f"does not match parent folder name '{participant_id}'"
                )

            # Evidence cross-reference checks
            valid_eids = _collect_evidence_ids(answer)

            for claim in answer.claims:
                errors.extend(
                    _check_evidence_refs(
                        claim.evidence_ids, valid_eids, f"claims[{claim.id}].evidence_ids"
                    )
                )
                contradicted_by = getattr(claim, 'contradicted_by', []) or []
                errors.extend(
                    _check_evidence_refs(
                        contradicted_by,
                        valid_eids,
                        f"claims[{claim.id}].contradicted_by",
                    )
                )

            for item in answer.timeline:
                errors.extend(
                    _check_evidence_refs(
                        item.evidence_ids,
                        valid_eids,
                        f"timeline['{item.title}'].evidence_ids",
                    )
                )

            for rec in answer.recommendations:
                errors.extend(
                    _check_evidence_refs(
                        rec.evidence_ids,
                        valid_eids,
                        f"recommendations[{rec.id}].evidence_ids",
                    )
                )

            for entity in answer.entities:
                errors.extend(
                    _check_evidence_refs(
                        entity.evidence_ids,
                        valid_eids,
                        f"entities[{entity.id}].evidence_ids",
                    )
                )

            for risk in answer.risks:
                errors.extend(
                    _check_evidence_refs(
                        risk.evidence_ids,
                        valid_eids,
                        f"risks[{risk.id}].evidence_ids",
                    )
                )

    # --- context_trace.json ---
    trace_path = submission_path / "context_trace.json"
    if trace_path.exists():
        try:
            raw_trace = load_json(trace_path)
        except RuntimeError as exc:
            errors.append(f"Cannot load context_trace.json: {exc}")
            raw_trace = None

        if raw_trace is not None:
            try:
                trace = ContextTrace.model_validate(raw_trace)
            except ValidationError as exc:
                for err in exc.errors():
                    field = ".".join(str(e) for e in err["loc"])
                    errors.append(
                        f"context_trace.json validation error at '{field}': {err['msg']}"
                    )
                trace = None

            if trace is not None:
                if trace.task_id != task_id:
                    errors.append(
                        f"context_trace.json task_id='{trace.task_id}' "
                        f"does not match folder name '{task_id}'"
                    )
                if trace.participant_id != participant_id:
                    errors.append(
                        f"context_trace.json participant_id='{trace.participant_id}' "
                        f"does not match parent folder name '{participant_id}'"
                    )

    return errors


# ---------------------------------------------------------------------------
# Bulk validation
# ---------------------------------------------------------------------------


def validate_all() -> dict[str, list[str]]:
    """Validate all tasks, participants, and submissions.

    Returns a dict mapping path string -> list of error strings.
    An empty list for a path means it is valid.
    """
    all_errors: dict[str, list[str]] = {}
    tasks_dir = get_tasks_dir()
    submissions_dir = get_submissions_dir()

    # Validate tasks
    for tid in task_ids():
        task_path = tasks_dir / tid
        errs = validate_task(task_path)
        all_errors[str(task_path)] = errs

    # Validate participants and their submissions
    for pid in participant_ids():
        participant_path = submissions_dir / pid
        p_errs = validate_participant(participant_path)
        all_errors[str(participant_path)] = p_errs

        # Validate each submission under this participant
        for sub_dir in sorted(participant_path.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name.startswith("."):
                continue
            if sub_dir.name == "participant.yaml":
                continue
            sub_errs = validate_submission(sub_dir)
            all_errors[str(sub_dir)] = sub_errs

    return all_errors


# ---------------------------------------------------------------------------
# Large-file check
# ---------------------------------------------------------------------------

# Files larger than this are considered "large raw data"
_LARGE_FILE_THRESHOLD_BYTES = 10 * 1024 * 1024  # 10 MB

_RAW_DATA_SUBDIRS = ["data/raw", "data/processed"]


def check_no_large_raw_data() -> list[str]:
    """Check that no large files are present in data/raw/ or data/processed/ under any task.

    Returns a list of error strings for each offending file.
    """
    errors: list[str] = []
    tasks_dir = get_tasks_dir()
    if not tasks_dir.exists():
        return errors

    for tid in task_ids():
        task_path = tasks_dir / tid
        for subdir_rel in _RAW_DATA_SUBDIRS:
            data_dir = task_path / subdir_rel
            if not data_dir.exists():
                continue
            for filepath in data_dir.rglob("*"):
                if filepath.is_file():
                    size = filepath.stat().st_size
                    if size > _LARGE_FILE_THRESHOLD_BYTES:
                        size_mb = size / (1024 * 1024)
                        errors.append(
                            f"Large file ({size_mb:.1f} MB) found in tracked path: "
                            f"{filepath.relative_to(find_repo_root())}"
                        )
    return errors
