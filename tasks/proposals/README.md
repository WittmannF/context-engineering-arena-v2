# Proposing a New Task

The Context Engineering Arena is always looking for new tasks that test the full spectrum of context engineering techniques against real, publicly accessible datasets.

## What Makes a Good Task

A good task:

1. **Has a large, public corpus** that cannot fit in a context window. If a competent analyst can read the entire dataset in 10 minutes, it does not test context engineering.

2. **Has a clear benchmark question** that is specific enough to evaluate but open enough to allow different strategies.

3. **Requires context selection** — the question cannot be answered by reading only the first few documents or by using only the LLM's prior knowledge.

4. **Has gradations** — there should be meaningful differences between a prompt-only baseline (~40/100) and a well-engineered approach (~85/100). Tasks where all approaches converge near the same score are poor benchmarks.

5. **Requires uncertainty handling** — a well-calibrated answer should distinguish what is documented from what is inferred. Tasks where everything is checkable without ambiguity don't test uncertainty handling.

6. **Is ethically tractable** — the task can be completed without requiring participants to make legally dangerous claims, deanonymize individuals, or violate dataset terms of use.

## What Makes a Good Dataset

Good datasets for this benchmark have:

- **Public availability** — freely downloadable or accessible via public API
- **Clear license** — permissive enough for research/benchmark use
- **Appropriate size** — large enough to require context selection (at minimum several thousand documents)
- **Heterogeneous content** — not uniform records but varied signals requiring judgment
- **Temporal dimension** — ideally data spanning enough time for temporal reasoning

## How to Propose a Task

1. Copy the `task-template/` directory to `proposals/task-XXX-your-task-id/`

2. Fill in all required files completely:
   - `task.yaml` — task definition
   - `README.md` — full description
   - `rubric.md` — scoring criteria
   - `data_manifest.yaml` — dataset details
   - `expected_answer_schema.json` — output schema

3. Open a pull request with the proposal

4. The proposal will be reviewed for:
   - Dataset accessibility and license
   - Benchmark question clarity
   - Scoring rubric quality
   - Ethical considerations
   - Differentiation from existing tasks

## Task ID Convention

Task IDs follow the pattern `task-NNN-short-description`:
- `NNN` is a three-digit zero-padded number assigned by the maintainers
- `short-description` uses hyphens, lowercase only, 3–6 words

In your proposal, use `task-XXX-your-description`. The number will be assigned when the task is accepted.

## File Structure

Every task must have exactly this structure:

```
tasks/task-XXX-your-task-id/
  task.yaml                    # Required: task definition
  README.md                    # Required: complete documentation
  rubric.md                    # Required: scoring rubric
  data_manifest.yaml           # Required: dataset details
  expected_answer_schema.json  # Required: JSON Schema for answers
  scripts/
    download.py                # Required: dataset download script
    prepare.py                 # Required: data normalization script
    sample.py                  # Required: sample creation script
  starter/
    README.md                  # Required: getting started guide
    baseline_prompt_only.md    # Required: weakest baseline prompt
    baseline_strategy.py       # Required: simple baseline script
```

All files must be complete. No TODOs, no stubs.

## Domains We Are Looking For

We are particularly interested in tasks from these domains:

- **Finance** — earnings call transcripts, SEC filings, credit rating reports, regulatory filings
- **Science** — preprint corpus (arXiv), clinical trial records, patent databases
- **Legal** — court decisions, contracts, regulatory documents
- **Web archaeology** — Wayback Machine snapshots of early web content, historical news archives
- **International government data** — EU, UK, India, South Africa, Mexico open government datasets
- **Code archaeology** — large repository history, deprecated API migration patterns

We already have tasks covering corporate investigation (Task 001), civic accountability (Task 002), and open-source ecosystem analysis (Task 003). Proposals in these domains are welcome but should offer something genuinely different.

## Domains to Avoid

- Tasks that require scraping sites that prohibit scraping in their ToS
- Tasks involving private data or data requiring special research agreements
- Tasks where the "correct" answer is highly subjective with no grounding criteria
- Tasks that primarily test LLM factual recall rather than context engineering
- Tasks that could be trivially gamed (e.g., by hardcoding the answer)

## Evaluation Criteria for Proposals

| Criterion | Description |
|---|---|
| Dataset Quality | Size, public access, license, heterogeneity |
| Question Clarity | Can we clearly define correct vs incorrect? |
| Baseline Spread | Is there a meaningful gap between weak and strong approaches? |
| Rubric Quality | Can judges consistently apply the rubric? |
| Ethical Safety | No legal/privacy risks in normal use |
| Novelty | Genuinely different from existing tasks |

## Review Process

1. Submit a pull request with your proposal
2. Maintainers will review within 2 weeks
3. Feedback will be provided as PR comments
4. After revisions, the task is accepted, assigned a number, and moved to `tasks/`
5. A baseline submission is added to `submissions/baseline-prompt-only/` at acceptance
