import type { TimelineItem } from '../types'
import clsx from 'clsx'

interface TimelineProps {
  items: TimelineItem[]
}

export default function Timeline({ items }: TimelineProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500 py-4">No timeline items.</p>
  }

  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-[88px] top-0 bottom-0 w-px bg-gray-800" />

      <div className="space-y-8">
        {items.map((item, idx) => (
          <div key={idx} className="flex gap-6">
            {/* Date column */}
            <div className="w-20 shrink-0 text-right">
              <span className="text-xs text-gray-500 leading-none">{item.date}</span>
            </div>

            {/* Dot */}
            <div className="relative shrink-0 flex items-start justify-center w-4 mt-0.5">
              <div className={clsx(
                'h-3 w-3 rounded-full border-2 bg-gray-950 z-10',
                item.significance === 'high'
                  ? 'border-red-500'
                  : item.significance === 'medium'
                  ? 'border-yellow-500'
                  : 'border-gray-600'
              )} />
            </div>

            {/* Content */}
            <div className="flex-1 pb-2">
              <h4 className={clsx(
                'font-semibold text-sm leading-snug mb-1',
                item.significance === 'high' ? 'text-red-300' : 'text-gray-200'
              )}>
                {item.title}
              </h4>
              <p className="text-sm text-gray-400 leading-relaxed">{item.description}</p>
              {item.evidence_ids && item.evidence_ids.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {item.evidence_ids.map((eid) => (
                    <span key={eid} className="badge-blue text-[10px] px-1.5">{eid}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
