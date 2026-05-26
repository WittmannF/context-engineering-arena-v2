# Task 003: Open Source Ecosystem Radar

## What This Task Is

The Open Source Ecosystem Radar asks you to process GH Archive event data and build a developer-focused page that identifies trends, anomalies, and concentration risks in the open-source ecosystem.

The benchmark question is:

> Which open-source repositories or ecosystems show unusual growth, decline, concentration risk, or emerging momentum in the selected time window?

You must answer this with evidence from the actual event data — specific repositories, specific metrics, specific time windows — not from general knowledge about GitHub trends.

## Why This Task Is Interesting

GH Archive is a high-volume event stream: GitHub generates roughly 3–10 million events per day across hundreds of thousands of repositories. The challenge is not finding data — it is finding signal in noise.

A single viral Reddit post can make a small repository look like a breakout star for 48 hours (WatchEvent spike), then disappear. A major release (ReleaseEvent) should be weighted differently than a star burst. A repository that slowly grows 500 contributors over 6 months is healthier than one that gets 50,000 stars in a weekend from a Product Hunt launch.

Concentration risk is a particularly interesting signal: if 80% of a language ecosystem's commits come from 3 organizations or 10 developers, that is a structural vulnerability. This kind of insight requires aggregation, not just ranking.

The task also tests your ability to communicate insights to a technical audience — developers who will quickly dismiss overconfident or poorly-evidenced claims.

## The Dataset

**Name:** GH Archive
**Source:** https://www.gharchive.org/
**License:** CC BY 4.0 (attribution required)
**Size:** ~50–150 MB per hour (gzip-compressed), ~1–3 GB per day uncompressed
**Format:** Hourly `.json.gz` files, each containing newline-delimited JSON events
**URL pattern:** `https://data.gharchive.org/YYYY-MM-DD-H.json.gz`

Example URLs:
- `https://data.gharchive.org/2025-01-01-0.json.gz` (midnight–1am UTC on Jan 1, 2025)
- `https://data.gharchive.org/2025-01-01-12.json.gz` (noon–1pm UTC on Jan 1, 2025)

Hours are 0–23. Each file covers one UTC hour.

### Key Event Types

| Event Type | Meaning | Relevance |
|---|---|---|
| `WatchEvent` | User starred a repo | Popularity signal (noisy) |
| `PushEvent` | Code pushed to a branch | Development activity |
| `PullRequestEvent` | PR opened/closed/merged | Collaboration signal |
| `IssuesEvent` | Issue opened/closed | User engagement |
| `ForkEvent` | Repo forked | Interest signal |
| `ReleaseEvent` | Release published | Project maturity signal |
| `CreateEvent` | Branch/tag/repo created | Activity signal |
| `MemberEvent` | Collaborator added | Organization signal |
| `PublicEvent` | Repo made public | New project signal |

## How to Download

```bash
# Sample mode: 2 hours from 2025-01-01
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --hours 2

# Full day
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --end-date 2025-01-01

# One week
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --end-date 2025-01-07

# Limit to specific max files
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --max-files 4
```

Note: ~50–150 MB per file. A full week (168 files) is ~8–25 GB uncompressed. Plan storage accordingly.

## How to Prepare the Data

```bash
python tasks/task-003-open-source-ecosystem-radar/scripts/prepare.py
```

This produces in `data/processed/task-003-open-source-ecosystem-radar/`:
- `top_repos_by_stars.json` — repositories with most WatchEvents
- `top_repos_by_forks.json` — repositories with most ForkEvents
- `event_type_distribution.json` — counts by event type
- `hourly_event_counts.json` — events per hour
- `repo_event_details.jsonl` — per-repo event summary

## The Benchmark Question

> Which open-source repositories or ecosystems show unusual growth, decline, concentration risk, or emerging momentum in the selected time window?

Your analysis must cover at least two of these four signals:
1. **Unusual growth** — repositories or ecosystems with event rates significantly above their baseline or peers
2. **Decline** — repositories or ecosystems with decreasing activity or engagement
3. **Concentration risk** — ecosystems where activity is highly concentrated in few actors or organizations
4. **Emerging momentum** — newer projects showing consistent upward trajectory

## What a Good Submission Looks Like

### Strong Submission
- Uses at least 24 hours of data (1 day minimum) for trend claims
- Distinguishes between different event types — not all events are equal
- Identifies specific repositories with specific evidence (not just "AI repos are trending")
- Notes anomalies with plausible explanations (release, PR coverage, HN/Reddit effect)
- Has a concentration risk analysis using contributor/organization distribution
- Explicitly caveats that 2 hours of data cannot establish a "trend" — only a snapshot
- Claims are labeled fact/interpretation/uncertainty

### Weak Submission
- Uses 2 hours of data and calls the most-starred repos "trending"
- Makes vague claims like "AI is growing fast" without specific evidence
- Treats WatchEvent volume as equivalent to development activity
- No concentration risk analysis
- No temporal dimension (a snapshot is not a trend)

## Scoring Notes

See `rubric.md` for the full rubric. Key differences from Tasks 001 and 002:

- **Aggregation correctness** is important — wrong event counts or misidentified event types will be caught
- **Signal vs Noise** rewards submissions that explain why a spike is or isn't meaningful
- **Developer Usefulness** is the primary human metric — would a developer actually use this page to make decisions?
- The task is easier to score well on when you have more than 2 hours of data

## Ethics Notes

- GH Archive records public GitHub events and public usernames. These are already public.
- Do not build profiles of individual developers from this data — focus on repositories and ecosystems
- CC BY 4.0 license requires attribution to GH Archive in your submission
- Do not attempt to identify or expose private repositories

## Attribution (required by CC BY 4.0)

Data source: GH Archive (https://www.gharchive.org/)
License: Creative Commons Attribution 4.0 International (CC BY 4.0)

## Files in This Task

```
tasks/task-003-open-source-ecosystem-radar/
  task.yaml                    # Task definition
  README.md                    # This file
  rubric.md                    # Detailed scoring rubric
  data_manifest.yaml           # Data sources and preparation steps
  expected_answer_schema.json  # JSON Schema for valid answers
  scripts/
    download.py                # Downloads .json.gz files from GH Archive
    prepare.py                 # Aggregates events into analysis files
    sample.py                  # Creates a small sample for testing
  starter/
    README.md                  # Getting started guide
    baseline_prompt_only.md    # Simple baseline prompt
    baseline_strategy.py       # Example baseline strategy script
```
