#!/usr/bin/env python3
"""
Sample script for Task 001: The Enron Investigation Brief

Takes the processed emails.jsonl and creates a small sample file
(first 100 emails) for quick testing and demonstration.

Usage:
    python sample.py
    python sample.py --n 200               # Different sample size
    python sample.py --input-file /path/to/emails.jsonl
    python sample.py --output-dir /path/to/output/
    python sample.py --random-seed 42      # Reproducible random sample
"""

import argparse
import json
import random
import sys
from pathlib import Path

DEFAULT_INPUT = Path("data/processed/task-001-enron-investigation/emails.jsonl")
DEFAULT_OUTPUT_DIR = Path("data/samples/task-001-enron-investigation")
DEFAULT_N = 100


def load_jsonl(path: Path):
    """Load all records from a JSONL file."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  Warning: Could not parse line {line_num}: {e}")
    return records


def write_jsonl(records, path: Path) -> None:
    """Write records to a JSONL file."""
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a small sample from processed Enron emails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sample.py                        # First 100 emails
  python sample.py --n 200               # First 200 emails
  python sample.py --random-seed 42      # Random sample with fixed seed
  python sample.py --strategy random     # Random instead of first-N
        """,
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to processed emails.jsonl (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=DEFAULT_N,
        help=f"Number of emails in the sample (default: {DEFAULT_N})",
    )
    parser.add_argument(
        "--strategy",
        choices=["first", "random", "stratified"],
        default="first",
        help="Sampling strategy: first (default), random, or stratified by user_folder",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (only used with --strategy random or stratified)",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"ERROR: Input file not found: {args.input_file}")
        print("Run prepare.py first to generate the processed dataset.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:    {args.input_file}")
    print(f"Output:   {args.output_dir}")
    print(f"Strategy: {args.strategy}")
    print(f"N:        {args.n}")
    print()

    # Load all records
    print("Loading processed emails...")
    all_records = load_jsonl(args.input_file)
    print(f"  Loaded {len(all_records):,} emails")

    if len(all_records) == 0:
        print("ERROR: No records found in input file.")
        sys.exit(1)

    # Sample
    if args.strategy == "first":
        sample = all_records[: args.n]
        print(f"  Strategy 'first': taking first {len(sample)} records")

    elif args.strategy == "random":
        if args.random_seed is not None:
            random.seed(args.random_seed)
            print(f"  Strategy 'random': using seed {args.random_seed}")
        else:
            print("  Strategy 'random': no seed (non-reproducible)")
        n = min(args.n, len(all_records))
        sample = random.sample(all_records, n)
        print(f"  Sampled {len(sample)} emails randomly")

    elif args.strategy == "stratified":
        # Sample proportionally from each user_folder
        if args.random_seed is not None:
            random.seed(args.random_seed)
        # Group by user_folder
        by_folder = {}
        for r in all_records:
            folder = r.get("user_folder", "unknown")
            by_folder.setdefault(folder, []).append(r)
        # Sample proportionally
        sample = []
        total = len(all_records)
        for folder, folder_records in by_folder.items():
            n_from_folder = max(1, int(args.n * len(folder_records) / total))
            picked = random.sample(folder_records, min(n_from_folder, len(folder_records)))
            sample.extend(picked)
        # Trim or top-up to exactly args.n
        random.shuffle(sample)
        sample = sample[: args.n]
        print(f"  Strategy 'stratified': sampled {len(sample)} emails across {len(by_folder)} folders")

    # Write sample
    output_path = args.output_dir / "sample_emails.jsonl"
    write_jsonl(sample, output_path)
    size_kb = output_path.stat().st_size / 1000
    print(f"\nSample written: {output_path}")
    print(f"  {len(sample)} emails, {size_kb:.1f} KB")

    # Print sample summary
    senders = set()
    folders = set()
    dates = []
    for r in sample:
        if r.get("sender"):
            senders.add(r["sender"])
        if r.get("user_folder"):
            folders.add(r["user_folder"])
        if r.get("date"):
            dates.append(r["date"])

    print(f"  Unique senders:      {len(senders)}")
    print(f"  Unique user folders: {len(folders)}")
    if dates:
        print(f"  Date range:          {min(dates)} — {max(dates)}")

    # Write a short metadata file
    meta = {
        "source": str(args.input_file),
        "n": len(sample),
        "strategy": args.strategy,
        "random_seed": args.random_seed,
        "unique_senders": len(senders),
        "unique_folders": len(folders),
        "date_range": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None,
        },
    }
    meta_path = args.output_dir / "sample_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"\nMetadata written: {meta_path}")
    print("\nDone. Use this sample for quick testing of your analysis pipeline.")


if __name__ == "__main__":
    main()
