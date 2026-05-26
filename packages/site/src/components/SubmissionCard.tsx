// @ts-nocheck
import { Link } from 'react-router-dom'
import { Zap, DollarSign, ChevronRight } from 'lucide-react'
import type { Submission } from '../types'
import clsx from 'clsx'

interface SubmissionCardProps {
  submission: Submission
  taskTitle?: string
}

function scoreColor(score: number): string {
  if (score >= 70) return 'text-green-400'
  if (score >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

function scoreBg(score: number): string {
  if (score >= 70) return 'bg-green-900/30 border-green-700/50'
  if (score >= 50) return 'bg-yellow-900/30 border-yellow-700/50'
  return 'bg-red-900/30 border-red-700/50'
}

const methodLabels: Record<string, string> = {
  keyword_search: 'Keyword',
  semantic_search: 'Semantic',
  hybrid_search: 'Hybrid',
  reranking: 'Reranking',
  hyde: 'HyDE',
  self_query: 'Self-Query',
  multi_hop: 'Multi-Hop',
  entity_expansion: 'Entity',
  temporal_filtering: 'Temporal',
  sliding_window: 'Sliding Window',
  summary_index: 'Summary Index',
  parent_document: 'Parent Doc',
}

export default function SubmissionCard({ submission, taskTitle }: SubmissionCardProps) {
  const score = submission.score?.overall ?? 0
  const methods = submission.context_trace.methods
  const activeMethods = Object.entries(methods)
    .filter(([, active]) => active)
    .map(([key]) => methodLabels[key] ?? key)

  return (
    <Link
      to={`/tasks/${submission.task_id}/submissions/${submission.participant_id}`}
      className="card flex flex-col gap-4 hover:border-gray-700 hover:bg-gray-800/50 transition-all group"
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="font-semibold text-gray-100 group-hover:text-blue-300 transition-colors">
            {submission.participant.display_name}
          </h3>
          {taskTitle && (
            <p className="text-xs text-gray-500 mt-0.5 truncate">{taskTitle}</p>
          )}
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {submission.score && (
            <span className={clsx('text-lg font-bold tabular-nums', scoreColor(score))}>
              {score}
            </span>
          )}
          <ChevronRight className="h-4 w-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
        </div>
      </div>

      {/* Score bar */}
      {submission.score && (
        <div className={clsx('rounded-lg border px-3 py-2', scoreBg(score))}>
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="text-gray-400">Overall Score</span>
            <span className={clsx('font-bold', scoreColor(score))}>{score} / 100</span>
          </div>
          <div className="h-1.5 rounded-full bg-gray-800">
            <div
              className={clsx(
                'h-1.5 rounded-full transition-all',
                score >= 70 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
              )}
              style={{ width: `${score}%` }}
            />
          </div>
        </div>
      )}

      {/* Active methods */}
      {activeMethods.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {activeMethods.slice(0, 4).map((m) => (
            <span key={m} className="badge-blue text-[10px] px-2">{m}</span>
          ))}
          {activeMethods.length > 4 && (
            <span className="badge-gray text-[10px] px-2">+{activeMethods.length - 4}</span>
          )}
        </div>
      )}

      {/* Stats */}
      <div className="flex items-center gap-4 text-xs text-gray-500 pt-2 border-t border-gray-800">
        <span className="flex items-center gap-1">
          <Zap className="h-3 w-3" />
          {submission.context_trace.stats.total_tokens_in_context.toLocaleString()} tokens
        </span>
        <span className="flex items-center gap-1">
          <DollarSign className="h-3 w-3" />
          ${submission.context_trace.stats.estimated_cost_usd.toFixed(4)}
        </span>
        <span>{submission.context_trace.stats.latency_seconds}s latency</span>
      </div>
    </Link>
  )
}
