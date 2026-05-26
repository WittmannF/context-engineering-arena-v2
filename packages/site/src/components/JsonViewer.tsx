import { useState } from 'react'
import { ChevronDown, ChevronRight, Copy, Check } from 'lucide-react'

interface JsonViewerProps {
  data: unknown
  label?: string
}

export default function JsonViewer({ data, label = 'Raw JSON' }: JsonViewerProps) {
  const [open, setOpen] = useState(false)
  const [copied, setCopied] = useState(false)

  const json = JSON.stringify(data, null, 2)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(json)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="border border-gray-700 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-gray-800/50 hover:bg-gray-800 transition-colors text-sm font-medium text-gray-300"
      >
        <span className="flex items-center gap-2">
          {open
            ? <ChevronDown className="h-4 w-4 text-blue-400" />
            : <ChevronRight className="h-4 w-4 text-gray-500" />
          }
          {label}
        </span>
        {open && (
          <button
            onClick={e => { e.stopPropagation(); void handleCopy() }}
            className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-200 px-2 py-1 rounded hover:bg-gray-700 transition-colors"
          >
            {copied
              ? <><Check className="h-3.5 w-3.5 text-green-400" /> Copied</>
              : <><Copy className="h-3.5 w-3.5" /> Copy</>
            }
          </button>
        )}
      </button>

      {open && (
        <div className="relative">
          <pre className="overflow-auto max-h-96 p-4 text-xs font-mono text-gray-300 bg-gray-900 leading-relaxed">
            <code>{json}</code>
          </pre>
        </div>
      )}
    </div>
  )
}
