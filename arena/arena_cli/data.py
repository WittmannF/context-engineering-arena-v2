"""Data download and preparation helpers for arena tasks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .utils import find_repo_root


def discover_task_script(task_id: str, script_name: str) -> Path:
    """Locate tasks/<task_id>/scripts/<script_name> under the repo root.

    Args:
        task_id: The task identifier (must match the folder name under tasks/).
        script_name: The script filename, e.g. 'download.py' or 'prepare.py'.

    Returns:
        Absolute path to the script.

    Raises:
        FileNotFoundError: If the script does not exist at the expected location.
    """
    repo_root = find_repo_root()
    script_path = repo_root / "tasks" / task_id / "scripts" / script_name
    if not script_path.exists():
        raise FileNotFoundError(
            f"Script '{script_name}' not found for task '{task_id}' "
            f"at expected path: {script_path}"
        )
    return script_path


def download_task_data(
    task_id: str,
    sample: bool = False,
    extra_args: list[str] | None = None,
) -> None:
    """Run the task's download.py script.

    Args:
        task_id: Task identifier.
        sample: If True, passes --sample-only to the script.
        extra_args: Additional arguments forwarded to the script.

    Raises:
        FileNotFoundError: If download.py does not exist for the task.
        subprocess.CalledProcessError: If the script exits with a non-zero code.
    """
    script = discover_task_script(task_id, "download.py")
    args = [sys.executable, str(script)]
    if sample:
        args.append("--sample-only")
    if extra_args:
        args.extend(extra_args)
    subprocess.run(args, check=True)


def prepare_task_data(
    task_id: str,
    extra_args: list[str] | None = None,
) -> None:
    """Run the task's prepare.py script.

    Args:
        task_id: Task identifier.
        extra_args: Additional arguments forwarded to the script.

    Raises:
        FileNotFoundError: If prepare.py does not exist for the task.
        subprocess.CalledProcessError: If the script exits with a non-zero code.
    """
    script = discover_task_script(task_id, "prepare.py")
    args = [sys.executable, str(script)]
    if extra_args:
        args.extend(extra_args)
    subprocess.run(args, check=True)
