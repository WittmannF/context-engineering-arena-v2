// @ts-nocheck
import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import Hero from '../components/Hero'
import TaskCard from '../components/TaskCard'
import SubmissionCard from '../components/SubmissionCard'
import tasksData from '../data/generated/tasks.json'
import submissionsData from '../data/generated/submissions.json'
import type { Task, Submission } from '../types'

const tasks = tasksData as Task[]
const submissions = submissionsData as Submission[]

const HOW_IT_WORKS = [
  {
    step: '01',
    title: 'Pick a Task',
    description: 'Choose a real-world investigation from the task catalog. Each task comes with a public dataset, a benchmark question, and a scoring rubric.',
  },
  {
    step: '02',
    title: 'Build Your Strategy',
    description: 'Design your context engineering approach: which retrieval methods to use, how to structure your evidence, and what to include or ignore.',
  },
  {
    step: '03',
    title: 'Generate Your Answer',
    description: 'Run your strategy against the dataset and produce a structured intelligence page with claims, evidence, timeline, and entities.',
  },
  {
    step: '04',
    title: 'Submit to GitHub',
    description: 'Open a pull request with your answer JSON and context trace. The arena publishes your score and Context X-Ray alongside all other submissions.',
  },
]

export default function HomePage() {
  const featuredTasks = tasks.slice(0, 3)
  const latestSubmissions = submissions.slice(0, 3)

  const taskTitleMap = Object.fromEntries(tasks.map(t => [t.id, t.title]))

  return (
    <div>
      <Hero />

      {/* Featured Tasks */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <p className="section-header">Featured Tasks</p>
            <h2 className="text-gray-100">Benchmark Challenges</h2>
          </div>
          <Link to="/tasks" className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 transition-colors">
            View all tasks <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredTasks.map(task => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      </section>

      {/* Latest Submissions */}
      <section className="border-t border-gray-800 bg-gray-900/30">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="flex items-center justify-between mb-8">
            <div>
              <p className="section-header">Latest Submissions</p>
              <h2 className="text-gray-100">Strategy Results</h2>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {latestSubmissions.map(sub => (
              <SubmissionCard
                key={`${sub.task_id}-${sub.participant_id}`}
                submission={sub}
                taskTitle={taskTitleMap[sub.task_id]}
              />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <p className="section-header">Process</p>
          <h2 className="text-gray-100">How It Works</h2>
          <p className="text-gray-400 mt-3 max-w-2xl mx-auto text-sm leading-relaxed">
            Anyone can participate. Tasks use fully public datasets. All strategies are transparent.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {HOW_IT_WORKS.map(({ step, title, description }) => (
            <div key={step} className="relative">
              <div className="card h-full">
                <div className="text-4xl font-extrabold text-gray-800 mb-4">{step}</div>
                <h3 className="font-semibold text-gray-100 mb-2">{title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer CTA */}
      <section className="border-t border-gray-800 bg-gradient-to-br from-blue-950/20 to-gray-950">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h2 className="text-gray-100 mb-4">Ready to compete?</h2>
          <p className="text-gray-400 text-sm max-w-xl mx-auto mb-8 leading-relaxed">
            Fork the repo, pick a task, and build the clearest intelligence page from the messiest context.
            Your strategy will be judged on evidence quality, not just accuracy.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/tasks" className="btn-primary text-sm px-6 py-3">
              Browse Tasks
            </Link>
            <Link to="/propose" className="btn-secondary text-sm px-6 py-3">
              Propose a Task
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
