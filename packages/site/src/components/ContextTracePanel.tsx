/* eslint-disable @typescript-eslint/no-explicit-any */
// @ts-nocheck
import type { ContextTrace } from '../types'
import { Zap, DollarSign, FileText, Database, Clock } from 'lucide-react'
import StrategyBadge from './StrategyBadge'
import clsx from 'clsx'

interface ContextTracePanelProps {
  trace: ContextTrace
}

export default function ContextTracePanel({ trace }: ContextTracePanelProps) {
  const { methods, stats } = trace

  return (
    <div className="space-y-6">
      {/* Strategy header */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-1">Strategy</p>
        <h3 className="font-semibold text-gray-100 text-lg">{trace.strategy_name}</h3>
        <p className="text-sm text-gray-400 mt-1 leading-relaxed">{trace.strategy_summary}</p>
      </div>

      {/* Methods grid */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">Methods</p>
        <div className="flex flex-wrap gap-2">
          {(Object.entries(methods) as [string, boolean][]).map(([key, active]) => (
            <StrategyBadge key={key} method={key} active={active} />
          ))}
        </div>
      </div>

      {/* Stats card */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">Context Statistics</p>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {[
            {
              icon: <Database className="h-4 w-4 text-blue-400" />,
              label: 'Docs Available',
              value: stats.documents_available.toLocaleString(),
            },
            {
              icon: <FileText className="h-4 w-4 text-green-400" />,
              label: 'Docs Used',
              value: `${stats.documents_used_in_answer} / ${stats.documents_retrieved}`,
            },
            {
              icon: <Zap className="h-4 w-4 text-yellow-400" />,
              label: 'Tokens',
              value: stats.total_tokens_in_context.toLocaleString(),
            },
            {
              icon: <DollarSign className="h-4 w-4 text-purple-400" />,
              label: 'Est. Cost',
              value: `$${stats.estimated_cost_usd.toFixed(4)}`,
            },
            {
              icon: <Clock className="h-4 w-4 text-orange-400" />,
              label: 'Latency',
              value: `${stats.latency_seconds}s`,
            },
          ].map(({ icon, label, value }) => (
            <div key={label} className="bg-gray-800/60 border border-gray-700 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                {icon}
                <span className="text-xs text-gray-500">{label}</span>
              </div>
              <p className="text-sm font-semibold text-gray-200 tabular-nums">{value}</p>
            </div>
          ))}
        </div>
        <div className="mt-3 grid grid-cols-2 gap-3 text-xs text-gray-500">
          <span>Documents opened: <strong className="text-gray-300">{stats.documents_opened}</strong></span>
          <span>Chunks retrieved: <strong className="text-gray-300">{stats.total_chunks_retrieved}</strong></span>
        </div>
      </div>

      {/* Retrieval trace */}
      {trace.retrieval_steps.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">Retrieval Trace</p>
          <div className="space-y-3">
            {trace.retrieval_steps.map((step) => (
              <div key={step.step} className="flex gap-3">
                <div className="shrink-0 flex h-6 w-6 items-center justify-center rounded-full bg-blue-900/50 border border-blue-700/50 text-xs font-bold text-blue-300">
                  {step.step}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <code className="text-xs font-mono text-gray-300 bg-gray-800 px-2 py-0.5 rounded truncate max-w-xs">
                      {step.query}
                    </code>
                    <span className="badge-blue text-[10px] px-1.5">{step.method}</span>
                    <span className="text-xs text-gray-500">{step.documents_returned} docs</span>
                  </div>
                  {step.top_result_preview && (
                    <p className="text-xs text-gray-500 line-clamp-1 italic">
                      &ldquo;{step.top_result_preview}&rdquo;
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Ignored */}
      {trace.what_was_ignored && trace.what_was_ignored.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-2">What Was Ignored</p>
          <ul className="space-y-1.5">
            {trace.what_was_ignored.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-400">
                <span className="text-gray-600 mt-1">—</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Failure modes */}
      {trace.known_failure_modes && trace.known_failure_modes.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-2">Known Failure Modes</p>
          <ul className="space-y-1.5">
            {trace.known_failure_modes.map((item, i) => (
              <li
                key={i}
                className={clsx(
                  'flex items-start gap-2 text-sm rounded-lg px-3 py-2',
                  'bg-red-950/20 border border-red-900/30 text-red-300'
                )}
              >
                <span className="mt-0.5">!</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
