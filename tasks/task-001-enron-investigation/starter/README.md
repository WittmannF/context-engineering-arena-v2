# Getting Started — Task 001: The Enron Investigation Brief

This guide walks you through the baseline approach and key strategies for Task 001.

## Step 1: Download and Prepare the Data

```bash
# Download (1.7 GB — skip this if you want to start with sample only)
python tasks/task-001-enron-investigation/scripts/download.py

# OR start with sample fixtures for testing
python tasks/task-001-enron-investigation/scripts/download.py --sample-only

# Prepare: parse emails to JSONL
python tasks/task-001-enron-investigation/scripts/prepare.py

# Create a small sample for rapid iteration
python tasks/task-001-enron-investigation/scripts/sample.py
```

After running these, you will have:
- `data/processed/task-001-enron-investigation/emails.jsonl` (~3 GB JSONL with all parsed emails)
- `data/processed/task-001-enron-investigation/dataset_stats.json` (summary stats)
- `data/samples/task-001-enron-investigation/sample_emails.jsonl` (100 emails for testing)

## Step 2: Understand the Corpus

Before writing any analysis code, spend 10 minutes exploring the data:

```python
import json

with open("data/processed/task-001-enron-investigation/emails.jsonl") as f:
    # Read first 5 emails
    for i, line in enumerate(f):
        if i >= 5: break
        email = json.loads(line)
        print(f"From: {email['sender']}")
        print(f"To:   {email['recipients']}")
        print(f"Date: {email['date']}")
        print(f"Subject: {email['subject']}")
        print(f"Body (first 200 chars): {email['body'][:200]}")
        print("---")
```

Key things to notice:
- Emails are sorted by file path, not by date
- Date parsing is imperfect — some emails have no date or malformed dates
- Many emails are forwarded chains with repeated content
- The "user_folder" field tells you which employee's mailbox this came from
- Automated notifications (IT, HR, calendar invites) are very common — filter them out

## Step 3: Identify What Matters

The corpus has 517,000 emails. You cannot read all of them. You need a strategy for which ones to prioritize.

**Key people to look for:**
- `kenneth.lay@enron.com` — Chairman and CEO
- `jeffrey.skilling@enron.com` — President and CEO (resigned Aug 2001)
- `andrew.fastow@enron.com` — CFO, architect of the SPE structures
- `sherron.watkins@enron.com` — VP who wrote the famous whistleblower memo
- `ben.glisan@enron.com` — Treasurer
- `richard.causey@enron.com` — Chief Accounting Officer
- `cliff.baxter@enron.com` — Vice Chairman (resigned May 2001)
- `lou.pai@enron.com` — CEO of Enron Energy Services
- `rick.buy@enron.com` — Chief Risk Officer

**Key topics to search for:**
- `LJM`, `LJM2`, `LJM Cayman` — Fastow's off-balance-sheet partnerships
- `Raptor`, `Raptor I`, `Raptor II`, `Raptor III`, `Raptor IV` — SPE vehicles
- `mark to market`, `mark-to-market`, `MTM` — accounting method at issue
- `JEDI`, `Chewco` — early SPEs (late 1990s)
- `Whitewing` — another partnership vehicle
- `earnings guidance`, `analyst call`, `street expectations` — pressure signals
- `restatement`, `write-down`, `accounting adjustment` — financial red flags
- `Watkins`, `memo`, `concern` — whistleblower context
- `Arthur Andersen`, `audit` — auditor involvement

**Key time periods:**
- 1999–2000: Rapid expansion, stock at peak, SPE structures being established
- Q1–Q2 2001: Early warning signs, Skilling resignation in August
- August–October 2001: Watkins memo, SEC inquiry begins
- November–December 2001: Bankruptcy, collapse

## Step 4: Choose a Strategy

See `baseline_prompt_only.md` for the simplest possible approach (and why it is weak).
See `baseline_strategy.py` for a slightly better programmatic approach.

For a competitive submission, consider:

### Strategy A: BM25 Keyword Search
Build a BM25 index over all emails. Run targeted keyword queries for each key topic (LJM, Raptor, mark-to-market, etc.). Collect the top-K results per query. This gives you a targeted corpus that is still much smaller than the full dataset.

**Tools:** `rank_bm25`, `whoosh`, `elasticsearch` (local mode)

### Strategy B: Dense Retrieval
Embed a subset of emails (10K–50K) using a sentence embedding model. For each investigation question, embed the query and retrieve the most semantically similar emails. Useful for finding emails that use indirect language ("the vehicle," "the arrangement") rather than explicit keywords.

**Tools:** `sentence-transformers`, `faiss`, `chromadb`, `qdrant`

### Strategy C: Hybrid BM25 + Dense
Combine both strategies. Use BM25 to get precision (exact keyword matches) and dense retrieval to get recall (related concepts). Rerank results by relevance.

### Strategy D: Entity-Centric Graph
Extract all named entities (people, organizations, dollar amounts) from every email. Build a communication graph. Identify high-centrality nodes and unusual patterns. Use the graph to guide deeper reading.

**Tools:** `spacy`, `networkx`, `neo4j` (local)

### Strategy E: Temporal Windows
Divide the corpus into time windows (month-by-month or quarter-by-quarter). In each window, identify the most active email threads, the most frequent topics, and the most central communicators. Compare across windows to detect changes over time.

## Step 5: Build the Output

Your output must match the schema in `expected_answer_schema.json`. At minimum:

1. An `executive_summary` (at least 200 chars)
2. At least 5 `claims`, each with `type`, `confidence`, and ideally `evidence_ids`
3. At least 3 `evidence` items with specific email references
4. At least 5 `timeline` events
5. All required sections in the `sections` array

## Common Pitfalls

1. **Confusing LLM knowledge with corpus evidence.** The LLM knows about Enron from training data. If you ask it about Enron without giving it actual emails, it will produce plausible-sounding but unverifiable claims. Every claim needs an evidence anchor from the dataset.

2. **Random sampling.** Picking 50 emails at random will overwhelmingly select low-signal emails (HR announcements, calendar invites, automated notifications). Use targeted retrieval.

3. **Missing the temporal arc.** Enron's story is about gradual deterioration. If all your evidence comes from October 2001, you're missing the 1999–2000 period when the structures were built.

4. **Overconfident claims.** Many things that look suspicious in email context have innocent explanations. Mark interpretations as `interpretation`, not `fact`.

5. **Forgetting what you didn't examine.** The "what was ignored" section of your submission matters. Explain the tradeoffs you made.

6. **Entity confusion.** There are multiple people named "Jeff" in the corpus. Make sure your entity extraction distinguishes them. Use email addresses, not just first names.

## Useful Resources

- CMU Enron Email Dataset: https://www.cs.cmu.edu/~enron/
- Enron: The Smartest Guys in the Room (2005 documentary) — useful for context
- The McLean & Elkind book "The Smartest Guys in the Room" — same
- SEC Litigation Releases on Enron: https://www.sec.gov/litigation/litreleases/enron.htm
- Sherron Watkins memo (public record): widely available online
- FERC investigation documents: https://www.ferc.gov/enron
