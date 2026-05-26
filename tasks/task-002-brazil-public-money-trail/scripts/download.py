#!/usr/bin/env python3
"""
Download script for Task 002: Brazil Public Money Trail

Fetches data from:
  - Câmara dos Deputados Dados Abertos API (no token required)
  - Portal da Transparência API (requires TRANSPARENCIA_API_TOKEN env var)
  - TCU Dados Abertos (optional, no token required)

Usage:
    python download.py --theme saude --year-start 2022 --year-end 2024
    python download.py --sample-only
    python download.py --skip-transparencia
    python download.py --theme educacao --year-start 2023 --year-end 2024
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ETHICS_NOTICE = """
=============================================================================
ETHICS AND LICENSE NOTICE — BRAZIL PUBLIC MONEY TRAIL
=============================================================================
This task uses public Brazilian government data:

  Câmara dos Deputados Dados Abertos
  License: Open Government Data (Lei de Acesso à Informação, Lei 12.527/2011)
  Attribution: Câmara dos Deputados do Brasil

  Portal da Transparência
  License: Open Government Data (CGU / Controladoria-Geral da União)
  Attribution: Controladoria-Geral da União

This data is provided for civic analysis, journalism, and research.

IMPORTANT RULES FOR USING THIS DATA:
  - Do NOT assert corruption, illegal conduct, or improper influence without
    documented evidence from an authoritative source (TCU ruling, court filing).
  - Correlation is NOT causation. Actors appearing in both datasets does not
    imply influence or wrongdoing.
  - Always classify links: direct_documented, same_theme, same_actor, etc.
  - Include a prominent disclaimer in your submission.
  - CNPJ/CPF numbers should only be shown when already public and relevant.
=============================================================================
"""

CAMARA_BASE = "https://dadosabertos.camara.leg.br/api/v2"
TRANSPARENCIA_BASE = "https://api.portaldatransparencia.gov.br/api-de-dados"

DEFAULT_OUTPUT_DIR = Path("data/raw/task-002-brazil-public-money-trail")


# ──────────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_requests():
    """Import requests, with helpful error message if not installed."""
    try:
        import requests
        return requests
    except ImportError:
        print("ERROR: 'requests' library not found. Install with: uv pip install requests")
        sys.exit(1)


def api_get(
    requests,
    url: str,
    params: Dict = None,
    headers: Dict = None,
    timeout: int = 30,
    retry: int = 3,
) -> Optional[Dict]:
    """
    Make a GET request to an API endpoint with retry logic.
    Returns parsed JSON or None on failure.
    """
    for attempt in range(retry):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                # Rate limited — wait and retry
                wait = 2 ** attempt * 2
                print(f"  Rate limited (429). Waiting {wait}s before retry {attempt+1}/{retry}...")
                time.sleep(wait)
                continue
            elif resp.status_code == 404:
                return None
            else:
                print(f"  HTTP {resp.status_code} for {url}")
                if attempt < retry - 1:
                    time.sleep(2)
                    continue
                return None
        except Exception as e:
            print(f"  Request error (attempt {attempt+1}/{retry}): {e}")
            if attempt < retry - 1:
                time.sleep(2)
    return None


def write_json(data: Any, path: Path) -> None:
    """Write data as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────────────────────────────────────
# Câmara dos Deputados API
# ──────────────────────────────────────────────────────────────────────────────

def fetch_camara_propositions(
    requests,
    theme_keyword: str,
    year_start: int,
    year_end: int,
    output_dir: Path,
    max_pages: int = 10,
) -> int:
    """
    Fetch legislative propositions from the Câmara API by keyword and date range.

    Endpoint: GET /api/v2/proposicoes
    Params:
        keywords: theme keyword (e.g., "saude", "educacao")
        dataInicio: start date (YYYY-01-01)
        dataFim: end date (YYYY-12-31)
        pagina: page number
        itens: items per page (max 100)

    Returns the number of propositions fetched.
    """
    all_propositions = []
    page = 1
    items_per_page = 100

    print(f"  Fetching propositions for theme='{theme_keyword}', {year_start}–{year_end}...")

    while page <= max_pages:
        params = {
            "keywords": theme_keyword,
            "dataApresentacaoInicio": f"{year_start}-01-01",
            "dataApresentacaoFim": f"{year_end}-12-31",
            "pagina": page,
            "itens": items_per_page,
            "ordem": "ASC",
            "ordenarPor": "dataApresentacao",
        }

        data = api_get(requests, f"{CAMARA_BASE}/proposicoes", params=params)

        if data is None:
            print(f"    Page {page}: request failed")
            break

        items = data.get("dados", [])
        if not items:
            print(f"    Page {page}: no more results")
            break

        all_propositions.extend(items)
        print(f"    Page {page}: fetched {len(items)} propositions (total: {len(all_propositions)})")

        # Check for next page link
        links = data.get("links", [])
        has_next = any(l.get("rel") == "next" for l in links)
        if not has_next:
            break

        page += 1
        # Polite rate limiting — Câmara API is sensitive to rapid requests
        time.sleep(0.5)

    output_path = output_dir / "camara_propositions.json"
    write_json({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "count": len(all_propositions), "dados": all_propositions}, output_path)
    print(f"  Saved {len(all_propositions)} propositions to {output_path}")
    return len(all_propositions)


def fetch_camara_deputies(
    requests,
    output_dir: Path,
    legislature: int = 57,
) -> int:
    """
    Fetch current deputies from the Câmara API.

    Endpoint: GET /api/v2/deputados
    """
    print(f"  Fetching deputies (legislature {legislature})...")

    params = {
        "idLegislatura": legislature,
        "pagina": 1,
        "itens": 513,
        "ordenarPor": "nome",
    }

    data = api_get(requests, f"{CAMARA_BASE}/deputados", params=params)

    if data is None:
        print("  WARNING: Could not fetch deputies.")
        return 0

    deputies = data.get("dados", [])
    output_path = output_dir / "camara_deputies.json"
    write_json({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "count": len(deputies), "dados": deputies}, output_path)
    print(f"  Saved {len(deputies)} deputies to {output_path}")

    time.sleep(0.5)
    return len(deputies)


def fetch_camara_proposition_details(
    requests,
    proposition_ids: List[int],
    output_dir: Path,
    max_details: int = 20,
) -> int:
    """
    Fetch detailed records for the most significant propositions.
    Only fetches up to max_details to limit API calls.
    """
    print(f"  Fetching details for up to {max_details} propositions...")
    details = []

    for i, prop_id in enumerate(proposition_ids[:max_details]):
        data = api_get(requests, f"{CAMARA_BASE}/proposicoes/{prop_id}")
        if data and "dados" in data:
            details.append(data["dados"])
        if (i + 1) % 5 == 0:
            print(f"    Fetched {i+1}/{min(max_details, len(proposition_ids))} details...")
        time.sleep(0.3)  # polite rate limiting

    output_path = output_dir / "camara_proposition_details.json"
    write_json({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "count": len(details), "dados": details}, output_path)
    print(f"  Saved {len(details)} proposition details to {output_path}")
    return len(details)


# ──────────────────────────────────────────────────────────────────────────────
# Portal da Transparência API
# ──────────────────────────────────────────────────────────────────────────────

def fetch_transparencia_spending(
    requests,
    theme_keyword: str,
    year_start: int,
    year_end: int,
    output_dir: Path,
    token: str,
    max_pages: int = 5,
) -> int:
    """
    Fetch federal spending records from Portal da Transparência.

    Endpoint: GET /api-de-dados/despesas/por-orgao
    Requires: TRANSPARENCIA_API_TOKEN in Authorization header

    Note: The Portal da Transparência API has several endpoints.
    We use /despesas/por-orgao to get spending aggregated by ministry/agency.
    For more granular data, use /despesas or /transferencias endpoints.
    """
    headers = {
        "chave-api-dados": token,
        "Accept": "application/json",
    }

    all_records = []

    for year in range(year_start, year_end + 1):
        print(f"  Fetching spending for year {year}...")

        # Spending by organ/ministry
        params = {
            "ano": year,
            "pagina": 1,
        }

        data = api_get(
            requests,
            f"{TRANSPARENCIA_BASE}/despesas/por-orgao",
            params=params,
            headers=headers,
        )

        if data is None:
            print(f"    WARNING: Could not fetch spending for {year}. Check token and API status.")
            print(f"    Portal da Transparência API docs: https://api.portaldatransparencia.gov.br/")
            continue

        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = data.get("dados", data.get("data", [data]))
        else:
            records = []

        # Filter by theme keyword if possible (not all endpoints support filtering)
        for r in records:
            r["_year"] = year
            r["_theme"] = theme_keyword
        all_records.extend(records)

        print(f"    Fetched {len(records)} spending records for {year}")
        time.sleep(1.0)  # Portal da Transparência has stricter rate limits

    if all_records:
        output_path = output_dir / "transparencia_spending.json"
        write_json({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "count": len(all_records), "dados": all_records}, output_path)
        print(f"  Saved {len(all_records)} spending records to {output_path}")

    return len(all_records)


def create_synthetic_transparencia_sample(output_dir: Path, theme: str, year_start: int, year_end: int) -> None:
    """
    Create a synthetic sample of Portal da Transparência data for use when no token is available.
    This is clearly marked as synthetic and mimics the real API schema.
    """
    print("\n  NOTE: Portal da Transparência token not available.")
    print("  Creating clearly-marked SYNTHETIC sample data for testing.")
    print("  To get real data, register at: https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email")
    print()

    synthetic_records = {
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "is_synthetic": True,
        "synthetic_note": (
            "THIS IS SYNTHETIC DATA for testing only. "
            "The structure mimics the Portal da Transparência API schema "
            "but values are illustrative, not real. "
            "Get real data by registering for an API token."
        ),
        "count": 6,
        "dados": [
            {
                "orgaoNome": "Ministério da Saúde",
                "orgaoCodigo": "36000",
                "valorDotacaoAtualizada": 180000000000.0,
                "valorEmpenhado": 172000000000.0,
                "valorLiquidado": 168000000000.0,
                "valorPago": 165000000000.0,
                "_year": year_start,
                "_theme": theme,
                "_synthetic": True,
            },
            {
                "orgaoNome": "Ministério da Saúde",
                "orgaoCodigo": "36000",
                "valorDotacaoAtualizada": 195000000000.0,
                "valorEmpenhado": 188000000000.0,
                "valorLiquidado": 183000000000.0,
                "valorPago": 180000000000.0,
                "_year": year_start + 1,
                "_theme": theme,
                "_synthetic": True,
            },
            {
                "orgaoNome": "Fundo Nacional de Saúde",
                "orgaoCodigo": "36901",
                "valorDotacaoAtualizada": 42000000000.0,
                "valorEmpenhado": 40500000000.0,
                "valorLiquidado": 39000000000.0,
                "valorPago": 38200000000.0,
                "_year": year_start,
                "_theme": theme,
                "_synthetic": True,
            },
            {
                "orgaoNome": "Fundo Nacional de Saúde",
                "orgaoCodigo": "36901",
                "valorDotacaoAtualizada": 45000000000.0,
                "valorEmpenhado": 43800000000.0,
                "valorLiquidado": 42100000000.0,
                "valorPago": 41500000000.0,
                "_year": year_start + 1,
                "_theme": theme,
                "_synthetic": True,
            },
            {
                "orgaoNome": "ANVISA - Agência Nacional de Vigilância Sanitária",
                "orgaoCodigo": "36211",
                "valorDotacaoAtualizada": 980000000.0,
                "valorEmpenhado": 921000000.0,
                "valorLiquidado": 905000000.0,
                "valorPago": 899000000.0,
                "_year": year_start,
                "_theme": theme,
                "_synthetic": True,
            },
            {
                "orgaoNome": "ANS - Agência Nacional de Saúde Suplementar",
                "orgaoCodigo": "36212",
                "valorDotacaoAtualizada": 510000000.0,
                "valorEmpenhado": 488000000.0,
                "valorLiquidado": 472000000.0,
                "valorPago": 469000000.0,
                "_year": year_start,
                "_theme": theme,
                "_synthetic": True,
            },
        ],
    }

    output_path = output_dir / "transparencia_spending_SYNTHETIC.json"
    write_json(synthetic_records, output_path)
    print(f"  Synthetic sample saved: {output_path}")
    print("  IMPORTANT: This file is clearly marked as synthetic. Do not use for real analysis.")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download data for Task 002: Brazil Public Money Trail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download.py --sample-only
  python download.py --theme saude --year-start 2022 --year-end 2024
  python download.py --theme educacao --skip-transparencia
  TRANSPARENCIA_API_TOKEN=mytoken python download.py --theme saude

Token:
  Register at https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
  Set: export TRANSPARENCIA_API_TOKEN=your-token
        """,
    )
    parser.add_argument(
        "--theme",
        default="saude",
        help="Policy theme keyword in Portuguese (default: saude). Examples: educacao, infraestrutura, seguridade",
    )
    parser.add_argument(
        "--year-start",
        type=int,
        default=2022,
        help="Start year for data collection (default: 2022)",
    )
    parser.add_argument(
        "--year-end",
        type=int,
        default=2024,
        help="End year for data collection (default: 2024)",
    )
    parser.add_argument(
        "--sample-only",
        action="store_true",
        help="Sample mode: only 2 pages of Câmara results, skip deputies detail",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if files exist",
    )
    parser.add_argument(
        "--skip-transparencia",
        action="store_true",
        help="Skip Portal da Transparência (useful when no token available)",
    )
    parser.add_argument(
        "--skip-tcu",
        action="store_true",
        help="Skip TCU data (default: TCU is optional)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    print(ETHICS_NOTICE)

    requests = get_requests()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {args.output_dir.resolve()}")
    print(f"Theme:      {args.theme}")
    print(f"Years:      {args.year_start}–{args.year_end}")
    print(f"Sample:     {args.sample_only}")
    print()

    stats = {}

    # ── Câmara dos Deputados ───────────────────────────────────────────────────
    print("=" * 50)
    print("CÂMARA DOS DEPUTADOS — Legislative Data")
    print("=" * 50)

    max_pages = 2 if args.sample_only else 10
    n_propositions = fetch_camara_propositions(
        requests,
        args.theme,
        args.year_start,
        args.year_end,
        args.output_dir,
        max_pages=max_pages,
    )
    stats["camara_propositions"] = n_propositions

    if not args.sample_only:
        n_deputies = fetch_camara_deputies(requests, args.output_dir)
        stats["camara_deputies"] = n_deputies

        # Fetch details for first 20 propositions
        props_file = args.output_dir / "camara_propositions.json"
        if props_file.exists():
            with open(props_file) as f:
                props_data = json.load(f)
            prop_ids = [p.get("id") for p in props_data.get("dados", []) if p.get("id")]
            n_details = fetch_camara_proposition_details(requests, prop_ids, args.output_dir)
            stats["camara_proposition_details"] = n_details
    else:
        print("  [Sample mode: skipping deputy details]")

    # ── Portal da Transparência ───────────────────────────────────────────────
    print()
    print("=" * 50)
    print("PORTAL DA TRANSPARÊNCIA — Spending Data")
    print("=" * 50)

    if args.skip_transparencia:
        print("  Skipped (--skip-transparencia flag set)")
        stats["transparencia"] = "skipped"
    else:
        token = os.environ.get("TRANSPARENCIA_API_TOKEN")
        if not token:
            print("  WARNING: TRANSPARENCIA_API_TOKEN not set in environment.")
            print()
            print("  To get a token:")
            print("  1. Go to https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email")
            print("  2. Register with your email")
            print("  3. Token will be emailed to you")
            print("  4. Set: export TRANSPARENCIA_API_TOKEN=your-token")
            print()
            print("  Creating synthetic sample data instead...")
            create_synthetic_transparencia_sample(args.output_dir, args.theme, args.year_start, args.year_end)
            stats["transparencia"] = "synthetic_sample"
        else:
            n_spending = fetch_transparencia_spending(
                requests,
                args.theme,
                args.year_start,
                args.year_end,
                args.output_dir,
                token,
                max_pages=2 if args.sample_only else 5,
            )
            stats["transparencia_spending_records"] = n_spending

    # ── Write stats ────────────────────────────────────────────────────────────
    stats_path = args.output_dir / "download_stats.json"
    write_json({
        "theme": args.theme,
        "year_start": args.year_start,
        "year_end": args.year_end,
        "sample_only": args.sample_only,
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stats": stats,
    }, stats_path)

    print()
    print("=" * 50)
    print("Download complete.")
    print(f"Stats: {stats_path}")
    print()
    print("Next: Run prepare.py to normalize and join data:")
    print("  python tasks/task-002-brazil-public-money-trail/scripts/prepare.py")


if __name__ == "__main__":
    main()
