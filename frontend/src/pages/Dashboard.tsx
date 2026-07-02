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
      <section className="rounded-[32px] border border-slate-800/80 bg-slate-950/95 p-10 shadow-2xl shadow-slate-950/30 ring-1 ring-slate-800/60">
        <div className="grid gap-8 xl:grid-cols-[1.6fr_1fr]">
          <div className="space-y-6">
            <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Recruiter command center</p>
            <h1 className="text-5xl font-semibold tracking-tight text-white">TalentGraph AI</h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-400">Manage your recruiting workflow with polished candidate insights, intelligent ranking support, and real-time fraud risk monitoring.</p>
            <div className="flex flex-wrap gap-3">
              <Link
                to="/ranking/new"
                className="rounded-3xl bg-gradient-to-r from-sky-500 to-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-sky-500/25 transition hover:from-sky-400 hover:to-violet-500"
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

          <div className="grid gap-4">
            <div className="rounded-[28px] bg-slate-900/90 p-7 shadow-xl shadow-slate-950/20 ring-1 ring-slate-800/80">
              <p className="text-xs uppercase tracking-[0.35em] text-slate-500">Today’s focus</p>
              <h2 className="mt-4 text-3xl font-semibold text-white">Align top talent to your highest-value roles.</h2>
              <p className="mt-3 text-sm leading-7 text-slate-400">Import datasets, review candidate intelligence, and make faster hiring decisions without switching tools.</p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-3xl bg-slate-900/90 p-5 shadow-lg shadow-slate-950/20 ring-1 ring-slate-800/70">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Jobs ready</p>
                <p className="mt-4 text-3xl font-semibold text-white">{loading ? '...' : stats?.total_jobs ?? 0}</p>
              </div>
              <div className="rounded-3xl bg-slate-900/90 p-5 shadow-lg shadow-slate-950/20 ring-1 ring-slate-800/70">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Alerts pending</p>
                <p className="mt-4 text-3xl font-semibold text-white">{loading ? '...' : stats?.fraud_alerts_pending ?? 0}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-4">
        {[
          {
            title: 'Total Jobs',
            value: loading ? '...' : stats?.total_jobs ?? 0,
            description: 'Active roles available',
            accent: 'from-sky-500 to-violet-600',
          },
          {
            title: 'Candidates',
            value: loading ? '...' : stats?.total_candidates ?? 0,
            description: 'Profiles assessed',
            accent: 'from-emerald-500 to-teal-500',
          },
          {
            title: 'Pending Rankings',
            value: loading ? '...' : stats?.total_rankings ?? 0,
            description: 'Workflows ready for review',
            accent: 'from-yellow-400 to-orange-500',
          },
          {
            title: 'Fraud Alerts',
            value: loading ? '...' : stats?.fraud_alerts_pending ?? 0,
            description: 'Risk flags detected',
            accent: 'from-fuchsia-500 to-cyan-500',
          },
        ].map((metric) => (
          <div key={metric.title} className="group overflow-hidden rounded-[28px] border border-slate-800 bg-slate-950/90 p-6 shadow-xl shadow-slate-950/20 transition hover:-translate-y-1 hover:border-slate-600">
            <div className={`mb-5 h-1.5 w-16 rounded-full bg-gradient-to-r ${metric.accent}`} />
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">{metric.title}</p>
            <p className="mt-4 text-4xl font-bold text-white">{metric.value}</p>
            <p className="mt-3 text-sm text-slate-400">{metric.description}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[32px] border border-slate-800 bg-slate-950/90 p-8 shadow-2xl shadow-slate-950/20">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-white">Job pipeline</h2>
              <p className="mt-2 text-sm text-slate-400">Track the latest roles and evaluate them for ranking.</p>
            </div>
            <span className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-200">Live</span>
          </div>
          <div className="mt-8 space-y-4">
            {jobs.length === 0 ? (
              <div className="space-y-4 rounded-[28px] border border-slate-800 bg-slate-900/80 p-6">
                <p className="text-slate-400">No jobs found yet. Add roles or import sample data to kickoff ranking workflows.</p>
                <button
                  type="button"
                  disabled={importingJobs}
                  onClick={handleImportSampleJobs}
                  className="rounded-3xl bg-gradient-to-r from-sky-500 to-violet-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-sky-400 hover:to-violet-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {importingJobs ? 'Importing jobs...' : 'Import sample jobs'}
                </button>
              </div>
            ) : (
              jobs.map((job) => (
                <div key={job.id} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 transition hover:-translate-y-1">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
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
              <p className="mt-2 text-sm text-slate-400">Ranking quality and system health at a glance.</p>
            </div>
            <span className="rounded-2xl bg-slate-900 px-4 py-2 text-sm text-slate-200">Summary</span>
          </div>
          <div className="mt-8 grid gap-6 sm:grid-cols-2">
            <div className="rounded-[28px] border border-slate-800 bg-slate-900/80 p-6">
              <p className="text-sm text-slate-400">Average ranking score</p>
              <p className="mt-3 text-4xl font-semibold text-white">{loading ? '...' : stats ? stats.average_ranking_score.toFixed(2) : '0.00'}</p>
            </div>
            <div className="rounded-[28px] border border-slate-800 bg-slate-900/80 p-6">
              <p className="text-sm text-slate-400">Processing latency</p>
              <p className="mt-3 text-4xl font-semibold text-white">{loading ? '...' : `${stats?.processing_time_ms ?? 0} ms`}</p>
            </div>
            <div className="rounded-[28px] border border-slate-800 bg-slate-900/80 p-6">
              <p className="text-sm text-slate-400">Risk status</p>
              <p className="mt-3 text-4xl font-semibold text-white">{stats?.fraud_alerts_pending ? 'Review alerts' : 'No active alerts'}</p>
            </div>
            <div className="rounded-[28px] border border-slate-800 bg-slate-900/80 p-6">
              <p className="text-sm text-slate-400">Active candidates</p>
              <p className="mt-3 text-4xl font-semibold text-white">{loading ? '...' : stats?.total_candidates ?? 0}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
