#!/usr/bin/env python3
"""
Download script for Task 003: Open Source Ecosystem Radar

Downloads hourly event files from GH Archive.
URL pattern: https://data.gharchive.org/YYYY-MM-DD-H.json.gz

Usage:
    python download.py --start-date 2025-01-01 --hours 2   # Sample: 2 hours
    python download.py --start-date 2025-01-01 --end-date 2025-01-01  # Full day (24 files)
    python download.py --start-date 2025-01-01 --end-date 2025-01-07  # One week
    python download.py --start-date 2025-01-01 --max-files 4          # Limit files
"""

import argparse
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

GHARCHIVE_BASE = "https://data.gharchive.org"
DEFAULT_OUTPUT_DIR = Path("data/raw/task-003-open-source-ecosystem-radar")
ATTRIBUTION = "Data source: GH Archive (https://www.gharchive.org/) — CC BY 4.0"


def get_requests():
    try:
        import requests
        return requests
    except ImportError:
        print("ERROR: 'requests' library not found. Install with: uv pip install requests")
        sys.exit(1)


def generate_urls(start_date: str, end_date: str, hours: int = None, max_files: int = None) -> List[Tuple[str, str]]:
    """
    Generate (url, filename) tuples for a date range.
    GH Archive uses 0-23 hour notation (no zero-padding).

    Args:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD (inclusive)
        hours: if set, only generate this many hours starting from start_date-0
        max_files: cap on total files

    Returns list of (url, filename) tuples.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start
    except ValueError as e:
        print(f"ERROR: Invalid date format: {e}")
        sys.exit(1)

    urls = []
    current = start

    while current <= end:
        for h in range(24):
            date_str = current.strftime("%Y-%m-%d")
            filename = f"{date_str}-{h}.json.gz"
            url = f"{GHARCHIVE_BASE}/{filename}"
            urls.append((url, filename))

            if hours and len(urls) >= hours:
                return urls[:max_files] if max_files else urls
            if max_files and len(urls) >= max_files:
                return urls

        current += timedelta(days=1)

    return urls[:max_files] if max_files else urls


def print_progress(downloaded: int, total: int, current_file: str, bar_width: int = 40) -> None:
    """Print download progress."""
    frac = downloaded / total if total > 0 else 0
    filled = int(bar_width * frac)
    bar = "=" * filled + "-" * (bar_width - filled)
    print(f"\r  [{bar}] {downloaded}/{total} {current_file[:30]:<30}", end="", flush=True)


def download_file(requests, url: str, dest_path: Path, chunk_size: int = 1024 * 64) -> bool:
    """
    Download a single file. Returns True on success, False on failure.
    """
    tmp_path = dest_path.with_suffix(".tmp")

    try:
        resp = requests.get(url, stream=True, timeout=60)
        if resp.status_code == 404:
            print(f"\n  404: {url} (file may not exist yet — check date)")
            return False
        resp.raise_for_status()

        with open(tmp_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        tmp_path.rename(dest_path)
        return True

    except Exception as e:
        print(f"\n  ERROR downloading {url}: {e}")
        if tmp_path.exists():
            tmp_path.unlink()
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download GH Archive data for Task 003",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{ATTRIBUTION}

Examples:
  python download.py --start-date 2025-01-01 --hours 2     # 2-hour sample
  python download.py --start-date 2025-01-01               # Full day (24 files ~1-3 GB)
  python download.py --start-date 2025-01-01 --end-date 2025-01-07  # One week
  python download.py --start-date 2025-01-01 --max-files 6

Note:
  Each file is 50-150 MB compressed.
  A full day = 24 files = ~1.2-3.6 GB.
  A week = 168 files = ~8-25 GB.
        """,
    )
    parser.add_argument(
        "--start-date",
        default="2025-01-01",
        help="Start date in YYYY-MM-DD format (default: 2025-01-01)",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help="End date in YYYY-MM-DD format (default: same as start-date)",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=None,
        help="Number of hours to download starting from start-date 00:00 UTC (overrides end-date)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Maximum number of files to download",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download files that already exist",
    )
    args = parser.parse_args()

    print(f"{ATTRIBUTION}\n")

    end_date = args.end_date or args.start_date
    urls = generate_urls(args.start_date, end_date, hours=args.hours, max_files=args.max_files)

    if not urls:
        print("ERROR: No files to download.")
        sys.exit(1)

    # Estimate size
    estimated_mb_per_file = 80  # midpoint of 50-150 MB range
    estimated_total_mb = len(urls) * estimated_mb_per_file
    print(f"Files to download: {len(urls)}")
    print(f"Estimated size:    ~{estimated_total_mb:,} MB (~{estimated_total_mb//1024:.1f} GB)")
    print(f"Output directory:  {args.output_dir.resolve()}")
    print()

    if len(urls) > 24 and not args.force:
        print(f"WARNING: Downloading {len(urls)} files (~{estimated_total_mb//1024:.1f} GB).")
        print("Press Ctrl+C to cancel, or continue...")
        time.sleep(2)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    requests = get_requests()

    downloaded = 0
    skipped = 0
    failed = 0
    start_time = time.time()

    for i, (url, filename) in enumerate(urls):
        dest = args.output_dir / filename

        if dest.exists() and not args.force:
            skipped += 1
            print_progress(i + 1, len(urls), f"[skip] {filename}")
            continue

        print_progress(i + 1, len(urls), filename)
        success = download_file(requests, url, dest)

        if success:
            downloaded += 1
            size_mb = dest.stat().st_size / 1_000_000
            print(f"\r  [{i+1}/{len(urls)}] {filename:<35} {size_mb:.1f} MB")
        else:
            failed += 1

        # Brief pause to avoid hammering GH Archive servers
        time.sleep(0.1)

    print()
    elapsed = time.time() - start_time
    total_size_mb = sum(
        (args.output_dir / fn).stat().st_size
        for _, fn in urls
        if (args.output_dir / fn).exists()
    ) / 1_000_000

    print(f"\nComplete in {elapsed:.1f}s:")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped:    {skipped} (already exist)")
    print(f"  Failed:     {failed}")
    print(f"  Total size: {total_size_mb:.1f} MB")

    if downloaded + skipped > 0:
        print(f"\nNext: Run prepare.py to aggregate events:")
        print(f"  python tasks/task-003-open-source-ecosystem-radar/scripts/prepare.py")


if __name__ == "__main__":
    main()
