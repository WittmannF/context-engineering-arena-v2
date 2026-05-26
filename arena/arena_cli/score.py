"""Scoring utilities for arena_cli.

Real scoring is performed manually by judges. This module provides helpers
to load existing scores and generate placeholder score structures.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .schemas import Score
from .utils import load_json


def compute_manual_score(answer_path: Path, trace_path: Path) -> dict:
    """Return a placeholder score dict for a submission.

    Real scoring is performed manually by human judges using the task rubric.
    This function creates a starter score structure that judges can fill in.

    Args:
        answer_path: Path to the submission's answer.json file.
        trace_path: Path to the submission's context_trace.json file.

    Returns:
        A dict conforming to the Score schema with zeroed-out scores and
        placeholder notes, ready to be persisted as score.json.
    """
    # Load answer to get task_id and participant_id
    try:
        raw_answer = load_json(answer_path)
        task_id = raw_answer.get("task_id", "unknown")
        participant_id = raw_answer.get("participant_id", "unknown")
    except RuntimeError:
        task_id = "unknown"
        participant_id = "unknown"

    # Build a placeholder score structure
    placeholder = {
        "task_id": task_id,
        "participant_id": participant_id,
        "overall_score": 0.0,
        "scores": [
            {
                "dimension": "accuracy",
                "score": 0.0,
                "max_score": 30.0,
                "rationale": "TODO: assess factual accuracy of claims",
            },
            {
                "dimension": "completeness",
                "score": 0.0,
                "max_score": 25.0,
                "rationale": "TODO: assess coverage of required answer elements",
            },
            {
                "dimension": "evidence_quality",
                "score": 0.0,
                "max_score": 20.0,
                "rationale": "TODO: assess quality and relevance of evidence cited",
            },
            {
                "dimension": "clarity",
                "score": 0.0,
                "max_score": 15.0,
                "rationale": "TODO: assess clarity and structure of the answer",
            },
            {
                "dimension": "context_efficiency",
                "score": 0.0,
                "max_score": 10.0,
                "rationale": "TODO: assess how well context was used (from context_trace.json)",
            },
        ],
        "notes": "Placeholder score — awaiting manual review.",
        "scored_by": None,
        "scored_at": None,
        "version": "1.0",
    }
    return placeholder


def load_score(score_path: Path) -> Optional[dict]:
    """Load and validate a score.json file.

    Args:
        score_path: Path to the score.json file.

    Returns:
        The score as a dict, or None if the file does not exist.

    Raises:
        RuntimeError: If the file exists but cannot be parsed or validated.
    """
    if not score_path.exists():
        return None

    raw = load_json(score_path)
    try:
        from pydantic import ValidationError

        score = Score.model_validate(raw)
        return score.model_dump()
    except ValidationError as exc:
        raise RuntimeError(f"score.json at {score_path} is invalid: {exc}") from exc
