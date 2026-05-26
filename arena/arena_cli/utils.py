"""Utility helpers for arena_cli."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# File loaders
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its contents as a dict.

    Raises a RuntimeError with a clear message on parse failure.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            result = yaml.safe_load(fh)
        if result is None:
            return {}
        if not isinstance(result, dict):
            raise RuntimeError(
                f"Expected a YAML mapping at {path}, got {type(result).__name__}"
            )
        return result
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Failed to parse YAML at {path}: {exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"Cannot open {path}: {exc}") from exc


def load_json(path: Path) -> dict:
    """Load a JSON file and return its contents as a dict.

    Raises a RuntimeError with a clear message on parse failure.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            result = json.load(fh)
        if not isinstance(result, dict):
            raise RuntimeError(
                f"Expected a JSON object at {path}, got {type(result).__name__}"
            )
        return result
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse JSON at {path}: {exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"Cannot open {path}: {exc}") from exc


# ---------------------------------------------------------------------------
# Repo navigation
# ---------------------------------------------------------------------------


def find_repo_root() -> Path:
    """Walk up from the current working directory to find the repo root.

    The repo root is identified by the presence of an ``arena/`` subdirectory
    (which contains ``pyproject.toml``).

    Raises FileNotFoundError if the repo root cannot be found.
    """
    candidate = Path.cwd().resolve()
    for directory in [candidate, *candidate.parents]:
        arena_dir = directory / "arena"
        if arena_dir.is_dir() and (arena_dir / "pyproject.toml").exists():
            return directory
    # Fallback: check whether we are already inside the arena/ package
    for directory in [candidate, *candidate.parents]:
        if (directory / "pyproject.toml").exists() and (
            directory / "arena_cli"
        ).is_dir():
            # We are inside arena/ itself — repo root is one level up
            return directory.parent
    raise FileNotFoundError(
        "Could not locate the repo root. "
        "Make sure you are running from inside the context-engineering-arena-v2 repository."
    )


def get_tasks_dir() -> Path:
    """Return the path to the tasks/ directory at the repo root."""
    return find_repo_root() / "tasks"


def get_submissions_dir() -> Path:
    """Return the path to the submissions/ directory at the repo root."""
    return find_repo_root() / "submissions"


def get_site_data_dir() -> Path:
    """Return the path to packages/site/src/data/generated/ at the repo root."""
    return find_repo_root() / "packages" / "site" / "src" / "data" / "generated"


# ---------------------------------------------------------------------------
# Discovery helpers
# ---------------------------------------------------------------------------


def task_ids() -> list[str]:
    """Return sorted list of all task folder names under tasks/.

    Excludes the ``proposals/`` subdirectory if present.
    """
    tasks_dir = get_tasks_dir()
    if not tasks_dir.exists():
        return []
    return sorted(
        d.name
        for d in tasks_dir.iterdir()
        if d.is_dir() and d.name != "proposals" and not d.name.startswith(".")
    )


def participant_ids() -> list[str]:
    """Return sorted list of all participant folder names under submissions/."""
    submissions_dir = get_submissions_dir()
    if not submissions_dir.exists():
        return []
    return sorted(
        d.name
        for d in submissions_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )
