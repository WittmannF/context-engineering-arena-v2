import type { Risk } from '../types'
import clsx from 'clsx'

interface RiskMatrixProps {
  risks: Risk[]
}

const severityStyle: Record<string, string> = {
  critical: 'badge-red',
  high: 'badge-red',
  medium: 'badge-yellow',
  low: 'badge-green',
}

const severityBorder: Record<string, string> = {
  critical: 'border-red-700/60 bg-red-950/20',
  high: 'border-red-800/40 bg-red-950/10',
  medium: 'border-yellow-700/40 bg-yellow-950/10',
  low: 'border-gray-700 bg-gray-800/30',
}

const likelihoodStyle: Record<string, string> = {
  very_high: 'badge-red',
  high: 'badge-yellow',
  medium: 'badge-yellow',
  low: 'badge-green',
}

export default function RiskMatrix({ risks }: RiskMatrixProps) {
  if (risks.length === 0) {
    return <p className="text-sm text-gray-500 py-4">No risks identified.</p>
  }

  // Sort by severity order
  const severityOrder: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3 }
  const sorted = [...risks].sort(
    (a, b) => (severityOrder[a.severity] ?? 9) - (severityOrder[b.severity] ?? 9)
  )

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {sorted.map((risk) => (
        <div
          key={risk.id}
          className={clsx('border rounded-xl p-4 space-y-3', severityBorder[risk.severity] ?? 'border-gray-700')}
        >
          <div className="flex items-start justify-between gap-2">
            <h4 className="font-semibold text-sm text-gray-200 leading-snug">{risk.title}</h4>
            <div className="flex flex-col gap-1 items-end shrink-0">
              <span className={clsx(severityStyle[risk.severity] ?? 'badge-gray')}>
                {risk.severity}
              </span>
              <span className={clsx(likelihoodStyle[risk.likelihood] ?? 'badge-gray')}>
                {risk.likelihood.replace('_', ' ')} likelihood
              </span>
            </div>
          </div>
          <p className="text-sm text-gray-400 leading-relaxed">{risk.description}</p>
          {risk.evidence_ids && risk.evidence_ids.length > 0 && (
            <div className="flex flex-wrap gap-1 pt-2 border-t border-gray-700/50">
              {risk.evidence_ids.map((eid) => (
                <span key={eid} className="badge-blue text-[10px] px-1.5">{eid}</span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
