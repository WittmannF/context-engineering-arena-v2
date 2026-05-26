# Data Directory

This directory holds downloaded and processed datasets. **Raw and processed data are gitignored and must never be committed.**

## Structure

```
data/
├── raw/          # Downloaded archives and API responses — gitignored
├── processed/    # Cleaned, parsed, and structured outputs — gitignored
└── samples/      # Tiny legally-safe samples only (may be committed if small and licensed)
```

## Policy

- `data/raw/` and `data/processed/` are listed in `.gitignore`. Do not force-add files from these directories.
- `data/samples/` may contain very small samples (< 1 MB) only if the data is legally safe to redistribute and properly attributed.
- Each task in `tasks/` includes a `data_manifest.yaml` and `scripts/download.py` that are the authoritative source for reproducing the data.

## Reproducing Data

```bash
# Download sample for a task
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample

# Prepare/process data
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

See each task's `README.md` for task-specific instructions.

## Ethics and Licensing

Each task's `data_manifest.yaml` documents the data source, license, and any ethics notes. Always read these before downloading or using data.
