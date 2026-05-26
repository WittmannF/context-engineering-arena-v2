# arena-cli

Command-line tools for the Context Engineering Arena benchmark platform.

## Installation

```bash
cd arena
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
# Validate all tasks and submissions
arena validate

# Validate a specific task
arena validate --task <task-id>

# Validate a specific participant's files
arena validate --participant <participant-id>

# Validate a specific submission
arena validate-submission --participant <participant-id> --task <task-id>

# List all tasks
arena list-tasks

# List all submissions
arena list-submissions

# Download task data (full dataset)
arena download-data --task <task-id>

# Download sample data only
arena download-data --task <task-id> --sample

# Prepare task data
arena prepare-data --task <task-id>

# Build the site catalog JSON files
arena build-catalog
```

## Repository structure expected

```
repo-root/
  tasks/
    <task-id>/
      task.yaml
      README.md
      rubric.md
      data_manifest.yaml
      expected_answer_schema.json
      scripts/
        download.py
        prepare.py
  submissions/
    <participant-id>/
      participant.yaml
      <task-id>/
        answer.json
        context_trace.json
        strategy.md
        score.json          # optional — added after scoring
  arena/                    # this package
  packages/
    site/
      src/
        data/
          generated/        # built by arena build-catalog
```

## Data model

- **Task**: benchmark task definition including domain, difficulty, scoring rubric, and data manifest.
- **Answer**: structured answer submitted by a participant, including claims, evidence, timeline, entities, risks, and recommendations.
- **ContextTrace**: full trace of how context was assembled (retrieval steps, compression, models used, token stats).
- **Score**: scoring result for a submission (currently manual; computed by judges).
- **Catalog**: denormalised JSON files consumed by the Next.js site.
