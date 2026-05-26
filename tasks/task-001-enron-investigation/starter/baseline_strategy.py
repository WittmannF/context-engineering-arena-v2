#!/usr/bin/env python3
"""
Baseline Strategy — Task 001: The Enron Investigation Brief

This script demonstrates a simple (but weak) baseline approach:
  1. Load processed emails.jsonl
  2. Take the first N emails (or a random sample)
  3. Format them as a prompt
  4. Call an LLM API to produce a structured answer
  5. Write the answer to answer.json

This is intentionally a weak baseline. It is provided to show
the minimum viable approach and to clarify why better strategies
are needed.

LIMITATIONS OF THIS APPROACH:
  - Only reads N emails out of 517,000 — 99.99% of the corpus is ignored
  - Random or sequential sampling does not target relevant evidence
  - LLM will likely fill gaps with prior knowledge about Enron
  - No cross-document analysis or pattern detection
  - Timeline is built from whatever happens to be in the sample

Usage:
    python baseline_strategy.py
    python baseline_strategy.py --n 100
    python baseline_strategy.py --model claude-3-haiku-20240307
    python baseline_strategy.py --input-file data/samples/task-001-enron-investigation/sample_emails.jsonl
"""

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_INPUT = Path("data/processed/task-001-enron-investigation/emails.jsonl")
DEFAULT_SAMPLE_INPUT = Path("data/samples/task-001-enron-investigation/sample_emails.jsonl")
DEFAULT_OUTPUT = Path("submissions/my-submission/task-001-enron-investigation/answer.json")
DEFAULT_N = 50


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1: Load emails from JSONL
# ──────────────────────────────────────────────────────────────────────────────

def load_emails(input_file: Path, n: int, strategy: str = "first", seed: int = None) -> List[Dict]:
    """
    Load N emails from the processed JSONL file.

    Strategy options:
      - "first": Take the first N emails (fast, but biased toward early file paths)
      - "random": Random sample (requires loading all emails first — slow for large files)

    Limitation: Neither strategy is good for investigation purposes.
    You want targeted retrieval, not random or sequential sampling.
    """
    records = []

    if strategy == "first":
        # Fast path: stop reading after N records
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                    if len(records) >= n:
                        break
                except json.JSONDecodeError:
                    continue
        print(f"  Loaded first {len(records)} emails from {input_file}")

    elif strategy == "random":
        # Slow path: load all, then sample
        # LIMITATION: For 517K emails this requires loading several GB into memory
        # In practice you would stream and reservoir-sample
        print(f"  Loading all emails for random sampling (this may be slow)...")
        all_records = []
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    all_records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        print(f"  Loaded {len(all_records):,} total emails")
        if seed is not None:
            random.seed(seed)
        records = random.sample(all_records, min(n, len(all_records)))
        print(f"  Sampled {len(records)} emails randomly")

    return records


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2: Format emails as prompt context
# ──────────────────────────────────────────────────────────────────────────────

def format_email_for_prompt(email: Dict, index: int) -> str:
    """
    Format a single email as text for inclusion in a prompt.

    LIMITATION: This format includes full body text which is inefficient.
    A better approach would:
      - Truncate long bodies
      - Include only the most relevant excerpt
      - Add metadata about why this email was selected
    """
    sender = email.get("sender", "(unknown)")
    recipients = ", ".join(email.get("recipients", []))
    date = email.get("date") or email.get("date_raw", "(unknown date)")
    subject = email.get("subject", "(no subject)")
    body = email.get("body", "")

    # Truncate body to 500 chars for this baseline
    # A better strategy would select the most relevant excerpt, not just truncate
    if len(body) > 500:
        body = body[:500] + " [... truncated ...]"

    lines = [
        f"--- EMAIL {index + 1} ---",
        f"From: {sender}",
        f"To: {recipients}",
        f"Date: {date}",
        f"Subject: {subject}",
        f"Body:",
        body,
        "",
    ]
    return "\n".join(lines)


def build_prompt(emails: List[Dict]) -> str:
    """
    Build the full investigation prompt from a list of emails.

    LIMITATION: This puts all emails in a single prompt with no retrieval strategy.
    With 50 emails at ~500 chars each, this is about 25,000 tokens of context.
    A 517K email corpus would require ~200M tokens — far beyond any context window.
    """
    email_texts = [format_email_for_prompt(e, i) for i, e in enumerate(emails)]
    emails_block = "\n".join(email_texts)

    prompt = f"""You are an investigative journalist analyzing the Enron email archive.
Below are {len(emails)} emails sampled from the Enron email dataset (CMU/FERC release,
~517,000 total emails). These are a very small sample — acknowledge this limitation.

Your task: Based primarily on these emails (flag when using general knowledge),
produce a structured investigation brief answering:

  "What warning signs, coordination patterns, or internal tensions were visible
  before Enron's collapse, and what evidence supports those conclusions?"

IMPORTANT RULES:
1. Every major claim must cite a specific email from the list below using "Email N" notation
2. Label each claim with its type: "fact" (directly evidenced), "interpretation" (plausible
   but uncertain), or "uncertainty" (cannot be determined from these emails)
3. Include an explicit section on what was NOT covered and why
4. Do NOT reproduce email text verbatim beyond short excerpts

Return a JSON object with this structure:
{{
  "task_id": "task-001-enron-investigation",
  "participant_id": "my-submission",
  "title": "Enron Investigation Brief",
  "executive_summary": "...",
  "sections": [
    {{"id": "executive-summary", "title": "Executive Summary", "content": "..."}},
    {{"id": "investigative-timeline", "title": "Investigative Timeline", "content": "..."}},
    {{"id": "key-people-and-communication-patterns", "title": "Key People", "content": "..."}},
    {{"id": "main-themes-and-topic-clusters", "title": "Main Themes", "content": "..."}},
    {{"id": "evidence-backed-claims", "title": "Evidence-Backed Claims", "content": "..."}},
    {{"id": "contradictions-and-weak-signals", "title": "Contradictions and Weak Signals", "content": "..."}},
    {{"id": "documents-that-mattered-most", "title": "Documents That Mattered Most", "content": "..."}},
    {{"id": "what-was-ignored-and-why", "title": "What Was Ignored and Why", "content": "..."}},
    {{"id": "context-engineering-strategy", "title": "Context Engineering Strategy", "content": "..."}},
    {{"id": "ethical-and-evidentiary-limitations", "title": "Ethics and Limitations", "content": "..."}}
  ],
  "claims": [
    {{
      "id": "claim-001",
      "type": "fact | interpretation | uncertainty",
      "claim": "...",
      "confidence": 0.0,
      "evidence_ids": ["ev-001"],
      "topic": "..."
    }}
  ],
  "evidence": [
    {{
      "id": "ev-001",
      "email_from": "...",
      "email_to": ["..."],
      "date": "...",
      "subject": "...",
      "excerpt": "...",
      "relevance": "..."
    }}
  ],
  "timeline": [
    {{
      "date": "...",
      "event": "...",
      "source": "corpus_email | external_context",
      "evidence_ids": []
    }}
  ],
  "entities": [
    {{
      "name": "...",
      "type": "person | organization | vehicle | partnership",
      "role": "...",
      "significance": "..."
    }}
  ],
  "uncertainties": [
    {{
      "question": "...",
      "reason": "...",
      "what_would_resolve_it": "..."
    }}
  ],
  "limitations": [
    {{
      "description": "...",
      "impact": "..."
    }}
  ]
}}

---

EMAILS ({len(emails)} of 517,401 total):

{emails_block}

---

Produce the JSON investigation brief now:"""

    return prompt


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3: Call the LLM API
# ──────────────────────────────────────────────────────────────────────────────

def call_llm(prompt: str, model: str = "claude-3-haiku-20240307") -> str:
    """
    Call an LLM API with the prompt and return the response text.

    This function uses the Anthropic SDK as an example.
    Adapt for your preferred API (OpenAI, Cohere, etc.).

    LIMITATION: A single API call with a large prompt is not iterative.
    Better strategies would use multiple targeted calls, one per investigation
    question, and combine results.

    Returns the raw response text (expected to be JSON).
    """
    # ── Anthropic Claude example ──────────────────────────────────────────────
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic SDK not installed. Run: uv pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment.")
        print("Set it with: export ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"  Calling {model}...")
    print(f"  Prompt length: ~{len(prompt) // 4:,} estimated tokens")

    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    elapsed = time.time() - start

    text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = input_tokens + output_tokens

    print(f"  Response received in {elapsed:.1f}s")
    print(f"  Input tokens:  {input_tokens:,}")
    print(f"  Output tokens: {output_tokens:,}")
    print(f"  Total tokens:  {total_tokens:,}")

    # ── OpenAI example (commented out) ────────────────────────────────────────
    # import openai
    # client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # response = client.chat.completions.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=4096,
    # )
    # text = response.choices[0].message.content

    return text


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4: Parse and validate the LLM response
# ──────────────────────────────────────────────────────────────────────────────

def parse_response(raw: str) -> Dict[str, Any]:
    """
    Parse the LLM response as JSON.

    LIMITATION: LLMs sometimes produce malformed JSON or wrap the JSON in markdown
    code fences. This handles the common cases but is not robust.
    A production system would use structured outputs (function calling / JSON mode).
    """
    raw = raw.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Find first and last ``` lines
        start = 1  # skip ```json or ``` line
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        raw = "\n".join(lines[start:end])

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse LLM response as JSON: {e}")
        print(f"  Raw response (first 500 chars): {raw[:500]}")
        # Return a minimal valid structure so the script doesn't crash
        return {
            "task_id": "task-001-enron-investigation",
            "participant_id": "my-submission",
            "title": "Enron Investigation Brief (parse error)",
            "executive_summary": f"ERROR: LLM response could not be parsed as JSON. Raw: {raw[:200]}",
            "sections": [],
            "claims": [],
            "evidence": [],
            "timeline": [],
            "entities": [],
            "limitations": [{"description": "LLM response could not be parsed as JSON", "impact": "all output is missing"}],
            "_parse_error": str(e),
            "_raw_response": raw[:2000],
        }


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5: Write output
# ──────────────────────────────────────────────────────────────────────────────

def write_output(answer: Dict[str, Any], output_path: Path) -> None:
    """Write the answer.json file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(answer, f, indent=2, ensure_ascii=False)
    size_kb = output_path.stat().st_size / 1000
    print(f"  Written: {output_path} ({size_kb:.1f} KB)")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Baseline strategy for Task 001 — Enron Investigation Brief",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This is a WEAK BASELINE. Expected score: ~41/100.

Why it's weak:
  - Only reads {n} of 517,000 emails
  - No targeted retrieval strategy
  - LLM fills gaps with prior knowledge
  - No cross-document analysis

For a better approach, see the Hybrid RAG baseline.
        """,
    )
    parser.add_argument(
        "--n",
        type=int,
        default=DEFAULT_N,
        help=f"Number of emails to include in the prompt (default: {DEFAULT_N})",
    )
    parser.add_argument(
        "--strategy",
        choices=["first", "random"],
        default="first",
        help="Email selection strategy (default: first)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (only with --strategy random)",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=None,
        help="Input emails.jsonl file (auto-detects sample or full)",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output answer.json file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--model",
        default="claude-3-haiku-20240307",
        help="LLM model to use (default: claude-3-haiku-20240307)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build prompt and print it without calling the LLM",
    )
    args = parser.parse_args()

    # Auto-detect input file
    if args.input_file is None:
        if DEFAULT_SAMPLE_INPUT.exists():
            args.input_file = DEFAULT_SAMPLE_INPUT
            print(f"Using sample input: {args.input_file}")
        elif DEFAULT_INPUT.exists():
            args.input_file = DEFAULT_INPUT
            print(f"Using full input: {args.input_file}")
        else:
            print(f"ERROR: No input file found. Run prepare.py first.")
            print(f"  Expected: {DEFAULT_SAMPLE_INPUT}")
            print(f"       or: {DEFAULT_INPUT}")
            sys.exit(1)

    print("=" * 60)
    print("Baseline Strategy — Task 001: Enron Investigation")
    print("=" * 60)
    print(f"  Input:    {args.input_file}")
    print(f"  Output:   {args.output_file}")
    print(f"  N emails: {args.n}")
    print(f"  Strategy: {args.strategy}")
    print(f"  Model:    {args.model}")
    print()

    # Step 1: Load emails
    print("Step 1: Loading emails...")
    emails = load_emails(args.input_file, args.n, args.strategy, args.seed)

    if not emails:
        print("ERROR: No emails loaded.")
        sys.exit(1)

    # Step 2: Build prompt
    print(f"\nStep 2: Building prompt from {len(emails)} emails...")
    prompt = build_prompt(emails)
    estimated_tokens = len(prompt) // 4
    print(f"  Prompt length: ~{estimated_tokens:,} estimated tokens")
    print(f"  Corpus coverage: {len(emails)/517401*100:.4f}% of total dataset")
    print()
    print(f"  NOTE: This baseline reads only {len(emails):,} of 517,401 emails ({len(emails)/517401*100:.4f}%).")
    print(f"        The remaining 99.99% of the corpus is ignored.")
    print(f"        Any claims not supported by these {len(emails)} emails will likely")
    print(f"        come from LLM prior knowledge, not the dataset.")

    if args.dry_run:
        print("\n--- DRY RUN: Prompt (first 2000 chars) ---")
        print(prompt[:2000])
        print("--- END DRY RUN ---")
        print("\nDry run complete. No LLM call made.")
        return

    # Step 3: Call LLM
    print(f"\nStep 3: Calling LLM ({args.model})...")
    raw_response = call_llm(prompt, args.model)

    # Step 4: Parse response
    print("\nStep 4: Parsing LLM response...")
    answer = parse_response(raw_response)

    # Ensure required fields
    answer["task_id"] = "task-001-enron-investigation"
    answer["submitted_at"] = datetime.utcnow().isoformat() + "Z"
    answer["context_strategy"] = (
        f"Prompt-only baseline: {args.n} emails selected using '{args.strategy}' strategy. "
        f"No retrieval, indexing, or iterative refinement. "
        f"Model: {args.model}. "
        f"Coverage: {len(emails)/517401*100:.4f}% of total corpus."
    )

    # Count what we got
    n_claims = len(answer.get("claims", []))
    n_evidence = len(answer.get("evidence", []))
    n_timeline = len(answer.get("timeline", []))
    print(f"  Claims:   {n_claims}")
    print(f"  Evidence: {n_evidence}")
    print(f"  Timeline: {n_timeline} events")

    if n_claims < 5:
        print(f"  WARNING: Only {n_claims} claims (minimum is 5). Response may be incomplete.")
    if n_evidence < 3:
        print(f"  WARNING: Only {n_evidence} evidence items (minimum is 3).")

    # Step 5: Write output
    print(f"\nStep 5: Writing answer.json...")
    write_output(answer, args.output_file)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  Answer: {args.output_file}")
    print()
    print("LIMITATIONS OF THIS BASELINE:")
    print(f"  - Only read {len(emails):,} of 517,401 emails ({len(emails)/517401*100:.4f}% coverage)")
    print(f"  - No targeted retrieval — {args.strategy} selection")
    print(f"  - LLM may have used prior Enron knowledge to fill gaps")
    print(f"  - No cross-document analysis or entity tracking")
    print(f"  - Expected score: ~41/100 overall")
    print()
    print("For a stronger approach, implement Hybrid BM25 + Dense retrieval.")
    print("See: submissions/baseline-hybrid-rag/ for comparison.")


if __name__ == "__main__":
    main()
