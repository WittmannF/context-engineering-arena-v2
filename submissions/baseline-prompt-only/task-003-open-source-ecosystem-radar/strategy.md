# Strategy Description — Baseline Prompt-Only (Task 003)

## What Was Done

The GH Archive baseline used a three-step process:

1. **Download**: Downloaded 2 hours of GH Archive data (2025-01-01-0.json.gz and 2025-01-01-1.json.gz, ~149 MB compressed).

2. **Aggregate**: Ran prepare.py on the two files, which parsed all 412,847 events and produced aggregated output files: top-50 repos by stars, forks, pushes, and PRs; event type distribution; hourly event counts.

3. **Generate**: Formatted the top-20 lists and event distribution as a single LLM prompt and called claude-3-haiku-20240307 to produce the structured analysis.

Unlike Tasks 001 and 002, the bottleneck in this task is not context selection but rather the aggregation step. prepare.py ran in ~4 minutes and did the hard computational work. The LLM's job was to interpret already-aggregated results, which is a much easier task.

## Why This Baseline Scores Higher

Task 003 scores higher (~62/100) than Task 001 (~41/100) or Task 002's data-joining dimension (~15/100) for a specific structural reason: the aggregation pre-processing handles the large data volume, and the LLM only sees a compact summary.

With 2 hours of data (149 MB compressed, 412K events), the entire analysis fits comfortably in one LLM context window after aggregation. This is a different problem structure than the Enron task, where the raw data is too large to aggregate into a single compact summary.

## The Main Limitation: Data Window

The fundamental weakness of this baseline is the 2-hour data window. The task asks for "unusual growth, decline, concentration risk, or emerging momentum" — but you cannot detect growth, decline, or momentum from a single 2-hour snapshot. You can only report what was most active in that window.

The submission addresses this honestly: every trend-adjacent claim is labeled `uncertainty`, and the caveats section prominently flags the 2-hour limitation. This honest uncertainty handling is why the uncertainty dimension scores well.

The holiday timing (New Year's Day midnight) is an additional wrinkle. Professional development activity at midnight on Jan 1 is not representative of normal GitHub patterns. Star activity is likely elevated (people bookmarking repos to explore in the new year) and push activity is likely depressed (developers are not at work). Identifying this bias and noting it is good analysis.

## What the Submission Does Well

1. **Aggregation efficiency**: The approach correctly separates the data processing problem (parse 412K events) from the context engineering problem (interpret the aggregated results). Prepare.py handles the former; the LLM handles the latter.

2. **Claim type discipline**: Star count rankings are labeled `fact` (they are direct counts). The interpretation of the star-to-push ratio is labeled `interpretation`. Any trend claim is labeled `uncertainty` with an explicit time window caveat.

3. **Honest attribution**: The CC BY 4.0 GH Archive attribution is included as required.

4. **Holiday bias acknowledgment**: The submission correctly identifies that 00:00-02:00 UTC on Jan 1 is a non-representative window and flags this prominently.

## What Would Improve the Score

The biggest lever is more data:

- **1 day (24 hours)**: Would allow intra-day comparison. Still too short for trend detection.
- **1 week (168 hours)**: Would allow day-over-day comparisons. First window where weak trend claims become defensible.
- **4 weeks (672 hours)**: Would allow meaningful trend, growth, and concentration analysis.

Secondary improvements:
- **Bot filtering**: Identify and exclude automated accounts from push rankings
- **Baseline comparison**: Download the same 2-hour window from 7 days prior for anomaly detection
- **Release correlation**: Check ReleaseEvent timing against star spikes to identify "got released → got stars" patterns
- **External context enrichment**: Check Hacker News and Twitter/X for posts about top-starred repos in this window

## The Aggregation Insight

The key insight from this task is that aggregation-first context engineering can make large datasets tractable without retrieval. With 412K events, individual event retrieval is infeasible in a prompt. But aggregating to top-20 lists reduces the relevant context to ~80 records — easily within any LLM context window.

The limitation is that aggregation loses fine-grained signal. Knowing that microsoft/vscode got 847 stars doesn't tell you why — you'd need to look at the individual events to find patterns. For the purposes of this baseline, aggregate statistics are sufficient. For a higher-scoring submission, you'd need a hybrid approach: aggregate for overview, then retrieve detail for specific interesting repos.
