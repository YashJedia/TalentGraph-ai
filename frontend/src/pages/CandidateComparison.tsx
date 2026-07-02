import { useEffect, useState } from 'react'
import { api } from '../services/api'

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
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-semibold text-white">Candidate Comparison</h1>
        <p className="mt-3 text-slate-400 max-w-2xl">Compare multiple candidate profiles side-by-side for hiring decisions.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white">Select role</h2>
              <p className="mt-2 text-sm text-slate-400">Choose the job that will guide the comparison scores.</p>
            </div>
          </div>

          <select
            value={selectedJobId}
            onChange={(event) => setSelectedJobId(event.target.value)}
            className="mt-5 w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-4 text-slate-100 outline-none focus:border-sky-500"
          >
            <option value="">Select a job</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.job_title} — {job.company_name}
              </option>
            ))}
          </select>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-950/95 p-5">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Selected candidates</p>
            <p className="mt-2 text-slate-300">{selectedCandidateIds.length} / 5</p>
          </div>

          <button
            type="button"
            onClick={handleCompare}
            disabled={!selectedJobId || selectedCandidateIds.length < 2 || loading}
            className="mt-6 w-full rounded-3xl bg-gradient-to-r from-sky-500 to-violet-600 px-5 py-4 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Comparing…' : 'Compare candidates'}
          </button>
        </div>

        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <h2 className="text-xl font-semibold text-white">Candidate roster</h2>
          <p className="mt-2 text-sm text-slate-400">Pick up to five candidates for side-by-side analysis.</p>

          <div className="mt-6 space-y-3 max-h-[520px] overflow-auto pr-2">
            {candidates.length === 0 ? (
              <div className="rounded-3xl border border-slate-800 bg-slate-950/95 p-6 text-slate-400">
                Loading candidates…
              </div>
            ) : (
              candidates.map((candidate) => (
                <button
                  key={candidate.id}
                  onClick={() => toggleCandidateSelection(candidate.id)}
                  className={`w-full rounded-3xl border px-4 py-4 text-left transition ${
                    selectedCandidateIds.includes(candidate.id)
                      ? 'border-sky-500 bg-sky-500/10 text-white'
                      : 'border-slate-800 bg-slate-900 text-slate-200 hover:border-slate-600 hover:bg-slate-900/80'
                  }`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-semibold text-white">{candidate.anonymized_name}</p>
                      <p className="text-xs text-slate-500">{candidate.current_title || 'No title'}</p>
                    </div>
                    <span className="text-sm text-slate-400">{candidate.years_of_experience ?? '—'} yrs</span>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      </div>

      {comparison && (
        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white">Comparison results</h2>
              <p className="mt-2 text-sm text-slate-400">Review candidate ranking output and recommendations.</p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-950/95 px-4 py-2 text-sm text-slate-300">
              {comparison.candidates.length} candidates compared
            </div>
          </div>

          <div className="mt-6 overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/95 shadow-inner shadow-slate-950/10">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
                <thead className="bg-slate-900 text-slate-400">
                  <tr>
                    <th className="px-4 py-4">Candidate</th>
                    <th className="px-4 py-4">Rank</th>
                    <th className="px-4 py-4">Score</th>
                    <th className="px-4 py-4">Hidden gem</th>
                    <th className="px-4 py-4">Fraud</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {comparison.candidates.map((item) => (
                    <tr key={item.id} className="transition hover:bg-slate-900/80">
                      <td className="px-4 py-4">
                        <div className="font-semibold text-white">{item.candidate?.anonymized_name ?? item.candidate_id}</div>
                        <div className="text-slate-400">{item.candidate?.current_title ?? 'Candidate profile'}</div>
                      </td>
                      <td className="px-4 py-4">{item.rank}</td>
                      <td className="px-4 py-4">{Math.round(item.final_score * 100)}%</td>
                      <td className="px-4 py-4">{item.is_hidden_gem ? 'Yes' : 'No'}</td>
                      <td className="px-4 py-4">{item.is_fraud_flagged ? 'Yes' : 'No'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-950/95 p-5 text-slate-300">
            <p className="font-semibold text-white">Recommendations</p>
            <ul className="mt-3 space-y-2 list-disc pl-5 text-slate-400">
              {comparison.recommendations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
