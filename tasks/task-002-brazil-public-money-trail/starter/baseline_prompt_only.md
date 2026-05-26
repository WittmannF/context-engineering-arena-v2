# Baseline Prompt — Task 002: Brazil Public Money Trail

This is the simplest possible approach to this task. It demonstrates why naive prompting is insufficient for civic data analysis and why the Data Joining and Fact vs Inference dimensions are particularly hard to satisfy without real retrieval.

## What This Baseline Does

1. Fetches 2 pages of health propositions from the Câmara API (sample mode)
2. Does NOT fetch Portal da Transparência data (no token)
3. Formats the Câmara API results as a prompt
4. Asks an LLM to produce a structured analysis

## The Prompt

```
You are a civic data analyst working on Brazilian public accountability.
Below is a list of legislative propositions from the Câmara dos Deputados
Dados Abertos API, fetched for the theme "saúde" (health), 2022–2024.

IMPORTANT:
1. Analyze ONLY the data provided below — do not use prior knowledge about
   Brazilian politics to fill gaps.
2. Label every claim as: fact (directly in the data), interpretation
   (reasonable inference), or uncertainty (cannot be determined).
3. Classify every link between legislative and spending data using this taxonomy:
   - direct_documented_link: explicitly documented connection
   - same_theme_link: same policy domain, no direct connection
   - same_actor_link: same person in both datasets
   - same_agency_link: same ministry/agency
   - same_time_window_link: temporal co-occurrence only
   - weak_or_hypothetical_link: speculative
4. NEVER assert corruption or illegal conduct without authoritative evidence.
5. Include a prominent disclaimer that this page does not allege wrongdoing.

The following data sources were available:
  - Câmara API: YES (propositions below)
  - Portal da Transparência: NOT AVAILABLE (no API token)

Because Portal da Transparência data is missing, you CANNOT:
  - State actual spending figures
  - Connect propositions to budget execution
  - Classify any link as direct_documented_link

You MUST note these limitations prominently.

---

CÂMARA API DATA — HEALTH PROPOSITIONS (2022–2024):

{INSERT_API_RESPONSE_HERE}

---

Produce a JSON analysis brief for task-002-brazil-public-money-trail.
```

## Why This Baseline Is Weak

### 1. One Data Source Only

The task requires joining two sources: Câmara (legislative) and Portal da Transparência (spending). This baseline only has Câmara data. It will score 0 or near-0 on the Data Joining dimension, which has a weight of 0.20.

A submission with only one data source cannot make any `direct_documented_link` claims and cannot produce the required `money-flow-overview` or `public-spending-timeline` sections.

### 2. LLM Will Be Tempted to Fill Gaps

Without spending data, the LLM may use its training knowledge to invent plausible Brazilian government spending figures. This would score poorly on Hallucination Avoidance. The prompt explicitly prohibits this, but LLMs don't always comply.

### 3. Link Classification Is Empty

With only Câmara data, all links are either `same_theme_link` or not classifiable at all. The task rewards the ability to distinguish link types — with one dataset, there is nothing to classify.

### 4. Proposition Summaries Are in Portuguese

The Câmara API returns ementas (proposition summaries) in Portuguese. An LLM can translate these, but it cannot verify translation accuracy without knowing the legislative context.

## What This Baseline CAN Produce Well

- A reasonable `legislative-activity-timeline` from Câmara data
- Correct `entity` extraction (deputy names, parties, states are in the API)
- Honest uncertainty acknowledgment for everything requiring spending data
- A good `what-could-not-be-verified` section

## Expected Score

| Dimension | Expected Score |
|---|---|
| Data Joining | ~15/100 (one source only) |
| Legislative Timeline | ~65/100 (reasonable from API data) |
| Spending Summary | ~5/100 (no data) |
| Evidence Quality | ~48/100 (Câmara API cited but not Transparência) |
| Fact vs Inference | ~78/100 (good because gaps are acknowledged) |
| Uncertainty Handling | ~80/100 (missing data clearly flagged) |
| Civic Usefulness | ~40/100 (half the picture is missing) |
| Hallucination Avoidance | ~70/100 (if LLM respects the constraints) |
| Reproducibility | ~45/100 |
| **Overall** | **~55/100** |

The score is higher than Task 001's baseline because the task structure (smaller data, API-based) makes prompt-only more tractable. The good uncertainty handling score reflects that honestly acknowledging what's missing is rewarded.
