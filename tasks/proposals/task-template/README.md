# Task XXX: Your Task Title

<!-- Replace all placeholder text below. Every section is required. -->

## What This Task Is

<!-- Describe the task in 2-3 paragraphs. What is the corpus? What is the benchmark question?
     What kind of analysis is required? Why is this interesting? -->

The benchmark question is:

> [Your benchmark question here]

## Why This Task Is Interesting

<!-- Explain why this task requires context engineering specifically. Why can't you just
     read all the documents? Why can't you just ask the LLM without retrieval?
     What makes the corpus challenging (size, heterogeneity, noise, etc.)? -->

## The Dataset

**Name:** [Dataset name]
**Source:** [URL]
**License:** [License]
**Size:** [Approximate size]
**Access:** [How to access it]

[Description of the dataset's structure and content.]

## How to Download

```bash
python tasks/task-XXX-your-task-id/scripts/download.py
python tasks/task-XXX-your-task-id/scripts/download.py --sample-only
```

## How to Prepare the Data

```bash
python tasks/task-XXX-your-task-id/scripts/prepare.py
```

[Describe what the prepare script produces and the schema of the output files.]

## The Benchmark Question

> [Your benchmark question repeated here]

[Explain the four or five dimensions of the question. What does a complete answer look like?]

## What a Good Submission Looks Like

[Describe a strong submission: what it contains, what evidence it uses, how it handles uncertainty.]

[Describe a weak submission: what common failure modes look like.]

## Scoring Notes

See `rubric.md` for the full scoring rubric.

| Dimension | Weight | What Matters |
|---|---|---|
| [Dimension 1] | [Weight] | [Description] |
| [Dimension 2] | [Weight] | [Description] |

## Ethics Notes

<!-- Are there privacy, legal, or safety concerns with this dataset or task?
     What should participants be careful about? -->

## Files in This Task

```
tasks/task-XXX-your-task-id/
  task.yaml
  README.md
  rubric.md
  data_manifest.yaml
  expected_answer_schema.json
  scripts/
    download.py
    prepare.py
    sample.py
  starter/
    README.md
    baseline_prompt_only.md
    baseline_strategy.py
```
