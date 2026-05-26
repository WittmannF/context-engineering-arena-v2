import { ExternalLink, Check, X } from 'lucide-react'

const GOOD_TASK_CRITERIA = [
  'Uses a fully public dataset that anyone can download or query via API',
  'Has a specific, answerable benchmark question — not "tell me about X"',
  'Rewards evidence quality: good answers cite specific documents',
  'Has a plausible difficulty level (medium–expert is the sweet spot)',
  'Has a scoring rubric draft with 3–5 weighted dimensions',
  'Is reproducible: anyone starting fresh can get the same data',
  'Has real-world significance: an investigator or analyst would actually care',
  'Can be completed in a reasonable token budget (under $1 in API costs)',
]

const BAD_TASK_CRITERIA = [
  'Requires proprietary or paywalled data',
  'The answer is fully known and unambiguous (there\'s no "context engineering" needed)',
  'Too broad: "summarize the internet in 2020"',
  'Depends on real-time or unstable data sources',
  'Requires domain expertise to evaluate (no rubric can be written)',
  'Could embarrass or endanger real individuals',
  'The "correct" answer requires illegal data access',
]

const STEPS = [
  {
    number: '01',
    title: 'Check existing tasks',
    description: 'Read through the current task catalog to ensure your idea is not already covered. Similar tasks in different domains are fine.',
  },
  {
    number: '02',
    title: 'Verify the dataset',
    description: 'Download or access the dataset yourself. Confirm it is publicly accessible, note the license, and estimate its size.',
  },
  {
    number: '03',
    title: 'Draft the benchmark question',
    description: 'Write the single question that a submission must answer. It should be specific, evidence-demanding, and appropriately hard.',
  },
  {
    number: '04',
    title: 'Write a scoring rubric',
    description: 'Define 3–5 scoring dimensions with weights that sum to 100. Each dimension should be assessable without running the model again.',
  },
  {
    number: '05',
    title: 'Open a GitHub issue',
    description: 'Use the "Propose Task" issue template. Fill in all required fields. Include a sample answer sketch to demonstrate the task is solvable.',
  },
  {
    number: '06',
    title: 'Discussion and approval',
    description: 'Maintainers and community members will review and suggest refinements. Approved tasks are merged into the task catalog.',
  },
]

const CHECKLIST = [
  'Dataset URL is public and stable (not a personal Dropbox)',
  'License permits research and derivative works',
  'Benchmark question is a single sentence',
  'Scoring rubric has 3–5 dimensions with weights summing to 100',
  'Safety notes address any sensitive content in the dataset',
  'I have verified I can access the dataset right now',
  'Estimated difficulty is justified with reasoning',
  'I have sketched a plausible (if imperfect) answer',
]

export default function ProposeTaskPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-10">
        <p className="section-header">Community</p>
        <h1 className="text-gray-100 mb-4">Propose a Task</h1>
        <p className="text-gray-400 leading-relaxed max-w-2xl">
          The task catalog is community-driven. If you have a real-world intelligence challenge
          backed by a public dataset, you can propose it for the arena. The best tasks are those
          where the evidence matters — not just the answer.
        </p>
      </div>

      {/* Good vs Bad */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <div className="card border-green-800/40 bg-green-950/10">
          <h3 className="text-green-300 mb-4 flex items-center gap-2">
            <Check className="h-5 w-5" />
            What makes a good task
          </h3>
          <ul className="space-y-2">
            {GOOD_TASK_CRITERIA.map((c, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                <Check className="h-3.5 w-3.5 text-green-500 mt-0.5 shrink-0" />
                {c}
              </li>
            ))}
          </ul>
        </div>

        <div className="card border-red-800/40 bg-red-950/10">
          <h3 className="text-red-300 mb-4 flex items-center gap-2">
            <X className="h-5 w-5" />
            What makes a bad task
          </h3>
          <ul className="space-y-2">
            {BAD_TASK_CRITERIA.map((c, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                <X className="h-3.5 w-3.5 text-red-500 mt-0.5 shrink-0" />
                {c}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Steps */}
      <div className="mb-12">
        <h2 className="text-gray-100 mb-8">How to Propose</h2>
        <div className="space-y-6">
          {STEPS.map(({ number, title, description }) => (
            <div key={number} className="flex gap-6">
              <div className="shrink-0 flex h-10 w-10 items-center justify-center rounded-full bg-gray-800 border border-gray-700 text-sm font-bold text-gray-400">
                {number}
              </div>
              <div className="flex-1 pt-1">
                <h3 className="font-semibold text-gray-200 mb-1">{title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Checklist */}
      <div className="mb-12">
        <h2 className="text-gray-100 mb-6">Quality Checklist</h2>
        <div className="card space-y-3">
          <p className="text-sm text-gray-400 mb-4">
            Before opening the issue, verify all of the following:
          </p>
          {CHECKLIST.map((item, i) => (
            <label key={i} className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                className="mt-0.5 h-4 w-4 rounded border-gray-600 bg-gray-800 text-blue-600 focus:ring-blue-500 focus:ring-offset-0 focus:ring-offset-gray-900 cursor-pointer"
              />
              <span className="text-sm text-gray-300 group-hover:text-gray-100 transition-colors">{item}</span>
            </label>
          ))}
        </div>
      </div>

      {/* CTA */}
      <div className="card border-blue-700/40 bg-blue-950/10 text-center">
        <h3 className="text-gray-100 mb-3">Ready to propose?</h3>
        <p className="text-sm text-gray-400 mb-6 max-w-md mx-auto">
          Open a GitHub issue using the task proposal template. Maintainers typically respond within a week.
        </p>
        <a
          href="https://github.com/your-org/context-engineering-arena-v2/issues/new?template=propose-task.yml"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary inline-flex items-center gap-2"
        >
          Open Proposal Issue
          <ExternalLink className="h-4 w-4" />
        </a>
        <p className="text-xs text-gray-600 mt-4">
          You will need a GitHub account. All proposals are public.
        </p>
      </div>
    </div>
  )
}
