import { Link } from 'react-router-dom'
import { ExternalLink } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-gray-800 bg-gray-950 mt-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
          <div>
            <p className="text-sm font-semibold text-gray-300 mb-3">Context Engineering Arena</p>
            <p className="text-xs text-gray-500 leading-relaxed">
              Build the clearest page from the messiest context. An open benchmark for context engineering strategies.
            </p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">Navigation</p>
            <ul className="space-y-2">
              {[
                { to: '/tasks', label: 'Browse Tasks' },
                { to: '/propose', label: 'Propose a Task' },
                { to: '/about', label: 'About' },
                { to: '/compare/task-001-enron-investigation', label: 'Compare Strategies' },
              ].map(({ to, label }) => (
                <li key={to}>
                  <Link to={to} className="text-xs text-gray-400 hover:text-gray-200 transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">Resources</p>
            <ul className="space-y-2">
              {[
                { href: 'https://github.com/your-org/context-engineering-arena-v2', label: 'GitHub Repository' },
                { href: 'https://github.com/your-org/context-engineering-arena-v2/blob/main/LICENSE', label: 'License (MIT)' },
                { href: 'https://github.com/your-org/context-engineering-arena-v2/issues/new', label: 'Open an Issue' },
                { href: 'https://github.com/your-org/context-engineering-arena-v2/discussions', label: 'Discussions' },
              ].map(({ href, label }) => (
                <li key={href}>
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 transition-colors"
                  >
                    {label}
                    <ExternalLink className="h-2.5 w-2.5" />
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-gray-600">
            &copy; {new Date().getFullYear()} Context Engineering Arena. Open source under MIT License.
          </p>
          <p className="text-xs text-gray-600">
            Data from public datasets. No affiliation with Enron, Brazilian government, or GitHub.
          </p>
        </div>
      </div>
    </footer>
  )
}
