#!/usr/bin/env python3
"""
Prepare script for Task 001: The Enron Investigation Brief

Walks the Enron email directory tree, parses each email, and writes:
  - emails.jsonl          (one JSON object per email)
  - dataset_stats.json    (counts and summary)

Usage:
    python prepare.py
    python prepare.py --sample-only          # Process only first 500 emails
    python prepare.py --format sqlite        # Write to SQLite instead of JSONL
    python prepare.py --input-dir /path/to/enron_mail/
    python prepare.py --output-dir /path/to/output/
"""

import argparse
import email
import email.policy
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_INPUT_DIR = Path("data/raw/task-001-enron-investigation")
DEFAULT_OUTPUT_DIR = Path("data/processed/task-001-enron-investigation")


def extract_email_address(raw: str) -> str:
    """Extract a clean email address from a raw header value."""
    if not raw:
        return ""
    raw = raw.strip()
    # Try to extract <email> pattern
    match = re.search(r"<([^>]+)>", raw)
    if match:
        return match.group(1).strip().lower()
    # Otherwise return as-is if it looks like an email
    if "@" in raw:
        return raw.lower()
    return raw.lower()


def parse_recipients(raw: str) -> List[str]:
    """Parse a comma-separated list of recipients from an email header."""
    if not raw:
        return []
    parts = re.split(r",\s*", raw)
    result = []
    for part in parts:
        addr = extract_email_address(part.strip())
        if addr:
            result.append(addr)
    return result


def parse_date(date_str: str) -> Optional[str]:
    """
    Attempt to parse an email Date header into an ISO 8601 string.
    Returns None if parsing fails.
    """
    if not date_str:
        return None
    try:
        # email.utils.parsedate_to_datetime handles most RFC 2822 formats
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str.strip())
        return dt.isoformat()
    except Exception:
        return date_str.strip()


def extract_text_body(msg: email.message.Message) -> str:
    """
    Walk a MIME message and extract the plain text body.
    Handles multipart messages, prefers text/plain.
    """
    body_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        text = payload.decode(charset, errors="replace")
                    except (LookupError, UnicodeDecodeError):
                        text = payload.decode("utf-8", errors="replace")
                    body_parts.append(text)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
                text = payload.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                text = payload.decode("utf-8", errors="replace")
            body_parts.append(text)

    body = "\n".join(body_parts).strip()

    # Truncate very long bodies to 10,000 chars to keep JSONL manageable
    if len(body) > 10000:
        body = body[:10000] + "\n[... truncated at 10,000 chars ...]"

    return body


def parse_email_file(file_path: Path, base_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Parse a single email file and return a dict record.
    Returns None if the file cannot be parsed as an email.
    """
    try:
        # Read raw bytes first to handle encoding issues
        raw_bytes = file_path.read_bytes()

        # Parse the email
        msg = email.message_from_bytes(raw_bytes, policy=email.policy.compat32)

        # Extract basic header fields
        message_id = (msg.get("Message-ID") or "").strip()
        sender_raw = msg.get("From") or ""
        to_raw = msg.get("To") or ""
        cc_raw = msg.get("Cc") or ""
        bcc_raw = msg.get("Bcc") or ""
        subject = (msg.get("Subject") or "").strip()
        date_raw = msg.get("Date") or ""
        x_folder = (msg.get("X-Folder") or "").strip()
        x_origin = (msg.get("X-Origin") or "").strip()

        sender = extract_email_address(sender_raw)
        recipients = parse_recipients(to_raw)
        cc = parse_recipients(cc_raw)
        bcc = parse_recipients(bcc_raw)
        date_parsed = parse_date(date_raw)

        body = extract_text_body(msg)

        # Compute relative file path from base dir
        try:
            rel_path = str(file_path.relative_to(base_dir))
        except ValueError:
            rel_path = str(file_path)

        # User folder is the top-level directory in the archive structure
        path_parts = rel_path.replace("\\", "/").split("/")
        user_folder = "/".join(path_parts[:2]) if len(path_parts) >= 2 else path_parts[0]

        return {
            "message_id": message_id,
            "sender": sender,
            "recipients": recipients,
            "cc": cc,
            "bcc": bcc,
            "subject": subject,
            "date": date_parsed,
            "date_raw": date_raw,
            "body": body,
            "body_length": len(body),
            "file_path": rel_path,
            "user_folder": user_folder,
            "x_folder": x_folder,
            "x_origin": x_origin,
        }

    except Exception as e:
        # Log parse errors but continue
        return None


def find_email_files(input_dir: Path) -> List[Path]:
    """
    Walk the directory tree and find all email files.
    Enron email files are typically named as numbers with a trailing period (e.g. '123.')
    or numeric filenames without extension.
    """
    email_files = []
    for root, dirs, files in os.walk(input_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            # Skip obvious non-email files
            if fname.startswith("."):
                continue
            if fname.endswith(".md") or fname.endswith(".txt") and "README" in fname.upper():
                continue
            email_files.append(Path(root) / fname)
    return sorted(email_files)


def write_jsonl(records: List[Dict[str, Any]], output_path: Path) -> None:
    """Write records to a JSONL file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")


def write_sqlite(records: List[Dict[str, Any]], output_path: Path) -> None:
    """Write records to a SQLite database."""
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT,
            sender TEXT,
            recipients TEXT,
            cc TEXT,
            subject TEXT,
            date TEXT,
            date_raw TEXT,
            body TEXT,
            body_length INTEGER,
            file_path TEXT,
            user_folder TEXT,
            x_folder TEXT,
            x_origin TEXT
        )
    """)

    for r in records:
        cursor.execute("""
            INSERT INTO emails
            (message_id, sender, recipients, cc, subject, date, date_raw,
             body, body_length, file_path, user_folder, x_folder, x_origin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("message_id", ""),
            r.get("sender", ""),
            json.dumps(r.get("recipients", [])),
            json.dumps(r.get("cc", [])),
            r.get("subject", ""),
            r.get("date", ""),
            r.get("date_raw", ""),
            r.get("body", ""),
            r.get("body_length", 0),
            r.get("file_path", ""),
            r.get("user_folder", ""),
            r.get("x_folder", ""),
            r.get("x_origin", ""),
        ))

    conn.commit()
    conn.close()


def compute_stats(records: List[Dict[str, Any]], parse_errors: int, total_files: int) -> Dict[str, Any]:
    """Compute dataset statistics from the parsed records."""
    senders = {}
    dates = []
    folders = {}
    subject_lengths = []
    body_lengths = []
    no_body_count = 0
    no_date_count = 0

    for r in records:
        sender = r.get("sender", "")
        if sender:
            senders[sender] = senders.get(sender, 0) + 1

        date = r.get("date")
        if date:
            dates.append(date)
        else:
            no_date_count += 1

        folder = r.get("user_folder", "unknown")
        folders[folder] = folders.get(folder, 0) + 1

        body = r.get("body", "")
        bl = len(body)
        body_lengths.append(bl)
        if bl == 0:
            no_body_count += 1

        subj = r.get("subject", "")
        subject_lengths.append(len(subj))

    top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:20]

    return {
        "total_files_found": total_files,
        "total_emails_parsed": len(records),
        "parse_errors": parse_errors,
        "unique_senders": len(senders),
        "top_20_senders": [{"sender": s, "count": c} for s, c in top_senders],
        "unique_user_folders": len(folders),
        "date_range_approx": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None,
        },
        "emails_with_no_date": no_date_count,
        "emails_with_no_body": no_body_count,
        "avg_body_length_chars": int(sum(body_lengths) / len(body_lengths)) if body_lengths else 0,
        "avg_subject_length_chars": int(sum(subject_lengths) / len(subject_lengths)) if subject_lengths else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse Enron emails into JSONL format for Task 001",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prepare.py
  python prepare.py --sample-only
  python prepare.py --format sqlite
  python prepare.py --input-dir data/raw/task-001-enron-investigation/enron_mail_20150507/
        """,
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Input directory containing extracted Enron archive (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for processed data (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--sample-only",
        action="store_true",
        help="Process only the first 500 emails (for quick testing)",
    )
    parser.add_argument(
        "--format",
        choices=["jsonl", "sqlite"],
        default="jsonl",
        help="Output format: jsonl (default) or sqlite",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"ERROR: Input directory not found: {args.input_dir}")
        print("Run download.py first to get the dataset.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input:  {args.input_dir.resolve()}")
    print(f"Output: {args.output_dir.resolve()}")
    print(f"Format: {args.format}")
    if args.sample_only:
        print("Mode:   SAMPLE (first 500 emails only)")
    else:
        print("Mode:   FULL")
    print()

    # Find all email files
    print("Scanning for email files...")
    email_files = find_email_files(args.input_dir)
    print(f"  Found {len(email_files):,} files")

    if args.sample_only:
        email_files = email_files[:500]
        print(f"  Sample mode: limited to {len(email_files)} files")
    print()

    # Parse emails
    print("Parsing emails...")
    records = []
    parse_errors = 0
    total_files = len(email_files)
    report_every = max(1, total_files // 20)

    start_time = time.time()

    for i, file_path in enumerate(email_files):
        record = parse_email_file(file_path, args.input_dir)
        if record is not None:
            records.append(record)
        else:
            parse_errors += 1

        if (i + 1) % report_every == 0 or (i + 1) == total_files:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            pct = (i + 1) / total_files * 100
            print(
                f"  [{pct:5.1f}%] {i+1:,}/{total_files:,} files processed "
                f"({len(records):,} parsed, {parse_errors:,} errors) "
                f"[{rate:.0f} emails/sec]"
            )

    elapsed = time.time() - start_time
    print(f"\nParsing complete in {elapsed:.1f}s")
    print(f"  Parsed:      {len(records):,} emails")
    print(f"  Errors:      {parse_errors:,} files")
    print()

    # Write output
    if args.format == "jsonl":
        output_path = args.output_dir / "emails.jsonl"
        print(f"Writing JSONL: {output_path}")
        write_jsonl(records, output_path)
        size_mb = output_path.stat().st_size / 1_000_000
        print(f"  Written: {size_mb:.1f} MB ({len(records):,} records)")
    else:
        output_path = args.output_dir / "emails.db"
        print(f"Writing SQLite: {output_path}")
        write_sqlite(records, output_path)
        size_mb = output_path.stat().st_size / 1_000_000
        print(f"  Written: {size_mb:.1f} MB ({len(records):,} records)")

    # Compute and write stats
    print("\nComputing dataset statistics...")
    stats = compute_stats(records, parse_errors, total_files)
    stats_path = args.output_dir / "dataset_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"  Stats written: {stats_path}")

    print("\nDataset summary:")
    print(f"  Total emails parsed:   {stats['total_emails_parsed']:,}")
    print(f"  Unique senders:        {stats['unique_senders']:,}")
    print(f"  User folders:          {stats['unique_user_folders']:,}")
    print(f"  Date range:            {stats['date_range_approx']['earliest']} — {stats['date_range_approx']['latest']}")
    print(f"  Avg body length:       {stats['avg_body_length_chars']:,} chars")
    print()
    print("Top 5 senders by email count:")
    for entry in stats["top_20_senders"][:5]:
        print(f"  {entry['count']:6,}  {entry['sender']}")

    print("\nDone. Ready for analysis.")
    print(f"\nNext: Run sample.py to create a small sample:")
    print(f"  python tasks/task-001-enron-investigation/scripts/sample.py")


if __name__ == "__main__":
    main()
