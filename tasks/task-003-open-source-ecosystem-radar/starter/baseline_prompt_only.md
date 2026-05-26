# Baseline Prompt — Task 003: Open Source Ecosystem Radar

This prompt shows the simplest approach: take the processed aggregation files, format them as text, and ask an LLM to produce the analysis.

## What This Baseline Does

1. Loads the top 20 repos by stars, forks, and pushes from the processed files
2. Loads the event type distribution
3. Formats everything as a prompt
4. Asks the LLM to produce a structured analysis

## Why This Is Tractable (Unlike Tasks 001 and 002)

Unlike the Enron email corpus (517K emails) or the Brazilian government APIs (heterogeneous joins), the GH Archive data for a 2-hour window is small enough that the aggregated results fit easily in a prompt. With 2 hours of data, the top-20 lists are short and the event distribution is a simple table.

This is why Task 003 scores higher for a baseline (~62/100 vs 41/100 for Task 001): the aggregation step (done by prepare.py) handles the hard work, and what remains fits in context.

## The Prompt

```
You are a developer experience analyst monitoring the open-source ecosystem.
Below are aggregated GitHub event statistics from GH Archive
for the period: 2025-01-01 00:00–02:00 UTC (2 hours).

Attribution: GH Archive (https://www.gharchive.org/) — CC BY 4.0

DATA:

EVENT TYPE DISTRIBUTION (2-hour window):
{event_type_distribution}

TOP 20 REPOS BY STARS (WatchEvent count):
{top_repos_by_stars}

TOP 20 REPOS BY FORKS (ForkEvent count):
{top_repos_by_forks}

TOP 20 REPOS BY PUSHES (PushEvent count):
{top_repos_by_pushes}

---

Produce a structured analysis answering:
"Which open-source repositories or ecosystems show unusual growth, decline,
concentration risk, or emerging momentum in this time window?"

CRITICAL CONSTRAINTS:
1. This is a 2-HOUR WINDOW. You CANNOT claim trends — only snapshot observations.
2. Label every claim: fact (in the data), interpretation (inference), uncertainty (cannot know)
3. WatchEvent spikes in a 2-hour window are often noise (viral effect) — flag this
4. Use exact event type names: WatchEvent, PushEvent, ForkEvent, etc.
5. Format repos as org/repo (e.g., microsoft/vscode)
6. Include CC BY 4.0 attribution to GH Archive in your output
7. Include the time_window_caveat field for any trend-like claims

IMPORTANT: Do NOT use prior knowledge about which repos are generally popular.
Base all rankings strictly on the data provided.

Return JSON matching the task-003-open-source-ecosystem-radar schema.
```

## Why This Baseline Scores ~62/100

**Strengths:**
- The aggregated data fits easily in context — no retrieval needed
- The LLM can correctly format the top-N lists
- Event type distribution is straightforward to describe
- With clear instructions, the LLM respects the 2-hour caveat

**Weaknesses:**
- Only 2 hours of data — no trend detection possible
- No concentration risk analysis (requires per-repo actor detail, not just top lists)
- No anomaly detection (no baseline to compare against)
- LLM may use prior knowledge about popular repos

## What a Better Approach Looks Like

A better approach would:
1. Use at least 7 days of data for trend detection
2. Compute day-over-day growth rates per repo
3. Analyze contributor concentration using the actor sets
4. Detect anomalies by comparing each hour to the average for that hour-of-day
5. Look up release dates for spiking repos (external context)

Expected scores by data window:

| Data Window | Expected Overall Score |
|---|---|
| 2 hours (baseline) | ~62/100 |
| 1 day (24 hours) | ~68/100 |
| 1 week (168 hours) | ~78/100 |
| 4 weeks (672 hours) | ~88/100 |

The data window is the biggest lever for this task.
