# Scoring Rubric — Task 001: The Enron Investigation Brief

Each dimension is scored 0–10. The overall score is a weighted average. See weights below.

---

## Dimension 1: Evidence Quality (Weight: 0.25)

Measures whether claims in the submission are backed by specific, traceable evidence from the dataset.

### Full Marks (9–10)
- Every major claim (labeled `fact` or `interpretation`) cites at least one evidence item with a specific email reference (message_id, sender, date, and a verbatim or paraphrased excerpt)
- Evidence items are relevant to the claim they support — not merely co-present in the corpus
- Short excerpts are used; email bodies are not reproduced in full
- Evidence spans multiple people, time periods, and topics — not all from one folder or one week
- At least 10 distinct evidence items in the submission

### Partial Marks (5–8)
- Most claims have evidence, but some major claims lack citations
- Some evidence items are only loosely related to the claims they support
- Evidence comes from a narrow time period or a single employee's mailbox
- 5–9 distinct evidence items

### Low Marks (1–4)
- Many claims lack any evidence citation
- Evidence items reference emails that appear generic or cannot be verified in the dataset
- Evidence is clearly drawn from LLM prior knowledge about Enron (dates, names, events) rather than retrieved emails
- Fewer than 5 distinct evidence items

### Zero (0)
- No evidence items, or all evidence items appear fabricated

### Example: High-Quality Claim with Good Evidence

```
Claim: "Andy Fastow used internal Enron email to coordinate LJM transaction structures with finance staff
while simultaneously managing LJM as an outside general partner."
Type: fact
Confidence: 0.78
Evidence: [
  {
    "evidence_id": "ev-012",
    "email_from": "andrew.fastow@enron.com",
    "email_to": ["ben.glisan@enron.com", "richard.buy@enron.com"],
    "date": "2001-06-14",
    "subject": "LJM2 — Raptor IV closing schedule",
    "excerpt": "...we need to get the Raptor IV closing docs to the board sub-committee
    by Friday. Let's align on valuations before we loop in outside counsel...",
    "relevance": "Shows Fastow coordinating from an Enron email address on LJM transaction
    details, supporting the conflict of interest pattern."
  }
]
```

### Example: Low-Quality Claim with Poor Evidence

```
Claim: "Enron executives knew the company was in trouble by mid-2001."
Type: fact
Confidence: 0.9
Evidence: [
  {
    "evidence_id": "ev-003",
    "excerpt": "There were concerns about the financial situation at Enron.",
    "source": "general knowledge"
  }
]
```

**Problems:** The claim is vague, the confidence is overstated, and the evidence is a paraphrase of general knowledge, not a specific email.

---

## Dimension 2: Timeline Quality (Weight: 0.15)

Measures whether the investigative timeline is built from parsed email dates in the dataset rather than from prior knowledge.

### Full Marks (9–10)
- At least 8 timeline events
- Events span the full arc of the corpus (1998/1999 through late 2001)
- Event dates are traceable to specific emails or clusters of emails in the dataset
- Timeline distinguishes between events documented in the corpus vs. external events cited for context
- External events (e.g., SEC filing, bankruptcy) are clearly labeled as context, not corpus evidence
- Temporal gaps are noted and acknowledged

### Partial Marks (5–8)
- 5–7 timeline events
- Most events are corpus-derived but some appear to come from general Enron knowledge
- Timeline covers the main arc but misses important periods
- Minimal distinction between corpus-derived and context events

### Low Marks (1–4)
- Fewer than 5 events
- Timeline appears to be built from Wikipedia or general Enron knowledge, not the email corpus
- Events are not anchored to specific emails or time periods

### Zero (0)
- No timeline provided, or timeline is entirely fabricated

---

## Dimension 3: Entity Extraction Quality (Weight: 0.10)

Measures accuracy and completeness of identified people, organizations, and entities.

### Full Marks (9–10)
- Key people correctly identified with their roles: Ken Lay (Chairman/CEO), Jeff Skilling (CEO/President), Andy Fastow (CFO), Sherron Watkins (VP Corporate Development, whistleblower), Ben Glisan (Treasurer), Rebecca Mark, Lou Pai, Cliff Baxter
- Key entities correctly described: LJM Cayman LP, LJM2 Co-Investment LP, Raptor vehicles (I–IV), JEDI partnership, Chewco, Whitewing
- At least 5 distinct people and 5 distinct organizations/entities identified
- No major entity confusion (e.g., conflating people with similar names)
- Communication patterns between key entities described (who emails whom, at what frequency)

### Partial Marks (5–8)
- Most key figures identified but some roles are incorrect or incomplete
- Some SPEs and vehicles described but not all
- Limited communication pattern analysis

### Low Marks (1–4)
- Only the most famous names (Lay, Skilling, Fastow) identified
- No organizational entities (SPEs, partnerships) described
- Entity descriptions contain factual errors

---

## Dimension 4: Uncertainty Handling (Weight: 0.20)

Measures whether the submission correctly labels claims with appropriate confidence levels and explicitly flags speculative inferences.

### Full Marks (9–10)
- All claims have a `type` field: `fact`, `interpretation`, or `uncertainty`
- `fact` claims are only used for things directly documented in the corpus with clear, unambiguous evidence
- `interpretation` claims are used where evidence exists but multiple explanations are plausible
- `uncertainty` claims are used for things the submission cannot verify from the corpus
- A dedicated `uncertainties` section exists listing open questions
- The submission explicitly states what was NOT examined and why
- Confidence scores (0.0–1.0) are present and calibrated — confident claims (>0.85) are backed by strong evidence; uncertain claims (<0.60) are labeled accordingly

### Partial Marks (5–8)
- Most claims have type labels but some are missing
- Occasional overconfidence (labeling an inference as a fact)
- Uncertainties section exists but is brief
- Confidence scores present but not well-calibrated

### Low Marks (1–4)
- Many claims have no type label
- Multiple clear inferences labeled as facts
- No uncertainties section
- No acknowledgment of what was not examined

### Zero (0)
- All claims labeled as facts; no uncertainty acknowledged anywhere

---

## Dimension 5: Hallucination Avoidance (Weight: 0.20)

Measures whether the submission fabricates evidence, emails, or facts not present in the dataset.

### Full Marks (9–10)
- No fabricated email excerpts — all excerpts can be traced to the dataset (or are explicitly labeled as paraphrased/representative)
- No invented dates, message IDs, or people not in the dataset
- Claims about events after the corpus ends (post-December 2001) are labeled as external context
- The submission acknowledges when it relies on prior knowledge rather than the dataset
- Any facts sourced outside the corpus (e.g., SEC filings, public record) are explicitly attributed as external

### Partial Marks (5–8)
- No obviously fabricated emails, but some claims blend corpus evidence with prior knowledge without clear attribution
- A few dates or names appear slightly off but not egregiously wrong
- Minor confusion between corpus-derived claims and externally-known facts

### Low Marks (1–4)
- At least one fabricated email excerpt or invented evidence item
- Claims about specific internal conversations that are not documented in the corpus
- Message IDs or file paths that do not match the dataset format

### Zero (0)
- Multiple fabricated email excerpts, or the entire evidence section appears invented

---

## Dimension 6: Context Efficiency (Weight: 0.05)

Measures how well the submission used its context budget relative to what it retrieved and what it produced.

### Full Marks (9–10)
- A `context_trace.json` is provided showing what was retrieved and why
- The ratio of documents_used_in_final to documents_retrieved is reasonable (not padding the prompt with irrelevant material)
- Token estimates are plausible and the strategy is described coherently
- The submission explains its filtering or ranking decisions

### Partial Marks (5–8)
- Context trace provided but incomplete
- Some inefficiency in document selection visible from the trace

### Low Marks (1–4)
- No context trace, or context trace shows random or unfiltered document selection
- Obvious padding (hundreds of emails included, most irrelevant)

---

## Dimension 7: Usefulness of the Final Page (Weight: 0.05)

Measures whether a non-expert reader (investigative journalist, policy researcher) would find the page genuinely useful.

### Full Marks (9–10)
- An investigative journalist encountering this page for the first time could immediately understand what happened and follow up on the most important leads
- The page clearly prioritizes the most significant findings
- Visual structure (timeline, claim-evidence table, entity cards) is coherent and navigable
- The uncertainty section helps the reader calibrate what to trust

### Partial Marks (5–8)
- Useful but dense — requires effort to navigate
- Important findings may be buried in long lists

### Low Marks (1–4)
- Disorganized or confusing
- Reads like a data dump rather than an investigative brief
- A reader would not know what to do with this information

---

## Automatic Metrics

The following are computed automatically and feed into the scores above:

| Metric | Description |
|---|---|
| `evidence_id_coverage_rate` | Fraction of claims that have at least one evidence_id |
| `claim_confidence_distribution` | Distribution of confidence scores across claims |
| `timeline_completeness` | Number of timeline events divided by expected minimum (8) |
| `claim_type_distribution` | Fraction of claims labeled fact / interpretation / uncertainty |

A submission that has 0% `evidence_id_coverage_rate` automatically scores 0 on Evidence Quality regardless of other factors.

---

## Penalties

The following incur automatic score deductions:

| Issue | Penalty |
|---|---|
| Fabricated email excerpt (one instance) | –10 points from Evidence Quality |
| Fabricated email excerpt (three or more instances) | –25 points from Evidence Quality |
| No `type` field on any claim | –15 points from Uncertainty Handling |
| All claims labeled `fact` with confidence > 0.9 | –10 points from Uncertainty Handling |
| No context_trace.json provided | –5 points from Context Efficiency |
| Timeline has fewer than 3 events | –10 points from Timeline Quality |
| Missing required sections | –5 points per missing section |
