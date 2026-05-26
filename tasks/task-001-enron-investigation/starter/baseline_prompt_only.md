# Baseline Prompt — Task 001: Enron Investigation Brief

This is the simplest possible approach to this task. It is intentionally weak.
Use it as a starting point to understand what the task requires, not as a competitive strategy.

## What This Baseline Does

1. Loads a random sample of 50 emails from the processed dataset
2. Formats them as a single prompt
3. Asks an LLM to produce a structured investigation brief
4. Accepts whatever the LLM produces

## The Prompt

```
You are an investigative journalist analyzing the Enron email archive.
Below are 50 emails from the Enron email dataset (CMU/FERC release).
These were selected randomly from the corpus of ~517,000 emails.

Based ONLY on the emails below (do not use prior knowledge about Enron),
produce an investigation brief that answers:

  "What warning signs, coordination patterns, or internal tensions were
  visible before Enron's collapse, and what evidence supports those conclusions?"

Your brief must include:
1. EXECUTIVE SUMMARY (3-4 paragraphs)
2. INVESTIGATIVE TIMELINE (at least 5 events)
3. KEY PEOPLE AND COMMUNICATION PATTERNS
4. MAIN THEMES
5. EVIDENCE-BACKED CLAIMS (at least 5 claims, labeled fact/interpretation/uncertainty)
6. CONTRADICTIONS AND WEAK SIGNALS
7. DOCUMENTS THAT MATTERED MOST
8. WHAT WAS NOT EXAMINED AND WHY
9. LIMITATIONS OF THIS ANALYSIS

IMPORTANT RULES:
- Every claim must cite a specific email from the list below
- If you cannot support a claim with these emails, label it as "uncertainty"
- Do not invent email content
- Do not use your general knowledge about Enron — only these 50 emails

---

EMAILS:

{INSERT_50_RANDOM_EMAILS_HERE}

---

Produce your brief in JSON format matching this structure:
{INSERT_SCHEMA_HERE}
```

## Why This Baseline Is Weak

### 1. Random Sampling Is Not Investigation

With 517,000 emails, selecting 50 at random means each email has a 0.01% chance of being
picked. The probability that your 50 emails include:
- A Ken Lay email: ~15% (if Lay has ~80,000 emails, which is generous)
- A Fastow email about LJM: <1%
- The Sherron Watkins memo: ~0.002%

You will almost certainly get 50 emails about:
- HR announcements
- IT support tickets
- Calendar invites
- Pipeline logistics
- Routine trading updates

These emails tell you very little about the fraud.

### 2. The LLM Will Fill Gaps with Prior Knowledge

When the model cannot find evidence for a claim in 50 random emails, it will often
draw on its training data about Enron. This means the "evidence" in the output may
sound convincing but actually comes from Wikipedia or news articles, not the dataset.

This is the main reason the baseline scores poorly on Evidence Quality (expected: ~22/100).

### 3. 50 Emails Is Too Narrow to Build a Timeline

A meaningful investigative timeline requires evidence from multiple time periods.
50 random emails are unlikely to cover the full 1998–2001 arc. The timeline produced
by this baseline will either be sparse (few events) or hallucinated (events from
prior knowledge, not the corpus).

### 4. No Cross-Document Reasoning

This baseline reads each email in isolation. It cannot detect patterns like:
- "Fastow emailed this same group of people every time an SPE transaction closed"
- "The frequency of emails about earnings guidance spiked in Q3 2001"
- "Employees started using vague language ('the arrangement') around a specific date"

These patterns require indexing the corpus and searching it, not sampling it.

## What a Better Approach Looks Like

Compare this baseline to the Hybrid RAG baseline:
- Instead of 50 random emails: 850 targeted emails retrieved via keyword + semantic search
- Instead of one prompt: 8 targeted retrieval queries, each designed to find specific evidence
- Instead of random selection: evidence ranked by relevance to specific claims

The Hybrid RAG baseline scores ~68/100 vs this baseline's ~41/100.

An optimal approach would score 85+/100 and would likely involve:
- Full corpus indexing (all 517,000 emails)
- Entity-aware retrieval (know who you're looking for)
- Temporal-stratified sampling (ensure coverage across years)
- Iterative investigation (use initial findings to guide follow-up queries)
- Dedicated uncertainty handling (distinguish corpus evidence from prior knowledge)

## Expected Score

| Dimension | Expected Score |
|---|---|
| Evidence Quality | ~22/100 |
| Timeline Quality | ~35/100 |
| Entity Extraction | ~55/100 |
| Uncertainty Handling | ~65/100 |
| Hallucination Avoidance | ~38/100 |
| Context Efficiency | ~38/100 |
| Page Usefulness | ~55/100 |
| **Overall** | **~41/100** |

The relatively high Uncertainty Handling score is because this baseline document
explicitly acknowledges its limitations. A strategy that acknowledges uncertainty
scores better than one that makes overconfident claims, even if both have weak evidence.
