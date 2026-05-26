# Task 002: Brazil Public Money Trail

## What This Task Is

The Brazil Public Money Trail asks you to trace a Brazilian public policy theme — such as health, education, infrastructure, or social protection — from its legislative footprint in the Câmara dos Deputados to actual federal spending on the Portal da Transparência.

The benchmark question is:

> Trace one Brazilian public policy theme from legislative activity to federal public spending. What can be verified, which actors and agencies appear, what changed over time, and what questions remain open?

This is a civic accountability task. Your output should help a Brazilian journalist, civic researcher, or engaged citizen understand how a policy theme moves through the legislative process and how money flows to implement it — while being scrupulously honest about what cannot be determined from the data.

## Why This Task Is Interesting

Unlike many data journalism tasks that work with a single clean dataset, this task requires joining three heterogeneous public data sources that were not designed to talk to each other:

1. **Legislative data** (Câmara API): propositions, votes, authorship, themes
2. **Spending data** (Portal da Transparência): federal budget execution, transfers, contracts
3. **Oversight signals** (TCU, optional): audit reports and irregularities

The challenge is not just retrieval — it is entity resolution and link classification. A deputy who authored a health bill may or may not have influenced health ministry spending. The same ministry name may appear differently across datasets. A budget program code connects legislative intent to actual execution, but only if you know how to follow the code.

This task strongly tests the ability to distinguish what is documented from what is inferred. Correlation — the same actor, the same theme, the same time window — is not causation. A civic accountability page that implies improper influence without documented evidence causes real harm. The rubric heavily penalizes this.

## The Datasets

### Primary: Câmara dos Deputados Dados Abertos

**URL:** https://dadosabertos.camara.leg.br/swagger/api.html
**License:** Open Government Data (Brazil's Lei de Acesso à Informação)
**Access:** Free, no authentication required
**What it contains:**
- Legislative propositions (bills, amendments, resolutions)
- Deputy records and party affiliations
- Voting records by proposition
- Deputy speeches (discursos)
- Committee compositions
- Proposition themes (temas)

Key endpoints:
- `GET /api/v2/proposicoes` — search propositions by keyword and theme
- `GET /api/v2/deputados` — list deputies
- `GET /api/v2/proposicoes/{id}/votacoes` — votes on a specific proposition

### Primary: Portal da Transparência

**URL:** https://api.portaldatransparencia.gov.br/
**License:** Open Government Data (Brazil)
**Access:** Free, but requires a token (register at https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email)
**What it contains:**
- Federal spending by program, ministry, contractor
- Budget execution (LOA, emendas parlamentares)
- Transfers to states and municipalities
- Federal contracts and procurement

### Optional: TCU Dados Abertos

**URL:** https://sites.tcu.gov.br/dados-abertos/
**License:** Open Government Data (Brazil)
**What it contains:**
- Audit reports
- Identified irregularities
- Sanctions and accountability findings

## How to Download

```bash
# Sample mode (no token required — uses Câmara API only)
python tasks/task-002-brazil-public-money-trail/scripts/download.py --sample-only

# Full download for health theme, 2022-2024
python tasks/task-002-brazil-public-money-trail/scripts/download.py \
    --theme saude \
    --year-start 2022 \
    --year-end 2024

# Skip Portal da Transparência (if you don't have a token yet)
python tasks/task-002-brazil-public-money-trail/scripts/download.py \
    --theme saude \
    --skip-transparencia

# With Portal da Transparência token
export TRANSPARENCIA_API_TOKEN=your-token-here
python tasks/task-002-brazil-public-money-trail/scripts/download.py \
    --theme saude
```

**Getting the Portal da Transparência token:**
Register at https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
The token is delivered by email within minutes. Set it as an environment variable.

## How to Prepare the Data

```bash
python tasks/task-002-brazil-public-money-trail/scripts/prepare.py
```

This produces in `data/processed/task-002-brazil-public-money-trail/`:
- `propositions.jsonl` — normalized legislative propositions
- `deputies.jsonl` — deputy records with party and state
- `expenses.jsonl` — normalized spending records (if token was available)
- `timeline_events.jsonl` — unified timeline across sources
- `candidate_links.jsonl` — candidate connections between legislative and spending data, each classified by link type
- `evidence_index.jsonl` — all evidence items for indexing
- `dataset_stats.json` — summary statistics

## The Benchmark Question

> Trace one Brazilian public policy theme from legislative activity to federal public spending. What can be verified, which actors and agencies appear, what changed over time, and what questions remain open?

The question has four parts, all of which must be addressed:

1. **What can be verified?** You must distinguish documented facts (proposition was approved, budget was transferred) from inferences (this deputy influenced that spending decision).

2. **Which actors and agencies appear?** You must identify the key people and institutions in the data, including their official roles.

3. **What changed over time?** The analysis must have a temporal dimension — not just a snapshot.

4. **What questions remain open?** The submission must explicitly identify what the data cannot answer.

## What a Good Submission Looks Like

A strong submission will:

1. **Choose a coherent theme** — "health" is very broad; "Programa Farmácia Popular budget evolution 2022–2024" is more tractable. Narrow themes produce better submissions than sprawling ones.

2. **Join data across sources** — A submission that only uses Câmara data or only uses Portal da Transparência data scores poorly on "quality of data joining."

3. **Classify every link** — Each connection between a legislative event and a spending event must be labeled: `direct_documented_link`, `same_theme_link`, `same_actor_link`, `same_agency_link`, `same_time_window_link`, or `weak_or_hypothetical_link`.

4. **Avoid implying causation** — Never write "Deputy X's bill caused Ministry Y to spend R$Z." Write "A bill authored by Deputy X on [theme] passed in [period]. In the same period, Ministry Y's spending on [same theme] increased by R$Z. We classify this as a `same_theme_link` — it does not establish that the bill caused the spending change."

5. **Work in Portuguese when necessary** — API results and data fields are in Portuguese. Your analysis can be in English or Portuguese, but Brazilian institution names should be rendered correctly (e.g., "Câmara dos Deputados," not "Brazilian Congress").

A weak submission will:
- Imply corruption or improper influence without documented evidence
- Fail to join the legislative and spending datasets
- Only cite one data source
- Present all links as equally direct without classification
- Omit the limitations and what-could-not-be-verified sections

## Scoring Notes

See `rubric.md` for the full scoring rubric. Key differences from Task 001:

- **Fact vs Inference** is weighted heavily and has its own scoring dimension
- **Civic Usefulness** rewards submissions that would actually help a citizen or journalist understand public spending
- **Reproducibility** matters here because Brazilian government APIs sometimes change or rate-limit — documenting your exact API calls and parameters helps others verify your work
- **Link classification quality** is scored specifically: you must label every link between datasets, and mislabeling a hypothetical link as a direct link incurs a penalty

## Ethics Notes

This is a public accountability task. The goal is to help citizens understand how their government spends money, not to accuse individuals of wrongdoing.

- All data used must be publicly available (Câmara API and Portal da Transparência are both open government datasets)
- CNPJ (company tax ID) and CPF (individual tax ID) numbers should only be shown when they are already public and directly relevant to the analysis
- Do not assert corruption, illegal conduct, or improper influence without documentary evidence from an authoritative source (TCU ruling, court filing, etc.)
- Include a prominent disclaimer that your page organizes public data and does not allege wrongdoing
- Bureaucratic processes (e.g., automatic budget transfers under approved programs) often explain patterns that superficially look suspicious

## Files in This Task

```
tasks/task-002-brazil-public-money-trail/
  task.yaml                    # Task definition
  README.md                    # This file
  rubric.md                    # Detailed scoring rubric
  data_manifest.yaml           # Data sources and preparation steps
  expected_answer_schema.json  # JSON Schema for valid answers
  scripts/
    download.py                # Downloads from Câmara and Transparência APIs
    prepare.py                 # Normalizes and joins raw data
    sample.py                  # Creates a small sample for testing
  starter/
    README.md                  # Getting started guide
    baseline_prompt_only.md    # Simple baseline prompt
    baseline_strategy.py       # Example baseline strategy script
```
