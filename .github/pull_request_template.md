## Summary

<!-- Describe what this PR adds or changes -->

## Type of Change

- [ ] New submission (strategy for an existing task)
- [ ] New task proposal
- [ ] Bug fix
- [ ] Site improvement
- [ ] CLI improvement
- [ ] Documentation update

## Submission Checklist (for strategy submissions only)

- [ ] Validated locally: `python -m arena_cli.cli validate-submission --participant <id> --task <task-id>`
- [ ] `answer.json` is present and valid JSON
- [ ] `context_trace.json` is present and valid JSON
- [ ] `strategy.md` is present with a meaningful description of the approach
- [ ] Every major claim has at least one `evidence_id` pointing to a real entry in `evidence`
- [ ] No raw datasets committed — `data/raw/` and `data/processed/` are gitignored
- [ ] Known limitations documented in `answer.json` → `limitations`
- [ ] Unsupported claims marked with `claim_type: "uncertainty"` or `confidence: "low"`
- [ ] `participant.yaml` present with `id` matching the folder name

## Notes for Reviewers

<!-- Anything specific you want reviewers to check -->
