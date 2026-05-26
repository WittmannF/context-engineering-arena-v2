import ReactMarkdown from 'react-markdown'
import clsx from 'clsx'

interface MarkdownBlockProps {
  content: string
  className?: string
}

export default function MarkdownBlock({ content, className }: MarkdownBlockProps) {
  return (
    <div className={clsx('prose prose-invert prose-sm max-w-none', className)}>
      <ReactMarkdown
        components={{
          h1: ({ children }) => <h1 className="text-2xl font-bold text-gray-100 mb-4">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold text-gray-100 mt-6 mb-3">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-semibold text-gray-200 mt-5 mb-2">{children}</h3>,
          p: ({ children }) => <p className="text-gray-300 leading-relaxed mb-4">{children}</p>,
          ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-4 text-gray-300">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 mb-4 text-gray-300">{children}</ol>,
          li: ({ children }) => <li className="text-gray-300 leading-relaxed">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-gray-100">{children}</strong>,
          em: ({ children }) => <em className="italic text-gray-300">{children}</em>,
          code: ({ children }) => (
            <code className="bg-gray-800 text-blue-300 px-1.5 py-0.5 rounded text-xs font-mono">
              {children}
            </code>
          ),
          pre: ({ children }) => (
            <pre className="bg-gray-800 border border-gray-700 rounded-lg p-4 overflow-x-auto text-xs font-mono text-gray-300 mb-4">
              {children}
            </pre>
          ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-blue-600 pl-4 my-4 text-gray-400 italic">
              {children}
            </blockquote>
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 underline"
            >
              {children}
            </a>
          ),
          hr: () => <hr className="border-gray-700 my-6" />,
          table: ({ children }) => (
            <div className="overflow-x-auto mb-4">
              <table className="w-full text-sm border-collapse border border-gray-700">
                {children}
              </table>
            </div>
          ),
          th: ({ children }) => (
            <th className="border border-gray-700 px-3 py-2 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-800">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-gray-700 px-3 py-2 text-gray-300 text-sm">
              {children}
            </td>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
