// @ts-nocheck
import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import ScoreBreakdown from '../components/ScoreBreakdown'
import StrategyBadge from '../components/StrategyBadge'
import EmptyState from '../components/EmptyState'
import submissionsData from '../data/generated/submissions.json'
import tasksData from '../data/generated/tasks.json'
import type { Submission, Task } from '../types'
import clsx from 'clsx'

const submissions = submissionsData as Submission[]
const tasks = tasksData as Task[]

function scoreColor(s: number): string {
  if (s >= 70) return 'text-green-400'
  if (s >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

export default function ComparePage() {
  const { taskId } = useParams<{ taskId: string }>()
  const task = tasks.find(t => t.id === taskId)
  const taskSubmissions = submissions.filter(s => s.task_id === taskId)

  const [leftId, setLeftId] = useState(taskSubmissions[0]?.participant_id ?? '')
  const [rightId, setRightId] = useState(taskSubmissions[1]?.participant_id ?? '')

  const leftSub = taskSubmissions.find(s => s.participant_id === leftId)
  const rightSub = taskSubmissions.find(s => s.participant_id === rightId)

  if (!task) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <EmptyState
          title="Task not found"
          description="This task does not exist."
          actionLabel="Browse Tasks"
          actionTo="/tasks"
        />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <Link to={`/tasks/${taskId}`} className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors mb-8">
        <ArrowLeft className="h-4 w-4" />
        {task.title}
      </Link>

      <div className="mb-10">
        <p className="section-header">Side-by-side</p>
        <h1 className="text-gray-100 mb-2">Compare Strategies</h1>
        <p className="text-gray-400 text-sm max-w-2xl">
          Select two submissions for <span className="text-gray-200 font-medium">{task.title}</span> to compare their strategies, scores, and context usage.
        </p>
      </div>

      {/* Dropdowns */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-10">
        {[
          { value: leftId, onChange: setLeftId, label: 'Submission A' },
          { value: rightId, onChange: setRightId, label: 'Submission B' },
        ].map(({ value, onChange, label }) => (
          <div key={label}>
            <label className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-2 block">
              {label}
            </label>
            <select
              value={value}
              onChange={e => onChange(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-sm text-gray-200 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
            >
              <option value="">Select a submission...</option>
              {taskSubmissions.map(s => (
                <option key={s.participant_id} value={s.participant_id}>
                  {s.participant.display_name}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>

      {taskSubmissions.length < 2 && (
        <div className="mb-8 px-4 py-3 bg-yellow-950/30 border border-yellow-800/40 rounded-xl text-sm text-yellow-300">
          Only one submission exists for this task. Add another to enable comparison.
        </div>
      )}

      {leftSub && rightSub && (
        <div className="space-y-10">
          {/* Overview cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[leftSub, rightSub].map((sub, idx) => (
              <div key={sub.participant_id} className="card">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className={clsx('text-xs font-bold uppercase tracking-widest', idx === 0 ? 'text-blue-400' : 'text-purple-400')}>
                      {idx === 0 ? 'A' : 'B'}
                    </span>
                    <h3 className="text-gray-100 mt-1">{sub.participant.display_name}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">{sub.participant.type} &bull; {sub.participant.description}</p>
                  </div>
                  {sub.score && (
                    <span className={clsx('text-3xl font-extrabold tabular-nums', scoreColor(sub.score.overall))}>
                      {sub.score.overall}
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-3 gap-3 mb-4 text-xs">
                  <div className="bg-gray-800/50 rounded-lg p-2 text-center">
                    <p className="text-gray-500">Tokens</p>
                    <p className="text-gray-200 font-medium tabular-nums">{sub.context_trace.stats.total_tokens_in_context.toLocaleString()}</p>
                  </div>
                  <div className="bg-gray-800/50 rounded-lg p-2 text-center">
                    <p className="text-gray-500">Cost</p>
                    <p className="text-gray-200 font-medium">${sub.context_trace.stats.estimated_cost_usd.toFixed(4)}</p>
                  </div>
                  <div className="bg-gray-800/50 rounded-lg p-2 text-center">
                    <p className="text-gray-500">Docs Used</p>
                    <p className="text-gray-200 font-medium">{sub.context_trace.stats.documents_used_in_answer}</p>
                  </div>
                </div>

                <div className="text-xs text-gray-500 mb-3 grid grid-cols-2 gap-2">
                  <span>Claims: <strong className="text-gray-300">{sub.answer.claims.length}</strong></span>
                  <span>Evidence: <strong className="text-gray-300">{sub.answer.evidence.length}</strong></span>
                  <span>Timeline: <strong className="text-gray-300">{sub.answer.timeline?.length ?? 0}</strong></span>
                  <span>Entities: <strong className="text-gray-300">{sub.answer.entities?.length ?? 0}</strong></span>
                </div>

                <Link
                  to={`/tasks/${taskId}/submissions/${sub.participant_id}`}
                  className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 transition-colors"
                >
                  View full submission <ArrowRight className="h-3 w-3" />
                </Link>
              </div>
            ))}
          </div>

          {/* Score comparison */}
          {leftSub.score && rightSub.score && (
            <div>
              <p className="section-header">Score Breakdown</p>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="card">
                  <p className="text-xs font-bold text-blue-400 uppercase tracking-widest mb-4">A — {leftSub.participant.display_name}</p>
                  <ScoreBreakdown score={leftSub.score} compact />
                </div>
                <div className="card">
                  <p className="text-xs font-bold text-purple-400 uppercase tracking-widest mb-4">B — {rightSub.participant.display_name}</p>
                  <ScoreBreakdown score={rightSub.score} compact />
                </div>
              </div>
            </div>
          )}

          {/* Methods comparison */}
          <div>
            <p className="section-header">Methods Comparison</p>
            <div className="card overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="text-left py-2 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Method</th>
                    <th className="text-center py-2 px-4 text-xs font-semibold uppercase tracking-widest text-blue-400">A</th>
                    <th className="text-center py-2 px-4 text-xs font-semibold uppercase tracking-widest text-purple-400">B</th>
                  </tr>
                </thead>
                <tbody>
                  {(Object.entries(leftSub.context_trace.methods) as [string, boolean][]).map(([method, leftActive]) => {
                    const rightActive = (rightSub.context_trace.methods as unknown as Record<string, boolean>)[method] ?? false
                    return (
                      <tr key={method} className="border-b border-gray-800/50">
                        <td className="py-2 px-4">
                          <StrategyBadge method={method} active={leftActive || rightActive} />
                        </td>
                        <td className="py-2 px-4 text-center">
                          {leftActive ? (
                            <span className="text-green-400 font-bold">✓</span>
                          ) : (
                            <span className="text-gray-700">—</span>
                          )}
                        </td>
                        <td className="py-2 px-4 text-center">
                          {rightActive ? (
                            <span className="text-green-400 font-bold">✓</span>
                          ) : (
                            <span className="text-gray-700">—</span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Strategy summaries */}
          <div>
            <p className="section-header">Strategy Summaries</p>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {[leftSub, rightSub].map((sub, idx) => (
                <div key={sub.participant_id} className="card">
                  <p className={clsx('text-xs font-bold uppercase tracking-widest mb-2', idx === 0 ? 'text-blue-400' : 'text-purple-400')}>
                    {idx === 0 ? 'A' : 'B'} — {sub.context_trace.strategy_name}
                  </p>
                  <p className="text-sm text-gray-400 leading-relaxed">{sub.context_trace.strategy_summary}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {(!leftSub || !rightSub) && taskSubmissions.length >= 2 && (
        <div className="text-center py-12 text-gray-500 text-sm">
          Select two submissions above to compare them.
        </div>
      )}
    </div>
  )
}
