import { Link } from 'react-router-dom'
import { ExternalLink } from 'lucide-react'

const ROADMAP = [
  { status: 'done', label: 'Launch task catalog (3 tasks)' },
  { status: 'done', label: 'Baseline submissions for all tasks' },
  { status: 'done', label: 'Context X-Ray (context_trace.json schema)' },
  { status: 'in-progress', label: 'Automated scoring pipeline' },
  { status: 'in-progress', label: 'Task proposal workflow (GitHub issues)' },
  { status: 'planned', label: 'Entity graph visualization' },
  { status: 'planned', label: 'LLM-as-judge scoring option' },
  { status: 'planned', label: '10+ community tasks' },
  { status: 'planned', label: 'Leaderboard API for integrations' },
  { status: 'planned', label: 'Downloadable dataset of all answer JSONs' },
]

const STATUS_STYLE: Record<string, string> = {
  done: 'badge-green',
  'in-progress': 'badge-yellow',
  planned: 'badge-gray',
}

const STATUS_LABEL: Record<string, string> = {
  done: 'Done',
  'in-progress': 'In Progress',
  planned: 'Planned',
}

export default function AboutPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12 space-y-16">
      {/* What is context engineering */}
      <section>
        <p className="section-header">Foundation</p>
        <h1 className="text-gray-100 mb-6">About the Arena</h1>

        <div className="card space-y-4">
          <h2 className="text-gray-100">What is context engineering?</h2>
          <p className="text-gray-300 leading-relaxed">
            Context engineering is the discipline of deciding what information to give a language model,
            when, and in what form. It sits between prompt engineering (how you phrase the request) and
            traditional NLP (the statistical processing layer). In practice, context engineering covers:
          </p>
          <ul className="list-disc list-inside space-y-2 text-gray-300 text-sm leading-relaxed">
            <li>Which retrieval methods to use (keyword, semantic, hybrid)</li>
            <li>How to chunk, rank, and filter documents before putting them in context</li>
            <li>When to use multi-hop retrieval versus a single query</li>
            <li>What to deliberately exclude to stay within token budgets</li>
            <li>How to trace which context drove which claims in the final output</li>
          </ul>
        </div>
      </section>

      {/* Why this arena */}
      <section>
        <div className="card space-y-4">
          <h2 className="text-gray-100">Why does this arena exist?</h2>
          <p className="text-gray-300 leading-relaxed">
            Most LLM benchmarks test knowledge retrieval or reasoning in isolation. They do not test
            the end-to-end question of: given a real, messy corpus and a real investigation question,
            how good is your strategy for extracting and presenting evidence?
          </p>
          <p className="text-gray-300 leading-relaxed">
            The Context Engineering Arena fills that gap. Every task uses a public dataset that was
            not part of any LLM&rsquo;s training cutoff by default (or where training data is irrelevant
            because the task is about structure, not recall). Every answer must cite sources.
            Every strategy must be transparent about what it retrieved and what it ignored.
          </p>
          <p className="text-gray-300 leading-relaxed">
            The result is a benchmark where you cannot cheat by memorizing the answer — you have to
            actually build a good information extraction pipeline.
          </p>
        </div>
      </section>

      {/* How it differs from RAG benchmarks */}
      <section>
        <div className="card space-y-4">
          <h2 className="text-gray-100">How is this different from RAG benchmarks?</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm mt-2">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-3 px-3 text-xs font-semibold uppercase tracking-widest text-gray-500">Dimension</th>
                  <th className="text-left py-3 px-3 text-xs font-semibold uppercase tracking-widest text-gray-500">Typical RAG Benchmarks</th>
                  <th className="text-left py-3 px-3 text-xs font-semibold uppercase tracking-widest text-blue-400">Context Engineering Arena</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                {[
                  ['Answer format', 'Short factoid', 'Structured evidence page'],
                  ['Evaluation', 'Exact match / F1', 'Multi-dimension rubric'],
                  ['Evidence tracing', 'Not required', 'Required — every claim cited'],
                  ['Dataset size', 'Wikipedia-scale', 'Real-world noisy corpora'],
                  ['Strategy exposure', 'Hidden', 'Fully transparent (context_trace)'],
                  ['Token cost', 'Not measured', 'Scored dimension'],
                  ['Uncertainty', 'Not required', 'Required — known unknowns explicit'],
                ].map(([dim, rag, arena]) => (
                  <tr key={dim} className="border-b border-gray-800/50">
                    <td className="py-2.5 px-3 font-medium text-gray-200">{dim}</td>
                    <td className="py-2.5 px-3 text-gray-500">{rag}</td>
                    <td className="py-2.5 px-3 text-blue-300">{arena}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* What good submissions look like */}
      <section>
        <div className="card space-y-4">
          <h2 className="text-gray-100">What do good submissions look like?</h2>
          <p className="text-gray-300 leading-relaxed">
            A great submission scores well on all five dimensions:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              {
                label: 'Answer Quality (30%)',
                description: 'The narrative is accurate, specific, and directly addresses the benchmark question. It does not recite the question back — it answers it.',
              },
              {
                label: 'Evidence Quality (25%)',
                description: 'Every claim cites a verifiable source ID. Evidence excerpts match the claim. No fabricated citations.',
              },
              {
                label: 'Context Efficiency (20%)',
                description: 'The token budget is justified. The submission extracts maximum insight from minimum context — not the inverse.',
              },
              {
                label: 'Uncertainty Handling (15%)',
                description: 'Known unknowns are documented. The submission does not overclaim. Confidence levels are calibrated.',
              },
              {
                label: 'Visual Clarity (10%)',
                description: 'The page is readable. Sections are logical. A human analyst could use this document.',
              },
            ].map(({ label, description }) => (
              <div key={label} className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
                <p className="font-semibold text-sm text-gray-200 mb-2">{label}</p>
                <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Ethics */}
      <section>
        <div className="card border-orange-800/30 bg-orange-950/10 space-y-4">
          <h2 className="text-gray-100">Ethics Principles</h2>
          <ul className="space-y-3">
            {[
              'All tasks use fully public datasets. No private, leaked, or proprietary data.',
              'Submissions must not make false accusations against real individuals. Claims must be grounded in corpus evidence.',
              'Tasks involving sensitive subjects (e.g., corporate fraud) require safety notes and should explicitly bound the scope of conclusions.',
              'The arena does not endorse any conclusions drawn from the corpus. Baselines are illustrative, not authoritative.',
              'Any real-world harm discovered through arena tasks (e.g., ongoing data breaches) should be reported through appropriate channels before publication.',
              'AI-generated submissions should identify themselves as such in the participant metadata.',
            ].map((principle, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
                <span className="text-orange-400 font-bold mt-0.5 shrink-0">{i + 1}.</span>
                {principle}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Roadmap */}
      <section>
        <h2 className="text-gray-100 mb-6">Roadmap</h2>
        <div className="card space-y-3">
          {ROADMAP.map(({ status, label }) => (
            <div key={label} className="flex items-center gap-4">
              <span className={STATUS_STYLE[status] + ' w-24 justify-center shrink-0'}>
                {STATUS_LABEL[status]}
              </span>
              <span className="text-sm text-gray-300">{label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Get involved */}
      <section className="text-center pb-8">
        <h2 className="text-gray-100 mb-4">Get Involved</h2>
        <p className="text-gray-400 text-sm max-w-lg mx-auto mb-8 leading-relaxed">
          The arena is fully open source. Star the repo, propose a task, submit a strategy,
          or open an issue to discuss ideas.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="https://github.com/your-org/context-engineering-arena-v2"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary inline-flex items-center gap-2"
          >
            View on GitHub
            <ExternalLink className="h-4 w-4" />
          </a>
          <Link to="/propose" className="btn-secondary">
            Propose a Task
          </Link>
        </div>
      </section>
    </div>
  )
}
