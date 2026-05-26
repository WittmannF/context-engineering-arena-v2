// @ts-nocheck
import { useParams, Link } from 'react-router-dom'
import { ExternalLink, ArrowLeft, Tag } from 'lucide-react'
import DatasetStats from '../components/DatasetStats'
import LeaderboardTable from '../components/LeaderboardTable'
import EmptyState from '../components/EmptyState'
import tasksData from '../data/generated/tasks.json'
import submissionsData from '../data/generated/submissions.json'
import leaderboardData from '../data/generated/leaderboard.json'
import type { Task, Submission, LeaderboardEntry } from '../types'
import clsx from 'clsx'

const tasks = tasksData as Task[]
const submissions = submissionsData as Submission[]
const leaderboard = leaderboardData as LeaderboardEntry[]

const difficultyStyle: Record<string, string> = {
  easy: 'badge-green',
  medium: 'badge-yellow',
  hard: 'badge-red',
  expert: 'badge-purple',
}

const domainLabels: Record<string, string> = {
  'corporate-investigation': 'Corporate Investigation',
  'public-accountability': 'Public Accountability',
  'open-source': 'Open Source',
  'finance': 'Finance',
  'science': 'Science',
  'legal': 'Legal',
}

export default function TaskDetailPage() {
  const { taskId } = useParams<{ taskId: string }>()
  const task = tasks.find(t => t.id === taskId)

  if (!task) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <EmptyState
          title="Task not found"
          description="This task does not exist or has been removed."
          actionLabel="Browse Tasks"
          actionTo="/tasks"
        />
      </div>
    )
  }

  const taskLeaderboard = leaderboard.find(lb => lb.task_id === taskId)
  const taskSubmissions = submissions.filter(s => s.task_id === taskId)

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      {/* Back navigation */}
      <Link to="/tasks" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors mb-8">
        <ArrowLeft className="h-4 w-4" />
        All tasks
      </Link>

      {/* Header */}
      <div className="mb-10">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className={clsx(difficultyStyle[task.difficulty] ?? 'badge-gray')}>
            {task.difficulty}
          </span>
          <span className="badge-blue">
            {domainLabels[task.domain] ?? task.domain}
          </span>
        </div>

        <h1 className="text-gray-100 mb-4">{task.title}</h1>

        <p className="text-gray-400 leading-relaxed max-w-3xl mb-4">
          {task.short_description}
        </p>

        {task.long_description && (
          <p className="text-gray-500 text-sm leading-relaxed max-w-3xl">
            {task.long_description}
          </p>
        )}

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mt-4">
          {task.tags.map(tag => (
            <span key={tag} className="badge-gray flex items-center gap-1">
              <Tag className="h-2.5 w-2.5" />
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Benchmark Question */}
          <div>
            <p className="section-header">Benchmark Question</p>
            <div className="bg-blue-950/30 border border-blue-800/40 rounded-xl p-5">
              <p className="text-blue-200 leading-relaxed font-medium text-base">
                &ldquo;{task.benchmark_question}&rdquo;
              </p>
            </div>
          </div>

          {/* Required Outputs */}
          {task.outputs && (task.outputs as any).required_sections?.length > 0 && (
            <div>
              <p className="section-header">Required Output Sections</p>
              <div className="card">
                <ul className="space-y-2">
                  {((task.outputs as any).required_sections as string[]).map((output: string, i: number) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
                      <span className="text-blue-400 font-bold mt-0.5 shrink-0">{i + 1}.</span>
                      {output}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Scoring Dimensions */}
          {task.scoring && (task.scoring as any).dimensions?.length > 0 && (
            <div>
              <p className="section-header">Scoring Dimensions</p>
              <div className="card space-y-2">
                {((task.scoring as any).dimensions as string[]).map((dim: string, i: number) => (
                  <div key={i} className="flex items-center gap-2 text-sm text-gray-300">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400 shrink-0" />
                    {dim}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Safety Notes */}
          {task.safety && (task.safety as any).recommended_mitigations?.length > 0 && (
            <div>
              <p className="section-header">Safety Notes</p>
              <div className="bg-orange-950/20 border border-orange-800/40 rounded-xl p-4 text-sm text-orange-200 space-y-1">
                {((task.safety as any).recommended_mitigations as string[]).map((note: string, i: number) => (
                  <p key={i}>• {note}</p>
                ))}
              </div>
            </div>
          )}

          {/* Submit instructions */}
          <div>
            <p className="section-header">Submit a Strategy</p>
            <div className="card">
              <p className="text-sm text-gray-400 mb-4 leading-relaxed">
                Submissions are made via GitHub pull request. Your PR should include an{' '}
                <code className="bg-gray-800 text-blue-300 px-1.5 py-0.5 rounded text-xs font-mono">answer.json</code> and{' '}
                <code className="bg-gray-800 text-blue-300 px-1.5 py-0.5 rounded text-xs font-mono">context_trace.json</code> in the correct directory.
              </p>
              <div className="bg-gray-800 rounded-lg p-3 font-mono text-xs text-gray-300 mb-4 overflow-x-auto">
                <div>submissions/</div>
                <div className="ml-4">{task.id}/</div>
                <div className="ml-8">your-participant-id/</div>
                <div className="ml-12">answer.json</div>
                <div className="ml-12">context_trace.json</div>
              </div>
              <a
                href={`https://github.com/your-org/context-engineering-arena-v2/issues/new?template=propose-task.yml&title=Submission:+${task.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-sm inline-flex items-center gap-2"
              >
                Open Submission PR
                <ExternalLink className="h-3.5 w-3.5" />
              </a>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Dataset */}
          <div>
            <p className="section-header">Dataset</p>
            <DatasetStats dataset={task.dataset} />
          </div>

          {/* Quick stats */}
          <div className="card space-y-3">
            <p className="section-header !mb-2">Stats</p>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Submissions</span>
              <span className="text-gray-200 font-medium">{task.submission_count ?? 0}</span>
            </div>
            {task.best_score !== undefined && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Best Score</span>
                <span className={clsx(
                  'font-bold',
                  task.best_score >= 70 ? 'text-green-400' : task.best_score >= 50 ? 'text-yellow-400' : 'text-red-400'
                )}>
                  {task.best_score}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Leaderboard */}
      <div className="mt-12">
        <p className="section-header">Leaderboard</p>
        <h2 className="text-gray-100 mb-6">Submissions</h2>

        {taskLeaderboard && taskLeaderboard.rankings.length > 0 ? (
          <div className="card p-0 overflow-hidden">
            <LeaderboardTable
              leaderboard={taskLeaderboard}
              submissions={taskSubmissions}
              taskId={task.id}
            />
          </div>
        ) : (
          <EmptyState
            title="No submissions yet"
            description="Be the first to submit a strategy for this task."
            actionLabel="Submit a Strategy"
            actionHref="https://github.com/your-org/context-engineering-arena-v2"
          />
        )}
      </div>
    </div>
  )
}
