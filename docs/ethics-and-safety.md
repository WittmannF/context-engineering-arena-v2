# Ethics and Safety

Context Engineering Arena processes real-world data about real individuals, institutions, and events. This document explains the ethical standards that all participants and task authors must follow.

## Core Principles

### 1. Distinguish Evidence from Inference

Never present an inference as a fact. Every claim must be typed as one of:
- `fact` — directly supported by cited evidence
- `interpretation` — a reasonable inference from cited evidence
- `recommendation` — an actionable suggestion
- `uncertainty` — something that cannot be determined from available evidence

Presenting an interpretation as a fact is a scoring violation and may result in a submission being removed.

### 2. Avoid Defamatory Claims

Do not make claims that:
- Assert illegal conduct without authoritative evidence (e.g., court records, regulatory findings)
- Attribute malicious intent to real individuals without strong evidentiary support
- Present speculation as established fact about named real people

This applies even when the underlying data suggests wrongdoing. The job of this benchmark is to organize evidence and surface patterns — not to render legal or moral verdicts.

### 3. Correlation Is Not Causation

Submissions that connect multiple datasets (such as Task 002, Brazil Public Money Trail) must never present a thematic co-occurrence as proof of influence, coordination, or wrongdoing.

Example of acceptable framing:
> "The same agency appears in both the legislative record and the spending record for the same time period. This is a correlation that warrants further investigation, not evidence of improper influence."

Example of unacceptable framing:
> "Deputy X's committee involvement led directly to Agency Y receiving inflated contracts."

### 4. Handle Personal Data Carefully

- Only display personal information that is already publicly available through official records.
- Do not expose private contact details, home addresses, or sensitive personal information even if it appears in the dataset.
- For Enron: emails were of employees acting in professional roles. Avoid analyzing private personal content unrelated to the corporate investigation.
- For Brazil data: display only officially published public servant information.
- For GH Archive: focus on repository and ecosystem trends, not individual developer profiling.

### 5. Mark Limitations Explicitly

Every submission must include a `limitations` array in `answer.json`. This must acknowledge:
- Data coverage gaps (what was not available)
- Retrieval limitations (what your pipeline may have missed)
- Temporal scope limitations
- Any specific caveats about the task corpus

Submissions without a meaningful limitations section will receive a lower uncertainty handling score.

## Task-Specific Guidelines

### Task 001 — Enron Email Dataset

- Focus on organizational patterns and communication structures, not on prosecuting individuals.
- Many employees in the dataset were not senior executives and had limited knowledge or responsibility.
- Cite evidence for any characterization of an individual's role or awareness.
- Use phrases like "available emails suggest" rather than "X knew" unless the evidence is direct.

### Task 002 — Brazil Public Money Trail

- This is a civic accountability task, not an accusation engine.
- Include a visible disclaimer: "This page organizes public data and does not allege wrongdoing."
- Classify all links between entities by type: direct, thematic, actor-based, or hypothetical.
- Do not imply corruption, fraud, or improper influence without direct authoritative evidence.
- Bureaucratic patterns that look unusual may have legitimate explanations — note this possibility.

### Task 003 — GH Archive

- GitHub usernames are public but should not be used to track or profile individual developers.
- Focus on repository and ecosystem-level patterns.
- Be careful attributing "growth" or "decline" to a repository without adequate time windows.

## Enforcement

Submissions that violate these guidelines may be:
1. Flagged for revision with a comment explaining the issue
2. Removed from the leaderboard pending revision
3. Refused from the repository if revisions are not made

Maintainers are not lawyers and cannot provide legal advice. When in doubt about whether a claim is appropriate, mark it as `claim_type: "uncertainty"` or remove it.

## Reporting Concerns

If you see a submission that you believe violates these guidelines, open a GitHub issue with the title `[Ethics Concern] <participant-id> / <task-id>` and describe the specific concern. Maintainers will review within a reasonable time.
