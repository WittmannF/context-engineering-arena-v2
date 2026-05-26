import { useState } from 'react'
import { Search } from 'lucide-react'
import TaskCard from '../components/TaskCard'
import tasksData from '../data/generated/tasks.json'
import type { Task } from '../types'
import clsx from 'clsx'

const tasks = tasksData as Task[]

const DOMAINS = [
  { value: 'all', label: 'All' },
  { value: 'corporate-investigation', label: 'Corporate Investigation' },
  { value: 'public-accountability', label: 'Public Accountability' },
  { value: 'open-source', label: 'Open Source' },
  { value: 'finance', label: 'Finance' },
  { value: 'science', label: 'Science' },
  { value: 'legal', label: 'Legal' },
]

const DIFFICULTIES = [
  { value: 'all', label: 'All Difficulties' },
  { value: 'easy', label: 'Easy' },
  { value: 'medium', label: 'Medium' },
  { value: 'hard', label: 'Hard' },
  { value: 'expert', label: 'Expert' },
]

export default function TasksPage() {
  const [domain, setDomain] = useState('all')
  const [difficulty, setDifficulty] = useState('all')
  const [search, setSearch] = useState('')

  const filtered = tasks.filter(t => {
    const matchDomain = domain === 'all' || t.domain === domain
    const matchDiff = difficulty === 'all' || t.difficulty === difficulty
    const matchSearch =
      search === '' ||
      t.title.toLowerCase().includes(search.toLowerCase()) ||
      t.short_description.toLowerCase().includes(search.toLowerCase()) ||
      t.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
    return matchDomain && matchDiff && matchSearch
  })

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-10">
        <p className="section-header">Benchmark</p>
        <h1 className="text-gray-100 mb-3">Tasks</h1>
        <p className="text-gray-400 text-sm max-w-2xl leading-relaxed">
          Each task is a real-world intelligence challenge backed by a public dataset. Pick a task,
          build your context engineering strategy, and submit your evidence-backed answer.
        </p>
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
        <input
          type="text"
          placeholder="Search tasks by title, description, or tag..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        {/* Domain filter */}
        <div>
          <p className="text-xs text-gray-500 mb-2">Domain</p>
          <div className="flex flex-wrap gap-2">
            {DOMAINS.map(d => (
              <button
                key={d.value}
                onClick={() => setDomain(d.value)}
                className={clsx(
                  'px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                  domain === d.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:text-gray-200 border border-gray-700'
                )}
              >
                {d.label}
              </button>
            ))}
          </div>
        </div>

        {/* Difficulty filter */}
        <div>
          <p className="text-xs text-gray-500 mb-2">Difficulty</p>
          <div className="flex flex-wrap gap-2">
            {DIFFICULTIES.map(d => (
              <button
                key={d.value}
                onClick={() => setDifficulty(d.value)}
                className={clsx(
                  'px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                  difficulty === d.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:text-gray-200 border border-gray-700'
                )}
              >
                {d.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Count */}
      <p className="text-sm text-gray-500 mb-6">
        Showing <span className="text-gray-300 font-medium">{filtered.length}</span> task{filtered.length !== 1 ? 's' : ''}
        {(domain !== 'all' || difficulty !== 'all' || search) && (
          <button
            onClick={() => { setDomain('all'); setDifficulty('all'); setSearch('') }}
            className="ml-3 text-blue-400 hover:text-blue-300 transition-colors"
          >
            Clear filters
          </button>
        )}
      </p>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(task => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="text-gray-400 text-sm">No tasks match your filters.</p>
          <button
            onClick={() => { setDomain('all'); setDifficulty('all'); setSearch('') }}
            className="btn-secondary text-sm mt-4"
          >
            Clear filters
          </button>
        </div>
      )}
    </div>
  )
}
