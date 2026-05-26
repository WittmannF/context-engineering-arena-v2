// @ts-nocheck
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Zap, DollarSign, Clock, FileText } from 'lucide-react'
import Timeline from '../components/Timeline'
import ClaimsTable from '../components/ClaimsTable'
import EvidenceTable from '../components/EvidenceTable'
import EntityGraphPlaceholder from '../components/EntityGraphPlaceholder'
import RiskMatrix from '../components/RiskMatrix'
import ContextTracePanel from '../components/ContextTracePanel'
import ScoreBreakdown from '../components/ScoreBreakdown'
import StrategyBadge from '../components/StrategyBadge'
import JsonViewer from '../components/JsonViewer'
import EmptyState from '../components/EmptyState'
import MarkdownBlock from '../components/MarkdownBlock'
import submissionsData from '../data/generated/submissions.json'
import tasksData from '../data/generated/tasks.json'
import type { Submission, Task } from '../types'
import clsx from 'clsx'

const submissions = submissionsData as Submission[]
const tasks = tasksData as Task[]

function SectionWrapper({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="scroll-mt-20">
      <div className="border-b border-gray-800 pb-2 mb-6">
        <h2 className="text-gray-100">{title}</h2>
      </div>
      {children}
    </section>
  )
}

export default function SubmissionPage() {
  const { taskId, participantId } = useParams<{ taskId: string; participantId: string }>()

  const submission = submissions.find(
    s => s.task_id === taskId && s.participant_id === participantId
  )
  const task = tasks.find(t => t.id === taskId)

  if (!submission) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <EmptyState
          title="Submission not found"
          description="This submission does not exist or has not been indexed yet."
          actionLabel="Browse Tasks"
          actionTo="/tasks"
        />
      </div>
    )
  }

  const { answer, context_trace, score, participant } = submission
  const activeMethods = Object.entries(context_trace.methods)
    .filter(([, v]) => v)
    .map(([k]) => k)

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Back */}
      <Link
        to={`/tasks/${taskId}`}
        className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors mb-8"
      >
        <ArrowLeft className="h-4 w-4" />
        {task?.title ?? 'Task'}
      </Link>

      {/* 1. Header */}
      <div className="mb-10">
        <div className="flex flex-col lg:flex-row lg:items-start gap-6">
          <div className="flex-1">
            <p className="text-xs font-semibold uppercase tracking-widest text-gray-500 mb-1">
              {task?.title ?? taskId}
            </p>
            <h1 className="text-gray-100 mb-2">{answer.title}</h1>
            <p className="text-sm text-gray-400 mb-4">{participant.display_name} &bull; {participant.type}</p>

            {/* Method badges */}
            <div className="flex flex-wrap gap-2">
              {Object.entries(context_trace.methods).map(([key, active]) => (
                <StrategyBadge key={key} method={key} active={active} />
              ))}
            </div>
          </div>

          {/* Score */}
          {score && (
            <div className="lg:w-64">
              <ScoreBreakdown score={score} />
            </div>
          )}
        </div>
      </div>

      {/* 2. Stats bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        {[
          {
            icon: <Zap className="h-5 w-5 text-yellow-400" />,
            label: 'Tokens in Context',
            value: context_trace.stats.total_tokens_in_context.toLocaleString(),
          },
          {
            icon: <DollarSign className="h-5 w-5 text-green-400" />,
            label: 'Estimated Cost',
            value: `$${context_trace.stats.estimated_cost_usd.toFixed(4)}`,
          },
          {
            icon: <Clock className="h-5 w-5 text-blue-400" />,
            label: 'Latency',
            value: `${context_trace.stats.latency_seconds}s`,
          },
          {
            icon: <FileText className="h-5 w-5 text-purple-400" />,
            label: 'Documents Used',
            value: `${context_trace.stats.documents_used_in_answer} / ${context_trace.stats.documents_available.toLocaleString()}`,
          },
        ].map(({ icon, label, value }) => (
          <div key={label} className="card flex items-center gap-3">
            <div className="shrink-0">{icon}</div>
            <div>
              <p className="text-[10px] uppercase tracking-widest text-gray-500">{label}</p>
              <p className="text-sm font-semibold text-gray-200 tabular-nums">{value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-14">
        {/* 3. Executive Summary */}
        <SectionWrapper id="summary" title="Executive Summary">
          <div className="card">
            <p className="text-gray-300 leading-relaxed">{answer.executive_summary}</p>
          </div>
        </SectionWrapper>

        {/* Answer Sections */}
        {answer.sections.length > 0 && (
          <SectionWrapper id="analysis" title="Analysis">
            <div className="space-y-6">
              {answer.sections.map(section => (
                <div key={section.id} className="card">
                  <h3 className="text-gray-100 mb-3">{section.title}</h3>
                  <MarkdownBlock content={section.content} />
                </div>
              ))}
            </div>
          </SectionWrapper>
        )}

        {/* 4. Timeline */}
        {answer.timeline && answer.timeline.length > 0 && (
          <SectionWrapper id="timeline" title="Timeline">
            <div className="card">
              <Timeline items={answer.timeline} />
            </div>
          </SectionWrapper>
        )}

        {/* 5. Claims */}
        {answer.claims.length > 0 && (
          <SectionWrapper id="claims" title={`Claims (${answer.claims.length})`}>
            <div className="card p-0 overflow-hidden">
              <ClaimsTable claims={answer.claims} />
            </div>
          </SectionWrapper>
        )}

        {/* 6. Evidence */}
        {answer.evidence.length > 0 && (
          <SectionWrapper id="evidence" title={`Evidence (${answer.evidence.length})`}>
            <div className="card p-0 overflow-hidden">
              <EvidenceTable evidence={answer.evidence} />
            </div>
          </SectionWrapper>
        )}

        {/* 7. Entities */}
        {answer.entities && answer.entities.length > 0 && (
          <SectionWrapper id="entities" title={`Entities (${answer.entities.length})`}>
            <EntityGraphPlaceholder entities={answer.entities} />
          </SectionWrapper>
        )}

        {/* 8. Risks */}
        {answer.risks && answer.risks.length > 0 && (
          <SectionWrapper id="risks" title={`Risks (${answer.risks.length})`}>
            <RiskMatrix risks={answer.risks} />
          </SectionWrapper>
        )}

        {/* 9. Recommendations */}
        {answer.recommendations && answer.recommendations.length > 0 && (
          <SectionWrapper id="recommendations" title="Recommendations">
            <div className="space-y-3">
              {answer.recommendations.map((rec, i) => (
                <div
                  key={rec.id}
                  className={clsx(
                    'flex gap-4 p-4 rounded-xl border',
                    rec.priority === 'high'
                      ? 'border-blue-700/50 bg-blue-950/20'
                      : rec.priority === 'medium'
                      ? 'border-gray-700 bg-gray-800/30'
                      : 'border-gray-800 bg-gray-900/30'
                  )}
                >
                  <span className="text-blue-400 font-bold text-sm mt-0.5 shrink-0">{i + 1}.</span>
                  <div className="flex-1">
                    <p className="text-sm text-gray-300 leading-relaxed">{rec.text}</p>
                    {rec.evidence_ids && rec.evidence_ids.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {rec.evidence_ids.map(eid => (
                          <span key={eid} className="badge-blue text-[10px] px-1.5">{eid}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  {rec.priority && (
                    <span className={clsx(
                      'badge shrink-0 text-[10px]',
                      rec.priority === 'high' ? 'badge-red' : rec.priority === 'medium' ? 'badge-yellow' : 'badge-gray'
                    )}>
                      {rec.priority}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </SectionWrapper>
        )}

        {/* 10. Uncertainties */}
        {answer.uncertainties && answer.uncertainties.length > 0 && (
          <SectionWrapper id="uncertainties" title="Uncertainties">
            <div className="space-y-3">
              {answer.uncertainties.map(unc => (
                <div key={unc.id} className="card space-y-2">
                  <p className="text-sm text-gray-300 leading-relaxed">{unc.description}</p>
                  {unc.impact && (
                    <p className="text-xs text-yellow-400">
                      <strong>Impact:</strong> {unc.impact}
                    </p>
                  )}
                  {unc.resolution_path && (
                    <p className="text-xs text-gray-500">
                      <strong className="text-gray-400">Resolution path:</strong> {unc.resolution_path}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </SectionWrapper>
        )}

        {/* 11. Context X-Ray */}
        <SectionWrapper id="context-trace" title="Context X-Ray">
          <div className="card">
            <ContextTracePanel trace={context_trace} />
          </div>
        </SectionWrapper>

        {/* 12. Limitations */}
        {answer.limitations && answer.limitations.length > 0 && (
          <SectionWrapper id="limitations" title="Limitations">
            <div className="card">
              <ul className="space-y-2">
                {answer.limitations.map((lim, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-gray-400">
                    <span className="text-gray-600 mt-1 shrink-0">—</span>
                    {lim}
                  </li>
                ))}
              </ul>
            </div>
          </SectionWrapper>
        )}

        {/* 13. Raw JSON */}
        <SectionWrapper id="raw" title="Raw Data">
          <div className="space-y-3">
            <JsonViewer data={answer} label="answer.json" />
            <JsonViewer data={context_trace} label="context_trace.json" />
            {score && <JsonViewer data={score} label="score.json" />}
          </div>
        </SectionWrapper>
      </div>

      {/* Active methods summary in sticky bottom bar could go here, but keep it clean */}
      {activeMethods.length > 0 && (
        <div className="mt-12 pt-8 border-t border-gray-800">
          <p className="text-xs text-gray-500 mb-2">Active strategies in this submission</p>
          <div className="flex flex-wrap gap-2">
            {activeMethods.map(m => (
              <StrategyBadge key={m} method={m} active />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
