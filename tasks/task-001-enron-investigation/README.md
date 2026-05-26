# Task 001: The Enron Investigation Brief

## What This Task Is

The Enron Investigation Brief asks you to process the CMU Enron Email Dataset — over 500,000 emails from roughly 150 Enron employees — and produce an evidence-backed investigative page that helps readers understand what was happening inside the company before its collapse in December 2001.

This is not a question-answering task. The benchmark question is open-ended by design:

> What warning signs, coordination patterns, or internal tensions were visible before the collapse, and what evidence supports those conclusions?

Your job is to select the most relevant evidence from a noisy, large corpus; organize it into a coherent narrative; distinguish facts from inferences; and produce a page that would be genuinely useful to an investigative journalist or policy researcher.

## Why This Task Is Interesting

The Enron email corpus is one of the most studied real-world datasets in NLP, but most prior work treats it as a classification or retrieval benchmark. This task treats it as a context engineering challenge:

- The corpus is too large to fit in any context window. You must choose what to read.
- The relevant signals are buried in routine business emails, calendar invites, and forwarded spreadsheets.
- Much of what you find will be ambiguous — an email expressing "concern" about accounting practices could be professional caution, or it could be a red flag. You must label your uncertainty.
- The key people (Lay, Skilling, Fastow, Watkins) are well-known, but the corpus also contains lesser-known employees whose behavior matters. Your entity extraction needs to work for the whole graph, not just the famous names.
- The temporal arc — gradual deterioration from 1999 through the 2001 collapse — requires reasoning across years of messages, not a single event.

## The Dataset

**Name:** Enron Email Dataset (CMU/FERC release)
**Source:** https://www.cs.cmu.edu/~enron/
**License:** Public domain — released by FERC as part of its investigation into Enron's collapse
**Size:** ~1.7 GB compressed (enron_mail_20150507.tar.gz), ~517,401 emails
**Structure:** Directory tree organized by employee username, then mailbox folder (inbox, sent, deleted, etc.)

The dataset was originally collected and prepared by William Cohen at CMU. It has been cleaned and re-released several times; the 2015 version is the most commonly used.

## How to Download

Use the provided download script:

```bash
# Full dataset
python tasks/task-001-enron-investigation/scripts/download.py

# Sample only (for local testing)
python tasks/task-001-enron-investigation/scripts/download.py --sample-only

# Force re-download
python tasks/task-001-enron-investigation/scripts/download.py --force
```

The script downloads to `data/raw/task-001-enron-investigation/` by default.

**Note:** The full download is ~1.7 GB. Budget time accordingly on slow connections.

## How to Prepare the Data

After downloading, run the preparation script:

```bash
# Full processing
python tasks/task-001-enron-investigation/scripts/prepare.py

# Sample mode (first 500 emails only)
python tasks/task-001-enron-investigation/scripts/prepare.py --sample-only

# Output to custom directory
python tasks/task-001-enron-investigation/scripts/prepare.py --output-dir data/processed/my-task-001/
```

This produces `data/processed/task-001-enron-investigation/emails.jsonl` with one JSON object per email containing:

```json
{
  "message_id": "<...",
  "sender": "ken.lay@enron.com",
  "recipients": ["jeff.skilling@enron.com"],
  "cc": [],
  "subject": "Re: Q3 results",
  "date": "2001-09-12T14:23:00",
  "body": "...",
  "file_path": "enron_mail/lay-k/inbox/123.",
  "user_folder": "lay-k/inbox"
}
```

## The Benchmark Question

> What warning signs, coordination patterns, or internal tensions were visible before the collapse, and what evidence supports those conclusions?

A submission must address this question with:
- A clear executive summary answering it at a high level
- An investigative timeline showing how events unfolded
- Specific claims backed by cited evidence from the dataset
- Explicit uncertainty labels where evidence is weak or ambiguous
- An honest account of what was not examined and why

## What a Good Submission Looks Like

A strong submission will:

1. **Select evidence deliberately** — not randomly, not by keyword alone. It will show evidence of a retrieval strategy that targeted relevant signals.

2. **Build a coherent narrative** — the executive summary and timeline will tell a story that is supported by the evidence section, not contradicted by it.

3. **Label claims precisely** — each major claim will be labeled `fact`, `interpretation`, or `uncertainty` and cite at least one evidence item.

4. **Handle the famous names but not only the famous names** — Lay, Skilling, and Fastow appear in the rubric, but strong submissions will also surface the network of communication around them, including mid-level employees like Sherron Watkins, Ben Glisan, and others.

5. **Explicitly list what was not covered** — the corpus is too large to fully process. A good submission acknowledges this and explains the tradeoffs made.

6. **Avoid hallucination** — claims should be traceable to evidence items. If a claim cannot be grounded in the dataset, it must be labeled `uncertainty` or omitted.

A weak submission will:
- Make confident claims that rest on LLM prior knowledge about Enron, not on the dataset
- Randomly sample 50 emails and call it analysis
- Provide no timeline or a timeline built from Wikipedia, not the emails
- Treat all claims as equally certain

## Scoring Notes

See `rubric.md` for the full scoring rubric. Summary:

| Dimension | Weight | What Matters |
|---|---|---|
| Evidence Quality | High | Are claims backed by specific emails? |
| Timeline Quality | High | Is the timeline built from parsed dates? |
| Entity Extraction | Medium | Are key people and entities correctly identified? |
| Uncertainty Handling | High | Are inferences labeled as such? |
| Hallucination Avoidance | High | Are claims traceable to the corpus? |
| Context Efficiency | Medium | Did you use context wisely relative to what you retrieved? |
| Page Usefulness | Medium | Would an investigative journalist find this useful? |

## Ethics Notes

This dataset contains personal emails of real individuals, some of whom faced criminal prosecution. Others were ordinary employees with little involvement in the fraud.

- Focus on organizational patterns and documented behavior, not personal character judgments.
- Do not reproduce email content verbatim beyond short excerpts needed to support specific claims.
- Mark all inferences about intent as uncertain — you cannot know what someone intended from their emails alone.
- Do not use this task output to make new legal or reputational claims beyond what the public record already supports.
- Several Enron executives were convicted; others were acquitted; others were never charged. The email dataset does not resolve legal questions.

## Files in This Task

```
tasks/task-001-enron-investigation/
  task.yaml                    # Task definition
  README.md                    # This file
  rubric.md                    # Detailed scoring rubric
  data_manifest.yaml           # Data sources and preparation steps
  expected_answer_schema.json  # JSON Schema for valid answers
  scripts/
    download.py                # Downloads the dataset
    prepare.py                 # Parses emails to JSONL
    sample.py                  # Creates a small sample for testing
  starter/
    README.md                  # Getting started guide
    baseline_prompt_only.md    # Simple baseline prompt
    baseline_strategy.py       # Example baseline strategy script
```
