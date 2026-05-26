# Task Authoring Guide

This guide explains how to design and submit a new benchmark task for the Context Engineering Arena.

## What Makes a Good Arena Task?

A good task has these properties:

1. **Large or complex corpus** — thousands of documents, messy formatting, heterogeneous sources. If the corpus fits in one LLM context window, it's too small.

2. **Publicly accessible data** — the data must be freely downloadable or accessible via a public API. No paywalled, private, or copyrighted data that cannot be redistributed.

3. **A synthesis question** — the benchmark question must require combining information from multiple sources. It cannot be answered by a single search query, a Wikipedia lookup, or a direct database query.

4. **Evidence structure** — the question must be answerable with citable evidence. Claims can be verified, disputed, or graded.

5. **Meaningful uncertainty** — not everything can be known. Good tasks have natural gaps, contradictions, and weak signals.

6. **Visual affordances** — the answer should want to be a page with timelines, tables, and entity cards, not just a paragraph.

7. **Objective enough to evaluate** — reviewers need to be able to distinguish good submissions from bad ones without knowing the "right answer" in advance.

## What Makes a Bad Task?

- **Trivia** — "Who was the CEO of Enron in 2001?" is a lookup, not a synthesis problem.
- **Single-source** — tasks where all relevant information is in one document are too easy.
- **Private data** — any data that cannot be redistributed or publicly accessed.
- **Copyrighted content** — full books, licensed articles, proprietary databases.
- **Unsafe conclusions** — tasks that require making unverifiable medical, legal, or defamatory claims.
- **No verifiable evidence** — if claims can't be grounded in source documents, the benchmark can't be scored.

## Step-by-Step: Authoring a Task

### 1. Choose a corpus

Identify a large, publicly accessible dataset that is:
- Messy and heterogeneous (emails, HTML pages, API responses, government filings, event logs)
- Large enough that no participant can read everything
- Rich enough in relationships that synthesis is possible
- Legally safe to download and analyze

### 2. Write the benchmark question

The benchmark question must:
- Be open-ended enough that different strategies produce meaningfully different pages
- Be specific enough that a reviewer can evaluate an answer
- Require synthesis across multiple documents
- Have inherent uncertainty that good participants should acknowledge

Example of a good benchmark question:
> "Which open-source repositories or ecosystems show unusual growth, decline, concentration risk, or emerging momentum in the selected time window?"

Example of a bad benchmark question:
> "What is the most starred repository on GitHub?"

### 3. Define required page sections

List the sections that a good answer page must include. Think of these as the chapters of a well-organized report. For example:

- Executive Summary
- Investigative Timeline
- Key Actors and Relationships
- Evidence-backed Claims
- Contradictions and Weak Signals
- What Could Not Be Determined
- Limitations

### 4. Define the scoring rubric

Write a `rubric.md` that explains what earns a high score on each dimension. Be specific:
- What would a 90/100 answer quality submission look like?
- What specific behaviors are penalized?
- What are the expected claim types?

### 5. Write download and prepare scripts

Every task needs:
- `scripts/download.py` — downloads raw data from the source
- `scripts/prepare.py` — parses and normalizes data into JSONL/CSV

Requirements:
- `download.py` must support `--sample-only` for local testing
- Scripts must not require raw data to be committed
- Scripts must print a data ethics notice before downloading sensitive data
- Scripts must handle encoding errors gracefully

### 6. Define sample mode

Sample mode must produce a small dataset (< 50 MB) that:
- Exercises the full pipeline
- Takes under 5 minutes to download and prepare
- Is representative of the full dataset

Without sample mode, participants cannot develop locally.

### 7. Write the data manifest

Fill in `data_manifest.yaml` with:
- Source name, URL, license
- Whether a token is required
- Preparation steps
- Ethics notes

### 8. Document safety and ethics concerns

Every task must include:
- Privacy risks (does the data contain personal information?)
- Legal risks (are there licensing restrictions?)
- Recommended mitigations (how should participants handle sensitive content?)

### 9. Create starter content

Provide:
- `starter/README.md` — orientation for first-time participants
- `starter/baseline_prompt_only.md` — a simple baseline prompt
- `starter/baseline_strategy.py` — a minimal code baseline

## Ethics Checklist

Before submitting a task proposal, confirm:

- [ ] Data is publicly accessible without authentication (or token registration is free and easy)
- [ ] Data license permits analysis and output publication
- [ ] No sensitive personal information that cannot be publicly disclosed
- [ ] No medical, legal, or financial data requiring professional licensing to interpret
- [ ] Benchmark question does not require making defamatory claims
- [ ] Safety notes documented in `task.yaml` and `data_manifest.yaml`

## How to Submit a Task Proposal

**Option A — GitHub Issue**

Open an issue using the "Propose a New Task" template.

**Option B — Pull Request**

1. Copy `tasks/proposals/task-template/` to `tasks/proposals/task-your-id/`
2. Fill in all files
3. Open a PR with title `[Task Proposal] Your Task Title`

Maintainers will review the proposal and may ask for revisions before promoting it to an official task.
