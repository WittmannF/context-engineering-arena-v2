// @ts-nocheck
import type { Score } from '../types'
import clsx from 'clsx'

interface ScoreBreakdownProps {
  score: Score
  compact?: boolean
}

function scoreColor(s: number): string {
  if (s >= 70) return 'text-green-400'
  if (s >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

function barColor(s: number): string {
  if (s >= 70) return 'bg-green-500'
  if (s >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

export default function ScoreBreakdown({ score, compact = false }: ScoreBreakdownProps) {
  return (
    <div className="space-y-4">
      {/* Overall score */}
      <div className={clsx('flex items-center justify-between p-4 rounded-xl border',
        score.overall >= 70 ? 'bg-green-950/20 border-green-800/40' :
        score.overall >= 50 ? 'bg-yellow-950/20 border-yellow-800/40' :
        'bg-red-950/20 border-red-800/40'
      )}>
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-widest">Overall Score</p>
          <p className={clsx('text-4xl font-extrabold tabular-nums mt-1', scoreColor(score.overall))}>
            {score.overall}
          </p>
          <p className="text-xs text-gray-500 mt-1">/ 100</p>
        </div>
        <div className="text-right">
          <div className="h-20 w-20 relative flex items-center justify-center">
            <svg viewBox="0 0 36 36" className="h-20 w-20 -rotate-90">
              <circle
                cx="18" cy="18" r="15.9"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                className="text-gray-800"
              />
              <circle
                cx="18" cy="18" r="15.9"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeDasharray={`${score.overall} ${100 - score.overall}`}
                strokeLinecap="round"
                className={score.overall >= 70 ? 'text-green-500' : score.overall >= 50 ? 'text-yellow-500' : 'text-red-500'}
              />
            </svg>
            <span className={clsx('absolute text-sm font-bold', scoreColor(score.overall))}>
              {score.overall}%
            </span>
          </div>
        </div>
      </div>

      {/* Dimensions */}
      <div className="space-y-3">
        {score.dimensions.map((dim) => (
          <div key={dim.label}>
            <div className="flex items-center justify-between mb-1.5">
              <span className={clsx('text-sm text-gray-300', compact && 'text-xs')}>{dim.label}</span>
              <span className={clsx('font-bold tabular-nums', scoreColor(dim.score), compact ? 'text-sm' : 'text-base')}>
                {dim.score}
              </span>
            </div>
            <div className="h-2 rounded-full bg-gray-800">
              <div
                className={clsx('h-2 rounded-full transition-all', barColor(dim.score))}
                style={{ width: `${dim.score}%` }}
              />
            </div>
            {!compact && dim.notes && (
              <p className="text-xs text-gray-500 mt-1">{dim.notes}</p>
            )}
          </div>
        ))}
      </div>

      {/* Meta */}
      {!compact && (
        <div className="text-xs text-gray-600 pt-2 border-t border-gray-800">
          Scored by {score.scored_by}
          {score.scored_at && <> &bull; {score.scored_at}</>}
          {score.notes && <p className="mt-1 text-gray-500">{score.notes}</p>}
        </div>
      )}
    </div>
  )
}
