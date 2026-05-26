import { Info } from 'lucide-react'
import type { Entity } from '../types'
import clsx from 'clsx'

interface EntityGraphPlaceholderProps {
  entities: Entity[]
}

const entityTypeStyle: Record<string, string> = {
  person: 'badge-blue',
  organization: 'badge-purple',
  location: 'badge-green',
  financial: 'badge-yellow',
  event: 'badge-red',
  concept: 'badge-gray',
  other: 'badge-gray',
}

export default function EntityGraphPlaceholder({ entities }: EntityGraphPlaceholderProps) {
  return (
    <div>
      <div className="flex items-center gap-2 mb-4 px-3 py-2 rounded-lg bg-blue-900/20 border border-blue-800/40 text-xs text-blue-300">
        <Info className="h-3.5 w-3.5 shrink-0" />
        Full graph visualization coming soon. Entities are shown as cards below.
      </div>

      {entities.length === 0 ? (
        <p className="text-sm text-gray-500 py-4">No entities extracted.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {entities.map((entity) => (
            <div key={entity.id} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-semibold text-sm text-gray-200 leading-snug">{entity.name}</h4>
                <span className={clsx('shrink-0', entityTypeStyle[entity.type] ?? 'badge-gray')}>
                  {entity.type}
                </span>
              </div>
              {entity.description && (
                <p className="text-xs text-gray-400 leading-relaxed mb-3">{entity.description}</p>
              )}
              {entity.aliases && entity.aliases.length > 0 && (
                <p className="text-xs text-gray-600 mb-2">
                  Also known as: {entity.aliases.join(', ')}
                </p>
              )}
              {entity.evidence_ids && entity.evidence_ids.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2 pt-2 border-t border-gray-700">
                  {entity.evidence_ids.slice(0, 4).map((eid) => (
                    <span key={eid} className="badge-blue text-[10px] px-1.5">{eid}</span>
                  ))}
                  {entity.evidence_ids.length > 4 && (
                    <span className="badge-gray text-[10px] px-1.5">+{entity.evidence_ids.length - 4}</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
