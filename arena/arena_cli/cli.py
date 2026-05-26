"""Typer CLI for Context Engineering Arena."""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich import box

app = typer.Typer(
    name="arena",
    help="Context Engineering Arena CLI — validate tasks, manage data, build catalog.",
    no_args_is_help=True,
)
console = Console()
err_console = Console(stderr=True)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@app.command()
def validate(
    task: str = typer.Option(None, "--task", "-t", help="Validate a specific task by ID"),
    participant: str = typer.Option(
        None, "--participant", "-p", help="Validate a specific participant"
    ),
) -> None:
    """Validate tasks and submissions.

    Without options, validates everything in the repo. Use --task or
    --participant to scope validation to a single task or participant.
    """
    from .utils import get_tasks_dir, get_submissions_dir
    from .validate import (
        validate_task as _validate_task,
        validate_participant as _validate_participant,
        validate_submission as _validate_submission,
        validate_all,
        check_no_large_raw_data,
    )

    all_errors: dict[str, list[str]] = {}

    if task and participant:
        # Validate a single submission
        sub_path = get_submissions_dir() / participant / task
        if not sub_path.exists():
            err_console.print(
                f"[red]Submission path not found:[/red] {sub_path}"
            )
            raise typer.Exit(code=1)
        errs = _validate_submission(sub_path)
        all_errors[str(sub_path)] = errs

    elif task:
        task_path = get_tasks_dir() / task
        if not task_path.exists():
            err_console.print(f"[red]Task not found:[/red] {task_path}")
            raise typer.Exit(code=1)
        errs = _validate_task(task_path)
        all_errors[str(task_path)] = errs

    elif participant:
        participant_path = get_submissions_dir() / participant
        if not participant_path.exists():
            err_console.print(f"[red]Participant not found:[/red] {participant_path}")
            raise typer.Exit(code=1)
        errs = _validate_participant(participant_path)
        all_errors[str(participant_path)] = errs
        # Also validate all submissions for this participant
        for sub_dir in sorted(participant_path.iterdir()):
            if sub_dir.is_dir() and not sub_dir.name.startswith("."):
                sub_errs = _validate_submission(sub_dir)
                all_errors[str(sub_dir)] = sub_errs

    else:
        # Validate everything
        all_errors = validate_all()
        large_file_errors = check_no_large_raw_data()
        if large_file_errors:
            all_errors["large_data_check"] = large_file_errors

    _print_validation_results(all_errors)

    total_errors = sum(len(v) for v in all_errors.values())
    if total_errors > 0:
        raise typer.Exit(code=1)


def _print_validation_results(all_errors: dict[str, list[str]]) -> None:
    """Print validation results as a rich table."""
    total_paths = len(all_errors)
    error_paths = {k: v for k, v in all_errors.items() if v}
    ok_paths = total_paths - len(error_paths)

    if not error_paths:
        console.print(
            f"\n[bold green]All {total_paths} items validated successfully.[/bold green]\n"
        )
        return

    console.print()
    for path_str, errors in sorted(error_paths.items()):
        console.print(f"[bold red]FAIL[/bold red] [dim]{path_str}[/dim]")
        for err in errors:
            console.print(f"  [red]•[/red] {err}")
    console.print()
    total_errors = sum(len(v) for v in error_paths.items())
    total_error_count = sum(len(v) for v in all_errors.values())
    console.print(
        f"[bold]Result:[/bold] "
        f"[green]{ok_paths} passed[/green], "
        f"[red]{len(error_paths)} failed[/red] "
        f"({total_error_count} error(s) total)\n"
    )


# ---------------------------------------------------------------------------
# validate-submission
# ---------------------------------------------------------------------------


@app.command(name="validate-submission")
def validate_submission_cmd(
    participant: str = typer.Option(..., "--participant", "-p", help="Participant ID"),
    task: str = typer.Option(..., "--task", "-t", help="Task ID"),
) -> None:
    """Validate a specific submission (submissions/<participant>/<task>/)."""
    from .utils import get_submissions_dir
    from .validate import validate_submission as _validate_submission

    sub_path = get_submissions_dir() / participant / task
    if not sub_path.exists():
        err_console.print(f"[red]Submission path not found:[/red] {sub_path}")
        raise typer.Exit(code=1)

    errors = _validate_submission(sub_path)
    if errors:
        console.print(f"\n[bold red]FAIL[/bold red] {sub_path}")
        for err in errors:
            console.print(f"  [red]•[/red] {err}")
        console.print()
        raise typer.Exit(code=1)
    else:
        console.print(f"\n[bold green]OK[/bold green] {sub_path}\n")


# ---------------------------------------------------------------------------
# build-catalog
# ---------------------------------------------------------------------------


@app.command(name="build-catalog")
def build_catalog_cmd() -> None:
    """Build the site catalog JSON files from tasks and submissions."""
    from .build_catalog import build_catalog

    console.print("[bold]Building catalog...[/bold]")
    try:
        build_catalog()
    except Exception as exc:
        err_console.print(f"[red]Build failed:[/red] {exc}")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# list-tasks
# ---------------------------------------------------------------------------


@app.command(name="list-tasks")
def list_tasks() -> None:
    """List all available tasks."""
    from .utils import get_tasks_dir, task_ids
    from .schemas import Task
    from .utils import load_yaml

    ids = task_ids()
    if not ids:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Arena Tasks", box=box.ROUNDED, show_lines=False)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title")
    table.add_column("Domain", style="magenta")
    table.add_column("Difficulty", style="yellow")
    table.add_column("Tags")

    tasks_dir = get_tasks_dir()
    for tid in ids:
        yaml_path = tasks_dir / tid / "task.yaml"
        if not yaml_path.exists():
            table.add_row(tid, "[dim]task.yaml missing[/dim]", "", "", "")
            continue
        try:
            raw = load_yaml(yaml_path)
            task = Task.model_validate(raw)
            tags_str = ", ".join(task.tags) if task.tags else ""
            table.add_row(
                task.id,
                task.title,
                task.domain,
                task.difficulty,
                tags_str,
            )
        except Exception as exc:
            table.add_row(tid, f"[red]Error: {exc}[/red]", "", "", "")

    console.print(table)
    console.print(f"\n[dim]{len(ids)} task(s) found.[/dim]\n")


# ---------------------------------------------------------------------------
# list-submissions
# ---------------------------------------------------------------------------


@app.command(name="list-submissions")
def list_submissions() -> None:
    """List all submissions across all participants."""
    from .utils import get_submissions_dir, participant_ids
    from .schemas import Score
    from .utils import load_json

    pids = participant_ids()
    if not pids:
        console.print("[yellow]No submissions found.[/yellow]")
        return

    table = Table(title="Arena Submissions", box=box.ROUNDED, show_lines=False)
    table.add_column("Participant", style="cyan", no_wrap=True)
    table.add_column("Task ID", style="green", no_wrap=True)
    table.add_column("Answer", style="dim")
    table.add_column("Trace", style="dim")
    table.add_column("Score", justify="right")

    submissions_dir = get_submissions_dir()
    total = 0
    for pid in pids:
        p_path = submissions_dir / pid
        for sub_dir in sorted(p_path.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name.startswith("."):
                continue
            has_answer = "yes" if (sub_dir / "answer.json").exists() else "[red]no[/red]"
            has_trace = "yes" if (sub_dir / "context_trace.json").exists() else "[red]no[/red]"

            score_str = "[dim]unscored[/dim]"
            score_path = sub_dir / "score.json"
            if score_path.exists():
                try:
                    raw_score = load_json(score_path)
                    score_obj = Score.model_validate(raw_score)
                    score_str = f"[bold]{score_obj.overall_score:.1f}[/bold]"
                except Exception:
                    score_str = "[red]invalid[/red]"

            table.add_row(pid, sub_dir.name, has_answer, has_trace, score_str)
            total += 1

    console.print(table)
    console.print(f"\n[dim]{total} submission(s) found.[/dim]\n")


# ---------------------------------------------------------------------------
# download-data
# ---------------------------------------------------------------------------


@app.command(name="download-data")
def download_data(
    task: str = typer.Option(..., "--task", "-t", help="Task ID"),
    sample: bool = typer.Option(
        False, "--sample", help="Download sample subset only"
    ),
) -> None:
    """Download data for a task by running its download.py script."""
    from .data import download_task_data

    mode = "sample" if sample else "full"
    console.print(f"[bold]Downloading {mode} data for task:[/bold] {task}")
    try:
        download_task_data(task, sample=sample)
        console.print(f"[green]Download complete.[/green]")
    except FileNotFoundError as exc:
        err_console.print(f"[red]Script not found:[/red] {exc}")
        raise typer.Exit(code=1)
    except Exception as exc:
        err_console.print(f"[red]Download failed:[/red] {exc}")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# prepare-data
# ---------------------------------------------------------------------------


@app.command(name="prepare-data")
def prepare_data(
    task: str = typer.Option(..., "--task", "-t", help="Task ID"),
) -> None:
    """Prepare data for a task by running its prepare.py script."""
    from .data import prepare_task_data

    console.print(f"[bold]Preparing data for task:[/bold] {task}")
    try:
        prepare_task_data(task)
        console.print(f"[green]Preparation complete.[/green]")
    except FileNotFoundError as exc:
        err_console.print(f"[red]Script not found:[/red] {exc}")
        raise typer.Exit(code=1)
    except Exception as exc:
        err_console.print(f"[red]Preparation failed:[/red] {exc}")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
