# Scoring Rubric — Task 003: Open Source Ecosystem Radar

Each dimension is scored 0–10. The overall score is a weighted average.

---

## Dimension 1: Correct Aggregation (Weight: 0.25)

Measures whether event counts, rankings, and aggregations are arithmetically correct and methodologically sound.

### Full Marks (9–10)
- Event counts per repository are accurate (verifiable from the raw data)
- Event types are correctly identified and not confused (WatchEvent ≠ PushEvent ≠ ForkEvent)
- Time windows are clearly stated and respected (if claiming "top repos in 24 hours," all 24 hours are covered)
- Distinct event types are correctly counted separately (stars and forks are separate metrics)
- Top-N lists are consistent with the underlying data
- Deduplication handled correctly (same repo counted once, not once per event)

### Partial Marks (5–8)
- Most aggregations correct but a few minor errors
- Event types generally correct but occasional confusion
- Time window stated but slightly inconsistent

### Low Marks (1–4)
- Multiple incorrect event counts
- Event types confused or mislabeled
- Rankings inconsistent with stated methodology

### Zero (0)
- Aggregations appear fabricated

---

## Dimension 2: Signal vs Noise Discrimination (Weight: 0.25)

Measures the ability to distinguish meaningful trends from transient artifacts.

### Full Marks (9–10)
- The submission distinguishes between event types by their signal quality:
  - `WatchEvent` spikes are treated as popularity signals that may be transient
  - `PushEvent`/`PullRequestEvent` patterns are treated as stronger development activity signals
  - `ReleaseEvent` is noted as a meaningful milestone signal
- Viral spikes (sudden large WatchEvent bursts) are flagged as potentially noise
- Sustained patterns over multiple hours/days are weighted higher than single-hour spikes
- The submission explains why a repository is notable, not just that it is ranked #1
- At least one anomaly is identified and a plausible explanation is offered

### Partial Marks (5–8)
- Some signal/noise discrimination present but not systematic
- Most repositories explained but a few just ranked without context
- WatchEvent spikes handled but other event types not differentiated

### Low Marks (1–4)
- All event types treated equally
- Rankings presented without context
- No anomaly identification

---

## Dimension 3: Useful Trend Explanations (Weight: 0.15)

Measures whether the trend insights are actually useful to a developer reader.

### Full Marks (9–10)
- Each major finding includes a plausible explanation of why this is happening
- Explanations reference verifiable context (e.g., "recent release on this date," "related HN discussion time window")
- Concentration risk analysis explains the structural implication (e.g., "if this org stops contributing, 60% of commits stop")
- Emerging vs declining is distinguished and explained
- Recommendations for developers are specific and actionable

### Partial Marks (5–8)
- Most findings have explanations, but some are vague
- Concentration risk present but not well explained

### Low Marks (1–4)
- Explanations are generic ("AI is popular")
- No concentration risk analysis
- No actionable recommendations

---

## Dimension 4: Evidence Quality (Weight: 0.15)

Measures whether claims are backed by specific, traceable evidence from the dataset.

### Full Marks (9–10)
- Every major claim cites a specific repository name, event count, and time window
- Evidence references specific files from the processed dataset
- At least 6 distinct evidence items
- Mix of different event types in evidence (not all WatchEvents)

### Partial Marks (5–8)
- Most claims have evidence but some are vague
- 4–5 evidence items

### Low Marks (1–4)
- Claims not backed by specific evidence
- Evidence appears to reference general GitHub knowledge, not GH Archive data

---

## Dimension 5: Context Efficiency (Weight: 0.10)

Measures how well the submission used its processing budget.

### Full Marks (9–10)
- Context trace shows what files were processed, how many events, and what was summarized vs. read in full
- The submission explains how it handled the large event volume (aggregation, sampling, filtering)
- Token estimates are plausible

### Partial Marks (5–8)
- Context trace present but incomplete

### Low Marks (1–4)
- No context trace
- No indication of how the large event volume was handled

---

## Dimension 6: Clarity for Developers (Weight: 0.10)

Measures whether a developer would find this page clear, well-organized, and directly useful.

### Full Marks (9–10)
- Repository names are formatted correctly (org/repo format, e.g., `torvalds/linux`)
- Technical terms are used correctly (WatchEvent, PushEvent, etc.)
- Findings are organized by what matters (not just ranked by event count)
- A developer could make a decision (which library to adopt, which project to watch) based on this page
- Caveats are honest and don't undermine all findings ("caveat everything" is not the goal)

### Partial Marks (5–8)
- Mostly clear but some organizational issues
- Repository names occasionally incorrect format

### Low Marks (1–4)
- Hard to navigate
- Technical terms incorrect
- Unhelpful for any decision

---

## Data Size and Scoring Caveats

The amount of data processed significantly affects what can be claimed:

| Data Volume | Minimum Claims Supported |
|---|---|
| 1–2 hours | Snapshot only — no trend claims. Can rank repos in this window. |
| 1 day (24 hours) | Intra-day patterns. Weak trend signals. |
| 3–7 days | Weekly patterns visible. Day-over-day trends supportable. |
| 2–4 weeks | Monthly patterns. Trends vs. anomalies more distinguishable. |

A submission that uses 2 hours of data and claims to identify "trends" will be penalized under Signal vs Noise Discrimination, even if the aggregation is correct.

Submissions must explicitly state their data window and limit trend claims accordingly.

---

## Example: High-Quality Evidence Item

```json
{
  "id": "ev-003",
  "repo": "microsoft/vscode",
  "event_type": "WatchEvent",
  "count": 847,
  "time_window": "2025-01-01T00:00:00Z to 2025-01-01T02:00:00Z (2 hours)",
  "rank": 1,
  "source_files": ["2025-01-01-0.json.gz", "2025-01-01-1.json.gz"],
  "notes": "847 stars in 2 hours. No release event in this window. May reflect organic activity or external promotion. Baseline star rate for vscode not available in this 2-hour window."
}
```

Why this is high quality:
- Specific repo name, event type, count
- Exact time window stated
- Source files named
- Notes acknowledge limitations (no baseline, possible noise)

---

## Example: Low-Quality Evidence Item

```json
{
  "id": "ev-001",
  "claim": "AI repositories are trending on GitHub",
  "evidence": "Many AI repos appeared in top starred list"
}
```

Why this is poor:
- No specific repository names
- No event counts
- "Many" is vague
- No time window
- Appears to be based on general knowledge, not specific data

---

## Automatic Penalties

| Issue | Penalty |
|---|---|
| Claiming "trend" from less than 1 hour of data | –15 pts Signal vs Noise |
| Event type misidentification (WatchEvent called PushEvent, etc.) | –10 pts Aggregation |
| Top-N list that cannot be reproduced from stated data | –15 pts Aggregation |
| Missing attribution to GH Archive (CC BY 4.0) | –5 pts overall |
| No context trace | –5 pts Context Efficiency |
| Missing required sections | –5 pts per section |
