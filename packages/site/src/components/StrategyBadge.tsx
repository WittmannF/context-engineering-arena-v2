import clsx from 'clsx'

interface StrategyBadgeProps {
  method: string
  active: boolean
}

const methodLabels: Record<string, string> = {
  keyword_search: 'Keyword Search',
  semantic_search: 'Semantic Search',
  hybrid_search: 'Hybrid Search',
  reranking: 'Reranking',
  hyde: 'HyDE',
  self_query: 'Self-Query',
  multi_hop: 'Multi-Hop',
  entity_expansion: 'Entity Expansion',
  temporal_filtering: 'Temporal Filter',
  sliding_window: 'Sliding Window',
  summary_index: 'Summary Index',
  parent_document: 'Parent Document',
}

export default function StrategyBadge({ method, active }: StrategyBadgeProps) {
  const label = methodLabels[method] ?? method.replace(/_/g, ' ')

  return (
    <span
      className={clsx(
        'badge text-xs px-2.5 py-1 font-medium',
        active
          ? 'bg-blue-900/50 text-blue-300 border border-blue-700/50'
          : 'bg-gray-800/50 text-gray-600 border border-gray-700/50 line-through'
      )}
    >
      {label}
    </span>
  )
}
