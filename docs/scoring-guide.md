# Scoring Guide

## Overview

Submissions are scored manually in the current version of the arena. Future versions will include automatic scoring components. Each submission receives a score on six dimensions plus an overall score (0–100).

## Current Scoring Process

1. A maintainer or community reviewer reads the submission's `answer.json`, `context_trace.json`, and `strategy.md`.
2. They score each dimension independently (0–100).
3. They write a `score.json` with notes explaining the scores.
4. Scores are published in `submissions/<participant>/<task>/score.json` and reflected in the leaderboard.
5. Participants may open a GitHub issue to dispute a score; maintainers will re-review.

Scoring is not fast. Expect 1–3 weeks for a scored result after submission.

---

## Scoring Dimensions

### 1. Answer Quality (0–100)

Does the final answer accurately and usefully address the benchmark question?

| Score | Meaning |
|-------|---------|
| 90–100 | The conclusion is accurate, well-organized, draws on the full breadth of relevant evidence, and would genuinely help a reader understand the corpus. |
| 70–89 | Mostly accurate, good organization, minor gaps or overstatements. |
| 50–69 | Partially accurate, some useful synthesis, but notable gaps or misleading organization. |
| 30–49 | Superficial, heavily reliant on prior knowledge rather than corpus, or poorly organized. |
| 0–29 | Inaccurate, fabricated, or irrelevant to the benchmark question. |

### 2. Evidence Quality (0–100)

Are claims backed by real, specific evidence from the corpus?

| Score | Meaning |
|-------|---------|
| 90–100 | Every non-trivial claim cites a real source. Evidence excerpts are accurate. Source IDs are traceable. |
| 70–89 | Most claims are evidenced. A few minor claims lack citations. |
| 50–69 | Some evidencing, but many important claims lack support. |
| 30–49 | Sparse evidencing. Most claims are either uncited or cite irrelevant sources. |
| 0–29 | Fabricated evidence, invented citations, or no evidence at all. |

**What gets penalized:**
- Claiming an email says something it does not say
- Inventing document IDs or source references
- Citing a source for a claim it does not support
- Using evidence from outside the task corpus without disclosure

### 3. Context Efficiency (0–100)

Was the context budget (tokens, retrieved documents) used efficiently?

| Score | Meaning |
|-------|---------|
| 90–100 | High-quality output achieved with a minimal, well-targeted context budget. |
| 70–89 | Reasonable efficiency with minor waste. |
| 50–69 | Moderate efficiency. Token use is high relative to output quality. |
| 30–49 | Low efficiency. Large context budgets with weak output. |
| 0–29 | Extremely wasteful or the context trace is missing/inaccurate. |

### 4. Uncertainty Handling (0–100)

Are unknowns, weak signals, and contradictions explicitly surfaced?

| Score | Meaning |
|-------|---------|
| 90–100 | All major uncertainties are named and explained. Weak signals are marked as such. Contradictions are documented. |
| 70–89 | Most uncertainties handled. Minor gaps. |
| 50–69 | Some uncertainty acknowledged but important gaps omitted. |
| 30–49 | Overconfident. Presents inferences as facts. |
| 0–29 | No uncertainty handling. All claims stated with uniform confidence. |

**What gets penalized:**
- Stating an inference as a fact
- Presenting correlation as causation
- Ignoring documented contradictions in the evidence
- Omitting important caveats about data coverage

### 5. Visual Clarity (0–100)

Is the output page readable and useful for a non-specialist?

| Score | Meaning |
|-------|---------|
| 90–100 | The page is organized, scannable, well-structured. A non-specialist could follow the argument. |
| 70–89 | Generally readable with minor structural issues. |
| 50–69 | Somewhat readable but dense, repetitive, or poorly organized. |
| 30–49 | Hard to follow. Important information buried or out of order. |
| 0–29 | Unreadable, incomplete, or a raw data dump. |

### 6. Reproducibility (0–100)

Can the submission be re-run to produce equivalent results?

| Score | Meaning |
|-------|---------|
| 90–100 | Full code provided, documented, runnable. Deterministic or near-deterministic output. |
| 70–89 | Code provided with minor documentation gaps. |
| 50–69 | Strategy described clearly enough to re-implement without code. |
| 30–49 | Vague strategy description. Hard to reproduce. |
| 0–29 | No reproducibility information. Black-box submission. |

---

## Overall Score

The overall score is a weighted average of the six dimensions. Current weights (subject to change):

| Dimension | Weight |
|-----------|--------|
| Answer Quality | 25% |
| Evidence Quality | 25% |
| Context Efficiency | 15% |
| Uncertainty Handling | 15% |
| Visual Clarity | 10% |
| Reproducibility | 10% |

---

## Good Claim vs. Bad Claim

**Good claim:**
```json
{
  "claim": "Internal communications in Q3 2001 show executives were aware of balance sheet pressure and were discussing potential corrective actions.",
  "claim_type": "fact",
  "confidence": "medium",
  "evidence_ids": ["email-2001-08-14-lay-to-skilling", "email-2001-09-02-fastow-to-finance"],
  "notes": "Both cited emails explicitly mention balance sheet concerns. The word 'corrective' is not in the emails; this is an interpretive summary."
}
```

**Bad claim:**
```json
{
  "claim": "Executives knew the company was committing fraud.",
  "claim_type": "fact",
  "confidence": "high",
  "evidence_ids": []
}
```
Problems: no evidence, overconfident, asserts intent without support.

---

## Future Automatic Scoring

Planned future metrics:
- **Claim accuracy** against hidden gold labels (where maintainers provide ground truth)
- **Hallucination detection** — LLM-as-judge checking whether evidence excerpts support their claims
- **Evidence precision** — fraction of cited evidence that is genuinely relevant
- **Evidence recall** — fraction of known-relevant sources that were found
- **Cost-adjusted score** — quality per dollar of API spend
- **Human usefulness score** — crowd-sourced ratings

---

## Requesting a Score

Open a GitHub issue with title `[Score Request] <participant-id> / <task-id>` and link to your submission PR. Maintainers will prioritize scoring in order of request.
