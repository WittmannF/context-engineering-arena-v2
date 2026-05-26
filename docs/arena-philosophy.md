# Arena Philosophy

## The Core Insight

The best LLM systems are not just better prompts. They are better context systems.

Most benchmark failures happen not because the model reasoned incorrectly, but because the context was assembled poorly: too much noise, too little signal, missing the one document that changes everything, or presenting evidence in a format the model cannot reason over efficiently.

This is the problem Context Engineering Arena is designed to measure.

## What We Mean by Context Engineering

Context engineering is the discipline of deciding *what information* to give a language model, *when*, *in what form*, and *how much of it* — in order to produce the most accurate, useful, and efficient output.

It includes:
- **Retrieval strategy** — BM25 keyword search, dense embeddings, hybrid retrieval, contextual retrieval
- **Compression** — summarization trees, truncation, distillation, token budgeting
- **Isolation** — identifying the most relevant document fragments rather than stuffing full documents
- **Synthesis** — combining evidence from multiple sources coherently
- **Citation management** — preserving provenance so claims can be verified
- **Memory architectures** — maintaining context across multiple LLM calls
- **Multi-agent orchestration** — routing different subtasks to different context pipelines
- **Uncertainty signaling** — explicitly representing what is known, what is inferred, and what is unknown

Simple prompt engineering asks: "what do I say to the model?" Context engineering asks: "what does the model need to know, and how do I get it there?"

## Why the Page Is the Final Artifact

Every submission must produce a *page* — not just a JSON answer, not just a score on a hidden benchmark.

This is a deliberate design choice.

A page can be inspected by a human. It can be trusted, questioned, refined, and used. It forces the participant to organize evidence into a format that is readable, citable, and falsifiable. A page that looks good but cannot be verified is penalized. A page that is dense with evidence but unreadable is penalized.

The page is also the right metaphor for the real-world use case: investigative journalism, civic accountability, technical due diligence, research synthesis, and knowledge management all require not just "the answer" but an *inspectable artifact* that shows its work.

## The Context X-Ray

Every submission must expose its context engineering decisions through a `context_trace.json` file. This file is rendered on the website as the **Context X-Ray** panel.

The Context X-Ray shows:
- How many documents were available vs. how many were actually read
- Which retrieval methods were used
- How many tokens were consumed
- What was deliberately ignored and why
- What failure modes the participant identified

This makes the invisible visible. Two submissions might produce similar final pages — but their Context X-Rays reveal radically different pipelines. One might use 5,000 tokens efficiently. Another might burn 150,000 tokens on noise. The arena rewards the former.

## Why This Differs From RAG Benchmarks

Standard RAG benchmarks measure retrieval accuracy (did the right document get retrieved?) and answer accuracy (was the final answer correct?) separately. They treat the pipeline as a black box and the output as a string to compare against a gold label.

This arena measures the entire transformation. The questions it asks are:
- Was the evidence well-selected?
- Are the claims grounded in verifiable sources?
- Was uncertainty handled correctly?
- Could a human inspect this page and trust it?
- Was the context budget used efficiently?
- Can the pipeline be reproduced?

There is no hidden gold label to match. There is a human-readable page to evaluate.

## What the Arena Rewards

The arena rewards the transformation from messy data to inspectable understanding. It rewards:

- **Evidence chains** — every non-trivial claim cites a real source
- **Uncertainty transparency** — weak signals and gaps are explicitly surfaced
- **Context efficiency** — high-quality output without excessive token waste
- **Retrieval precision** — finding the right documents, not all documents
- **Visual organization** — making the output readable for a non-specialist
- **Reproducibility** — the pipeline can be re-run

It penalizes fabricated evidence, unsupported confident claims, token-inefficient pipelines, and pages that are correct but unreadable.
