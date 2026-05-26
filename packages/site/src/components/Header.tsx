import { NavLink } from 'react-router-dom'
import { ExternalLink, Target } from 'lucide-react'
import clsx from 'clsx'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-800 bg-gray-950/90 backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <NavLink to="/" className="flex items-center gap-3 group">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 group-hover:bg-blue-500 transition-colors">
              <Target className="h-5 w-5 text-white" />
            </div>
            <div className="hidden sm:block">
              <span className="text-sm font-bold text-gray-100">Context Engineering Arena</span>
              <p className="text-[10px] text-gray-500 leading-none mt-0.5">Build the clearest page from the messiest context</p>
            </div>
          </NavLink>

          {/* Navigation */}
          <nav className="flex items-center gap-1">
            {[
              { to: '/tasks', label: 'Tasks' },
              { to: '/compare/task-001-enron-investigation', label: 'Compare' },
              { to: '/propose', label: 'Propose' },
              { to: '/about', label: 'About' },
            ].map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  clsx(
                    'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors',
                    isActive
                      ? 'bg-gray-800 text-gray-100'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
                  )
                }
              >
                {label}
              </NavLink>
            ))}

            <a
              href="https://github.com/your-org/context-engineering-arena-v2"
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-400 hover:text-gray-200 rounded-lg hover:bg-gray-800/50 transition-colors border border-gray-700 hover:border-gray-600"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}
