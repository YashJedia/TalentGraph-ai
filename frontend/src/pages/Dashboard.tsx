import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { Link } from 'react-router-dom'
import {
  Users,
  Briefcase,
  AlertTriangle,
  Zap,
  Activity,
  ArrowUpRight,
  Database,
  Sparkles,
  TrendingUp,
} from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

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
      setMessage('Sample jobs imported successfully. Refresh to see them.')
      // Auto-reload after a delay to get new stats
      setTimeout(() => window.location.reload(), 1500)
    } catch (error) {
      console.error('Import jobs failed', error)
      setMessage('Failed to import sample jobs.')
    } finally {
      setImportingJobs(false)
    }
  }

  const handleImportCandidateDataset = async () => {
    setImportingCandidates(true)
    setMessage('Importing candidate dataset... this may take a moment.')
    try {
      await api.importCandidateDataset(100)
      setMessage('Candidate dataset import started. Refresh in a few moments.')
      setTimeout(() => window.location.reload(), 2000)
    } catch (error) {
      console.error('Import candidates failed', error)
      setMessage('Failed to import candidate dataset.')
    } finally {
      setImportingCandidates(false)
    }
  }

  // Generate dynamic chart data based on stats
  const performanceChartData = [
    { name: '00:00', latency: (stats?.processing_time_ms ?? 340) * 0.9, candidates: Math.round((stats?.total_candidates ?? 20) * 0.25) },
    { name: '04:00', latency: (stats?.processing_time_ms ?? 340) * 1.1, candidates: Math.round((stats?.total_candidates ?? 20) * 0.4) },
    { name: '08:00', latency: (stats?.processing_time_ms ?? 340) * 1.3, candidates: Math.round((stats?.total_candidates ?? 20) * 0.6) },
    { name: '12:00', latency: (stats?.processing_time_ms ?? 340) * 0.8, candidates: Math.round((stats?.total_candidates ?? 20) * 0.75) },
    { name: '16:00', latency: (stats?.processing_time_ms ?? 340) * 1.0, candidates: Math.round((stats?.total_candidates ?? 20) * 0.9) },
    { name: '20:00', latency: (stats?.processing_time_ms ?? 340) * 0.95, candidates: stats?.total_candidates ?? 0 },
  ]

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Hero Welcome banner */}
      <section className="relative overflow-hidden rounded-[32px] border border-slate-800 bg-slate-950/80 p-8 md:p-10 shadow-2xl ring-1 ring-white/5">
        <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-br from-sky-500/10 to-violet-600/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="grid gap-8 lg:grid-cols-[1.6fr_1fr] relative z-10">
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full bg-sky-500/10 border border-sky-500/20 px-3 py-1 text-xs text-sky-400 font-bold uppercase tracking-wider">
              <Sparkles size={11} className="animate-spin" />
              <span>Multi-Agent Recruitment Platform</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white">
              TalentGraph AI
            </h1>
            <p className="max-w-2xl text-base md:text-lg leading-relaxed text-slate-400">
              Analyze talent pipelines with explainable scoring models, promotion velocity estimates, and statistical neural network anomaly flags.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                to="/ranking/new"
                className="rounded-xl bg-gradient-to-r from-sky-500 to-violet-600 px-5  py-3 text-sm font-bold text-white shadow-lg shadow-sky-500/25 transition hover:from-sky-400 hover:to-violet-500 hover:scale-[1.02]"
              >
                Launch Score Engine
              </Link>
              <Link
                to="/fraud-alerts"
                className="rounded-xl border border-slate-800 bg-slate-900/60 px-5 py-3 text-sm font-bold text-slate-300 transition hover:border-slate-700 hover:bg-slate-800 hover:text-white"
              >
                Inspect Compliance Alerts
              </Link>
            </div>
          </div>

          <div className="grid gap-4">
            <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-6 flex flex-col justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Autonomous Agents</p>
                <h2 className="mt-2 text-xl font-bold text-white">Continuous Verification</h2>
                <p className="mt-2 text-xs leading-relaxed text-slate-400">
                  Self-healing algorithms process overlapping career tenures and flag skill stuffing across imported rosters.
                </p>
              </div>
            </div>
            <div className="grid gap-3 grid-cols-2">
              <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-4">
                <p className="text-[10px] uppercase font-bold tracking-wider text-slate-500">Active Roles</p>
                {loading ? (
                  <div className="mt-2 h-8 w-16 rounded shimmer-placeholder" />
                ) : (
                  <p className="mt-1 text-2xl font-black text-white">{stats?.total_jobs ?? 0}</p>
                )}
              </div>
              <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-4">
                <p className="text-[10px] uppercase font-bold tracking-wider text-slate-500">Unresolved Threats</p>
                {loading ? (
                  <div className="mt-2 h-8 w-16 rounded shimmer-placeholder" />
                ) : (
                  <p className={`mt-1 text-2xl font-black ${stats?.fraud_alerts_pending ? 'text-red-400' : 'text-white'}`}>
                    {stats?.fraud_alerts_pending ?? 0}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Metrics Row */}
      <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            title: 'Active Jobs',
            value: stats?.total_jobs ?? 0,
            desc: 'Indexed job targets',
            icon: Briefcase,
            color: 'text-sky-400 bg-sky-500/10 border-sky-500/15',
          },
          {
            title: 'Assessed Profiles',
            value: stats?.total_candidates ?? 0,
            desc: 'Loaded database records',
            icon: Users,
            color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/15',
          },
          {
            title: 'Computed Rankings',
            value: stats?.total_rankings ?? 0,
            desc: 'Active comparison sets',
            icon: Zap,
            color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/15',
          },
          {
            title: 'Security Alarms',
            value: stats?.fraud_alerts_pending ?? 0,
            desc: 'Outstanding risk items',
            icon: AlertTriangle,
            color: 'text-rose-400 bg-rose-500/10 border-rose-500/15',
          },
        ].map((item) => {
          const Icon = item.icon
          return (
            <div
              key={item.title}
              className="glass-card glow-card rounded-2xl p-5 border border-slate-800/80 bg-slate-950/40 flex items-center justify-between"
            >
              <div>
                <span className="text-xs uppercase tracking-wider font-bold text-slate-500">{item.title}</span>
                {loading ? (
                  <div className="mt-3 h-8 w-24 rounded shimmer-placeholder" />
                ) : (
                  <p className="mt-2 text-3xl font-black text-white">{item.value}</p>
                )}
                <span className="mt-1 text-[11px] text-slate-400 block">{item.desc}</span>
              </div>
              <div className={`h-12 w-12 rounded-xl flex items-center justify-center border ${item.color}`}>
                <Icon size={20} />
              </div>
            </div>
          )
        })}
      </section>

      {/* Main Grid: Pipeline and Telemetry Chart */}
      <section className="grid gap-6 lg:grid-cols-2">
        {/* Pipeline / Data Imports */}
        <div className="glass-card rounded-[24px] p-6 border border-slate-800 bg-slate-950/40">
          <div className="flex items-center justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Database size={16} className="text-purple-400" />
                Active Job Pipeline
              </h2>
              <p className="text-xs text-slate-400">Launch ratings and orchestrate agent verification.</p>
            </div>
            <span className="rounded-lg bg-slate-900 px-3 py-1 text-xs font-semibold text-sky-400 border border-slate-800">
              Database Sync
            </span>
          </div>

          <div className="mt-6 space-y-4">
            {jobs.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-800 bg-slate-900/10 p-6 text-center space-y-4">
                <p className="text-xs text-slate-400 max-w-sm mx-auto">
                  No core jobs detected. Import the sample roles mock database to initialize active recruiters ranking states.
                </p>
                <button
                  type="button"
                  disabled={importingJobs}
                  onClick={handleImportSampleJobs}
                  className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-500 px-4 py-2.5 text-xs font-bold text-white transition disabled:opacity-60"
                >
                  {importingJobs ? 'Injecting Mock Roles...' : 'Inject Sample Jobs'}
                </button>
              </div>
            ) : (
              jobs.map((job) => (
                <div
                  key={job.id}
                  className="group rounded-xl border border-slate-800/80 bg-slate-900/25 p-4 transition-all hover:bg-slate-900/50 hover:border-slate-700/60"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{job.company_name}</span>
                      <h3 className="text-sm font-semibold text-slate-200 mt-0.5">{job.job_title}</h3>
                    </div>
                    <Link
                      to={`/ranking/${job.id}`}
                      className="inline-flex h-9 items-center justify-center gap-1.5 rounded-lg bg-slate-900 group-hover:bg-sky-600 px-3.5 text-xs font-bold text-slate-300 group-hover:text-white transition border border-slate-800 group-hover:border-sky-500"
                    >
                      <span>Analyze</span>
                      <ArrowUpRight size={13} />
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Candidate Import Widget */}
          {stats !== null && stats.total_candidates === 0 && (
            <div className="mt-5 rounded-xl border border-slate-800 bg-slate-900/20 p-5 space-y-3">
              <div>
                <h4 className="text-xs font-bold text-slate-300">Database Core Empty</h4>
                <p className="text-[11px] text-slate-400 mt-1">
                  Load candidate diagnostic records to populate pipeline intelligence reports.
                </p>
              </div>
              <button
                type="button"
                disabled={importingCandidates}
                onClick={handleImportCandidateDataset}
                className="w-full rounded-xl bg-emerald-600/90 hover:bg-emerald-500 py-3 text-xs font-bold text-white transition disabled:opacity-60"
              >
                {importingCandidates ? 'Parsing Dataset...' : 'Import Candidate Dataset'}
              </button>
            </div>
          )}

          {message && (
            <div className="mt-4 rounded-xl bg-slate-900/80 border border-slate-800/60 p-3.5 text-xs text-sky-300 font-mono text-center">
              {message}
            </div>
          )}
        </div>

        {/* Intelligence Telemetry Visualizations */}
        <div className="glass-card rounded-[24px] p-6 border border-slate-800 bg-slate-950/40 flex flex-col">
          <div className="flex items-center justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Activity size={16} className="text-sky-400" />
                Diagnostic Telemetry
              </h2>
              <p className="text-xs text-slate-400">Response latencies and loaded records across zones.</p>
            </div>
            <span className="rounded-lg bg-slate-900 px-3 py-1 text-xs font-semibold text-slate-400 border border-slate-800 flex items-center gap-1.5">
              <TrendingUp size={11} className="text-sky-500" />
              Live Activity
            </span>
          </div>

          {/* Area Chart Container */}
          <div className="mt-6 h-52 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performanceChartData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="#6b7280" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#6b7280" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    borderColor: 'rgba(148, 163, 184, 0.15)',
                    borderRadius: '8px',
                    fontSize: '11px',
                    color: '#fff',
                  }}
                />
                <Area type="monotone" dataKey="latency" name="Latency (ms)" stroke="#38bdf8" strokeWidth={2} fillOpacity={1} fill="url(#colorLatency)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Health Stats Grid */}
          <div className="mt-auto pt-6 border-t border-slate-900 grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-slate-900 bg-slate-900/10 p-4">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Average Score</span>
              {loading ? (
                <div className="mt-2 h-6 w-12 rounded shimmer-placeholder" />
              ) : (
                <p className="mt-1 text-xl font-bold text-slate-200">
                  {stats ? (stats.average_ranking_score * 100).toFixed(1) : '0.0'}%
                </p>
              )}
            </div>
            <div className="rounded-xl border border-slate-900 bg-slate-900/10 p-4">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Compute Cost</span>
              {loading ? (
                <div className="mt-2 h-6 w-12 rounded shimmer-placeholder" />
              ) : (
                <p className="mt-1 text-xl font-bold text-slate-200">
                  {stats?.processing_time_ms ?? 0} ms
                </p>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
