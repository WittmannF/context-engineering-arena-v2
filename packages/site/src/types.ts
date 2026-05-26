// ─── Dataset ──────────────────────────────────────────────────────────────────

export interface Dataset {
  name: string
  source_url?: string
  license?: string
  access_method?: string
  expected_size?: string
  sample_available?: boolean
}

// ─── Task ─────────────────────────────────────────────────────────────────────

export interface Task {
  id: string
  title: string
  short_description: string
  long_description?: string
  benchmark_question?: string
  domain: string
  difficulty: 'easy' | 'medium' | 'hard' | 'expert'
  tags: string[]
  dataset?: Dataset
  outputs?: Record<string, unknown>
  scoring?: Record<string, unknown>
  safety?: Record<string, unknown>
  submission_count?: number
  best_score?: number
  // catalog fields from build_catalog.py
  has_sample?: boolean
  num_submissions?: number
  top_score?: number | null
}

// ─── Evidence ─────────────────────────────────────────────────────────────────

export interface Evidence {
  id: string
  source_type?: string
  title?: string
  date?: string
  excerpt?: string
  source_id?: string
  url?: string
  metadata?: Record<string, unknown>
  [key: string]: unknown
}

// ─── Claim ────────────────────────────────────────────────────────────────────

export type ClaimType = 'fact' | 'interpretation' | 'recommendation' | 'uncertainty' | string
export type ConfidenceLevel = 'high' | 'medium' | 'low' | number | string

export interface Claim {
  id?: string
  claim?: string
  text?: string
  claim_type?: ClaimType
  type?: string
  confidence?: ConfidenceLevel
  evidence_ids?: string[]
  notes?: string
  [key: string]: unknown
}

// ─── Timeline ─────────────────────────────────────────────────────────────────

export interface TimelineItem {
  date?: string
  title?: string
  description?: string
  evidence_ids?: string[]
  significance?: string
  [key: string]: unknown
}

// ─── Entity ───────────────────────────────────────────────────────────────────

export interface Entity {
  id?: string
  name?: string
  type?: string
  description?: string
  evidence_ids?: string[]
  aliases?: string[]
  [key: string]: unknown
}

// ─── Risk ─────────────────────────────────────────────────────────────────────

export interface Risk {
  id?: string
  title?: string
  description?: string
  severity?: string
  likelihood?: string
  evidence_ids?: string[]
  [key: string]: unknown
}

// ─── Uncertainty ──────────────────────────────────────────────────────────────

export interface Uncertainty {
  id?: string
  description?: string
  why_it_matters?: string
  missing_evidence?: string
  impact?: string
  resolution_path?: string
  [key: string]: unknown
}

// ─── Recommendation ───────────────────────────────────────────────────────────

export interface Recommendation {
  id?: string
  title?: string
  text?: string
  priority?: string
  evidence_ids?: string[]
  description?: string
  rationale?: string
  [key: string]: unknown
}

// ─── Answer ───────────────────────────────────────────────────────────────────

export interface AnswerSection {
  id?: string
  title?: string
  content?: string
  type?: string
  items?: unknown[]
}

export interface Answer {
  task_id?: string
  participant_id?: string
  title?: string
  executive_summary?: string
  sections?: AnswerSection[]
  timeline?: TimelineItem[]
  claims?: Claim[]
  evidence?: Evidence[]
  entities?: Entity[]
  risks?: Risk[]
  uncertainties?: Uncertainty[]
  recommendations?: Recommendation[]
  limitations?: string[] | string
  [key: string]: unknown
}

// ─── Context Trace ────────────────────────────────────────────────────────────

export interface ContextMethods {
  prompt_only?: boolean
  long_context?: boolean
  rag?: boolean
  hybrid_retrieval?: boolean
  bm25?: boolean
  dense_embeddings?: boolean
  reranking?: boolean
  contextual_retrieval?: boolean
  memory?: boolean
  llm_generated_wiki?: boolean
  multi_agent?: boolean
  summarization?: boolean
  compression?: boolean
  graph_extraction?: boolean
  human_in_the_loop?: boolean
  [key: string]: boolean | undefined
}

export interface ContextStats {
  documents_available?: number
  documents_opened?: number
  documents_retrieved?: number
  documents_used_in_final?: number
  chunks_created?: number
  chunks_retrieved?: number
  chunks_used_in_final?: number
  input_tokens_estimated?: number
  output_tokens_estimated?: number
  total_tokens_estimated?: number
  estimated_cost_usd?: number
  latency_seconds?: number
  [key: string]: number | undefined
}

export interface RetrievalStep {
  step?: number
  query?: string
  method?: string
  top_k?: number
  selected_evidence_ids?: string[]
  [key: string]: unknown
}

export interface ContextTrace {
  task_id?: string
  participant_id?: string
  strategy_name?: string
  strategy_summary?: string
  methods?: ContextMethods
  models?: Array<{ provider: string; model: string; purpose: string }>
  context_stats?: ContextStats
  retrieval_trace?: RetrievalStep[]
  compression_trace?: unknown[]
  what_was_ignored?: Array<{ description: string; reason: string } | string>
  known_failure_modes?: string[]
  [key: string]: unknown
}

// ─── Score ────────────────────────────────────────────────────────────────────

export interface Score {
  task_id?: string
  participant_id?: string
  overall_score?: number
  scores?: {
    answer_quality?: number
    evidence_quality?: number
    context_efficiency?: number
    uncertainty_handling?: number
    visual_clarity?: number
    reproducibility?: number
  }
  scored_by?: string
  scored_at?: string
  notes?: string
}

// ─── Participant ──────────────────────────────────────────────────────────────

export interface Participant {
  id: string
  display_name: string
  type?: string
  description?: string
  github?: string
  website?: string
  contact?: string
}

// ─── Submission ───────────────────────────────────────────────────────────────

export interface Submission {
  participant_id: string
  participant?: Participant
  task_id: string
  answer?: Answer
  context_trace?: ContextTrace
  score?: Score
  // catalog summary fields
  participant_display_name?: string
  participant_type?: string
  methods?: Record<string, boolean>
  overall_score?: number | null
  rank?: number | null
  submitted_at?: string
  context_stats?: Record<string, unknown>
}

// ─── Leaderboard ──────────────────────────────────────────────────────────────

export interface LeaderboardRanking {
  rank: number
  participant_id: string
  participant_display_name: string
  overall_score: number
  scored_by?: string
}

export interface LeaderboardEntry {
  task_id: string
  task_title?: string
  domain?: string
  difficulty?: string
  rankings: LeaderboardRanking[]
}
