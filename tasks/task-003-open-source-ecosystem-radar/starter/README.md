# Getting Started — Task 003: Open Source Ecosystem Radar

## Step 1: Download Data

```bash
# Quick start: 2-hour sample (small, fast)
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --hours 2

# Better: full day for meaningful analysis
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01

# Best for trend detection: one week (168 files, ~8-25 GB)
python tasks/task-003-open-source-ecosystem-radar/scripts/download.py \
    --start-date 2025-01-01 \
    --end-date 2025-01-07
```

## Step 2: Prepare Aggregated Data

```bash
python tasks/task-003-open-source-ecosystem-radar/scripts/prepare.py
```

## Step 3: Understand the Data

GH Archive events have this general structure:

```json
{
  "id": "12345678901",
  "type": "WatchEvent",
  "actor": {"login": "someuser", "id": 12345},
  "repo": {"id": 67890, "name": "org/repo-name"},
  "org": {"login": "org-name"},
  "payload": {"action": "started"},
  "created_at": "2025-01-01T00:15:23Z"
}
```

**WatchEvent** = someone starred the repository (payload.action is always "started")
**PushEvent** = code pushed; payload contains commits array
**PullRequestEvent** = PR opened/closed/merged/etc.
**ForkEvent** = someone forked the repository
**ReleaseEvent** = a release was published; payload.release has tag_name, body, etc.

## Step 4: Know What You Can and Cannot Claim

**With 2 hours of data:**
- You CAN: rank the most-starred, most-pushed, most-forked repos in those 2 hours
- You CAN: describe the event type distribution
- You CANNOT: claim any repo is "trending" (no baseline to compare to)
- You CANNOT: detect anomalies (no normal to compare to)

**With 1 day of data:**
- You CAN: show intra-day patterns (night vs day activity, timezone effects)
- You CAN: identify repos with high activity across multiple hours (slightly more signal)
- You STILL CANNOT: establish meaningful trends (need at least a week)

**With 1 week of data:**
- You CAN: detect day-over-day changes
- You CAN: distinguish sustained growth from one-day spikes
- You CAN: make weak trend claims (label as `interpretation`, not `fact`)

**With 4+ weeks:**
- You CAN: make trend claims with higher confidence
- You CAN: seasonal analysis (weekday vs weekend patterns)
- You CAN: label growth trajectories as `fact` if consistent across weeks

## Step 5: Signal Hierarchy

Not all events have equal value as signals. From most to least reliable as "health" signals:

1. **PushEvent** — someone wrote code. Strong development signal.
2. **PullRequestEvent (closed+merged)** — code was reviewed and merged. Strong collaboration signal.
3. **ReleaseEvent** — a version was shipped. Strong maturity signal.
4. **IssuesEvent (opened+closed)** — users are engaged and problems are being resolved.
5. **ForkEvent** — someone wants to extend the project. Interest signal.
6. **WatchEvent** — someone starred. Popularity signal, but highly noisy (viral effects).
7. **CreateEvent (branch)** — active development. Weak signal on its own.

A repo with 100 pushes and 5 releases in a week is healthier than a repo with 10,000 stars and 0 pushes.

## Step 6: Concentration Risk

Concentration risk is a unique signal in this task. To compute it:

```python
import json
from collections import Counter

# Load repo details
details = []
with open("data/processed/task-003-open-source-ecosystem-radar/repo_event_details.jsonl") as f:
    for line in f:
        details.append(json.loads(line))

# For a given repo, high unique_actors = good diversity
# Low unique_actors + high PushEvent count = high concentration

for repo in details[:20]:
    if repo.get("PushEvent", 0) > 50:
        actors = repo.get("unique_actors", 1)
        pushes = repo.get("PushEvent", 0)
        concentration = pushes / max(actors, 1)
        print(f"{repo['repo']:50s} {pushes:5d} pushes / {actors:4d} actors = {concentration:.1f} concentration")
```

A very high ratio (e.g., 50 pushes per 1 actor) may indicate single-maintainer risk.

## Common Mistakes

1. **Calling a star spike a trend.** A repo that gets 5,000 stars in 2 hours is not "trending" — it may have been featured on HN, Reddit, or Twitter. Without baseline data, you can only say "unusually high WatchEvent activity in this window."

2. **Treating all repos as equal.** A repo with 1 WatchEvent may be a fork of a popular project. Filter out forks and archived repos when possible.

3. **Not attributing GH Archive.** The CC BY 4.0 license requires attribution. Every submission must include: "Data: GH Archive (https://www.gharchive.org/) CC BY 4.0"

4. **Missing the claim type label.** Every claim must be labeled `fact`, `interpretation`, or `uncertainty`. "Top starred repo in this 2-hour window is X with Y stars" is a `fact`. "X is gaining momentum" is an `interpretation` at best.

5. **Wrong event type names.** Use the exact names: `WatchEvent` (not "StarEvent"), `PushEvent` (not "CommitEvent"), etc.

## Quick Exploration Script

```python
import gzip
import json
from collections import Counter

path = "data/raw/task-003-open-source-ecosystem-radar/2025-01-01-0.json.gz"

event_types = Counter()
repo_stars = Counter()

with gzip.open(path) as f:
    for line in f:
        ev = json.loads(line)
        event_types[ev["type"]] += 1
        if ev["type"] == "WatchEvent":
            repo_stars[ev["repo"]["name"]] += 1

print("Event type distribution (first hour):")
for et, count in event_types.most_common(10):
    print(f"  {et:30s} {count:7,}")

print("\nTop 10 starred repos (first hour):")
for repo, count in repo_stars.most_common(10):
    print(f"  {count:5d}  {repo}")
```
