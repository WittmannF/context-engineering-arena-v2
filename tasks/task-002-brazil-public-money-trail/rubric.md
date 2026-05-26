# Scoring Rubric — Task 002: Brazil Public Money Trail

Each dimension is scored 0–10. The overall score is a weighted average. See weights below.

---

## Dimension 1: Quality of Data Joining (Weight: 0.20)

Measures whether the submission successfully joined data from at least two sources (Câmara API and Portal da Transparência) and produced a coherent cross-source analysis.

### Full Marks (9–10)
- Data from both Câmara (legislative) and Portal da Transparência (spending) is present and cited
- The submission explicitly traces connections between legislative events and spending events
- Entity names are normalized across sources (e.g., the same ministry appears as the same entity even if named differently in each API)
- Budget program codes or functional classification codes are used to link legislative intent to specific spending lines
- Data coverage dates are consistent across sources (same theme, overlapping time periods)

### Partial Marks (5–8)
- Both sources used but joining is partial or superficial
- Some entity normalization done but inconsistencies remain
- Time periods don't perfectly overlap but the submission acknowledges this

### Low Marks (1–4)
- Only one data source used (Câmara OR Transparência, not both)
- No meaningful join attempted
- Sources listed but not actually connected in the analysis

### Zero (0)
- No actual data retrieved or joined; analysis appears to be entirely from prior knowledge

---

## Dimension 2: Correctness of Legislative Timeline (Weight: 0.10)

Measures whether the legislative timeline accurately reflects data from the Câmara API.

### Full Marks (9–10)
- Timeline includes real proposition numbers (PL, PEC, MP format) with correct years
- Proposition status is accurately stated (tramitando, aprovado, arquivado, etc.)
- Authorship is correct (deputy name, party, state)
- Key dates are consistent with API responses (date of presentation, vote dates, etc.)
- At least 5 legislative events in the timeline

### Partial Marks (5–8)
- Most timeline entries are accurate but a few have minor errors
- Some propositions missing or dates slightly off
- 3–4 events in timeline

### Low Marks (1–4)
- Multiple errors in proposition numbers or status
- Timeline appears built from general knowledge rather than API data
- Fewer than 3 events

---

## Dimension 3: Correctness of Public Spending Summary (Weight: 0.10)

Measures whether spending figures and programs are correctly represented.

### Full Marks (9–10)
- Spending figures are from Portal da Transparência and are labeled with the year/period they cover
- Program names use official terminology (ação orçamentária, programa, órgão)
- Percentages and comparisons are arithmetically correct
- Transfers to states/municipalities correctly distinguished from direct federal spending
- At least 3 spending data points with source attribution

### Partial Marks (5–8)
- Spending data present but some figures have minor errors or missing attribution
- Program names slightly off but recognizable
- 2 spending data points

### Low Marks (1–4)
- Spending figures appear invented or unsourced
- Program names incorrect or confused
- Only one spending data point

### Zero (0)
- No spending data, or all spending data appears fabricated

---

## Dimension 4: Evidence Quality (Weight: 0.15)

Measures whether claims are backed by specific, attributed evidence from the APIs.

### Full Marks (9–10)
- Every major claim cites a specific API response with enough detail to reproduce (endpoint, parameters, record ID or proposition number)
- Evidence is relevant to the claim it supports
- At least 8 distinct evidence items
- Mix of legislative and spending evidence

### Partial Marks (5–8)
- Most claims have evidence but some lack citations
- Some evidence loosely related to claims
- 5–7 evidence items

### Low Marks (1–4)
- Many claims without evidence
- Evidence citations too vague to reproduce (e.g., "Câmara API" without parameters)
- Fewer than 5 evidence items

---

## Dimension 5: Fact vs Inference Distinction (Weight: 0.20)

This dimension is weighted heavily because this task specifically tests the ability to distinguish documented facts from analytical inferences.

### Full Marks (9–10)
- Every claim is labeled `fact`, `interpretation`, or `uncertainty`
- Links between legislative and spending data are classified using the required taxonomy:
  - `direct_documented_link`: explicitly documented connection (e.g., a budget amendment directly authorizing funds for a named program)
  - `same_theme_link`: both events are in the same policy domain but no documented direct connection
  - `same_actor_link`: the same individual appears on both sides but without documented causal connection
  - `same_agency_link`: the same ministry/agency appears in both datasets in the same period
  - `same_time_window_link`: temporal co-occurrence only
  - `weak_or_hypothetical_link`: speculative connection
- The submission never presents a `same_theme_link` as a `direct_documented_link`
- A prominent disclaimer states the page does not allege wrongdoing

### Partial Marks (5–8)
- Most claims labeled but some missing type annotations
- Most links classified but occasional mislabeling
- Disclaimer present but understated

### Low Marks (1–4)
- Many claims with no type label
- Links classified simplistically (just "direct" vs "indirect") without the required taxonomy
- At least one instance of a same-theme or same-actor link presented as a direct documented causal link
- No disclaimer

### Zero (0)
- Multiple clear inferences presented as facts
- The submission implies corruption or improper conduct without documentary evidence

**Penalty:** Any instance of asserting illegal conduct or corruption without an authoritative source (court ruling, TCU sanction, etc.) results in an automatic –20 point deduction from the overall score, regardless of other dimension scores.

---

## Dimension 6: Uncertainty Handling (Weight: 0.10)

### Full Marks (9–10)
- Dedicated `what-could-not-be-verified` section with at least 3 items
- Explicit statement about Portal da Transparência data availability (or unavailability in sample mode)
- Open questions are framed as questions, not rhetorical accusations
- Confidence scores present and calibrated

### Partial Marks (5–8)
- Uncertainty section present but brief
- Most open questions framed appropriately
- Some calibration issues

### Low Marks (1–4)
- No uncertainty section
- Open questions framed as rhetorical accusations
- No acknowledgment of data gaps

---

## Dimension 7: Civic Usefulness (Weight: 0.05)

Measures whether a Brazilian citizen, journalist, or civic researcher would find this page genuinely useful.

### Full Marks (9–10)
- A person with no specialized knowledge could understand what happened and why it matters
- The `recommended-next-investigations` section provides specific, actionable follow-up steps
- The analysis is oriented toward accountability (what was done with public money) rather than accusation
- Key figures are presented in their institutional context, not as individual targets

### Partial Marks (5–8)
- Useful for a specialist but requires background knowledge to navigate
- Some actionable recommendations

### Low Marks (1–4)
- Dense and confusing
- Recommendations are vague or missing
- Reads as an accusation rather than an accountability analysis

---

## Dimension 8: Hallucination Avoidance (Weight: 0.05)

### Full Marks (9–10)
- No invented proposition numbers, spending figures, or official names
- All Brazilian institution names are correctly spelled and titled
- All API endpoints and parameters cited are real and accessible

### Partial Marks (5–8)
- Minor name or spelling errors in institution names
- A few propositions listed with slightly wrong numbers

### Low Marks (1–4)
- Invented proposition numbers or spending figures
- Incorrect institution names

---

## Dimension 9: Reproducibility (Weight: 0.05)

### Full Marks (9–10)
- A `context_trace.json` shows exact API calls (endpoints + parameters)
- The analysis can be reproduced by re-running the download and prepare scripts with the same parameters
- Theme, year range, and any API token usage are documented

### Partial Marks (5–8)
- Context trace present but incomplete

### Low Marks (1–4)
- No context trace
- Analysis not reproducible from scripts

---

## Example: High-Quality Claim with Good Evidence (Fact)

```json
{
  "id": "claim-007",
  "type": "fact",
  "claim": "Between January 2022 and December 2024, 47 propositions tagged with the theme 'Saúde' (Health) were submitted to the Câmara dos Deputados, of which 12 were approved and 35 remain in tramitação.",
  "confidence": 0.91,
  "link_type": null,
  "evidence_ids": ["ev-camara-001", "ev-camara-002"],
  "source": "Câmara API /api/v2/proposicoes?tema=saude&dataInicio=2022-01-01&dataFim=2024-12-31"
}
```

Why this is high quality:
- Specific numbers derived from an API call
- API endpoint and parameters specified
- Confidence is high (0.91) because this is a direct count
- Claim is factual and does not imply causation

---

## Example: Low-Quality Claim

```json
{
  "id": "claim-012",
  "type": "fact",
  "claim": "Deputy João Silva used his position on the health committee to direct R$50 million in spending to his district.",
  "confidence": 0.8,
  "evidence_ids": []
}
```

Why this is low quality:
- No evidence citations
- Asserts causation ("used his position to direct") without documentary evidence
- This would be labeled `type: fact` but describes a causal relationship that would require direct evidence
- This type of claim, unsubstantiated, would trigger the –20 point misconduct-allegation penalty

---

## Correct Claim from the Same Facts

```json
{
  "id": "claim-012",
  "type": "interpretation",
  "claim": "Deputy João Silva authored 3 health propositions in 2023. In the same year, R$50 million in Emenda Parlamentar (individual parliamentary amendment) transfers were made to his home state of Minas Gerais for health programs. We classify this as a same_actor_link and same_time_window_link. Whether his amendments directly funded these transfers requires review of the specific emenda identifiers, which were not available in our dataset.",
  "confidence": 0.52,
  "link_type": "same_actor_link + same_time_window_link",
  "evidence_ids": ["ev-camara-003", "ev-transparencia-007"],
  "what_would_resolve_this": "Matching emenda parliamentary IDs from Câmara against emenda expenditure records in Portal da Transparência"
}
```

Why this is better:
- Presents the facts accurately
- Explicitly classifies the link type
- Does not allege causation
- Explains what data would be needed to resolve the question
- Lower confidence (0.52) reflects genuine uncertainty

---

## Automatic Penalties Summary

| Issue | Penalty |
|---|---|
| Asserting corruption/illegal conduct without authoritative source | –20 pts overall |
| Missing `fact-vs-inference` distinction in all claims | –15 pts on Fact vs Inference |
| Missing disclaimer about non-allegation of wrongdoing | –5 pts on Fact vs Inference |
| Only one data source used | –20 pts on Data Joining |
| Missing `what-could-not-be-verified` section | –10 pts on Uncertainty |
| Invented spending figures | –15 pts on Spending Summary |
| No context trace | –5 pts on Reproducibility |
