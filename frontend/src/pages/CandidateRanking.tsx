import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../services/api'
import { AlertTriangle, Trophy, RefreshCw, Sparkles, HelpCircle, Briefcase } from 'lucide-react'

type Job = {
  id: string
  job_title: string
  company_name: string
  job_description?: string
  required_experience_years?: number
  seniority_level?: string
  location?: string
}

type CandidateSummary = {
  id: string
  candidate_id: string
  anonymized_name?: string
  headline?: string
  current_title?: string
  current_company?: string
  years_of_experience?: number
  growth_score?: number
  behavioral_score?: number
  fraud_risk_score?: number
  profile_completeness?: number
}

type Ranking = {
  id: string
  job_id: string
  candidate_id: string
  candidate?: CandidateSummary
  final_score: number
  rank: number
  percentile: number
  top_strengths: string[]
  potential_risks: string[]
  is_hidden_gem: boolean
  is_fraud_flagged: boolean
}

export default function CandidateRanking() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [jobs, setJobs] = useState<Job[]>([])
  const [rankings, setRankings] = useState<Ranking[]>([])
  const [selectedJobId, setSelectedJobId] = useState(jobId ?? '')
  const [loading, setLoading] = useState(true)
  const [rankLoading, setRankLoading] = useState(false)
  const [error, setError] = useState('')
  const [statusMessage, setStatusMessage] = useState('')

  useEffect(() => {
    async function loadJobs() {
      try {
        const response = await api.getJobs()
        setJobs(response.data)
      } catch (e) {
        console.error('Failed to load jobs', e)
      }
    }
    loadJobs()
  }, [])

  useEffect(() => {
    async function loadRanking() {
      if (!selectedJobId) {
        setLoading(false)
        return
      }
      setLoading(true)
      setError('')
      try {
        const rankingResponse = await api.getRankings(selectedJobId, 50)
        setRankings(rankingResponse.data.ranked_candidates)
      } catch (e: any) {
        setError('Unable to load ranking data. Confirm the job exists and try again.')
        setRankings([])
      } finally {
        setLoading(false)
      }
    }
    loadRanking()
  }, [selectedJobId])

  const handleRankJob = async () => {
    if (!selectedJobId) {
      return
    }
    setRankLoading(true)
    setStatusMessage('Ranking candidates for the selected job...')
    try {
      await api.rankCandidatesForJob(selectedJobId, 50)
      setStatusMessage('Ranking completed. Refreshing results.')
      const rankingResponse = await api.getRankings(selectedJobId, 50)
      setRankings(rankingResponse.data.ranked_candidates)
      setError('')
    } catch (e: any) {
      setError('Failed to compute rankings. Please try again or check backend logs.')
    } finally {
      setRankLoading(false)
      setStatusMessage('')
    }
  }

  const selectedJob = useMemo(() => jobs.find((item) => item.id === selectedJobId), [jobs, selectedJobId])

  const handleJobChange = (value: string) => {
    setSelectedJobId(value)
    if (value) {
      navigate(`/ranking/${value}`)
    }
  }

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
          Candidate Ranking
        </h1>
        <p className="mt-2 text-sm text-slate-400 max-w-2xl">
          Evaluate credentials against custom target requirements using our multi-agent composite scoring models.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
        {/* Left card control */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 flex flex-col gap-6 h-fit">
          <h2 className="text-lg font-bold text-white flex items-center gap-2 border-b border-slate-900 pb-3">
            <Briefcase size={16} className="text-sky-400" />
            Select Position
          </h2>

          <div className="space-y-5">
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Position Profile</label>
              <select
                value={selectedJobId}
                onChange={(event) => handleJobChange(event.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-900/30 px-3.5 py-3 text-sm text-slate-100 outline-none focus:border-sky-500"
              >
                <option value="" className="bg-slate-950">Pick a job role</option>
                {jobs.map((jobItem) => (
                  <option key={jobItem.id} value={jobItem.id} className="bg-slate-950">
                    {jobItem.job_title} ({jobItem.company_name})
                  </option>
                ))}
              </select>
            </div>

            {selectedJobId ? (
              <div className="space-y-4">
                <button
                  type="button"
                  onClick={handleRankJob}
                  disabled={rankLoading}
                  className="w-full rounded-xl bg-gradient-to-r from-sky-500 to-violet-600 px-4 py-3 text-xs font-bold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500 disabled:cursor-not-allowed disabled:opacity-60 flex items-center justify-center gap-1.5"
                >
                  <RefreshCw size={12} className={rankLoading ? 'animate-spin' : ''} />
                  {rankLoading ? 'Computing ratings...' : 'Trigger Agents Review'}
                </button>
                {statusMessage && (
                  <p className="text-[11px] text-sky-400 font-mono text-center">{statusMessage}</p>
                )}
              </div>
            ) : (
              <div className="rounded-xl border border-slate-800 bg-slate-900/10 p-5 text-xs text-slate-500 leading-relaxed text-center">
                Select a target role to initialize active scoring rosters and agent reports.
              </div>
            )}
          </div>
        </div>

        {/* Right card ranking */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white">
                {selectedJob?.job_title ?? 'Rankings Pipeline'}
              </h2>
              <p className="text-xs text-slate-400">
                {selectedJob 
                  ? `${selectedJob.company_name} • ${selectedJob.location ?? 'Global/Remote'}` 
                  : 'Select a job search target in the left panel.'
                }
              </p>
            </div>
            {selectedJobId && (
              <span className="rounded-xl bg-slate-900 px-3.5 py-2 text-xs font-bold text-slate-300 border border-slate-800/80 shadow-md">
                {loading ? 'Analyzing...' : `${rankings.length} Matched Candidates`}
              </span>
            )}
          </div>

          {error && (
            <div className="mt-5 rounded-xl border border-rose-800 bg-rose-950/30 p-4 text-xs text-rose-300 font-mono">
              {error}
            </div>
          )}

          {/* Table display */}
          {!selectedJobId ? (
            <div className="mt-12 py-12 text-center text-slate-500 border border-dashed border-slate-800/60 rounded-xl max-w-md mx-auto px-6">
              <Trophy size={36} className="mx-auto text-slate-600 mb-4" />
              <h3 className="text-sm font-bold text-slate-400">No Target Selection</h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Choose a job profile to compare candidates, view alignment percentiles, fraud risks, and hidden gems.
              </p>
            </div>
          ) : loading ? (
            <div className="mt-8 space-y-4">
              {Array.from({ length: 6 }).map((_, idx) => (
                <div key={idx} className="h-10 rounded-lg shimmer-placeholder w-full" />
              ))}
            </div>
          ) : rankings.length === 0 ? (
            <div className="mt-8 border border-dashed border-slate-800/60 rounded-xl p-8 text-center text-slate-500 max-w-sm mx-auto">
              <HelpCircle size={28} className="mx-auto text-slate-600 mb-3" />
              <p className="text-xs">No analytics maps have been generated. Click "Trigger Agents Review" to compile composite weights.</p>
            </div>
          ) : (
            <div className="mt-6 overflow-hidden rounded-xl border border-slate-900 bg-slate-950/20">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-900/80 text-left text-xs text-slate-300">
                  <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider font-bold">
                    <tr>
                      <th className="px-5 py-3.5 text-center">Rank</th>
                      <th className="px-5 py-3.5">Candidate Details</th>
                      <th className="px-5 py-3.5">Agent Score</th>
                      <th className="px-5 py-3.5 text-center">Gem Status</th>
                      <th className="px-5 py-3.5 text-center">Compliance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-900/40">
                    {rankings.map((ranking) => (
                      <tr 
                        key={ranking.id} 
                        className="transition hover:bg-slate-900/35 group"
                      >
                        {/* Rank with Trophy indicator */}
                        <td className="px-5 py-4 text-center font-black">
                          {ranking.rank === 1 ? (
                            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 text-xs font-black shadow-lg shadow-yellow-500/5">
                              1
                            </span>
                          ) : ranking.rank === 2 ? (
                            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-slate-300/10 text-slate-200 border border-slate-300/30 text-xs font-black">
                              2
                            </span>
                          ) : ranking.rank === 3 ? (
                            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-amber-600/10 text-amber-500 border border-amber-600/30 text-xs font-black">
                              3
                            </span>
                          ) : (
                            <span className="text-slate-400">{ranking.rank}</span>
                          )}
                        </td>

                        {/* Name and description info */}
                        <td className="px-5 py-4">
                          <div className="font-bold text-white group-hover:text-sky-400 transition">
                            {ranking.candidate?.anonymized_name ?? ranking.candidate_id}
                          </div>
                          <div className="text-[10px] text-slate-500 mt-0.5 font-semibold">
                            {ranking.candidate?.current_title ?? 'Assessment Profile'}
                          </div>
                        </td>

                        {/* Score Badge */}
                        <td className="px-5 py-4">
                          <span className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-500/5 border border-indigo-500/10 px-2 py-1 text-xs font-black font-mono text-indigo-400">
                            {Math.round(ranking.final_score * 100)}%
                          </span>
                        </td>

                        {/* Gem Status */}
                        <td className="px-5 py-4 text-center">
                          {ranking.is_hidden_gem ? (
                            <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 text-[10px] font-bold text-emerald-400 shadow-inner">
                              <Sparkles size={10} className="animate-pulse" /> Hidden Gem
                            </span>
                          ) : (
                            <span className="inline-flex rounded-full bg-slate-900 border border-slate-800/80 px-2.5 py-0.5 text-[10px] text-slate-500">
                              Standard
                            </span>
                          )}
                        </td>

                        {/* Compliance (Fraud Flag) */}
                        <td className="px-5 py-4 text-center">
                          {ranking.is_fraud_flagged ? (
                            <span className="inline-flex items-center gap-1 rounded-full bg-rose-500/10 border border-rose-500/20 px-2.5 py-0.5 text-[10px] font-bold text-rose-400 indicator-pulse">
                              <AlertTriangle size={10} /> Flagged Anomaly
                            </span>
                          ) : (
                            <span className="inline-flex rounded-full bg-slate-900 border border-slate-800/80 px-2.5 py-0.5 text-[10px] text-emerald-400 font-bold">
                              Clear
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
