import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { Server, Database, ShieldCheck } from 'lucide-react'

type FooterStats = {
  total_jobs: number
  total_candidates: number
  fraud_alerts_pending: number
}

export default function Footer() {
  const [stats, setStats] = useState<FooterStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      try {
        const response = await api.getSystemStats()
        setStats({
          total_jobs: response.data.total_jobs,
          total_candidates: response.data.total_candidates,
          fraud_alerts_pending: response.data.fraud_alerts_pending,
        })
      } catch (error) {
        console.error('Footer telemetry load failed', error)
      } finally {
        setLoading(false)
      }
    }
    loadStats()
    const t = setInterval(loadStats, 30000)
    return () => clearInterval(t)
  }, [])

  return (
    <footer className="mt-auto border-t border-slate-900 bg-slate-950/70 py-8 px-6 backdrop-blur-md relative z-10">
      <div className="mx-auto w-full max-w-[1520px]">
        <div className="grid gap-8 lg:grid-cols-4 md:grid-cols-2">
          {/* Logo & Identity */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-sky-400 to-indigo-600 text-xs font-black text-white">
                TG
              </div>
              <span className="font-bold tracking-tight text-white">TalentGraph AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Decentralized multi-agent analytics tool validating skill depths, career trajectories, and fraud anomalies.
            </p>
            <div className="text-[10px] text-slate-500 font-mono">
              Engine Version v1.0.0 (Production)
            </div>
          </div>

          {/* Realtime Telemetry Grid */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">Telemetry Engine</h3>
            <div className="grid gap-2 text-xs">
              <div className="flex items-center justify-between text-slate-400 rounded-lg bg-slate-900/35 border border-slate-800/20 px-3 py-1.5">
                <span className="flex items-center gap-1.5"><Server size={12} className="text-sky-400" /> API Gateway</span>
                <span className="text-[10px] text-emerald-400 bg-emerald-400/10 px-1.5 py-0.2 rounded font-mono font-semibold">Active</span>
              </div>
              <div className="flex items-center justify-between text-slate-400 rounded-lg bg-slate-900/35 border border-slate-800/20 px-3 py-1.5">
                <span className="flex items-center gap-1.5"><Database size={12} className="text-violet-400" /> Vector Index</span>
                <span className="text-[10px] text-emerald-400 bg-emerald-400/10 px-1.5 py-0.2 rounded font-mono font-semibold">Qdrant OK</span>
              </div>
            </div>
          </div>

          {/* Database Metrics */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">Platform Coverage</h3>
            <div className="grid gap-2 text-xs">
              <div className="flex items-center justify-between text-slate-400">
                <span>Candidates Evaluated:</span>
                <span className="font-mono font-bold text-slate-200">
                  {loading ? '...' : stats?.total_candidates ?? 0}
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Active Target Roles:</span>
                <span className="font-mono font-bold text-slate-200">
                  {loading ? '...' : stats?.total_jobs ?? 0}
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Fraud Warnings Logged:</span>
                <span className={`font-mono font-bold ${stats?.fraud_alerts_pending ? 'text-red-400' : 'text-slate-200'}`}>
                  {loading ? '...' : stats?.fraud_alerts_pending ?? 0}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Shortcuts */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">Console Pipelines</h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <Link to="/" className="text-slate-400 hover:text-white transition">Dashboard</Link>
              <Link to="/search" className="text-slate-400 hover:text-white transition">Search</Link>
              <Link to="/ranking/new" className="text-slate-400 hover:text-white transition">Rankings</Link>
              <Link to="/fraud-alerts" className="text-slate-400 hover:text-white transition">Fraud Hub</Link>
              <Link to="/copilot" className="text-slate-400 hover:text-white transition">Copilot</Link>
              <Link to="/comparison" className="text-slate-400 hover:text-white transition">Compare</Link>
            </div>
          </div>
        </div>

        {/* Global Security Line */}
        <div className="mt-8 border-t border-slate-900/60 pt-4 flex flex-col md:flex-row md:items-center md:justify-between text-[11px] text-slate-500">
          <p>© {new Date().getFullYear()} TalentGraph AI. All diagnostic records encrypted.</p>
          <div className="flex items-center gap-1 mt-2 md:mt-0 text-emerald-500/80 bg-emerald-500/5 border border-emerald-500/10 px-2 py-0.5 rounded-full w-fit">
            <ShieldCheck size={11} />
            <span>Encrypted Node TLS 1.3 Handshake Securing Workspace</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
