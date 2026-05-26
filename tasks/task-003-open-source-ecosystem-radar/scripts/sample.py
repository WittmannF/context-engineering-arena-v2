#!/usr/bin/env python3
"""
Sample script for Task 003: Open Source Ecosystem Radar

Creates small samples of the processed output files for testing.

Usage:
    python sample.py
    python sample.py --top-n 20 --output-dir data/samples/task-003-open-source-ecosystem-radar/
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_INPUT_DIR = Path("data/processed/task-003-open-source-ecosystem-radar")
DEFAULT_OUTPUT_DIR = Path("data/samples/task-003-open-source-ecosystem-radar")


def read_json(path):
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def write_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_jsonl(path, n=None):
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


def write_jsonl(records, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Create sample from processed GH Archive data")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-n", type=int, default=20, help="Number of top repos to include (default: 20)")
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"ERROR: Input directory not found: {args.input_dir}")
        print("Run prepare.py first.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_dir}")
    print()

    # Trim top-N lists
    json_files = [
        "top_repos_by_stars.json",
        "top_repos_by_forks.json",
        "top_repos_by_pushes.json",
        "top_repos_by_prs.json",
        "event_type_distribution.json",
        "hourly_event_counts.json",
        "dataset_stats.json",
    ]

    for filename in json_files:
        src = args.input_dir / filename
        data = read_json(src)
        if data is None:
            print(f"  [skip] {filename}")
            continue
        # Trim repos list if present
        if "repos" in data:
            data["repos"] = data["repos"][:args.top_n]
            data["_sample_note"] = f"Trimmed to top {args.top_n}"
        dst = args.output_dir / filename
        write_json(data, dst)
        print(f"  Sampled: {dst}")

    # Trim repo details
    details_src = args.input_dir / "repo_event_details.jsonl"
    details = read_jsonl(details_src, args.top_n * 3)
    if details:
        details_dst = args.output_dir / "repo_event_details.jsonl"
        write_jsonl(details, details_dst)
        print(f"  Sampled: {details_dst} ({len(details)} records)")

    print("\nSample ready for testing.")


if __name__ == "__main__":
    main()
