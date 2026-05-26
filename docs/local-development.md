# Local Development Guide

## Prerequisites

- **Python 3.11+** — `python3 --version`
- **Node.js 20+** — `node --version`
- **uv** — `pip install uv` or `brew install uv`
- **Git**

## Quick Setup

The easiest way to get started:

```bash
git clone https://github.com/your-org/context-engineering-arena-v2
cd context-engineering-arena-v2
./scripts/bootstrap.sh
```

This script:
1. Creates `data/raw/`, `data/processed/`, `data/samples/` directories
2. Creates and activates a Python virtual environment in `arena/.venv/`
3. Installs the `arena-cli` package in editable mode
4. Installs Node dependencies for the site
5. Builds the initial catalog

## Manual Setup

If you prefer step-by-step:

### Python Environment

```bash
cd arena
uv venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
uv pip install -e .
cd ..
```

Verify installation:
```bash
python -m arena_cli.cli --help
```

### Site Dependencies

```bash
cd packages/site
npm install
cd ../..
```

### Build the Catalog

The site imports pre-generated JSON files. Build them before running the dev server:

```bash
source arena/.venv/bin/activate
python -m arena_cli.cli build-catalog
```

This reads all `task.yaml`, `participant.yaml`, `answer.json`, etc. and writes to `packages/site/src/data/generated/`.

### Start the Dev Server

```bash
cd packages/site
npm run dev
```

Visit `http://localhost:5173`.

## Workflow: Developing a Submission

```bash
# 1. Activate the Python environment
source arena/.venv/bin/activate

# 2. Download sample data for a task
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample
python -m arena_cli.cli prepare-data --task task-001-enron-investigation

# 3. Edit your submission files
$EDITOR submissions/your-team/task-001-enron-investigation/answer.json

# 4. Validate
python -m arena_cli.cli validate-submission \
  --participant your-team \
  --task task-001-enron-investigation

# 5. Rebuild catalog and preview
python -m arena_cli.cli build-catalog
# In another terminal: cd packages/site && npm run dev
```

## CLI Commands Reference

```bash
# Validate everything
python -m arena_cli.cli validate

# Validate one submission
python -m arena_cli.cli validate-submission --participant baseline-prompt-only --task task-001-enron-investigation

# Build catalog (writes JSON to packages/site/src/data/generated/)
python -m arena_cli.cli build-catalog

# List available tasks
python -m arena_cli.cli list-tasks

# List all submissions
python -m arena_cli.cli list-submissions

# Download data for a task (sample mode)
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample

# Prepare data for a task
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

## Site Build

```bash
cd packages/site

# Development server with hot reload
npm run dev

# Production build
npm run build

# Preview production build locally
npm run preview
```

The production build outputs to `packages/site/dist/`.

## Troubleshooting

### `python -m arena_cli.cli` not found

Make sure you activated the virtual environment: `source arena/.venv/bin/activate`

### `ModuleNotFoundError: No module named 'arena_cli'`

Re-install in editable mode:
```bash
cd arena
uv pip install -e .
```

### Site shows no tasks or submissions

Run `python -m arena_cli.cli build-catalog` to regenerate the data files the site depends on.

### TypeScript errors during `npm run build`

Check that your `tsconfig.app.json` is present and that all imports in `src/` have corresponding type definitions.

### `npm run dev` port conflict

Change the port: `npm run dev -- --port 3000`

### Task download script fails

Check the task's `data_manifest.yaml` for required environment variables (e.g., `TRANSPARENCIA_API_TOKEN` for Task 002). Run with `--sample-only` to skip sources that need tokens.
