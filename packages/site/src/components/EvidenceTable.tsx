import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
import type { Evidence } from '../types'
import clsx from 'clsx'

interface EvidenceTableProps {
  evidence: Evidence[]
}

const sourceTypeBadge: Record<string, string> = {
  email: 'badge-blue',
  document: 'badge-gray',
  api: 'badge-green',
  web: 'badge-purple',
  database: 'badge-yellow',
  report: 'badge-yellow',
  other: 'badge-gray',
}

export default function EvidenceTable({ evidence }: EvidenceTableProps) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  const toggle = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  if (evidence.length === 0) {
    return <p className="text-sm text-gray-500 py-4">No evidence items.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-800">
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 w-8" />
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Type</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500">Title</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden sm:table-cell">Date</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden md:table-cell">Excerpt</th>
            <th className="text-left py-3 px-4 text-xs font-semibold uppercase tracking-widest text-gray-500 hidden lg:table-cell">Source ID</th>
          </tr>
        </thead>
        <tbody>
          {evidence.map((ev) => {
            const isOpen = expanded.has(ev.id)
            return (
              <>
                <tr
                  key={ev.id}
                  className="border-b border-gray-800/50 hover:bg-gray-800/20 transition-colors cursor-pointer"
                  onClick={() => toggle(ev.id)}
                >
                  <td className="py-3 px-4">
                    {isOpen
                      ? <ChevronDown className="h-3.5 w-3.5 text-blue-400" />
                      : <ChevronRight className="h-3.5 w-3.5 text-gray-500" />
                    }
                  </td>
                  <td className="py-3 px-4">
                    <span className={clsx(sourceTypeBadge[ev.source_type] ?? 'badge-gray')}>
                      {ev.source_type}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="font-medium text-gray-200">{ev.title}</span>
                  </td>
                  <td className="py-3 px-4 text-gray-500 hidden sm:table-cell whitespace-nowrap">
                    {ev.date ?? '—'}
                  </td>
                  <td className="py-3 px-4 text-gray-400 hidden md:table-cell max-w-xs">
                    <span className="line-clamp-1">{ev.excerpt}</span>
                  </td>
                  <td className="py-3 px-4 text-gray-600 hidden lg:table-cell font-mono text-xs">
                    {ev.source_id ?? '—'}
                  </td>
                </tr>
                {isOpen && (
                  <tr key={`${ev.id}-expanded`} className="border-b border-gray-800">
                    <td colSpan={6} className="px-4 pb-4 pt-2 bg-gray-900/50">
                      <div className="rounded-lg border border-gray-700 p-4 space-y-3">
                        <div>
                          <p className="text-xs text-gray-500 uppercase tracking-widest mb-1">Full Excerpt</p>
                          <p className="text-sm text-gray-300 leading-relaxed">{ev.excerpt}</p>
                        </div>
                        <div className="flex flex-wrap gap-4 text-xs text-gray-500">
                          {ev.date && <span><strong className="text-gray-400">Date:</strong> {ev.date}</span>}
                          {ev.source_id && <span><strong className="text-gray-400">Source ID:</strong> <code className="font-mono text-gray-300">{ev.source_id}</code></span>}
                          {ev.url && (
                            <a
                              href={ev.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-400 hover:underline"
                              onClick={e => e.stopPropagation()}
                            >
                              View Source
                            </a>
                          )}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
