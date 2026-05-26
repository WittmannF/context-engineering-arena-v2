import { Link } from 'react-router-dom'
import { ExternalLink, Shield, Eye, Package } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-950/30 via-gray-950 to-gray-950 pointer-events-none" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-blue-600/5 rounded-full blur-3xl pointer-events-none" />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 sm:py-28">
        {/* Badge */}
        <div className="flex justify-center mb-8">
          <span className="badge-blue text-xs px-3 py-1">
            Open Benchmark &bull; Community Driven
          </span>
        </div>

        {/* Headline */}
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-100 mb-6">
            Context Engineering{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-blue-600">
              Arena
            </span>
          </h1>
          <p className="text-xl sm:text-2xl text-gray-400 font-light mb-4">
            Build the clearest page from the messiest context.
          </p>
          <p className="text-base text-gray-500 max-w-2xl mx-auto leading-relaxed">
            A community benchmark where participants compete to transform raw, noisy data — emails,
            government records, event streams — into structured, evidence-backed intelligence pages.
            Every claim needs a source. Every strategy is exposed.
          </p>
        </div>

        {/* CTA buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10">
          <Link to="/tasks" className="btn-primary text-sm px-6 py-3 w-full sm:w-auto text-center">
            Explore Tasks
          </Link>
          <a
            href="https://github.com/your-org/context-engineering-arena-v2"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary text-sm px-6 py-3 w-full sm:w-auto text-center flex items-center justify-center gap-2"
          >
            Submit a Strategy
            <ExternalLink className="h-4 w-4" />
          </a>
          <Link to="/propose" className="text-sm font-medium text-gray-400 hover:text-gray-200 transition-colors px-6 py-3 w-full sm:w-auto text-center">
            Propose a Task &rarr;
          </Link>
        </div>

        {/* Stats row */}
        <div className="flex flex-wrap items-center justify-center gap-8 mt-14 pt-10 border-t border-gray-800">
          {[
            { value: '3', label: 'Active Tasks' },
            { value: '4', label: 'Submissions' },
            { value: '3', label: 'Domains' },
            { value: '100%', label: 'Open Source' },
          ].map(({ value, label }) => (
            <div key={label} className="text-center">
              <div className="text-2xl font-bold text-gray-100">{value}</div>
              <div className="text-xs text-gray-500 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Feature cards */}
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card flex flex-col gap-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-900/50 border border-green-700/50">
              <Shield className="h-5 w-5 text-green-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-100 mb-2">Evidence-backed Pages</h3>
              <p className="text-sm text-gray-400 leading-relaxed">
                Every claim must cite a source. The scoring rubric rewards structured evidence,
                not confident hallucination. Sources are traced back to raw data.
              </p>
            </div>
          </div>

          <div className="card flex flex-col gap-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-900/50 border border-blue-700/50">
              <Eye className="h-5 w-5 text-blue-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-100 mb-2">Context X-Ray</h3>
              <p className="text-sm text-gray-400 leading-relaxed">
                Inspect the invisible decisions behind every answer. See which documents were retrieved,
                which were ignored, and exactly what tokens were spent.
              </p>
            </div>
          </div>

          <div className="card flex flex-col gap-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-900/50 border border-purple-700/50">
              <Package className="h-5 w-5 text-purple-400" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-100 mb-2">Open Task Marketplace</h3>
              <p className="text-sm text-gray-400 leading-relaxed">
                Community-designed real-world benchmarks. Tasks use public datasets — anyone can
                reproduce, challenge, and build on any result.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
