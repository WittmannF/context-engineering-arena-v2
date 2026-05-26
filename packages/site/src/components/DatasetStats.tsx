import { ExternalLink, Database, Download, Key } from 'lucide-react'
import type { Dataset } from '../types'
import clsx from 'clsx'

interface DatasetStatsProps {
  dataset: Dataset
}

const accessMethodLabel: Record<string, string> = {
  direct_download: 'Direct Download',
  public_api: 'Public API',
  kaggle: 'Kaggle',
  other: 'Other',
}

const accessMethodIcon: Record<string, React.ReactNode> = {
  direct_download: <Download className="h-3.5 w-3.5" />,
  public_api: <Key className="h-3.5 w-3.5" />,
  kaggle: <Database className="h-3.5 w-3.5" />,
  other: <Database className="h-3.5 w-3.5" />,
}

export default function DatasetStats({ dataset }: DatasetStatsProps) {
  return (
    <div className="card space-y-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <Database className="h-5 w-5 text-blue-400 shrink-0" />
          <h4 className="font-semibold text-gray-200">{dataset.name}</h4>
        </div>
        <a
          href={dataset.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 transition-colors shrink-0"
        >
          Source <ExternalLink className="h-3 w-3" />
        </a>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-gray-800/50 rounded-lg p-3">
          <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Access</p>
          <div className={clsx('flex items-center gap-1.5 text-xs font-medium',
            dataset.access_method === 'public_api' ? 'text-green-300' :
            dataset.access_method === 'direct_download' ? 'text-blue-300' : 'text-gray-300'
          )}>
            {accessMethodIcon[dataset.access_method]}
            {accessMethodLabel[dataset.access_method]}
          </div>
        </div>

        <div className="bg-gray-800/50 rounded-lg p-3">
          <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Size</p>
          <p className="text-xs font-medium text-gray-300">{dataset.expected_size}</p>
        </div>

        <div className="bg-gray-800/50 rounded-lg p-3">
          <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">License</p>
          <p className="text-xs font-medium text-gray-300 leading-snug">{dataset.license}</p>
        </div>

        <div className="bg-gray-800/50 rounded-lg p-3">
          <p className="text-[10px] uppercase tracking-widest text-gray-500 mb-1">Sample</p>
          <span className={dataset.sample_available ? 'badge-green' : 'badge-gray'}>
            {dataset.sample_available ? 'Available' : 'Not Available'}
          </span>
        </div>
      </div>
    </div>
  )
}
