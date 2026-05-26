import type { Claim } from '../types'
import clsx from 'clsx'

interface ClaimsTableProps {
  claims: Claim[]
  onEvidenceClick?: (evidenceId: string) => void
}

const claimTypeStyle: Record<string, string> = {
  fact: 'badge-blue',
  interpretation: 'badge-yellow',
  recommendation: 'badge-green',
  uncertainty: 'badge-gray',
}

const confidenceStyle: Record<string, string> = {
  high: 'badge-green',
  medium: 'badge-yellow',
  low: 'badge-red',
}

export default function ClaimsTable({ claims, onEvidenceClick }: ClaimsTableProps) {
  if (claims.length === 0) {
    return <p className="text-sm text-gray-500 py-4">No claims recorded.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-800">
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden sm:table-cell">ID</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Claim</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Type</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Confidence</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden md:table-cell">Evidence</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden lg:table-cell">Notes</th>
          </tr>
        </thead>
        <tbody>
          {claims.map((claim) => (
            <tr key={claim.id} className="border-b border-gray-800/50 hover:bg-gray-800/20 transition-colors">
              <td className="py-3 px-4 text-gray-600 font-mono text-xs hidden sm:table-cell">
                {claim.id}
              </td>
              <td className="py-3 px-4">
                <p className="text-gray-300 leading-relaxed">{claim.text}</p>
              </td>
              <td className="py-3 px-4">
                <span className={clsx(claimTypeStyle[claim.claim_type] ?? 'badge-gray')}>
                  {claim.claim_type}
                </span>
              </td>
              <td className="py-3 px-4">
                <span className={clsx(confidenceStyle[claim.confidence] ?? 'badge-gray')}>
                  {claim.confidence}
                </span>
              </td>
              <td className="py-3 px-4 hidden md:table-cell">
                <div className="flex flex-wrap gap-1">
                  {claim.evidence_ids.map((eid) => (
                    <button
                      key={eid}
                      onClick={() => onEvidenceClick?.(eid)}
                      className="badge-blue text-[10px] px-1.5 cursor-pointer hover:bg-blue-800/60 transition-colors"
                    >
                      {eid}
                    </button>
                  ))}
                </div>
              </td>
              <td className="py-3 px-4 text-xs text-gray-500 hidden lg:table-cell max-w-xs">
                {claim.notes ?? '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
