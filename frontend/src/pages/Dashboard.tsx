import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { Link } from 'react-router-dom'

type SystemStats = {
  total_jobs: number
  total_candidates: number
  total_rankings: number
  fraud_alerts_pending: number
  average_ranking_score: number
  processing_time_ms: number
}

type JobSummary = {
  id: string
  job_title: string
  company_name: string
}

export default function Dashboard() {
  const [stats, setStats] = useState<SystemStats | null>(null)
  const [jobs, setJobs] = useState<JobSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [importingJobs, setImportingJobs] = useState(false)
  const [importingCandidates, setImportingCandidates] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    async function loadData() {
      try {
        const [statsResponse, jobsResponse] = await Promise.all([
          api.getSystemStats(),
          api.getJobs(),
        ])
        setStats(statsResponse.data)
        setJobs(jobsResponse.data.slice(0, 4))
      } catch (error) {
        console.error('Dashboard load failed', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleImportSampleJobs = async () => {
    setImportingJobs(true)
    setMessage('Importing sample jobs...')
    try {
      await api.importSampleJobs()
      setMessage('Sample jobs imported successfully. Reload the page to see them.')
    } catch (error) {
      console.error('Import jobs failed', error)
      setMessage('Failed to import sample jobs. Check backend status and try again.')
    } finally {
      setImportingJobs(false)
    }
  }

  const handleImportCandidateDataset = async () => {
    setImportingCandidates(true)
    setMessage('Importing candidate dataset... this may take a few moments.')
    try {
      await api.importCandidateDataset(100)
      setMessage('Candidate dataset import started. Reload the page after a few moments.')
    } catch (error) {
      console.error('Import candidates failed', error)
      setMessage('Failed to import candidate dataset. Ensure the backend can access the dataset path.')
    } finally {
      setImportingCandidates(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-8 shadow-2xl shadow-slate-950/20">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Welcome back</p>
            <h1 className="text-4xl font-semibold text-white">Dashboard</h1>
            <p className="mt-3 text-slate-400 max-w-2xl">Monitor candidate pipelines, review ranking signals, and keep an eye on risk alerts from one intelligent recruiter console.</p>
          </div>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-2">
            <Link
              to="/ranking/new"
              className="rounded-3xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:from-blue-500 hover:to-indigo-500"
            >
              Review job ranking
            </Link>
            <Link
              to="/fraud-alerts"
              className="rounded-3xl border border-slate-700 bg-slate-900 px-6 py-3 text-sm font-semibold text-slate-200 transition hover:border-slate-500 hover:bg-slate-800"
            >
              View fraud alerts
            </Link>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-4">
        <div className="group overflow-hidden rounded-[28px] border border-slate-800 bg-slate-950/90 p-6 shadow-xl shadow-slate-950/20 transition hover:-translate-y-1 hover:border-slate-600">
          <div className="mb-5 h-1.5 w-16 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500" />
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Total Jobs</p>
          <p className="mt-4 text-4xl font-bold text-white">{loading ? '...' : stats?.total_jobs ?? 0}</p>
          <p className="mt-3 text-sm text-slate-400">Active positions open</p>
        </div>
        <div className="group overflow-hidden rounded-[28px] border border-slate-800 bg-slate-950/90 p-6 shadow-xl shadow-slate-950/20 transition hover:-translate-y-1 hover:border-slate-600">
          <div className="mb-5 h-1.5 w-16 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500" />
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Total Candidates</p>
          <p className="mt-4 text-4xl font-bold text-white">{loading ? '...' : stats?.total_candidates ?? 0}</p>
          <p className="mt-3 text-sm text-slate-400">Profiles assessed</p>
        </div>
        <div className="group overflow-hidden rounded-[28px] border border-slate-800 bg-slate-950/90 p-6 shadow-xl shadow-slate-950/20 transition hover:-translate-y-1 hover:border-slate-600">
          <div className="mb-5 h-1.5 w-16 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500" />
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Pending Rankings</p>
          <p className="mt-4 text-4xl font-bold text-white">{loading ? '...' : stats?.total_rankings ?? 0}</p>
          <p className="mt-3 text-sm text-slate-400">Ready for review</p>
        </div>
        <div className="group overflow-hidden rounded-[28px] border border-slate-800 bg-slate-950/90 p-6 shadow-xl shadow-slate-950/20 transition hover:-translate-y-1 hover:border-slate-600">
          <div className="mb-5 h-1.5 w-16 rounded-full bg-gradient-to-r from-rose-500 to-fuchsia-500" />
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Fraud Alerts</p>
          <p className="mt-4 text-4xl font-bold text-white">{loading ? '...' : stats?.fraud_alerts_pending ?? 0}</p>
          <p className="mt-3 text-sm text-slate-400">Risk flags detected</p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-8 shadow-2xl shadow-slate-950/20">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-white">Job pipeline</h2>
              <p className="mt-2 text-sm text-slate-400">Recently created jobs and roles available for ranking.</p>
            </div>
            <span className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-200">Live</span>
          </div>
          <div className="mt-8 space-y-4">
            {jobs.length === 0 ? (
              <div className="space-y-4">
                <p className="text-slate-400">No jobs found yet. Add jobs from the API or import sample data.</p>
                <button
                  type="button"
                  disabled={importingJobs}
                  onClick={handleImportSampleJobs}
                  className="rounded-3xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {importingJobs ? 'Importing jobs...' : 'Import sample jobs'}
                </button>
              </div>
            ) : (
              jobs.map((job) => (
                <div key={job.id} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm text-slate-400">{job.company_name}</p>
                      <h3 className="text-lg font-semibold text-white">{job.job_title}</h3>
                    </div>
                    <Link
                      to={`/ranking/${job.id}`}
                      className="rounded-2xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-500"
                    >
                      View ranking
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>
          {(stats?.total_candidates ?? 0) === 0 && (
            <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
              <p className="text-slate-300">The candidate dataset is not loaded yet.</p>
              <button
                type="button"
                disabled={importingCandidates}
                onClick={handleImportCandidateDataset}
                className="mt-4 rounded-3xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {importingCandidates ? 'Importing candidates...' : 'Import candidate dataset'}
              </button>
            </div>
          )}
          {message && (
            <div className="mt-4 rounded-3xl border border-slate-800 bg-slate-900/80 p-4 text-slate-200">
              {message}
            </div>
          )}
        </div>

        <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-8 shadow-2xl shadow-slate-950/20">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-white">Intelligence snapshot</h2>
              <p className="mt-2 text-sm text-slate-400">Average ranking quality and system health at a glance.</p>
            </div>
            <span className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-200">Summary</span>
          </div>
          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/60 p-6 text-slate-400">
            <p>
              Average ranking score: {loading ? '...' : stats ? stats.average_ranking_score.toFixed(2) : '0.00'}
            </p>
            <p className="mt-3">Processing latency is tracked per workflow and will appear here once live.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
