"""Pydantic v2 models for the Context Engineering Arena data model."""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Task models
# ---------------------------------------------------------------------------


class DatasetInfo(BaseModel):
    name: str = Field(..., description="Dataset name")
    version: Optional[str] = Field(None, description="Dataset version or release tag")
    url: Optional[str] = Field(None, description="Canonical URL for the dataset")
    license: Optional[str] = Field(None, description="License identifier, e.g. CC-BY-4.0")
    size_bytes: Optional[int] = Field(None, description="Approximate size in bytes")
    num_records: Optional[int] = Field(None, description="Number of records / rows")
    description: Optional[str] = Field(None, description="Short description of the dataset")


class TaskOutputs(BaseModel):
    format: Literal["json", "markdown", "text", "yaml"] = Field(
        "json", description="Expected output format"
    )
    schema_file: Optional[str] = Field(
        None, description="Path relative to task folder for JSON schema"
    )
    max_length_words: Optional[int] = Field(
        None, description="Soft limit on output length in words"
    )
    required_sections: list[str] = Field(
        default_factory=list,
        description="Section titles that must appear in the output",
    )


class TaskScoring(BaseModel):
    method: Literal["manual", "automated", "hybrid"] = Field(
        "manual", description="Primary scoring method"
    )
    rubric_file: str = Field("rubric.md", description="Path to rubric file relative to task folder")
    max_score: int = Field(100, description="Maximum achievable score")
    dimensions: list[str] = Field(
        default_factory=list,
        description="Scoring dimension names, e.g. accuracy, completeness, clarity",
    )
    automated_checks: list[str] = Field(
        default_factory=list,
        description="Automated checks that supplement manual scoring",
    )


class TaskSafety(BaseModel):
    sensitive_data: bool = Field(False, description="Whether the task involves sensitive data")
    pii_present: bool = Field(False, description="Whether PII is present in the dataset")
    ethical_review_required: bool = Field(False, description="Whether ethics board review is needed")
    notes: Optional[str] = Field(None, description="Free-form safety / ethics notes")


class Task(BaseModel):
    id: str = Field(..., description="Unique task identifier, must match folder name")
    title: str = Field(..., description="Human-readable task title")
    short_description: str = Field(..., description="One-sentence task summary")
    long_description: str = Field(..., description="Full task description in Markdown")
    benchmark_question: str = Field(
        ..., description="The exact question participants must answer"
    )
    domain: str = Field(..., description="Domain, e.g. biomedical, legal, financial, geospatial")
    difficulty: Literal["easy", "medium", "hard", "expert"] = Field(
        ..., description="Difficulty level"
    )
    tags: list[str] = Field(default_factory=list, description="Free-form tags")
    dataset: Optional[DatasetInfo] = Field(None, description="Primary dataset information")
    outputs: TaskOutputs = Field(default_factory=TaskOutputs, description="Output specification")
    scoring: TaskScoring = Field(default_factory=TaskScoring, description="Scoring configuration")
    safety: TaskSafety = Field(default_factory=TaskSafety, description="Safety flags")
    created_at: Optional[dt.date] = Field(None, description="Task creation date")
    updated_at: Optional[dt.date] = Field(None, description="Last update date")


# ---------------------------------------------------------------------------
# Data manifest models
# ---------------------------------------------------------------------------


class DataSource(BaseModel):
    model_config = {"extra": "allow"}

    name: str = Field(..., description="Human-readable source name")
    url: str = Field(..., description="Download URL or repository URL")
    license: Optional[str] = None
    access_method: Optional[str] = Field(None, description="How the data is obtained")
    expected_size: Optional[str] = None
    requires_token: bool = Field(False)
    token_env_var: Optional[str] = None
    download_script: Optional[str] = None
    sample_available: bool = Field(False)
    checksum: Optional[str] = None
    notes: Optional[str] = None


class DataManifest(BaseModel):
    task_id: str = Field(..., description="Task this manifest belongs to")
    sources: list[DataSource] = Field(default_factory=list, description="List of data sources")
    preparation_steps: list[str] = Field(
        default_factory=list,
        description="Ordered list of preparation steps",
    )
    ethics_notes: Optional[Any] = Field(None, description="Ethics and data-use notes")
    sample_mode_description: Optional[str] = Field(
        None, description="Describes what the sample mode provides"
    )
    output_files: list[str] = Field(
        default_factory=list,
        description="Files produced by prepare.py, relative to data/processed/",
    )


# ---------------------------------------------------------------------------
# Participant model
# ---------------------------------------------------------------------------


class Participant(BaseModel):
    model_config = {"extra": "allow"}

    id: str = Field(..., description="Unique participant identifier, must match folder name")
    display_name: str = Field(..., description="Human-readable team or system name")
    type: Optional[str] = Field(None, description="Participant type")
    website: Optional[str] = None
    github: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    affiliation: Optional[str] = None


# ---------------------------------------------------------------------------
# Answer / submission models
# ---------------------------------------------------------------------------


class Claim(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = Field(None, description="Unique claim ID")
    claim: Optional[str] = Field(None, description="The claim statement")
    claim_type: Optional[str] = Field(None, description="Type of claim")
    confidence: Optional[Any] = Field(None, description="Confidence level")
    evidence_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class Evidence(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = Field(None, description="Unique evidence ID")
    source_type: Optional[str] = Field(None, description="Type of evidence source")
    source_id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[Any] = None
    excerpt: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TimelineItem(BaseModel):
    model_config = {"extra": "allow"}

    date: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    evidence_ids: list[str] = Field(default_factory=list)
    significance: Optional[str] = None


class Entity(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    evidence_ids: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)


class Risk(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = None
    title: Optional[str] = None
    severity: Optional[str] = None
    likelihood: Optional[str] = None
    description: Optional[str] = None
    evidence_ids: list[str] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)


class Uncertainty(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = None
    description: Optional[str] = None
    why_it_matters: Optional[str] = None
    missing_evidence: Optional[str] = None


class Recommendation(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[str] = None
    description: Optional[str] = None
    rationale: Optional[str] = None
    evidence_ids: list[str] = Field(default_factory=list)
    timeframe: Optional[str] = None


class AnswerSection(BaseModel):
    id: str = Field(..., description="Unique section ID, e.g. S001")
    title: str = Field(..., description="Section title")
    type: Literal[
        "narrative", "table", "list", "chart_data", "comparison", "methodology", "appendix"
    ] = Field("narrative", description="Section type")
    content: Optional[str] = Field(None, description="Prose content of the section")
    items: list[Any] = Field(
        default_factory=list,
        description="Structured items (rows, list entries, etc.) for non-narrative sections",
    )
    claim_ids: list[str] = Field(
        default_factory=list, description="Claim IDs referenced in this section"
    )


class Answer(BaseModel):
    task_id: str = Field(..., description="ID of the task this answer addresses")
    participant_id: str = Field(..., description="ID of the participant who submitted")
    title: str = Field(..., description="Answer title")
    executive_summary: str = Field(
        ..., description="Short summary (2-5 sentences) of key findings"
    )
    sections: list[AnswerSection] = Field(
        default_factory=list, description="Main body sections"
    )
    claims: list[Claim] = Field(default_factory=list, description="All claims made")
    evidence: list[Evidence] = Field(default_factory=list, description="All evidence items")
    timeline: list[TimelineItem] = Field(
        default_factory=list, description="Chronological timeline of events"
    )
    entities: list[Entity] = Field(
        default_factory=list, description="Key entities mentioned in the answer"
    )
    risks: list[Risk] = Field(default_factory=list, description="Identified risks")
    uncertainties: list[Uncertainty] = Field(
        default_factory=list, description="Known uncertainties"
    )
    recommendations: list[Recommendation] = Field(
        default_factory=list, description="Actionable recommendations"
    )
    limitations: Optional[Any] = Field(
        None, description="Known limitations of this answer (string or list)"
    )
    submitted_at: Optional[Any] = Field(None, description="Submission timestamp")


# ---------------------------------------------------------------------------
# Context trace models
# ---------------------------------------------------------------------------


class ContextMethods(BaseModel):
    prompt_only: bool = Field(False, description="No retrieval — pure prompt with model knowledge")
    long_context: bool = Field(False, description="Entire corpus placed in context window")
    rag: bool = Field(False, description="Retrieval-augmented generation")
    hybrid_retrieval: bool = Field(False, description="Combination of multiple retrieval methods")
    bm25: bool = Field(False, description="BM25 keyword search")
    dense_embeddings: bool = Field(False, description="Dense vector / embedding search")
    reranking: bool = Field(False, description="Re-ranking step applied after initial retrieval")
    contextual_retrieval: bool = Field(False, description="Contextual retrieval (chunk-level context injection)")
    memory: bool = Field(False, description="Persistent memory mechanism used")
    llm_generated_wiki: bool = Field(False, description="LLM-generated knowledge base / wiki used")
    multi_agent: bool = Field(False, description="Multiple agents used")
    summarization: bool = Field(False, description="Summarization applied to reduce context size")
    compression: bool = Field(False, description="Prompt compression applied")
    graph_extraction: bool = Field(False, description="Knowledge graph extraction used")
    human_in_the_loop: bool = Field(False, description="Human guidance incorporated during processing")


class ModelInfo(BaseModel):
    provider: str = Field(..., description="Model provider, e.g. openai, anthropic, google")
    model: str = Field(..., description="Model name / version, e.g. gpt-4o, claude-3-5-sonnet")
    purpose: str = Field(
        ...,
        description="Role of this model, e.g. embedding, retrieval, generation, reranking",
    )
    context_window: Optional[int] = Field(None, description="Context window in tokens")
    temperature: Optional[float] = Field(None, description="Temperature used")


class ContextStats(BaseModel):
    total_tokens_in_context: Optional[int] = Field(
        None, description="Total tokens in the final context window"
    )
    tokens_from_retrieval: Optional[int] = Field(
        None, description="Tokens contributed by retrieved chunks"
    )
    tokens_from_compression: Optional[int] = Field(
        None, description="Tokens after compression, if applied"
    )
    num_documents_retrieved: Optional[int] = Field(
        None, description="Total documents / chunks retrieved"
    )
    num_documents_used: Optional[int] = Field(
        None, description="Documents / chunks actually placed in context"
    )
    num_retrieval_rounds: Optional[int] = Field(
        None, description="Number of retrieval iterations"
    )
    num_llm_calls: Optional[int] = Field(None, description="Total LLM API calls made")
    wall_time_seconds: Optional[float] = Field(
        None, description="Total wall-clock time in seconds"
    )
    total_cost_usd: Optional[float] = Field(
        None, description="Estimated total cost in USD"
    )
    compression_ratio: Optional[float] = Field(
        None, description="Ratio of tokens before / after compression"
    )


class RetrievalStep(BaseModel):
    step_index: int = Field(..., description="0-based step index")
    query: str = Field(..., description="Query used for retrieval")
    method: str = Field(..., description="Retrieval method used, e.g. bm25, dense, hybrid")
    num_results: int = Field(..., description="Number of results returned")
    top_scores: list[float] = Field(
        default_factory=list, description="Relevance scores for top results"
    )
    sources_used: list[str] = Field(
        default_factory=list, description="Source identifiers retrieved"
    )
    notes: Optional[str] = Field(None, description="Notes about this retrieval step")


class CompressionStep(BaseModel):
    step_index: int = Field(..., description="0-based step index")
    method: str = Field(..., description="Compression method, e.g. selective_summarization, reranking_cutoff")
    tokens_before: int = Field(..., description="Token count before compression")
    tokens_after: int = Field(..., description="Token count after compression")
    notes: Optional[str] = Field(None, description="Notes about this compression step")


class IgnoredItem(BaseModel):
    source_id: str = Field(..., description="Source that was retrieved but not used")
    reason: str = Field(..., description="Why this source was ignored")


class ContextTrace(BaseModel):
    task_id: str = Field(..., description="Task ID this trace belongs to")
    participant_id: str = Field(..., description="Participant ID this trace belongs to")
    methods: ContextMethods = Field(
        default_factory=ContextMethods, description="Methods employed"
    )
    models: list[ModelInfo] = Field(default_factory=list, description="Models used")
    stats: ContextStats = Field(default_factory=ContextStats, description="Aggregate statistics")
    retrieval_steps: list[RetrievalStep] = Field(
        default_factory=list, description="Ordered retrieval steps"
    )
    compression_steps: list[CompressionStep] = Field(
        default_factory=list, description="Ordered compression steps"
    )
    ignored_items: list[IgnoredItem] = Field(
        default_factory=list, description="Items retrieved but not used"
    )
    final_context_description: Optional[str] = Field(
        None, description="Prose description of what ended up in context"
    )
    implementation_notes: Optional[str] = Field(
        None, description="Implementation details, frameworks, and libraries used"
    )
    reproducibility_notes: Optional[str] = Field(
        None, description="Instructions to reproduce this trace"
    )


# ---------------------------------------------------------------------------
# Score models
# ---------------------------------------------------------------------------


class ScoreBreakdown(BaseModel):
    dimension: str = Field(..., description="Scoring dimension name")
    score: float = Field(..., description="Score for this dimension")
    max_score: float = Field(..., description="Maximum possible score for this dimension")
    rationale: Optional[str] = Field(None, description="Explanation of score awarded")


class Score(BaseModel):
    task_id: str = Field(..., description="Task ID")
    participant_id: str = Field(..., description="Participant ID")
    overall_score: float = Field(..., description="Overall score (0–100)")
    scores: list[ScoreBreakdown] = Field(
        default_factory=list, description="Per-dimension score breakdown"
    )
    notes: Optional[str] = Field(None, description="General scoring notes")
    scored_by: Optional[str] = Field(None, description="Judge or scorer identifier")
    scored_at: Optional[dt.datetime] = Field(None, description="When scoring was performed")
    version: str = Field("1.0", description="Scoring rubric version")


# ---------------------------------------------------------------------------
# Catalog / site data models
# ---------------------------------------------------------------------------


class TaskCatalogEntry(BaseModel):
    id: str
    title: str
    short_description: str
    domain: str
    difficulty: str
    tags: list[str]
    has_sample: bool = False
    num_submissions: int = 0
    top_score: Optional[float] = None


class SubmissionCatalogEntry(BaseModel):
    task_id: str
    participant_id: str
    participant_display_name: str
    participant_type: str
    methods: dict[str, bool] = Field(default_factory=dict)
    overall_score: Optional[float] = None
    rank: Optional[int] = None
    submitted_at: Optional[str] = None
    context_stats: dict[str, Any] = Field(default_factory=dict)


class LeaderboardEntry(BaseModel):
    task_id: str
    task_title: str
    domain: str
    difficulty: str
    rankings: list[SubmissionCatalogEntry] = Field(default_factory=list)
