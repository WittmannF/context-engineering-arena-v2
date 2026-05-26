#!/usr/bin/env python3
"""
Baseline Strategy — Task 002: Brazil Public Money Trail

Simple baseline that:
  1. Loads processed propositions and optional spending records
  2. Formats them as a prompt
  3. Calls an LLM to produce a structured civic analysis
  4. Writes answer.json

This is a WEAK BASELINE. Expected score: ~55/100.

Weaknesses:
  - Portal da Transparência data often unavailable (no token)
  - No cross-dataset entity resolution
  - No budget code matching for direct_documented_link classification
  - LLM may fill data gaps with prior knowledge

Usage:
    python baseline_strategy.py
    python baseline_strategy.py --theme saude --dry-run
    python baseline_strategy.py --model claude-3-haiku-20240307
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_INPUT_DIR = Path("data/processed/task-002-brazil-public-money-trail")
DEFAULT_SAMPLE_INPUT_DIR = Path("data/samples/task-002-brazil-public-money-trail")
DEFAULT_OUTPUT = Path("submissions/my-submission/task-002-brazil-public-money-trail/answer.json")

DISCLAIMER = (
    "DISCLAIMER: This page organizes publicly available Brazilian government data "
    "from the Câmara dos Deputados Dados Abertos API and Portal da Transparência. "
    "It does not allege wrongdoing, corruption, or illegal conduct by any individual "
    "or institution. Connections between legislative activity and public spending are "
    "classified by link type (direct_documented_link, same_theme_link, etc.) and "
    "do NOT imply causation. Correlation is not causation."
)


def load_jsonl(path: Path, n: int = None) -> List[Dict]:
    """Load records from a JSONL file."""
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


def load_json(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def format_proposition(p: Dict) -> str:
    """Format a proposition for the prompt."""
    return (
        f"[{p.get('short_id', p.get('id', '?'))}] "
        f"{p.get('ementa', 'no description')[:200]} "
        f"| Situation: {p.get('situacao', 'unknown')} "
        f"| Date: {p.get('data_apresentacao', 'unknown')}"
    )


def format_expense(e: Dict) -> str:
    """Format a spending record for the prompt."""
    synthetic_label = " [SYNTHETIC DATA - not real]" if e.get("is_synthetic") else ""
    return (
        f"{e.get('orgao_nome', '?')} (code {e.get('orgao_codigo', '?')}) "
        f"| Year: {e.get('year', '?')} "
        f"| Paid: R$ {e.get('valor_pago', 0):,.0f}{synthetic_label}"
    )


def build_prompt(
    propositions: List[Dict],
    expenses: List[Dict],
    candidate_links: List[Dict],
    theme: str,
    year_start: int,
    year_end: int,
    expenses_are_synthetic: bool,
) -> str:
    """Build the civic analysis prompt."""
    n_props = len(propositions)
    n_exp = len(expenses)

    props_text = "\n".join(f"  {i+1}. {format_proposition(p)}" for i, p in enumerate(propositions))
    if not props_text:
        props_text = "  (no propositions available)"

    if expenses:
        if expenses_are_synthetic:
            exp_header = f"PORTAL DA TRANSPARÊNCIA DATA (SYNTHETIC SAMPLE — NOT REAL DATA):"
        else:
            exp_header = "PORTAL DA TRANSPARÊNCIA DATA:"
        exp_text = "\n".join(f"  {i+1}. {format_expense(e)}" for i, e in enumerate(expenses))
    else:
        exp_header = "PORTAL DA TRANSPARÊNCIA DATA:"
        exp_text = "  (not available — API token not set)"

    link_text = ""
    if candidate_links:
        link_text = "\nCANDIDATE LINKS (pre-classified by prepare.py):\n"
        for link in candidate_links[:5]:
            link_text += f"  [{link['link_type']}] {link.get('explanation', '')[:150]}\n"

    prompt = f"""You are a civic data analyst for a Brazilian accountability journalism project.

TASK: Trace the policy theme '{theme}' from legislative activity to federal public spending,
covering years {year_start}–{year_end}. Answer: what can be verified, which actors and agencies
appear, what changed over time, and what questions remain open?

MANDATORY RULES:
1. Label every claim: "fact" (in the data), "interpretation" (inference), or "uncertainty"
2. Classify every cross-source link using ONLY: direct_documented_link, same_theme_link,
   same_actor_link, same_agency_link, same_time_window_link, weak_or_hypothetical_link
3. NEVER assert corruption or illegal conduct without authoritative evidence
4. NEVER upgrade a same_theme_link to direct_documented_link without a matching budget code
5. If Portal da Transparência data is synthetic or missing, mark ALL spending claims as uncertainty
6. Include this exact disclaimer: "{DISCLAIMER}"

DATA AVAILABLE:
  - Câmara Propositions: {n_props} propositions
  - Spending Records: {n_exp} records{"  [SYNTHETIC]" if expenses_are_synthetic else ""}
  - Pre-classified candidate links: {len(candidate_links)}

---

CÂMARA DOS DEPUTADOS — LEGISLATIVE PROPOSITIONS ({n_props} records, theme='{theme}', {year_start}-{year_end}):
{props_text}

{exp_header}
{exp_text}
{link_text}
---

Produce a JSON analysis matching the task-002-brazil-public-money-trail schema:
{{
  "task_id": "task-002-brazil-public-money-trail",
  "participant_id": "my-submission",
  "policy_theme": "{theme}",
  "year_range": {{"start": {year_start}, "end": {year_end}}},
  "title": "...",
  "disclaimer": "{DISCLAIMER}",
  "executive_summary": "...",
  "sections": [
    {{"id": "executive-summary", "title": "Executive Summary", "content": "..."}},
    {{"id": "policy-theme-and-scope", "title": "Policy Theme and Scope", "content": "..."}},
    {{"id": "legislative-activity-timeline", "title": "Legislative Activity Timeline", "content": "..."}},
    {{"id": "public-spending-timeline", "title": "Public Spending Timeline", "content": "..."}},
    {{"id": "actor-and-institution-map", "title": "Actors and Institutions", "content": "..."}},
    {{"id": "money-flow-overview", "title": "Money Flow Overview", "content": "..."}},
    {{"id": "evidence-backed-claims", "title": "Evidence-Backed Claims", "content": "..."}},
    {{"id": "direct-links-vs-hypotheses", "title": "Direct Links vs Hypotheses", "content": "..."}},
    {{"id": "red-flags-and-accountability-questions", "title": "Accountability Questions", "content": "..."}},
    {{"id": "what-could-not-be-verified", "title": "What Could Not Be Verified", "content": "..."}},
    {{"id": "recommended-next-investigations", "title": "Recommended Next Steps", "content": "..."}},
    {{"id": "context-engineering-strategy", "title": "Context Engineering Strategy", "content": "..."}},
    {{"id": "data-and-ethics-limitations", "title": "Data and Ethics Limitations", "content": "..."}}
  ],
  "claims": [...],
  "evidence": [...],
  "timeline": [...],
  "entities": [...],
  "candidate_links": [...],
  "limitations": [...]
}}

Be rigorous: never imply causation, always cite sources, always classify links.
"""
    return prompt


def call_llm(prompt: str, model: str) -> str:
    """Call an LLM API. Uses Anthropic Claude by default."""
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic SDK not installed. Run: uv pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    print(f"  Calling {model} (~{len(prompt)//4:,} estimated tokens)...")

    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.time() - start
    print(f"  Response in {elapsed:.1f}s | in={response.usage.input_tokens} out={response.usage.output_tokens}")
    return response.content[0].text


def parse_response(raw: str) -> Dict:
    """Parse LLM response as JSON."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        raw = "\n".join(lines[start:end])
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "task_id": "task-002-brazil-public-money-trail",
            "title": "Parse error",
            "executive_summary": f"ERROR: {e}",
            "sections": [],
            "claims": [],
            "evidence": [],
            "timeline": [],
            "entities": [],
            "limitations": [{"description": f"LLM response parse error: {e}"}],
            "_parse_error": str(e),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline strategy for Task 002")
    parser.add_argument("--theme", default="saude", help="Policy theme (default: saude)")
    parser.add_argument("--n-props", type=int, default=30, help="Propositions to include (default: 30)")
    parser.add_argument("--n-exp", type=int, default=10, help="Spending records to include (default: 10)")
    parser.add_argument("--input-dir", type=Path, default=None)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--model", default="claude-3-haiku-20240307")
    parser.add_argument("--dry-run", action="store_true", help="Build prompt without calling LLM")
    args = parser.parse_args()

    # Auto-detect input
    if args.input_dir is None:
        if DEFAULT_SAMPLE_INPUT_DIR.exists():
            args.input_dir = DEFAULT_SAMPLE_INPUT_DIR
        elif DEFAULT_INPUT_DIR.exists():
            args.input_dir = DEFAULT_INPUT_DIR
        else:
            print("ERROR: No processed data found. Run prepare.py first.")
            sys.exit(1)

    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_file}")
    print()

    # Load data
    propositions = load_jsonl(args.input_dir / "propositions.jsonl", args.n_props)
    deputies = load_jsonl(args.input_dir / "deputies.jsonl", 20)
    expenses_real = load_jsonl(args.input_dir / "expenses.jsonl", args.n_exp)
    expenses_synthetic = load_jsonl(args.input_dir / "expenses_SYNTHETIC.jsonl", args.n_exp)
    candidate_links = load_jsonl(args.input_dir / "candidate_links.jsonl", 10)
    stats = load_json(args.input_dir / "dataset_stats.json") or {}

    expenses = expenses_real if expenses_real else expenses_synthetic
    expenses_are_synthetic = bool(expenses_synthetic) and not expenses_real

    year_start = stats.get("year_start", 2022)
    year_end = stats.get("year_end", 2024)
    theme = stats.get("theme", args.theme)

    print(f"  Loaded {len(propositions)} propositions, {len(expenses)} spending records")
    if expenses_are_synthetic:
        print("  WARNING: Using synthetic spending data (no real Portal da Transparência data)")

    # Build prompt
    prompt = build_prompt(propositions, expenses, candidate_links, theme, year_start, year_end, expenses_are_synthetic)
    print(f"  Prompt: ~{len(prompt)//4:,} tokens")

    if args.dry_run:
        print("\n--- PROMPT (first 2000 chars) ---")
        print(prompt[:2000])
        return

    # Call LLM
    raw = call_llm(prompt, args.model)

    # Parse
    answer = parse_response(raw)
    answer["task_id"] = "task-002-brazil-public-money-trail"
    answer["submitted_at"] = datetime.utcnow().isoformat() + "Z"
    answer["data_sources_used"] = (
        ["camara", "transparencia"] if expenses_real
        else (["camara", "transparencia_synthetic"] if expenses_synthetic else ["camara"])
    )
    answer["disclaimer"] = DISCLAIMER

    # Write
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(answer, f, indent=2, ensure_ascii=False)
    print(f"\nAnswer written: {args.output_file}")
    print(f"  Claims: {len(answer.get('claims', []))}")
    print(f"  Evidence: {len(answer.get('evidence', []))}")
    print(f"  Timeline: {len(answer.get('timeline', []))}")


if __name__ == "__main__":
    main()
