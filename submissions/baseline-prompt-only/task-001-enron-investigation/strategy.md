# Strategy Description — Baseline Prompt-Only (Task 001)

## What Was Done

This is the simplest possible approach to the Enron Investigation task. The strategy has exactly three steps:

1. **Load the processed dataset.** The prepare.py script was run on the full Enron archive, producing emails.jsonl with 517,401 records.

2. **Take 50 emails.** The first 50 records from emails.jsonl were selected — effectively a sequential sample based on file path ordering (which corresponds roughly to alphabetical user folder order). No targeted selection was made. No filtering was applied.

3. **Send one prompt.** All 50 emails were formatted as text and sent in a single prompt to claude-3-haiku-20240307, asking for a structured investigation brief in JSON format.

The total cost was approximately $0.004. Total latency was approximately 12 seconds.

## Why This Is Weak

The fundamental problem is representativeness. The Enron corpus has 517,401 emails from roughly 150 employees. Selecting 50 emails at random (or sequentially) means that:

- The probability of including any specific email is 0.0097%
- The probability of including any specific person's emails depends on their volume, but for most key figures (Fastow, Watkins, Skilling) it is below 5%
- The emails that do appear are overwhelmingly routine operational communications — pipeline logistics, IT support, travel requests, HR announcements — rather than the finance and executive communications most relevant to the investigation

In practice, the 50 emails selected gave a reasonable cross-section of communication *style* at Enron but almost no direct evidence of the financial misconduct. The LLM was forced to either (a) acknowledge uncertainty or (b) draw on its training data about Enron to produce plausible-sounding but unverifiable claims. The investigation brief likely contains a mix of both.

## What Was Learned

Despite the weak evidence, the 50-email sample revealed some genuinely useful structural patterns:

- Investor relations communications in October 2001 contain information hold directives that are unusual for routine quarterly updates
- Finance-to-treasury communications use oblique terminology ("the vehicle," "the arrangement") rather than naming the specific SPEs
- The gap between executive-facing and analyst-facing communication is visible even in a small sample

These patterns might have been found by anyone with access to the dataset. The real test of context engineering is whether the submission could find the *specific* emails that best evidence these patterns — which random sampling cannot do.

## What a Better Approach Would Look Like

A meaningful investigation of the Enron corpus requires targeted retrieval. The 8–12 most important email threads in the corpus (the Watkins memo and response, the Raptor closing coordination, the earnings messaging holds) need to be found and surfaced — not hoped for in a random sample.

A BM25 index over all 517,401 emails could be built in roughly 20 minutes on a standard laptop. Running queries like "LJM," "Raptor," "mark to market," "restatement," and "SEC inquiry" would retrieve a few thousand emails covering the most relevant signals. A dense embedding approach could additionally surface emails that use indirect language ("the structures") without naming the entities.

The Hybrid RAG baseline (submissions/baseline-hybrid-rag/task-001-enron-investigation/) implements this and scores 68/100 versus this baseline's 41/100 — a 65% improvement from the same underlying task.

The gap between 41/100 and 68/100 represents the value of targeted retrieval over random sampling. The gap between 68/100 and a potential 85/100+ represents the additional value of more sophisticated context engineering: temporal-stratified retrieval, entity-aware graph analysis, iterative investigation, and careful compression.

## Honest Assessment

This baseline is honest about its limitations. The context_trace.json explicitly states that 517,351 emails were not read, and the answer.json's limitation section clearly flags the LLM prior knowledge problem. A submission that made overconfident claims from 50 random emails without acknowledging the limitations would score lower on Uncertainty Handling — which is the one dimension where this baseline does reasonably well.

The key lesson: for large corpus investigation tasks, the most important design decision is *what to read*, not *what to ask the LLM*. Getting the context selection right is the entire challenge.
