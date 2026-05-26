# Submissions

This directory contains all submissions to the Context Engineering Arena, organized by participant and task.

## Directory Structure

```
submissions/
  README.md                      # This file
  baseline-prompt-only/          # Official baseline: simple prompt, no retrieval
    participant.yaml             # Participant metadata
    task-001-enron-investigation/
      answer.json                # The complete structured answer
      context_trace.json         # Context engineering trace (what was retrieved and why)
      strategy.md                # Human-readable strategy description
      score.json                 # Scores per dimension
    task-002-brazil-public-money-trail/
      ...
    task-003-open-source-ecosystem-radar/
      ...
  baseline-hybrid-rag/           # Official baseline: BM25 + dense retrieval
    participant.yaml
    task-001-enron-investigation/
      ...
  your-participant-id/           # Your submission goes here
    participant.yaml
    task-001-enron-investigation/
      answer.json
      context_trace.json
      strategy.md
```

## Submitting Your Work

1. Create a directory under `submissions/` using your chosen participant ID
2. Add a `participant.yaml` file (see `baseline-prompt-only/participant.yaml` for format)
3. For each task you are submitting on, create the required files
4. Open a pull request

### Required Files Per Task

Every task submission must include:

| File | Description | Required |
|---|---|---|
| `answer.json` | Your complete structured answer | Yes |
| `context_trace.json` | What was retrieved and why | Yes |
| `strategy.md` | Human-readable strategy description (400–800 words) | Yes |
| `score.json` | Pre-computed scores (or leave empty — judges will fill in) | No |

### answer.json

Must validate against the task's `expected_answer_schema.json`. Key requirements:

- `task_id` must match exactly (e.g., `"task-001-enron-investigation"`)
- `participant_id` must match your participant ID
- All required sections must be present and non-empty
- Claims must have `type` (fact/interpretation/uncertainty), `confidence`, and `evidence_ids`
- At least the minimum number of claims, evidence items, and timeline events

### context_trace.json

The context trace is critical for evaluating context engineering quality. It must show:

- What retrieval methods were used (BM25, dense, hybrid, graph, etc.)
- How many documents were available, retrieved, and actually used in the final prompt
- Token estimates
- What was deliberately NOT included and why
- Known failure modes of the approach

See `baseline-prompt-only/task-001-enron-investigation/context_trace.json` for a complete example.

### strategy.md

Describe your approach in plain language:
- What retrieval method(s) did you use?
- What queries or search strategies?
- How did you handle document selection?
- What compression or summarization was applied?
- What would you do differently?

400–800 words. No code. Readable by a non-technical judge.

## Scoring

Submissions are scored on:
1. **Automatic metrics**: computed from the JSON structure
2. **Human evaluation**: scored by judges against the task rubric

Scores are stored in `score.json`. If you compute your own scores pre-submission, judges will verify them.

## The Baselines

### baseline-prompt-only

**Strategy:** Select N random/sequential documents from the corpus. Format them as a single prompt. Call an LLM once.

**Purpose:** Establishes the floor. Shows what naive prompting achieves.

**Expected scores:** Task 001: 41/100, Task 002: 55/100, Task 003: 62/100

### baseline-hybrid-rag

**Strategy:** Index all (or a large sample of) documents. Run targeted retrieval queries using BM25 + dense embeddings. Rerank results. Feed top-K documents to an LLM.

**Purpose:** Establishes a reasonable mid-tier baseline. Shows significant improvement over prompt-only.

**Expected scores:** Task 001: 68/100 (only Task 001 implemented)

## Participant Types

The `type` field in `participant.yaml` can be:

| Type | Description |
|---|---|
| `baseline` | Official baselines maintained by the arena |
| `participant` | External participant submission |
| `oracle` | A submission with privileged access to ground truth (for calibration only) |

## Privacy and Attribution

- Participant names and emails are public when submitted via PR
- You may use a pseudonym as your `participant_id`
- Submissions are public once merged
- Include all required dataset attributions (GH Archive CC BY 4.0, etc.) in your answers

## Leaderboard

Current leaderboard is maintained in the repository root. Scores update as new submissions are evaluated.

| Rank | Participant | Task 001 | Task 002 | Task 003 | Avg |
|---|---|---|---|---|---|
| — | baseline-hybrid-rag | 68 | — | — | — |
| — | baseline-prompt-only | 41 | 55 | 62 | 52.7 |
