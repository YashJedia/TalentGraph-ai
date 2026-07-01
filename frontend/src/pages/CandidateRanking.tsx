import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../services/api'

type Job = {
  id: string
  job_title: string
  company_name: string
  job_description?: string
  required_experience_years?: number
  seniority_level?: string
  location?: string
}

type Ranking = {
  id: string
  candidate_id: string
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
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white">Candidate Ranking</h1>
        <p className="mt-3 text-slate-400 max-w-2xl">Rank candidates for hiring roles using TalentGraph scoring signals.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
        <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-6 shadow-2xl shadow-slate-950/20">
          <h2 className="text-xl font-semibold text-white">Select job</h2>
          <p className="mt-2 text-sm text-slate-500">Choose a role to view ranked candidates.</p>

          <select
            value={selectedJobId}
            onChange={(event) => handleJobChange(event.target.value)}
            className="mt-5 w-full rounded-3xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100 outline-none focus:border-blue-500"
          >
            <option value="">Pick a job role</option>
            {jobs.map((jobItem) => (
              <option key={jobItem.id} value={jobItem.id}>
                {jobItem.job_title} — {jobItem.company_name}
              </option>
            ))}
          </select>

          {selectedJobId && (
            <div className="mt-5 flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                onClick={handleRankJob}
                disabled={rankLoading}
                className="inline-flex items-center justify-center rounded-3xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {rankLoading ? 'Ranking candidates...' : 'Rank candidates for this job'}
              </button>
              {statusMessage && <p className="text-sm text-slate-400">{statusMessage}</p>}
            </div>
          )}

          {!selectedJobId && (
            <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/60 p-5 text-slate-400">
              Select a job to populate ranking results and candidate insights.
            </div>
          )}
        </div>

        <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-6 shadow-2xl shadow-slate-950/20">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-white">{selectedJob?.job_title ?? 'Job ranking details'}</h2>
              <p className="mt-2 text-sm text-slate-400">{selectedJob ? `${selectedJob.company_name} • ${selectedJob.location ?? 'Remote/Multiple locations'}` : 'Choose a job from the left panel.'}</p>
            </div>
            <span className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-200">{loading ? 'Loading' : `${rankings.length} candidates`}</span>
          </div>

          {error && (
            <div className="mt-6 rounded-3xl border border-rose-700 bg-rose-950/60 p-5 text-rose-200">
              {error}
            </div>
          )}

          {selectedJobId && !loading && rankings.length === 0 && (
            <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/60 p-6 text-slate-400">
              No rankings available yet for this role. Confirm candidate data is loaded and trigger a ranking refresh.
            </div>
          )}

          {selectedJobId && rankings.length > 0 && (
            <div className="mt-8 overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/60">
              <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
                <thead className="bg-slate-950/95 text-slate-400">
                  <tr>
                    <th className="px-4 py-4">Rank</th>
                    <th className="px-4 py-4">Candidate</th>
                    <th className="px-4 py-4">Score</th>
                    <th className="px-4 py-4">Hidden gem</th>
                    <th className="px-4 py-4">Fraud flag</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {rankings.map((ranking) => (
                    <tr key={ranking.id} className="hover:bg-slate-900/80">
                      <td className="px-4 py-4 font-semibold text-white">{ranking.rank}</td>
                      <td className="px-4 py-4">{ranking.candidate_id}</td>
                      <td className="px-4 py-4">{Math.round(ranking.final_score * 100)}%</td>
                      <td className="px-4 py-4">
                        {ranking.is_hidden_gem ? (
                          <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs text-emerald-300">Hidden gem</span>
                        ) : (
                          <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-400">Standard</span>
                        )}
                      </td>
                      <td className="px-4 py-4">
                        {ranking.is_fraud_flagged ? (
                          <span className="rounded-full bg-rose-500/15 px-3 py-1 text-xs text-rose-300">Flagged</span>
                        ) : (
                          <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-400">Clear</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
