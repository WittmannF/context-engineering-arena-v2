# Context Engineering Arena

> Build the clearest page from the messiest context.

[![Validate](https://github.com/your-org/context-engineering-arena-v2/actions/workflows/validate.yml/badge.svg)](https://github.com/your-org/context-engineering-arena-v2/actions/workflows/validate.yml)

Context Engineering Arena is an open benchmark where developers compete to turn large, noisy, fragmented datasets into clear, evidence-backed web pages. Participants can use any context engineering strategy: prompt-only, long-context prompting, RAG, hybrid retrieval, reranking, LLM-generated wikis, memory files, multi-agent workflows, graph extraction, summarization trees, compression, or human-in-the-loop workflows.

The unit of competition is not just "the answer." It is the full transformation from messy context to useful, inspectable understanding.

## What is Context Engineering?

Context engineering is the practice of deciding what information a language model sees, when it sees it, how it is structured, and what gets left out. A model's output quality is constrained not just by its capabilities but by the quality of the context it receives. Context engineering covers retrieval (which documents to surface), compression (how to reduce noise without losing signal), isolation (which facts belong together), citation (which claims are backed by which sources), and synthesis (how to turn many partial signals into a coherent picture).

Context engineering is distinct from prompt engineering. While prompt engineering optimizes the instruction to the model, context engineering optimizes the information environment around it. The two are complementary, but the biggest unsolved problems in applied LLMs — hallucination, inconsistency, irrelevant retrievals, missed connections between distant documents — are primarily context problems, not prompt problems.

## Why Does This Benchmark Exist?

Most LLM benchmarks evaluate a single question-answer pair or a short generation. They do not evaluate the pipeline that produced the answer, the evidence behind it, or whether a human could inspect and trust it. This matters because real-world tasks — investigative research, financial analysis, compliance review, scientific synthesis — require not just a good answer but a defensible, traceable, inspectable process.

Context Engineering Arena fills that gap. Each task provides a large, messy, real-world corpus and asks participants to produce a structured web page that is simultaneously accurate, evidence-backed, uncertainty-aware, and readable. Participants must show their work: which documents they used, which they ignored and why, what retrieval or compression strategy they applied, and what they could not determine. The arena rewards systems that make invisible decisions visible.

## How It Works

1. A task defines a real-world corpus, a benchmark question, and a required output schema.
2. Participants submit structured answers with evidence citations, context traces, and strategy notes.
3. Each submission becomes a page on the public website.
4. Visitors can compare submissions, inspect strategies, and see which one transforms the messy corpus most clearly.
5. The arena rewards evidence quality, uncertainty handling, context efficiency, and useful visual organization.

## Quickstart

```bash
git clone https://github.com/your-org/context-engineering-arena-v2
cd context-engineering-arena-v2
./scripts/bootstrap.sh
python -m arena_cli.cli validate
python -m arena_cli.cli build-catalog
cd packages/site
npm run dev
```

## Download Sample Data

```bash
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

## Submit a Strategy

```bash
cp -r submissions/baseline-prompt-only submissions/my-team
# Edit participant.yaml, answer.json, context_trace.json, strategy.md
python -m arena_cli.cli validate-submission --participant my-team --task task-001-enron-investigation
python -m arena_cli.cli build-catalog
# Open a pull request
```

## Kickstart Tasks

| ID | Title | Domain | Dataset |
|----|-------|--------|---------|
| task-001-enron-investigation | The Enron Investigation Brief | Corporate Investigation | Enron Email Dataset (CMU) |
| task-002-brazil-public-money-trail | Brazil Public Money Trail | Public Accountability | Câmara dos Deputados + Portal da Transparência |
| task-003-open-source-ecosystem-radar | Open Source Ecosystem Radar | Open Source | GH Archive |

## Repository Structure

```
context-engineering-arena-v2/
├── arena/                    # Python CLI and scoring tools
│   └── arena_cli/           # CLI package (validate, build-catalog, etc.)
├── packages/
│   └── site/                # React/Vite static website
├── tasks/                   # Task definitions and data scripts
│   ├── task-001-enron-investigation/
│   ├── task-002-brazil-public-money-trail/
│   ├── task-003-open-source-ecosystem-radar/
│   └── proposals/           # Community task proposals
├── submissions/             # Participant submissions
│   ├── baseline-prompt-only/
│   └── baseline-hybrid-rag/
├── schemas/                 # JSON schemas for all data types
├── data/                    # Downloaded/processed data (gitignored except samples)
├── docs/                    # Project documentation
└── scripts/                 # Utility scripts
```

## Scoring

Submissions are scored across six dimensions:

- **Answer Quality** — Is the conclusion accurate and well-organized?
- **Evidence Quality** — Are claims backed by real evidence with citations?
- **Context Efficiency** — Was context used efficiently (tokens, retrieval precision)?
- **Uncertainty Handling** — Are unknowns, contradictions, and weak signals clearly marked?
- **Visual Clarity** — Is the output page readable and useful for a human?
- **Reproducibility** — Can the submission be re-run with the same results?

See [docs/scoring-guide.md](docs/scoring-guide.md) for details.

## Data Policy

Raw datasets are never committed to this repository. Each task includes download scripts and data manifests. See [docs/data-policy.md](docs/data-policy.md).

## Ethics and Safety

This benchmark processes real-world data about real individuals and institutions. Submissions must clearly distinguish evidence from inference, avoid defamatory claims, and include a limitations section. See [docs/ethics-and-safety.md](docs/ethics-and-safety.md).

## Roadmap

- [ ] Automatic scoring with LLM judge
- [ ] Hallucination detection metrics
- [ ] More tasks: SEC filings, scientific papers, legal documents
- [ ] Web UI for submission comparison
- [ ] Discord/community integration
- [ ] API for programmatic submission

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit strategies, propose tasks, and contribute code.

## License

MIT — see [LICENSE](LICENSE).
