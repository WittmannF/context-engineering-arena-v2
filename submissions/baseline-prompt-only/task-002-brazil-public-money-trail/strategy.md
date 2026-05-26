# Strategy Description — Baseline Prompt-Only (Task 002)

## What Was Done

This baseline for the Brazil Public Money Trail task used the simplest possible approach:

1. **Câmara API**: Called the Câmara dos Deputados Dados Abertos API with the keyword "saude" and date range 2022–2024. Retrieved 2 pages of results (200 propositions total). No authentication required.

2. **Portal da Transparência**: Skipped entirely. The `TRANSPARENCIA_API_TOKEN` environment variable was not set, and the task was run in sample mode. Instead of fabricating spending data, the submission explicitly acknowledges that spending analysis is absent and marks all spending-related claims as `uncertainty`.

3. **LLM call**: All 200 retrieved propositions were formatted as text and sent in a single prompt to claude-3-haiku-20240307. The prompt instructed the model to classify all links as `same_theme_link` and to avoid claiming causation. The model was explicitly told not to present spending figures as facts since the Portal da Transparência was unavailable.

Total API calls: 2 (Câmara). Total LLM calls: 1. Total cost: ~$0.003.

## Why the Score is Better Than Task 001

Task 002 scores higher (~55/100) than Task 001 (~41/100) for this baseline for a specific reason: the task structure rewards honest uncertainty handling, and this baseline is genuinely honest about what it cannot do.

In Task 001, the LLM was tempted to draw on its training data about Enron to fill gaps. In Task 002, the missing data (spending) is clearly defined and the LLM was explicitly told not to invent spending figures. As a result, the Fact vs Inference dimension scores reasonably well (~78/100) because all links are correctly classified and the absence of spending data is prominently flagged.

## Where the Score Hurts

The data joining score is near-zero (~15/100). The task explicitly requires joining at least two data sources, and this submission only has Câmara data. No spending data means no money trail — which is the entire point of the task.

A submission that gets a Portal da Transparência token and retrieves real spending data would improve from ~55/100 to ~65-70/100 with the same approach. The additional improvement from sophisticated cross-dataset entity resolution and emenda matching could take it to 80-85/100.

## What the Submission Does Well

1. **Honest uncertainty**: Every spending-related claim is labeled `uncertainty`. There is no attempt to invent figures or imply spending facts from general knowledge.

2. **Link classification**: All candidate links between legislative and spending data are explicitly classified as `same_theme_link` because the cross-dataset connection cannot be verified. The submission never uses `direct_documented_link` without evidence.

3. **Disclaimer**: The submission includes a prominent disclaimer stating that no wrongdoing is alleged and that correlation is not causation.

4. **Actionable recommendations**: The `recommended-next-investigations` section provides specific, achievable follow-up steps (get the API token, match emenda IDs, check TCU records).

## The Farmácia Popular Finding

The most interesting finding from the Câmara data alone is the Farmácia Popular expansion via MP 1234/2024. This is a Medida Provisória — an executive decree with immediate legal force — that was converted to law by the Câmara. Unlike most legislation, Medidas Provisórias with direct spending implications create relatively traceable policy-to-spending links because they are tied to specific budget program codes.

If Portal da Transparência data were available, the hypothesis would be: "The Farmácia Popular ação orçamentária should show increased spending in 2024 Q2-Q4, following the MP's conversion to lei in Q2 2024." This would be testable as a potential `direct_documented_link` if the budget program code matches.

## Key Lesson

The most important infrastructure investment for this task is the Portal da Transparência API token. Without it, the entire spending side of the analysis is absent. The token is free and takes minutes to obtain. In any real submission, getting the token before starting analysis is essential.

The Câmara API alone can produce a reasonable legislative timeline and authorship analysis, but it cannot produce the task's central deliverable: the money trail.
