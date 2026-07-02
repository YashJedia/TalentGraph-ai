import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { Users, ShieldCheck, CheckCircle2, AlertTriangle, Briefcase, Sliders, Sparkles } from 'lucide-react'

type Candidate = {
  id: string
  anonymized_name: string
  current_title?: string
  current_company?: string
  years_of_experience?: number
  location?: string
}

type ComparisonCandidate = {
  id: string
  candidate_id: string
  candidate?: {
    anonymized_name?: string
    current_title?: string
  }
  rank: number
  final_score: number
  is_hidden_gem: boolean
  is_fraud_flagged: boolean
}

type ComparisonResult = {
  candidates: ComparisonCandidate[]
  comparison_metrics: Record<string, unknown>
  recommendations: string[]
}

type Job = {
  id: string
  job_title: string
  company_name: string
}

export default function CandidateComparison() {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [jobs, setJobs] = useState<Job[]>([])
  const [selectedJobId, setSelectedJobId] = useState('')
  const [selectedCandidateIds, setSelectedCandidateIds] = useState<string[]>([])
  const [comparison, setComparison] = useState<ComparisonResult | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function loadData() {
      try {
        const [candidatesResponse, jobsResponse] = await Promise.all([
          api.getCandidates(),
          api.getJobs(),
        ])
        setCandidates(candidatesResponse.data)
        setJobs(jobsResponse.data)
      } catch (error) {
        console.error('Comparison page load failed', error)
      }
    }
    loadData()
  }, [])

  const toggleCandidateSelection = (candidateId: string) => {
    setSelectedCandidateIds((prev) =>
      prev.includes(candidateId) ? prev.filter((id) => id !== candidateId) : prev.length < 5 ? [...prev, candidateId] : prev
    )
  }

  const handleCompare = async () => {
    if (!selectedJobId || selectedCandidateIds.length < 2) {
      return
    }
    setLoading(true)
    try {
      const response = await api.compareCandidates(selectedCandidateIds, selectedJobId)
      setComparison(response.data)
    } catch (error) {
      console.error('Candidate comparison failed', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
          Candidate Comparison
        </h1>
        <p className="mt-2 text-sm text-slate-400 max-w-2xl">
          Conduct side-by-side matches for multiple profiles to determine role positioning metrics.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        {/* Left card selection */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 flex flex-col gap-6 h-fit">
          <div className="border-b border-slate-900 pb-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Briefcase size={16} className="text-sky-400" />
              Target Position Setup
            </h2>
            <p className="text-xs text-slate-400">Choose the job role that will guide weight distributions.</p>
          </div>

          <div className="space-y-4">
            <select
              value={selectedJobId}
              onChange={(event) => setSelectedJobId(event.target.value)}
              className="w-full rounded-xl border border-slate-800 bg-slate-900/30 px-3.5 py-3 text-sm text-slate-100 outline-none focus:border-sky-500"
            >
              <option value="" className="bg-slate-950">Select a job target</option>
              {jobs.map((job) => (
                <option key={job.id} value={job.id} className="bg-slate-950">
                  {job.job_title} ({job.company_name})
                </option>
              ))}
            </select>

            <div className="flex items-center justify-between text-xs rounded-xl border border-slate-800/80 bg-slate-900/10 p-4">
              <span className="text-slate-400 font-bold uppercase tracking-wider">Loaded comparisons:</span>
              <span className="font-mono font-black text-white px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/15">
                {selectedCandidateIds.length} / 5 Selected
              </span>
            </div>

            <button
              type="button"
              onClick={handleCompare}
              disabled={!selectedJobId || selectedCandidateIds.length < 2 || loading}
              className="w-full rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-3 text-xs font-bold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Evaluating details...' : 'Generate Matrix Comparison'}
            </button>
          </div>
        </div>

        {/* Right Candidate selection list */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 flex flex-col gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-1.5">
              <Users size={16} className="text-sky-400" />
              Candidate Roster
            </h2>
            <p className="text-xs text-slate-400">Match up to 5 profiles for evaluation.</p>
          </div>

          <div className="space-y-2.5 max-h-[460px] overflow-y-auto pr-1">
            {candidates.length === 0 ? (
              <div className="h-20 rounded-xl shimmer-placeholder" />
            ) : (
              candidates.map((candidate) => {
                const isSelected = selectedCandidateIds.includes(candidate.id)
                return (
                  <button
                    key={candidate.id}
                    onClick={() => toggleCandidateSelection(candidate.id)}
                    className={`w-full rounded-2xl border p-4 text-left transition-all ${
                      isSelected
                        ? 'border-sky-500/35 bg-sky-500/5 text-white glow-card scale-[1.01]'
                        : 'border-slate-800 bg-slate-900/30 text-slate-300 hover:border-slate-700/60 hover:bg-slate-900/50'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className={`font-bold text-sm ${isSelected ? 'text-sky-400' : 'text-white'}`}>
                          {candidate.anonymized_name}
                        </p>
                        <p className="text-[10px] text-slate-500 mt-0.5">{candidate.current_title || 'Expert candidate'}</p>
                      </div>
                      <span className="text-[10px] font-bold font-mono rounded bg-slate-900 px-2 py-0.5 border border-slate-800/80 text-slate-400">
                        {candidate.years_of_experience ?? 0} yrs
                      </span>
                    </div>
                  </button>
                )
              })
            )}
          </div>
        </div>
      </div>

      {/* Comparison results */}
      {comparison && (
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 space-y-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-1.5">
                <Sliders size={16} className="text-sky-400" />
                Comparison Score Matrix
              </h2>
              <p className="text-xs text-slate-400">Check calculated scores, hidden gems, and security attributes.</p>
            </div>
            <span className="rounded-xl bg-slate-900 border border-slate-800 px-3.5 py-1.5 text-xs text-slate-400">
              {comparison.candidates.length} Profiles Compared
            </span>
          </div>

          {/* Result grid table */}
          <div className="overflow-hidden rounded-xl border border-slate-900 bg-slate-950/20">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-900/80 text-left text-xs text-slate-300">
                <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider font-bold">
                  <tr>
                    <th className="px-5 py-3.5">Candidate name</th>
                    <th className="px-5 py-3.5 text-center">Rank</th>
                    <th className="px-5 py-3.5 text-center">Engine score</th>
                    <th className="px-5 py-3.5 text-center">Talent Status</th>
                    <th className="px-5 py-3.5 text-center">Compliance</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/40">
                  {comparison.candidates.map((item) => (
                    <tr key={item.id} className="transition hover:bg-slate-900/35">
                      <td className="px-5 py-4">
                        <div className="font-bold text-white">{item.candidate?.anonymized_name ?? item.candidate_id}</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">{item.candidate?.current_title ?? 'Expert Candidate'}</div>
                      </td>
                      <td className="px-5 py-4 text-center font-black text-slate-200">
                        {item.rank}
                      </td>
                      <td className="px-5 py-4 text-center">
                        <span className="inline-flex rounded-lg bg-indigo-500/5 border border-indigo-500/10 px-2.5 py-1 font-bold text-indigo-400 font-mono">
                          {Math.round(item.final_score * 100)}%
                        </span>
                      </td>
                      <td className="px-5 py-4 text-center">
                        {item.is_hidden_gem ? (
                          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 text-[10px] font-bold text-emerald-400">
                            <Sparkles size={10} /> Hidden Gem
                          </span>
                        ) : (
                          <span className="text-[10px] text-slate-500 font-semibold">Standard</span>
                        )}
                      </td>
                      <td className="px-5 py-4 text-center">
                        {item.is_fraud_flagged ? (
                          <span className="inline-flex items-center gap-1 rounded-full bg-rose-500/10 border border-rose-500/20 px-2.5 py-0.5 text-[10px] font-bold text-rose-400 leading-none">
                            <AlertTriangle size={10} /> Flagged
                          </span>
                        ) : (
                          <span className="text-[10px] text-emerald-400 font-bold">Clear</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recommendations block */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/10 p-5 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
              <ShieldCheck size={16} className="text-emerald-400" />
              Recruiter Strategy Recommendations
            </h3>
            <ul className="grid gap-2 text-xs text-slate-400">
              {comparison.recommendations.map((item, idx) => (
                <li key={idx} className="flex gap-2 items-start bg-slate-950/20 border border-slate-900/50 p-3 rounded-lg leading-relaxed">
                  <CheckCircle2 size={14} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
