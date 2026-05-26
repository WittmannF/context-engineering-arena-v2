# Data Policy

## Core Principle

**Raw datasets are never committed to this repository.** The repository contains only code, schemas, documentation, and structured submission outputs (JSON files). Large data files are downloaded and processed locally using the task scripts.

## Directory Policy

| Directory | Policy |
|-----------|--------|
| `data/raw/` | **Gitignored.** Downloaded archives, API responses, raw files. Never commit. |
| `data/processed/` | **Gitignored.** Parsed JSONL, CSV, SQLite, DuckDB files. Never commit. |
| `data/samples/` | **May be committed** if files are very small (< 1 MB total per task), legally safe to redistribute, and properly attributed. |

## What Is Allowed in Submissions

Submission files (`answer.json`, `context_trace.json`) may include:
- Short text excerpts from source documents (for evidence)
- Metadata about documents (dates, IDs, authors where public)
- Aggregated statistics

Submissions must **not** include:
- Full document texts copied verbatim at large scale
- Bulk raw data that belongs in `data/raw/` or `data/processed/`
- Personal information beyond what appears in an official public record

## Per-Task Data Notes

### Task 001 — Enron Email Dataset

The Enron Email Dataset was released by FERC for public investigation purposes. It is treated as a public record. However:
- The emails belong to real individuals, some of whom had peripheral involvement in the scandal.
- Do not reproduce email bodies verbatim beyond short evidentiary excerpts.
- Handle content about identified individuals with journalistic care.

### Task 002 — Brazil Public Data

Data from the Câmara dos Deputados and Portal da Transparência is released under Brazil's Open Government Data policy (Lei de Acesso à Informação). Terms:
- Attribution required.
- Portal da Transparência requires a free API token — do not commit tokens to the repository.
- CNPJ/CPF identifiers should only appear when already public and relevant to the analysis.

### Task 003 — GH Archive

GH Archive data is published under CC BY 4.0. Terms:
- Attribution to GH Archive required.
- Data includes public GitHub usernames — these are already public but should not be used to profile individuals.

## Reproducing Data

The source of truth for data reproduction is the task's download and prepare scripts:

```bash
# Download
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample

# Process
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

Each task's `data_manifest.yaml` documents the exact sources, versions, and licenses.

## Adding a New Task

If you propose a new task, you must:
1. Verify the data license permits analysis and output sharing.
2. Document the license in `data_manifest.yaml`.
3. Provide a working `download.py` with `--sample-only` support.
4. Document privacy risks and recommended mitigations in `task.yaml` and `data_manifest.yaml`.
5. Not commit raw data to your PR.

If the data license is unclear, open a GitHub issue before proceeding. Maintainers will review.
