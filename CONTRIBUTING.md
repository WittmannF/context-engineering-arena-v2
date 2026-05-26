# Contributing to Context Engineering Arena

Thank you for your interest in contributing. This guide explains how to submit strategies, propose tasks, improve the site, and contribute code.

## Ways to Contribute

- **Submit a strategy** — Apply a context engineering approach to an existing task and open a pull request.
- **Propose a new task** — Suggest a new benchmark task via a GitHub issue or a `tasks/proposals/` folder.
- **Improve the site** — Fix UI bugs, add visualizations, or improve the submission comparison experience in `packages/site/`.
- **Improve the CLI** — Add scoring features, new validation rules, or better reporting to `arena/arena_cli/`.
- **Fix bugs** — Open an issue or submit a fix for any bug in the CLI, site, or validation scripts.
- **Improve documentation** — Clarify guides, fix typos, or add examples to `docs/`.

---

## Submitting a Strategy

A strategy is a participant folder under `submissions/` containing your answer, context trace, and approach description.

### Step-by-step

1. **Fork and clone the repository.**

2. **Copy the baseline folder:**
   ```bash
   cp -r submissions/baseline-prompt-only submissions/<your-id>
   ```
   Your `<your-id>` must be lowercase, hyphen-separated, and unique (e.g., `acme-rag`, `my-team`).

3. **Edit `submissions/<your-id>/participant.yaml`:**
   ```yaml
   id: your-id
   display_name: "Your Display Name"
   type: community   # or team, bot
   website: "https://..."
   github: "your-github-handle"
   description: "A short description of your team or approach."
   contact: "you@example.com"
   ```

4. **Create a submission folder for your task:**
   ```bash
   mkdir submissions/<your-id>/task-001-enron-investigation
   ```

5. **Add the required files:**
   - `answer.json` — Your structured answer (see schemas/answer.schema.json and docs/submission-guide.md).
   - `context_trace.json` — How you processed the corpus (see schemas/context_trace.schema.json).
   - `strategy.md` — A human-readable description of your approach.

6. **Validate locally:**
   ```bash
   source arena/.venv/bin/activate
   python -m arena_cli.cli validate-submission --participant <your-id> --task task-001-enron-investigation
   ```
   Fix all errors before opening a PR.

7. **Build the catalog to test the site:**
   ```bash
   python -m arena_cli.cli build-catalog
   cd packages/site && npm run dev
   ```

8. **Open a pull request** against the `main` branch. Use the PR template and complete the submission checklist.

### What makes a strong submission?

- Every significant claim is backed by at least one `evidence_id` pointing to a real entry in your `evidence` array.
- Uncertainties are explicitly listed rather than papered over.
- Your `context_trace.json` accurately reflects what you actually did (tokens used, documents retrieved, methods applied).
- Your `strategy.md` is readable by someone unfamiliar with your stack.

---

## Proposing a Task

Good tasks have a publicly accessible corpus, a synthesis question that cannot be answered by a single search, and a clear set of required output sections.

### Via GitHub Issue

Open an issue using the **Propose a New Task** template. Include a title, the benchmark question, the dataset source, and why it is a context engineering challenge.

### Via tasks/proposals/ folder

For more detailed proposals, create a folder:
```bash
mkdir tasks/proposals/my-task-proposal
```

Add a `proposal.md` describing the task, dataset, benchmark question, required output sections, and known safety or ethics concerns. Open a pull request.

---

## Code Style

### Python

- Formatter and linter: `ruff` (configured in `arena/pyproject.toml`, line length 100).
- Run before committing: `ruff check arena/ && ruff format arena/`
- Type hints are required for all public functions.
- All new CLI commands must have a docstring used as the `--help` text.

### TypeScript / React

- Type check: `cd packages/site && npx tsc --noEmit`
- Follow existing component structure in `packages/site/src/`.
- Tailwind CSS for styling — do not add separate CSS files unless necessary.

---

## PR Checklist

Before opening a pull request, confirm:

- [ ] `python -m arena_cli.cli validate` passes with zero errors.
- [ ] For submissions: `python -m arena_cli.cli validate-submission` passes.
- [ ] `python -m arena_cli.cli build-catalog` completes without error.
- [ ] For site changes: `cd packages/site && npm run build` succeeds with no TypeScript errors.
- [ ] No raw or processed data files are included (`data/raw/`, `data/processed/` are gitignored).
- [ ] No API keys, tokens, or credentials appear anywhere in the diff.
- [ ] The PR description explains what changed and why.

---

## How Validation Works

Running `python -m arena_cli.cli validate` performs the following checks:

1. **Task validation** — Each `tasks/<task-id>/task.yaml` is parsed against the `Task` Pydantic model. Required fields, enum values, and nested objects are checked.
2. **Participant validation** — Each `submissions/<participant>/participant.yaml` is parsed against the `Participant` model.
3. **Submission validation** — Each `submissions/<participant>/<task-id>/` directory is checked for required files (`answer.json`, `context_trace.json`). If present, they are parsed against their schemas.
4. **Large data check** — The repository is scanned for files that look like raw data (`.csv`, `.jsonl`, `.parquet`, etc.) to catch accidental data commits.

Validation is also run automatically on every pull request via the GitHub Actions workflow at `.github/workflows/validate.yml`.

---

## How the Catalog is Generated

Running `python -m arena_cli.cli build-catalog` reads all task definitions and submission files, then writes JSON catalog files into `packages/site/src/data/generated/`. The site reads these files at build time to render task pages and submission comparisons. Always run `build-catalog` after adding or modifying tasks or submissions to keep the site in sync.

---

## Data Policy Summary

- Raw data is **never** committed to this repository.
- Each task provides a `download.py` script that fetches data on demand.
- Only tiny, legally-safe samples may live in `data/samples/`.
- Always check the dataset license before using data in a submission.

See [docs/data-policy.md](docs/data-policy.md) for the full policy.

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards. Report unacceptable behavior to the project maintainers.
