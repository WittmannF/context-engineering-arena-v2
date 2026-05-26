# Submission Guide

This guide explains exactly how to submit a strategy to the Context Engineering Arena.

## Prerequisites

- Python 3.11+
- Node 20+ (to preview the site locally)
- `uv` installed (`pip install uv`)
- Git and a GitHub account

## Step 1: Set Up the Repository

```bash
git clone https://github.com/your-org/context-engineering-arena-v2
cd context-engineering-arena-v2
./scripts/bootstrap.sh
```

## Step 2: Choose a Task

```bash
python -m arena_cli.cli list-tasks
```

Read the task's `README.md` and `rubric.md` before starting.

## Step 3: Download Sample Data

```bash
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

## Step 4: Create Your Submission Folder

```bash
cp -r submissions/baseline-prompt-only submissions/your-team-id
```

The folder name becomes your `participant_id`. Use lowercase letters, numbers, and hyphens only.

## Step 5: Edit `participant.yaml`

```yaml
id: your-team-id           # must match folder name exactly
display_name: "Your Team"
type: community             # baseline | community | team | bot
github: your-github-username
description: "One sentence describing your approach."
```

## Step 6: Build Your Answer

Edit `submissions/your-team-id/task-001-enron-investigation/answer.json`.

### Required fields

```json
{
  "task_id": "task-001-enron-investigation",
  "participant_id": "your-team-id",
  "title": "Your Page Title",
  "executive_summary": "2-4 paragraph summary of your findings.",
  "claims": [...],
  "evidence": [...],
  "limitations": [...]
}
```

### Writing good claims

Every claim must have a `claim_type`:
- `fact` — directly supported by evidence you cite
- `interpretation` — a reasonable inference from evidence you cite
- `recommendation` — an actionable suggestion
- `uncertainty` — something that cannot be determined from available evidence

Every non-trivial claim must have at least one `evidence_id` pointing to a real entry in your `evidence` array.

**Good:**
```json
{
  "id": "claim-001",
  "claim": "Senior finance executives were communicating about SPE consolidation risks in August 2001.",
  "claim_type": "fact",
  "confidence": "high",
  "evidence_ids": ["email-2001-08-22-glisan"],
  "notes": "Based on one email. Additional emails may exist."
}
```

**Bad:**
```json
{
  "id": "claim-001",
  "claim": "The company engaged in deliberate fraud.",
  "claim_type": "fact",
  "confidence": "high",
  "evidence_ids": []
}
```
Problems: no evidence, overconfident, asserts legal conclusion without support.

### Writing good evidence entries

```json
{
  "id": "email-2001-08-22-glisan",
  "source_type": "email",
  "source_id": "glisan-ben/deleted_items/123.txt",
  "title": "Re: Q3 balance sheet review",
  "date": "2001-08-22",
  "excerpt": "We need to address the Raptor exposure before end of quarter...",
  "location": "data/processed/task-001-enron-investigation/emails.jsonl"
}
```

The `excerpt` must be an actual quote or close paraphrase from the source. Never fabricate excerpts.

## Step 7: Fill in `context_trace.json`

This is required. It exposes your context engineering pipeline.

```json
{
  "task_id": "task-001-enron-investigation",
  "participant_id": "your-team-id",
  "strategy_name": "BM25 + Dense Hybrid Retrieval",
  "strategy_summary": "Indexed all emails with BM25, embedded a 10K sample, ran 12 targeted queries...",
  "methods": {
    "prompt_only": false,
    "rag": true,
    "bm25": true,
    "dense_embeddings": true,
    ...
  },
  "context_stats": {
    "documents_available": 517401,
    "documents_opened": 10000,
    "documents_used_in_final": 150,
    "total_tokens_estimated": 95000,
    "estimated_cost_usd": 0.31
  }
}
```

Be honest about your stats. Honest low numbers score better than inflated claims.

## Step 8: Write `strategy.md`

Explain your approach in plain language:
- What did you try?
- Why did you choose that strategy?
- How did you process the data?
- What retrieval or context methods did you use?
- What failed?
- What would you improve?
- How reproducible is this submission?

300–800 words is a good length.

## Step 9: Validate

```bash
python -m arena_cli.cli validate-submission \
  --participant your-team-id \
  --task task-001-enron-investigation
```

Fix any errors before proceeding.

## Step 10: Preview

```bash
python -m arena_cli.cli build-catalog
cd packages/site && npm run dev
```

Visit `http://localhost:5173` and navigate to your submission page. Verify it renders correctly.

## Step 11: Open a Pull Request

Push your branch and open a PR. Use the PR template checklist.

---

## Optional Files

You may also include:
- `run.py` — code to reproduce your submission
- `requirements.txt` or `pyproject.toml` — dependencies
- `notebooks/` — Jupyter notebooks showing your analysis
- `artifacts/` — intermediate outputs (embeddings, index files, etc.)
- `README.md` — extended documentation
