import { Link } from 'react-router-dom'
import { Database, Star, Users, ChevronRight } from 'lucide-react'
import type { Task } from '../types'
import clsx from 'clsx'

interface TaskCardProps {
  task: Task
}

const domainColors: Record<string, string> = {
  'corporate-investigation': 'badge-red',
  'public-accountability': 'badge-blue',
  'open-source': 'badge-green',
  'finance': 'badge-yellow',
  'science': 'badge-purple',
  'legal': 'badge-yellow',
}

const domainLabels: Record<string, string> = {
  'corporate-investigation': 'Corporate Investigation',
  'public-accountability': 'Public Accountability',
  'open-source': 'Open Source',
  'finance': 'Finance',
  'science': 'Science',
  'legal': 'Legal',
}

const difficultyColors: Record<string, string> = {
  easy: 'badge-green',
  medium: 'badge-yellow',
  hard: 'badge-red',
  expert: 'badge-purple',
}

function scoreColor(score: number): string {
  if (score >= 70) return 'text-green-400'
  if (score >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

export default function TaskCard({ task }: TaskCardProps) {
  return (
    <Link
      to={`/tasks/${task.id}`}
      className="card flex flex-col gap-4 hover:border-gray-700 hover:bg-gray-800/50 transition-all group"
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-wrap gap-2">
          <span className={clsx(domainColors[task.domain] ?? 'badge-gray')}>
            {domainLabels[task.domain] ?? task.domain}
          </span>
          <span className={clsx(difficultyColors[task.difficulty] ?? 'badge-gray')}>
            {task.difficulty}
          </span>
        </div>
        <ChevronRight className="h-4 w-4 text-gray-600 group-hover:text-gray-400 transition-colors shrink-0 mt-0.5" />
      </div>

      {/* Title */}
      <div>
        <h3 className="font-semibold text-gray-100 group-hover:text-blue-300 transition-colors leading-snug">
          {task.title}
        </h3>
        <p className="text-sm text-gray-400 mt-2 leading-relaxed line-clamp-3">
          {task.short_description}
        </p>
      </div>

      {/* Dataset info */}
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <Database className="h-3.5 w-3.5 shrink-0" />
        <span className="truncate">{task.dataset.name}</span>
      </div>

      {/* Tags */}
      {task.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {task.tags.slice(0, 4).map((tag) => (
            <span key={tag} className="badge-gray text-[10px] px-2">
              {tag}
            </span>
          ))}
          {task.tags.length > 4 && (
            <span className="badge-gray text-[10px] px-2">+{task.tags.length - 4}</span>
          )}
        </div>
      )}

      {/* Stats footer */}
      <div className="flex items-center justify-between pt-2 border-t border-gray-800 mt-auto">
        <div className="flex items-center gap-4 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <Users className="h-3 w-3" />
            {task.submission_count ?? 0} submissions
          </span>
        </div>
        {task.best_score !== undefined && (
          <span className="flex items-center gap-1 text-xs font-medium">
            <Star className="h-3 w-3 text-gray-500" />
            <span className={scoreColor(task.best_score)}>
              {task.best_score}
            </span>
          </span>
        )}
      </div>
    </Link>
  )
}
