#!/usr/bin/env python3
"""
Prepare script for Task 002: Brazil Public Money Trail

Reads raw JSON files from download.py and produces normalized JSONL files:
  - propositions.jsonl        (legislative propositions)
  - deputies.jsonl            (deputy records)
  - expenses.jsonl            (spending records, if available)
  - timeline_events.jsonl     (unified timeline across sources)
  - candidate_links.jsonl     (classified connections between legislative and spending)
  - evidence_index.jsonl      (all evidence items for indexing)
  - dataset_stats.json        (summary statistics)

Usage:
    python prepare.py
    python prepare.py --input-dir data/raw/task-002-brazil-public-money-trail/
    python prepare.py --output-dir data/processed/task-002-brazil-public-money-trail/
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_INPUT_DIR = Path("data/raw/task-002-brazil-public-money-trail")
DEFAULT_OUTPUT_DIR = Path("data/processed/task-002-brazil-public-money-trail")

# Link type taxonomy for candidate connections
LINK_TYPES = [
    "direct_documented_link",
    "same_theme_link",
    "same_actor_link",
    "same_agency_link",
    "same_time_window_link",
    "weak_or_hypothetical_link",
]


# ──────────────────────────────────────────────────────────────────────────────
# I/O helpers
# ──────────────────────────────────────────────────────────────────────────────

def read_json(path: Path) -> Optional[Any]:
    """Read a JSON file and return the parsed content."""
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_jsonl(records: List[Dict], path: Path) -> None:
    """Write records to a JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    print(f"  Written: {path} ({len(records)} records)")


def write_json(data: Any, path: Path) -> None:
    """Write data as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Written: {path}")


# ──────────────────────────────────────────────────────────────────────────────
# Normalize Câmara propositions
# ──────────────────────────────────────────────────────────────────────────────

def normalize_proposition(raw: Dict) -> Dict:
    """
    Normalize a raw Câmara API proposition record to a clean, consistent format.

    Câmara API fields vary by endpoint; this handles the /proposicoes list format.
    """
    prop_id = raw.get("id") or raw.get("idProposicao") or ""
    siglaTipo = raw.get("siglaTipo", "")
    numero = raw.get("numero", "")
    ano = raw.get("ano", "")
    ementa = raw.get("ementa") or raw.get("ementaDetalhada") or ""
    keywords = raw.get("keywords") or raw.get("palavrasChave") or ""
    apresentacao = raw.get("dataApresentacao", "")
    uri = raw.get("uri", "")
    situacao = raw.get("ultimoStatus", {}).get("descricaoSituacao", "") if isinstance(raw.get("ultimoStatus"), dict) else ""
    author = raw.get("ultimoStatus", {}).get("siglaOrgao", "") if isinstance(raw.get("ultimoStatus"), dict) else ""

    # Construct short ID like "PL 1234/2023"
    short_id = f"{siglaTipo} {numero}/{ano}".strip(" /") if siglaTipo else str(prop_id)

    return {
        "id": str(prop_id),
        "short_id": short_id,
        "tipo": siglaTipo,
        "numero": numero,
        "ano": ano,
        "ementa": ementa[:500] if ementa else "",
        "keywords": keywords,
        "data_apresentacao": apresentacao[:10] if apresentacao else "",
        "situacao": situacao,
        "orgao": author,
        "uri_camara": uri,
        "source": "camara",
    }


def process_propositions(raw_data: Dict) -> List[Dict]:
    """Process raw Câmara propositions into normalized records."""
    dados = raw_data.get("dados", [])
    normalized = []
    for item in dados:
        try:
            normalized.append(normalize_proposition(item))
        except Exception as e:
            print(f"  Warning: Could not normalize proposition {item.get('id')}: {e}")
    return normalized


# ──────────────────────────────────────────────────────────────────────────────
# Normalize Câmara deputies
# ──────────────────────────────────────────────────────────────────────────────

def normalize_deputy(raw: Dict) -> Dict:
    """Normalize a raw deputy record."""
    return {
        "id": str(raw.get("id", "")),
        "name": raw.get("nome", ""),
        "party": raw.get("siglaPartido", ""),
        "state": raw.get("siglaUf", ""),
        "legislature": raw.get("idLegislatura", ""),
        "uri_camara": raw.get("uri", ""),
        "photo_url": raw.get("urlFoto", ""),
        "source": "camara",
    }


def process_deputies(raw_data: Dict) -> List[Dict]:
    """Process raw deputy records."""
    dados = raw_data.get("dados", [])
    return [normalize_deputy(d) for d in dados if isinstance(d, dict)]


# ──────────────────────────────────────────────────────────────────────────────
# Normalize Portal da Transparência spending
# ──────────────────────────────────────────────────────────────────────────────

def normalize_expense(raw: Dict) -> Dict:
    """
    Normalize a raw Portal da Transparência spending record.

    The Portal da Transparência has several endpoint formats; this handles
    the /despesas/por-orgao aggregate format.
    """
    is_synthetic = raw.get("_synthetic", False)

    return {
        "orgao_nome": raw.get("orgaoNome") or raw.get("nomeOrgao") or "",
        "orgao_codigo": str(raw.get("orgaoCodigo") or raw.get("codigoOrgao") or ""),
        "year": raw.get("_year"),
        "theme": raw.get("_theme", ""),
        "valor_dotacao": float(raw.get("valorDotacaoAtualizada") or 0),
        "valor_empenhado": float(raw.get("valorEmpenhado") or 0),
        "valor_liquidado": float(raw.get("valorLiquidado") or 0),
        "valor_pago": float(raw.get("valorPago") or 0),
        "is_synthetic": is_synthetic,
        "source": "transparencia",
    }


def process_expenses(raw_data: Dict) -> List[Dict]:
    """Process raw spending records."""
    is_synthetic = raw_data.get("is_synthetic", False)
    dados = raw_data.get("dados", [])
    records = [normalize_expense(d) for d in dados if isinstance(d, dict)]
    if is_synthetic:
        print(f"  NOTE: Processing SYNTHETIC spending data (not real government figures)")
    return records


# ──────────────────────────────────────────────────────────────────────────────
# Build unified timeline
# ──────────────────────────────────────────────────────────────────────────────

def build_timeline(propositions: List[Dict], expenses: List[Dict]) -> List[Dict]:
    """
    Build a unified timeline of legislative and spending events.
    Each event has a source tag so readers know where it came from.
    """
    events = []

    # Add legislative events
    for prop in propositions:
        date = prop.get("data_apresentacao")
        if not date:
            continue
        events.append({
            "date": date,
            "event": f"Proposition {prop['short_id']} submitted: {prop['ementa'][:100]}",
            "event_type": "legislative",
            "source_api": "camara",
            "record_id": prop["id"],
            "situacao": prop.get("situacao", ""),
        })

    # Add spending events (annual)
    for exp in expenses:
        year = exp.get("year")
        if not year:
            continue
        events.append({
            "date": f"{year}-12-31",
            "event": f"Annual spending — {exp['orgao_nome']}: R$ {exp['valor_pago']:,.0f} paid",
            "event_type": "spending",
            "source_api": "transparencia",
            "record_id": exp.get("orgao_codigo", ""),
            "is_synthetic": exp.get("is_synthetic", False),
        })

    # Sort chronologically
    events.sort(key=lambda e: e.get("date") or "")
    return events


# ──────────────────────────────────────────────────────────────────────────────
# Build candidate links
# ──────────────────────────────────────────────────────────────────────────────

def build_candidate_links(
    propositions: List[Dict],
    expenses: List[Dict],
    theme: str,
) -> List[Dict]:
    """
    Build a list of candidate connections between legislative and spending data.
    Each connection is classified by link type.

    IMPORTANT: This function is conservative — it never upgrades a same_theme_link
    to a direct_documented_link without explicit documentary evidence.
    Most connections between legislative propositions and spending records are
    at best same_theme_link or same_time_window_link.
    """
    links = []
    link_counter = 1

    # For each combination, classify the link
    # In a real analysis, this would use budget program codes to find direct links
    # Without program codes, most links are same_theme or same_time_window

    for prop in propositions[:10]:  # Limit to 10 for performance in baseline
        prop_year = int(prop.get("ano") or 0) if str(prop.get("ano", "")).isdigit() else 0

        for exp in expenses[:5]:  # Limit to 5 spending records per proposition
            exp_year = int(exp.get("year") or 0)

            # Determine link type based on what we can verify
            # Without matching budget codes, we can only establish same_theme
            if abs(prop_year - exp_year) <= 1:
                link_type = "same_theme_link"
                confidence = 0.35
                explanation = (
                    f"Proposition {prop['short_id']} concerns '{prop.get('ementa', '')[:80]}' "
                    f"and spending from {exp['orgao_nome']} is in the same policy domain ({theme}). "
                    f"This is a thematic link only — no budget code match was found. "
                    f"This does not establish a causal or documented direct relationship."
                )
            else:
                link_type = "same_time_window_link"
                confidence = 0.20
                explanation = (
                    f"Proposition {prop['short_id']} (year {prop_year}) and "
                    f"spending from {exp['orgao_nome']} (year {exp_year}) appear in overlapping periods. "
                    f"This is a temporal co-occurrence only."
                )

            links.append({
                "id": f"link-{link_counter:03d}",
                "legislative_ref": prop["id"],
                "legislative_short_id": prop["short_id"],
                "spending_ref": exp.get("orgao_codigo", ""),
                "spending_orgao": exp.get("orgao_nome", ""),
                "link_type": link_type,
                "confidence": confidence,
                "explanation": explanation,
                "is_causal": False,  # Never set to True without documentary evidence
                "causal_warning": "This link does NOT establish causation. It is analytical/thematic.",
            })
            link_counter += 1

    return links


# ──────────────────────────────────────────────────────────────────────────────
# Build evidence index
# ──────────────────────────────────────────────────────────────────────────────

def build_evidence_index(
    propositions: List[Dict],
    deputies: List[Dict],
    expenses: List[Dict],
) -> List[Dict]:
    """Build a flat evidence index from all sources for easy citation."""
    evidence = []
    counter = 1

    for prop in propositions[:30]:  # Top 30 propositions as evidence
        evidence.append({
            "id": f"ev-camara-{counter:03d}",
            "source_api": "camara",
            "source_name": "Câmara dos Deputados Dados Abertos",
            "record_id": prop["id"],
            "description": f"Proposition {prop['short_id']}: {prop['ementa'][:200]}",
            "date": prop.get("data_apresentacao"),
            "url": prop.get("uri_camara"),
            "situacao": prop.get("situacao"),
            "endpoint": f"GET /api/v2/proposicoes/{prop['id']}",
        })
        counter += 1

    counter = 1
    for exp in expenses[:10]:  # Top 10 spending records as evidence
        evidence.append({
            "id": f"ev-transparencia-{counter:03d}",
            "source_api": "transparencia",
            "source_name": "Portal da Transparência",
            "record_id": exp.get("orgao_codigo"),
            "description": f"{exp['orgao_nome']} — year {exp.get('year')}: R$ {exp['valor_pago']:,.0f} paid",
            "value": f"R$ {exp['valor_pago']:,.0f}",
            "year": exp.get("year"),
            "is_synthetic": exp.get("is_synthetic", False),
        })
        counter += 1

    return evidence


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare data for Task 002: Brazil Public Money Trail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Raw data directory (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"ERROR: Input directory not found: {args.input_dir}")
        print("Run download.py first.")
        sys.exit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Input:  {args.input_dir.resolve()}")
    print(f"Output: {args.output_dir.resolve()}")
    print()

    # ── Read raw files ─────────────────────────────────────────────────────────
    print("Reading raw files...")
    props_raw = read_json(args.input_dir / "camara_propositions.json")
    deputies_raw = read_json(args.input_dir / "camara_deputies.json")
    expenses_raw = read_json(args.input_dir / "transparencia_spending.json")
    expenses_synthetic_raw = read_json(args.input_dir / "transparencia_spending_SYNTHETIC.json")
    download_stats = read_json(args.input_dir / "download_stats.json")

    theme = (download_stats or {}).get("theme", "saude")
    year_start = (download_stats or {}).get("year_start", 2022)
    year_end = (download_stats or {}).get("year_end", 2024)

    # ── Process propositions ───────────────────────────────────────────────────
    propositions = []
    if props_raw:
        print("\nProcessing legislative propositions...")
        propositions = process_propositions(props_raw)
        write_jsonl(propositions, args.output_dir / "propositions.jsonl")
    else:
        print("\nNo propositions data found. Run download.py first.")

    # ── Process deputies ───────────────────────────────────────────────────────
    deputies = []
    if deputies_raw:
        print("\nProcessing deputies...")
        deputies = process_deputies(deputies_raw)
        write_jsonl(deputies, args.output_dir / "deputies.jsonl")
    else:
        print("\nNo deputies data (OK in sample mode).")

    # ── Process expenses ───────────────────────────────────────────────────────
    expenses = []
    expenses_is_synthetic = False
    # Prefer real spending data; fall back to synthetic
    if expenses_raw:
        print("\nProcessing spending records (real data)...")
        expenses = process_expenses(expenses_raw)
        write_jsonl(expenses, args.output_dir / "expenses.jsonl")
    elif expenses_synthetic_raw:
        print("\nProcessing spending records (SYNTHETIC sample)...")
        expenses_is_synthetic = True
        expenses = process_expenses(expenses_synthetic_raw)
        # Write with _SYNTHETIC suffix to make clear this is not real data
        write_jsonl(expenses, args.output_dir / "expenses_SYNTHETIC.jsonl")
        print("  NOTE: Synthetic expense data written to expenses_SYNTHETIC.jsonl")
        print("  For real spending data, set TRANSPARENCIA_API_TOKEN and re-run download.py.")
    else:
        print("\nNo spending data (Portal da Transparência not available in this run).")

    # ── Build timeline ─────────────────────────────────────────────────────────
    print("\nBuilding unified timeline...")
    timeline = build_timeline(propositions, expenses)
    write_jsonl(timeline, args.output_dir / "timeline_events.jsonl")

    # ── Build candidate links ──────────────────────────────────────────────────
    print("\nBuilding candidate links...")
    links = build_candidate_links(propositions, expenses, theme)
    write_jsonl(links, args.output_dir / "candidate_links.jsonl")

    # ── Build evidence index ───────────────────────────────────────────────────
    print("\nBuilding evidence index...")
    evidence = build_evidence_index(propositions, deputies, expenses)
    write_jsonl(evidence, args.output_dir / "evidence_index.jsonl")

    # ── Write stats ────────────────────────────────────────────────────────────
    stats = {
        "theme": theme,
        "year_start": year_start,
        "year_end": year_end,
        "propositions_count": len(propositions),
        "deputies_count": len(deputies),
        "expenses_count": len(expenses),
        "expenses_is_synthetic": expenses_is_synthetic,
        "timeline_events_count": len(timeline),
        "candidate_links_count": len(links),
        "evidence_items_count": len(evidence),
        "prepared_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "data_sources_used": (
            ["camara", "transparencia"] if (expenses and not expenses_is_synthetic)
            else (["camara", "transparencia_synthetic"] if expenses_is_synthetic else ["camara"])
        ),
    }
    write_json(stats, args.output_dir / "dataset_stats.json")

    print()
    print("=" * 50)
    print("Preparation complete.")
    print(f"  Propositions:    {stats['propositions_count']}")
    print(f"  Deputies:        {stats['deputies_count']}")
    print(f"  Spending records:{stats['expenses_count']}" + (" (SYNTHETIC)" if expenses_is_synthetic else ""))
    print(f"  Timeline events: {stats['timeline_events_count']}")
    print(f"  Candidate links: {stats['candidate_links_count']}")
    print(f"  Evidence items:  {stats['evidence_items_count']}")
    if expenses_is_synthetic:
        print()
        print("  WARNING: Spending data is SYNTHETIC. For real analysis, set")
        print("  TRANSPARENCIA_API_TOKEN and re-run download.py.")


if __name__ == "__main__":
    main()
