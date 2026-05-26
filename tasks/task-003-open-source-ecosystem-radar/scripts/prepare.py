#!/usr/bin/env python3
"""
Prepare script for Task 003: Open Source Ecosystem Radar

Reads .json.gz files from GH Archive and produces aggregated analysis files:
  - top_repos_by_stars.json        (top repos by WatchEvent count)
  - top_repos_by_forks.json        (top repos by ForkEvent count)
  - top_repos_by_pushes.json       (top repos by PushEvent count)
  - top_repos_by_prs.json          (top repos by PullRequestEvent count)
  - event_type_distribution.json   (total events by type)
  - hourly_event_counts.json       (events per hour)
  - repo_event_details.jsonl       (per-repo event summary)
  - dataset_stats.json             (overall summary stats)

Usage:
    python prepare.py
    python prepare.py --input-dir data/raw/task-003-open-source-ecosystem-radar/
    python prepare.py --output-dir data/processed/task-003-open-source-ecosystem-radar/
    python prepare.py --top-n 100  # Include top 100 repos in each ranking
"""

import argparse
import gzip
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_INPUT_DIR = Path("data/raw/task-003-open-source-ecosystem-radar")
DEFAULT_OUTPUT_DIR = Path("data/processed/task-003-open-source-ecosystem-radar")
DEFAULT_TOP_N = 50

# Event types we care about for the analysis
TRACKED_EVENT_TYPES = {
    "WatchEvent",
    "PushEvent",
    "PullRequestEvent",
    "IssuesEvent",
    "ForkEvent",
    "ReleaseEvent",
    "CreateEvent",
    "MemberEvent",
    "PublicEvent",
    "IssueCommentEvent",
    "PullRequestReviewEvent",
    "CommitCommentEvent",
    "DeleteEvent",
}


def find_gz_files(input_dir: Path) -> List[Path]:
    """Find all .json.gz files in the input directory."""
    files = sorted(input_dir.glob("*.json.gz"))
    return files


def parse_event(line: bytes) -> Dict:
    """Parse a single event line. Returns {} on failure."""
    try:
        return json.loads(line)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def process_file(gz_path: Path, repo_events: Dict, event_type_counts: Dict, hourly_counts: Dict) -> Tuple[int, int]:
    """
    Process a single .json.gz file and accumulate into the aggregation dicts.

    Args:
        gz_path: path to .json.gz file
        repo_events: dict to accumulate per-repo event counts: {repo: {event_type: count}}
        event_type_counts: dict to accumulate total events by type: {event_type: count}
        hourly_counts: dict to accumulate events per hour: {hour_str: count}

    Returns (total_lines, error_count)
    """
    # Extract hour from filename e.g. "2025-01-01-0.json.gz"
    stem = gz_path.stem.replace(".json", "")  # "2025-01-01-0"
    parts = stem.split("-")
    if len(parts) >= 4:
        hour_key = "-".join(parts[:3]) + "T" + parts[3].zfill(2) + ":00:00Z"
    else:
        hour_key = stem

    total_lines = 0
    error_count = 0

    try:
        with gzip.open(gz_path, "rb") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                total_lines += 1

                event = parse_event(line)
                if not event:
                    error_count += 1
                    continue

                event_type = event.get("type", "Unknown")
                repo_info = event.get("repo", {}) or {}
                repo_name = repo_info.get("name", "")

                # Count event types
                event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

                # Count hourly events
                hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1

                # Only track events for repos with names, and only tracked event types
                if not repo_name or event_type not in TRACKED_EVENT_TYPES:
                    continue

                # Accumulate per-repo events
                if repo_name not in repo_events:
                    repo_events[repo_name] = defaultdict(int)
                    repo_events[repo_name]["_actor_set"] = set()
                    repo_events[repo_name]["_org_set"] = set()

                repo_events[repo_name][event_type] += 1
                repo_events[repo_name]["_total"] += 1

                # Track actors for concentration analysis
                actor = event.get("actor", {}) or {}
                actor_login = actor.get("login", "")
                if actor_login:
                    repo_events[repo_name]["_actor_set"].add(actor_login)

                # Track org
                org = event.get("org", {}) or {}
                org_login = org.get("login", "")
                if org_login:
                    repo_events[repo_name]["_org_set"].add(org_login)

    except gzip.BadGzipFile:
        print(f"\n  ERROR: Bad gzip file: {gz_path}")
        error_count += 1
    except Exception as e:
        print(f"\n  ERROR processing {gz_path}: {e}")
        error_count += 1

    return total_lines, error_count


def build_top_repos(repo_events: Dict, event_type: str, top_n: int) -> List[Dict]:
    """Build a ranked list of repos by a specific event type count."""
    ranked = []
    for repo, counts in repo_events.items():
        count = counts.get(event_type, 0)
        if count > 0:
            ranked.append({
                "rank": 0,  # filled in below
                "repo": repo,
                "org": repo.split("/")[0] if "/" in repo else "",
                "count": count,
                "event_type": event_type,
                "total_events": counts.get("_total", 0),
                "unique_actors": len(counts.get("_actor_set", set())),
            })

    ranked.sort(key=lambda x: x["count"], reverse=True)
    ranked = ranked[:top_n]

    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    return ranked


def build_repo_event_details(repo_events: Dict, top_n: int = 200) -> List[Dict]:
    """
    Build a detailed per-repo summary for the top N most active repos.
    Used for the repo_event_details.jsonl file.
    """
    # Sort by total events
    sorted_repos = sorted(
        repo_events.items(),
        key=lambda x: x[1].get("_total", 0),
        reverse=True
    )[:top_n]

    details = []
    for repo, counts in sorted_repos:
        # Convert sets to counts for JSON serialization
        detail = {
            "repo": repo,
            "org": repo.split("/")[0] if "/" in repo else "",
            "total_events": counts.get("_total", 0),
            "unique_actors": len(counts.get("_actor_set", set())),
            "unique_orgs": len(counts.get("_org_set", set())),
        }
        # Add per-event-type counts
        for et in TRACKED_EVENT_TYPES:
            if counts.get(et, 0) > 0:
                detail[et] = counts[et]

        details.append(detail)

    return details


def write_json(data: Any, path: Path, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    size_kb = path.stat().st_size / 1000
    print(f"  Written: {path} ({size_kb:.1f} KB)")


def write_jsonl(records: List[Dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    size_kb = path.stat().st_size / 1000
    print(f"  Written: {path} ({len(records)} records, {size_kb:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate GH Archive events for Task 003",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory with .json.gz files (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=DEFAULT_TOP_N,
        help=f"Number of top repos to include in each ranking (default: {DEFAULT_TOP_N})",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"ERROR: Input directory not found: {args.input_dir}")
        print("Run download.py first.")
        sys.exit(1)

    gz_files = find_gz_files(args.input_dir)
    if not gz_files:
        print(f"ERROR: No .json.gz files found in {args.input_dir}")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:  {args.input_dir.resolve()}")
    print(f"Output: {args.output_dir.resolve()}")
    print(f"Files:  {len(gz_files)} .json.gz files")
    print(f"Top-N:  {args.top_n}")
    print()

    # Aggregation state
    repo_events: Dict = {}
    event_type_counts: Dict = {}
    hourly_counts: Dict = {}

    total_lines = 0
    total_errors = 0
    start_time = time.time()

    for i, gz_file in enumerate(gz_files):
        pct = (i + 1) / len(gz_files) * 100
        size_mb = gz_file.stat().st_size / 1_000_000
        print(f"  [{pct:5.1f}%] {gz_file.name} ({size_mb:.1f} MB)", end="", flush=True)

        file_lines, file_errors = process_file(gz_file, repo_events, event_type_counts, hourly_counts)
        total_lines += file_lines
        total_errors += file_errors

        elapsed = time.time() - start_time
        print(f" -> {file_lines:,} events ({file_errors} errors) [{elapsed:.1f}s total]")

    print(f"\nProcessing complete:")
    print(f"  Total events:     {total_lines:,}")
    print(f"  Parse errors:     {total_errors:,}")
    print(f"  Unique repos:     {len(repo_events):,}")
    print(f"  Event types seen: {len(event_type_counts)}")
    print()

    # Build outputs
    print("Building output files...")

    # Top repos by stars (WatchEvent)
    top_stars = build_top_repos(repo_events, "WatchEvent", args.top_n)
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "event_type": "WatchEvent", "top_n": args.top_n, "repos": top_stars}, args.output_dir / "top_repos_by_stars.json")

    # Top repos by forks
    top_forks = build_top_repos(repo_events, "ForkEvent", args.top_n)
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "event_type": "ForkEvent", "top_n": args.top_n, "repos": top_forks}, args.output_dir / "top_repos_by_forks.json")

    # Top repos by pushes
    top_pushes = build_top_repos(repo_events, "PushEvent", args.top_n)
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "event_type": "PushEvent", "top_n": args.top_n, "repos": top_pushes}, args.output_dir / "top_repos_by_pushes.json")

    # Top repos by PRs
    top_prs = build_top_repos(repo_events, "PullRequestEvent", args.top_n)
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "event_type": "PullRequestEvent", "top_n": args.top_n, "repos": top_prs}, args.output_dir / "top_repos_by_prs.json")

    # Event type distribution
    sorted_event_types = sorted(event_type_counts.items(), key=lambda x: x[1], reverse=True)
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "total": sum(event_type_counts.values()), "distribution": [{"event_type": k, "count": v} for k, v in sorted_event_types]}, args.output_dir / "event_type_distribution.json")

    # Hourly event counts
    sorted_hours = sorted(hourly_counts.items())
    write_json({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "hourly": [{"hour": h, "count": c} for h, c in sorted_hours]}, args.output_dir / "hourly_event_counts.json")

    # Repo event details
    repo_details = build_repo_event_details(repo_events, top_n=min(500, len(repo_events)))
    write_jsonl(repo_details, args.output_dir / "repo_event_details.jsonl")

    # Dataset stats
    filenames = [f.name for f in gz_files]
    time_range_start = filenames[0].replace(".json.gz", "") if filenames else ""
    time_range_end = filenames[-1].replace(".json.gz", "") if filenames else ""

    stats = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "files_processed": len(gz_files),
        "total_events": total_lines,
        "parse_errors": total_errors,
        "unique_repos": len(repo_events),
        "event_types_seen": len(event_type_counts),
        "time_range_approx": {"start": time_range_start, "end": time_range_end},
        "hours_covered": len(gz_files),
        "top_repo_by_stars": top_stars[0]["repo"] if top_stars else None,
        "top_repo_by_forks": top_forks[0]["repo"] if top_forks else None,
        "top_repo_by_pushes": top_pushes[0]["repo"] if top_pushes else None,
        "attribution": "Data: GH Archive (https://www.gharchive.org/) CC BY 4.0",
    }
    write_json(stats, args.output_dir / "dataset_stats.json")

    print(f"\nDone. Top repos:")
    if top_stars:
        print(f"  Most starred: {top_stars[0]['repo']} ({top_stars[0]['count']:,} stars in window)")
    if top_pushes:
        print(f"  Most pushed:  {top_pushes[0]['repo']} ({top_pushes[0]['count']:,} pushes in window)")
    if top_forks:
        print(f"  Most forked:  {top_forks[0]['repo']} ({top_forks[0]['count']:,} forks in window)")

    print(f"\nNext: Run sample.py or use the processed data for analysis:")
    print(f"  python tasks/task-003-open-source-ecosystem-radar/scripts/sample.py")


# Fix missing Tuple import
from typing import Tuple


if __name__ == "__main__":
    main()
