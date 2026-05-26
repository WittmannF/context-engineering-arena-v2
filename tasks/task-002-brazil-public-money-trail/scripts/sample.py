#!/usr/bin/env python3
"""
Sample script for Task 002: Brazil Public Money Trail

Creates a small sample from processed data files for quick testing.

Usage:
    python sample.py
    python sample.py --n 20 --output-dir data/samples/task-002-brazil-public-money-trail/
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_INPUT_DIR = Path("data/processed/task-002-brazil-public-money-trail")
DEFAULT_OUTPUT_DIR = Path("data/samples/task-002-brazil-public-money-trail")


def read_jsonl(path: Path, n: int = None):
    """Read up to n records from a JSONL file."""
    if not path.exists():
        return []
    records = []
    with open(path, "r", encoding="utf-8") as f:
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


def write_jsonl(records, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create mini-sample from processed Brazil data")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--n", type=int, default=20, help="Records per file in sample (default: 20)")
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"ERROR: Input directory not found: {args.input_dir}")
        print("Run prepare.py first.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_dir}")
    print(f"N:      {args.n}")
    print()

    files_to_sample = [
        "propositions.jsonl",
        "deputies.jsonl",
        "expenses.jsonl",
        "expenses_SYNTHETIC.jsonl",
        "timeline_events.jsonl",
        "candidate_links.jsonl",
        "evidence_index.jsonl",
    ]

    for filename in files_to_sample:
        src = args.input_dir / filename
        if not src.exists():
            print(f"  [skip] {filename} (not found)")
            continue
        records = read_jsonl(src, args.n)
        dst = args.output_dir / filename
        write_jsonl(records, dst)
        print(f"  Sampled {len(records)} records: {dst}")

    # Copy stats
    stats_src = args.input_dir / "dataset_stats.json"
    if stats_src.exists():
        with open(stats_src) as f:
            stats = json.load(f)
        stats["sample_note"] = f"This is a sample of {args.n} records per file."
        stats_dst = args.output_dir / "dataset_stats.json"
        with open(stats_dst, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"  Copied stats: {stats_dst}")

    print("\nSample created. Ready for testing.")


if __name__ == "__main__":
    main()
