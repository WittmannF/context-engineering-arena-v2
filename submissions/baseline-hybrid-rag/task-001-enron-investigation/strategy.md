# Strategy Description — Hybrid RAG Baseline (Task 001)

## What Was Done

The Hybrid RAG baseline improves on the prompt-only approach by using targeted retrieval to find the most relevant emails from the corpus before synthesis.

**Step 1: BM25 Indexing**
Built a BM25 index (rank_bm25 library) over a 10,000-email sample from the processed emails.jsonl. The 10K sample was selected randomly from the full 517,401-email corpus. Index build time: approximately 45 seconds on a MacBook Pro M2.

**Step 2: Dense Embedding Indexing**
Generated dense embeddings for all 10,000 emails using OpenAI's text-embedding-3-small model (1536 dimensions, $0.00002/1K tokens). Stored in a FAISS flat index (exact nearest neighbor search). Total embedding cost: ~$0.08. Embedding generation time: ~12 minutes.

**Step 3: Targeted Retrieval Queries**
Ran 8 targeted queries representing the key investigation themes. For each query:
- BM25 retrieval: returned top-50 keyword-matched emails
- Dense retrieval: returned top-50 semantically similar emails
- Combined using Reciprocal Rank Fusion (RRF) for hybrid results

Total retrieved: ~850 unique emails across all queries (after deduplication).

**Step 4: Reranking and Selection**
Sorted all 850 retrieved emails by their maximum relevance score across all queries. Selected the top 150 for inclusion in the synthesis prompt.

**Step 5: Synthesis**
Fed all 150 emails to claude-3-sonnet-20240229 with a structured investigation prompt. Input: ~95,000 tokens. Output: ~5,800 tokens. Cost: ~$0.22. Latency: ~45 seconds.

Total infrastructure cost: ~$0.31 (BM25 free, embeddings $0.08, synthesis $0.22, overhead $0.01).

## What Worked

**Targeted retrieval found key documents.** The most significant difference from the prompt-only baseline is that targeted queries found documents that random sampling would almost never have found:
- The Raptor negative credit capacity email (ev-rag-003) would be found by "Raptor hedge vehicle accounting" with probability ~0% in random sampling but was retrieved in rank 1 from the BM25 query.
- The Watkins memo fragment in Lay's inbox was retrieved via "whistleblower Sherron Watkins memo" — a direct BM25 hit.
- The California energy strategy memo was found via "California energy crisis manipulation."

**The Hybrid approach outperformed BM25-only.** Several important emails used oblique language ("the vehicles," "the arrangement") that BM25 keyword matching would miss but dense retrieval captured because the surrounding context was semantically relevant.

**Evidence quality improved dramatically.** The prompt-only baseline had evidence items that were clearly constructed from LLM prior knowledge. The Hybrid RAG baseline has evidence items with specific file paths, specific retrieval ranks, and specific retrieval queries — they are traceable to the actual corpus.

## What Didn't Work as Well

**10K sample ceiling.** The dense embedding index only covered 10,000 of 517,401 emails. Several potentially important documents (board approval communications, Arthur Andersen partner emails, early 1999-2000 Chewco/JEDI communications) may not have been in the 10K sample. BM25 indexing of the full 517K corpus would have been better, but embedding costs for the full corpus would have been ~$10 vs $0.08 for 10K.

**Query design requires prior knowledge.** The 8 queries were designed based on what we already knew about the Enron fraud from public sources. This works for the known major themes but cannot surface unknown patterns. The BM25 query "Andy Fastow LJM partnership off balance sheet" presupposes that these are the right search terms.

**No temporal stratification.** The 10K sample was randomly selected without regard to time period. Important early communications (1998-1999 SPE formation period) may be underrepresented if the archive has more recent emails due to email retention practices.

**Context length limit.** 150 emails (~95K tokens) approaches the limit of what claude-3-sonnet can process in a single prompt. A longer context or a multi-pass approach could include more evidence.

## Comparison to Prompt-Only

| Metric | Prompt-Only | Hybrid RAG | Improvement |
|---|---|---|---|
| Documents used | 50 (random) | 150 (targeted) | 3x more, better targeted |
| Evidence quality score | 22 | 75 | +241% |
| Timeline quality score | 35 | 72 | +106% |
| Overall score | 41 | 68 | +66% |
| Cost | $0.004 | $0.31 | 78x higher |

The 66% overall score improvement comes primarily from evidence quality (random → targeted retrieval) and timeline quality (external knowledge → corpus-derived dates). The cost is 78x higher, but at $0.31 this is still very cheap for the amount of analytical work produced.

## Key Lesson for Participants

The most important lesson from this comparison: **what you read matters more than how you read it.** The Hybrid RAG baseline is not a more sophisticated reasoner than the prompt-only — it uses the same LLM architecture. The improvement comes entirely from reading 150 relevant emails instead of 50 random ones.

For investigators designing better strategies, the first question to ask is always: "What should I read?" Before writing any prompts, spend the effort designing a retrieval strategy that surfaces the emails most relevant to the investigation question.

The gap between this 68/100 and a potential 85+/100 score lies in:
1. Full corpus indexing (not just 10K sample)
2. Temporal stratification of the retrieval pool
3. Entity-graph extraction to surface coordination patterns
4. Iterative investigation (using findings from one pass to guide the next)
