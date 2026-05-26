// @ts-nocheck
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronUp, ChevronDown } from 'lucide-react'
import type { Submission, LeaderboardEntry } from '../types'
import clsx from 'clsx'

interface LeaderboardTableProps {
  leaderboard: LeaderboardEntry
  submissions: Submission[]
  taskId: string
}

function scoreColor(score: number): string {
  if (score >= 70) return 'text-green-400'
  if (score >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

const methodLabels: Record<string, string> = {
  keyword_search: 'Keyword',
  semantic_search: 'Semantic',
  hybrid_search: 'Hybrid',
  reranking: 'Rerank',
  hyde: 'HyDE',
  self_query: 'Self-Q',
  multi_hop: 'Multi-Hop',
  entity_expansion: 'Entity',
  temporal_filtering: 'Temporal',
  sliding_window: 'Win',
  summary_index: 'Summ',
  parent_document: 'Parent',
}

type SortKey = 'rank' | 'overall_score'

export default function LeaderboardTable({ leaderboard, submissions, taskId }: LeaderboardTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>('rank')
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc')

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir(key === 'overall_score' ? 'desc' : 'asc')
    }
  }

  const sorted = [...leaderboard.rankings].sort((a, b) => {
    const mult = sortDir === 'asc' ? 1 : -1
    if (sortKey === 'rank') return (a.rank - b.rank) * mult
    return (a.overall_score - b.overall_score) * mult
  })

  const submissionMap = new Map(submissions.map(s => [s.participant_id, s]))

  const SortIcon = ({ col }: { col: SortKey }) => {
    if (sortKey !== col) return <ChevronDown className="h-3 w-3 text-gray-600" />
    return sortDir === 'asc'
      ? <ChevronUp className="h-3 w-3 text-blue-400" />
      : <ChevronDown className="h-3 w-3 text-blue-400" />
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-800">
            <th
              className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 cursor-pointer hover:text-gray-300 select-none"
              onClick={() => handleSort('rank')}
            >
              <span className="flex items-center gap-1">Rank <SortIcon col="rank" /></span>
            </th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">
              Participant
            </th>
            <th
              className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 cursor-pointer hover:text-gray-300 select-none"
              onClick={() => handleSort('overall_score')}
            >
              <span className="flex items-center gap-1">Score <SortIcon col="overall_score" /></span>
            </th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden md:table-cell">
              Dimensions
            </th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden lg:table-cell">
              Methods
            </th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden sm:table-cell">
              Scored By
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((entry, i) => {
            const submission = submissionMap.get(entry.participant_id)
            const dims = submission?.score?.dimensions ?? []
            const methods = submission?.context_trace.methods
            const activeMethods = methods
              ? Object.entries(methods).filter(([, v]) => v).map(([k]) => methodLabels[k] ?? k)
              : []

            return (
              <tr
                key={entry.participant_id}
                className={clsx(
                  'border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors',
                  i === 0 && 'bg-yellow-950/10'
                )}
              >
                <td className="py-3 px-4">
                  <span className={clsx(
                    'font-bold text-base',
                    i === 0 ? 'text-yellow-400' : i === 1 ? 'text-gray-300' : 'text-gray-500'
                  )}>
                    {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : entry.rank === 3 ? '🥉' : `#${entry.rank}`}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <Link
                    to={`/tasks/${taskId}/submissions/${entry.participant_id}`}
                    className="font-medium text-gray-200 hover:text-blue-300 transition-colors"
                  >
                    {entry.participant_display_name}
                  </Link>
                </td>
                <td className="py-3 px-4">
                  <span className={clsx('font-bold text-lg tabular-nums', scoreColor(entry.overall_score))}>
                    {entry.overall_score}
                  </span>
                </td>
                <td className="py-3 px-4 hidden md:table-cell">
                  <div className="flex gap-3 text-xs text-gray-500">
                    {dims.slice(0, 3).map((d) => (
                      <span key={d.label} title={d.label}>
                        <span className="text-gray-400">{d.label.split(' ')[0]}</span>
                        {' '}
                        <span className={scoreColor(d.score)}>{d.score}</span>
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-3 px-4 hidden lg:table-cell">
                  <div className="flex flex-wrap gap-1">
                    {activeMethods.slice(0, 3).map((m) => (
                      <span key={m} className="badge-blue text-[10px] px-1.5">{m}</span>
                    ))}
                    {activeMethods.length > 3 && (
                      <span className="badge-gray text-[10px] px-1.5">+{activeMethods.length - 3}</span>
                    )}
                  </div>
                </td>
                <td className="py-3 px-4 text-xs text-gray-500 hidden sm:table-cell">
                  {entry.scored_by}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>

      {sorted.length === 0 && (
        <div className="py-12 text-center text-gray-500 text-sm">No submissions yet.</div>
      )}
    </div>
  )
}
