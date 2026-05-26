#!/usr/bin/env python3
"""
Download script for Task 001: The Enron Investigation Brief
Enron Email Dataset (CMU/FERC release)

Usage:
    python download.py                     # Full download
    python download.py --sample-only       # Sample mode (creates placeholder)
    python download.py --force             # Re-download even if file exists
    python download.py --output-dir /path  # Custom output directory
"""

import argparse
import os
import sys
import hashlib
import time
from pathlib import Path

FULL_URL = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
EXPECTED_SIZE_MB = 1730
ARCHIVE_FILENAME = "enron_mail_20150507.tar.gz"

ETHICS_NOTICE = """
=============================================================================
ETHICS AND LICENSE NOTICE — ENRON EMAIL DATASET
=============================================================================
This dataset contains personal emails from real individuals. It was released
by the Federal Energy Regulatory Commission (FERC) as part of its investigation
into Enron Corporation's collapse in 2001.

License: Public domain (released under FERC subpoena as public record)

Before using this data, please note:
  - Several individuals in this dataset were investigated, prosecuted, or
    acquitted. Others had no involvement in the fraud.
  - You must handle all personal communications with journalistic care.
  - Do not reproduce email content verbatim beyond short evidentiary excerpts.
  - Focus on organizational patterns rather than individual blame.
  - Mark all inferences about individual intent as uncertain.

This data is provided for research, journalism, and educational purposes.
Use it responsibly.
=============================================================================
"""


def print_progress(downloaded_bytes: int, total_bytes: int, bar_width: int = 50) -> None:
    """Print a text-based progress bar to stdout."""
    if total_bytes <= 0:
        print(f"\r  Downloaded: {downloaded_bytes / 1_000_000:.1f} MB", end="", flush=True)
        return
    fraction = downloaded_bytes / total_bytes
    filled = int(bar_width * fraction)
    bar = "=" * filled + "-" * (bar_width - filled)
    pct = fraction * 100
    mb_done = downloaded_bytes / 1_000_000
    mb_total = total_bytes / 1_000_000
    print(f"\r  [{bar}] {pct:.1f}% ({mb_done:.1f}/{mb_total:.1f} MB)", end="", flush=True)


def download_with_progress(url: str, dest_path: Path) -> None:
    """Download a file from url to dest_path with progress reporting."""
    try:
        import requests
    except ImportError:
        print("\nERROR: 'requests' library not found. Install with: uv pip install requests")
        sys.exit(1)

    print(f"  Downloading: {url}")
    print(f"  Destination: {dest_path}")
    print(f"  Expected size: ~{EXPECTED_SIZE_MB} MB")

    # Use a temp file to avoid partial downloads
    tmp_path = dest_path.with_suffix(".tmp")

    try:
        with requests.get(url, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0

            with open(tmp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        print_progress(downloaded, total)

        print()  # newline after progress bar
        tmp_path.rename(dest_path)
        print(f"  Saved to: {dest_path}")

    except requests.exceptions.ConnectionError as e:
        print(f"\nERROR: Connection failed: {e}")
        if tmp_path.exists():
            tmp_path.unlink()
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\nERROR: HTTP error: {e}")
        if tmp_path.exists():
            tmp_path.unlink()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        if tmp_path.exists():
            tmp_path.unlink()
        sys.exit(1)


def download_full(output_dir: Path, force: bool) -> None:
    """Download the full Enron Email Dataset."""
    dest = output_dir / ARCHIVE_FILENAME

    if dest.exists() and not force:
        size_mb = dest.stat().st_size / 1_000_000
        print(f"  Archive already exists: {dest} ({size_mb:.1f} MB)")
        print("  Use --force to re-download.")
        return

    download_with_progress(FULL_URL, dest)

    size_mb = dest.stat().st_size / 1_000_000
    print(f"\nDownload complete: {size_mb:.1f} MB")
    print("\nNext steps:")
    print("  1. Extract the archive:")
    print(f"       tar -xzf {dest} -C {output_dir}")
    print("  2. Prepare the data for analysis:")
    print("       python tasks/task-001-enron-investigation/scripts/prepare.py")


def download_sample(output_dir: Path, force: bool) -> None:
    """
    Create a sample directory with instructions.

    The Enron dataset does not have an official small sample mirror,
    so in sample mode we create a structured placeholder directory and
    download instructions. For a real sample, run prepare.py --sample-only
    after extracting the full archive.

    Alternatively, if you want a quick 100-email sample for testing without
    the full download, run:
        python scripts/prepare.py --sample-only
    after a partial extraction of the archive.
    """
    sample_dir = output_dir / "sample"
    instructions_file = sample_dir / "SAMPLE_MODE.md"

    if instructions_file.exists() and not force:
        print(f"  Sample directory already exists: {sample_dir}")
        print("  Use --force to recreate.")
        return

    sample_dir.mkdir(parents=True, exist_ok=True)

    instructions = """# Enron Dataset — Sample Mode

The full Enron email archive is 1.7 GB and must be downloaded from CMU.

## Quick Start: Partial Extraction for Sample Testing

If you want a small working sample without downloading the full archive:

1. Download just enough of the archive to get a sample:

   ```bash
   # Download the full archive (required for partial extraction)
   python scripts/download.py

   # Extract only one employee's folder (e.g., lay-k)
   tar -xzf data/raw/task-001-enron-investigation/enron_mail_20150507.tar.gz \\
       --strip-components=1 \\
       enron_mail_20150507/lay-k/ \\
       -C data/raw/task-001-enron-investigation/sample/
   ```

2. Run prepare.py in sample mode:
   ```bash
   python scripts/prepare.py \\
       --input-dir data/raw/task-001-enron-investigation/sample/ \\
       --output-dir data/processed/task-001-enron-investigation/ \\
       --sample-only
   ```

## Alternative: Use the Enron Subset on Kaggle

A pre-cleaned 500MB subset is available on Kaggle:
https://www.kaggle.com/datasets/wcukierski/enron-email-dataset

This can be used for testing. Note it may differ slightly from the CMU archive.

## Full Download

To download the complete 1.7 GB dataset:
```bash
python scripts/download.py
```
"""

    with open(instructions_file, "w", encoding="utf-8") as f:
        f.write(instructions)

    print(f"  Created sample placeholder at: {sample_dir}")
    print(f"  See {instructions_file} for instructions on getting a sample.")

    # Create a minimal synthetic test fixture with 5 fake emails
    fixtures_dir = sample_dir / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    fake_emails = [
        {
            "filename": "001.",
            "content": "Message-ID: <test-001@enron.com>\nDate: Mon, 15 Oct 2001 09:23:00 -0700\nFrom: kenneth.lay@enron.com\nTo: jeffrey.skilling@enron.com\nSubject: Q3 earnings call prep\n\nJeff,\n\nWe need to get aligned on messaging before the analyst call Thursday. \nI've asked Rick to prepare talking points on the trading segment.\n\nKen",
        },
        {
            "filename": "002.",
            "content": "Message-ID: <test-002@enron.com>\nDate: Wed, 17 Oct 2001 14:05:00 -0700\nFrom: sherron.watkins@enron.com\nTo: kenneth.lay@enron.com\nSubject: Skilling's Resignation\n\nDear Mr. Lay,\n\nHas Enron become a risky place to work? For those of us who didn't get \nout before the stock price dropped, I am incredibly nervous that we will \nimplode in a wave of accounting scandals. My eight years of Enron \nstock and options are worth nothing.\n\n[Note: This is a synthetic fixture email for testing only. The real Watkins memo \nis a well-documented public record.]",
        },
        {
            "filename": "003.",
            "content": "Message-ID: <test-003@enron.com>\nDate: Thu, 11 Oct 2001 11:30:00 -0700\nFrom: andrew.fastow@enron.com\nTo: ben.glisan@enron.com\nSubject: Raptor IV — closing docs\n\nBen,\n\nPlease coordinate with outside counsel on the Raptor IV closing schedule. \nWe need the valuation support finalized before we loop in the audit committee.\n\nAndy\n\n[Note: This is a synthetic fixture email for testing only.]",
        },
        {
            "filename": "004.",
            "content": "Message-ID: <test-004@enron.com>\nDate: Fri, 19 Oct 2001 08:15:00 -0700\nFrom: mark.koenig@enron.com\nTo: investor-relations@enron.com\nSubject: Analyst questions — follow up\n\nTeam,\n\nSeveral analysts are asking about the Raptors and the Q3 write-down. \nHold all replies until we've coordinated messaging with the executive team.\n\nMark\n\n[Note: This is a synthetic fixture email for testing only.]",
        },
        {
            "filename": "005.",
            "content": "Message-ID: <test-005@enron.com>\nDate: Mon, 29 Oct 2001 16:45:00 -0700\nFrom: jeffrey.skilling@enron.com\nTo: press@enron.com\nSubject: Media inquiry re: liquidity\n\nDo not comment on rumors. All press inquiries go through Koenig.\n\n[Note: This is a synthetic fixture email for testing only.]",
        },
    ]

    user_dir = fixtures_dir / "synthetic-test-user" / "inbox"
    user_dir.mkdir(parents=True, exist_ok=True)

    for email in fake_emails:
        path = user_dir / email["filename"]
        with open(path, "w", encoding="utf-8") as f:
            f.write(email["content"])

    print(f"  Created {len(fake_emails)} synthetic test fixtures at: {fixtures_dir}")
    print("  WARNING: These are synthetic fixtures for testing only. They do not represent")
    print("           real emails from the Enron dataset.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the Enron Email Dataset for Task 001",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download.py                          # Download full 1.7 GB archive
  python download.py --sample-only            # Create sample placeholder
  python download.py --force                  # Re-download even if exists
  python download.py --output-dir /tmp/enron  # Custom output directory
        """,
    )
    parser.add_argument(
        "--sample-only",
        action="store_true",
        help="Create sample placeholder directory instead of downloading full archive",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if the archive already exists",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/task-001-enron-investigation"),
        help="Output directory (default: data/raw/task-001-enron-investigation/)",
    )
    args = parser.parse_args()

    print(ETHICS_NOTICE)

    if not args.sample_only:
        print("Proceeding with full dataset download.")
        print("You can interrupt at any time with Ctrl+C.\n")

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {args.output_dir.resolve()}\n")

    if args.sample_only:
        print("SAMPLE MODE: Creating sample placeholder and test fixtures...")
        download_sample(args.output_dir, args.force)
    else:
        print("FULL MODE: Downloading Enron Email Dataset (~1.7 GB)...")
        download_full(args.output_dir, args.force)

    print("\nDone.")
    print("\nNext: Run prepare.py to parse emails into JSONL format:")
    print("  python tasks/task-001-enron-investigation/scripts/prepare.py")


if __name__ == "__main__":
    main()
