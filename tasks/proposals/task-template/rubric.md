# Scoring Rubric — Task XXX: Your Task Title

Each dimension is scored 0–10. The overall score is a weighted average.

<!-- Replace all placeholder dimensions with real ones for your task.
     Weights must sum to 1.0. -->

---

## Dimension 1: [Name] (Weight: 0.XX)

[Describe what this dimension measures.]

### Full Marks (9–10)
- [Specific criteria for full marks]

### Partial Marks (5–8)
- [Criteria for partial marks]

### Low Marks (1–4)
- [Criteria for low marks]

### Zero (0)
- [When to give zero]

---

## Dimension 2: [Name] (Weight: 0.XX)

[Continue for all dimensions...]

---

## Example: High-Quality Claim with Good Evidence

```json
{
  "id": "claim-001",
  "type": "fact | interpretation | uncertainty",
  "claim": "...",
  "confidence": 0.0,
  "evidence_ids": ["ev-001"]
}
```

[Explain why this is high quality]

---

## Example: Low-Quality Claim

```json
{
  "id": "claim-001",
  "claim": "Vague claim with no evidence",
  "type": "fact",
  "confidence": 0.95
}
```

[Explain what's wrong with this]

---

## Automatic Metrics

| Metric | Description |
|---|---|
| [metric_name] | [Description] |

---

## Automatic Penalties

| Issue | Penalty |
|---|---|
| [Issue] | [Penalty] |
