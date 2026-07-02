import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { Activity, Bell } from 'lucide-react'

type FraudAlert = {
  id: string
  candidate_id: string
  alert_type: string
  severity: string
  confidence_score: number
  description: string
  evidence: Record<string, unknown>
  created_at: string
}

type AlertResponse = {
  total_alerts: number
  by_severity: Record<string, number>
  recent_alerts: FraudAlert[]
}

export default function FraudAlerts() {
  const [alerts, setAlerts] = useState<AlertResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadAlerts() {
      try {
        const response = await api.getFraudAlerts()
        setAlerts(response.data)
      } catch (error) {
        console.error('Fraud alerts load failed', error)
      } finally {
        setLoading(false)
      }
    }
    loadAlerts()
  }, [])

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
          Fraud Compliance Alerts
        </h1>
        <p className="mt-2 text-sm text-slate-400 max-w-2xl">
          Track compliance issues, credential overlaps, and statistical anomaly indicators flagged by multi-agent audits.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
        {/* Left Side: Summary Panel */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 flex flex-col gap-6 h-fit">
          <h2 className="text-lg font-bold text-white flex items-center gap-2 border-b border-slate-900 pb-3">
            <Bell size={16} className="text-sky-400" />
            Vulnerability Summary
          </h2>

          <div className="space-y-3">
            {loading ? (
              <div className="h-24 rounded-lg shimmer-placeholder w-full" />
            ) : alerts ? (
              Object.entries(alerts.by_severity).map(([severity, count]) => {
                const isHigh = severity.toLowerCase() === 'high' || severity.toLowerCase() === 'critical'
                const isMed = severity.toLowerCase() === 'medium' || severity.toLowerCase() === 'warning'
                const accent = isHigh 
                  ? 'border-rose-500/15 bg-rose-500/5 text-rose-400' 
                  : isMed 
                  ? 'border-yellow-500/15 bg-yellow-500/5 text-yellow-400' 
                  : 'border-slate-800 bg-slate-900/40 text-slate-400'

                return (
                  <div 
                    key={severity} 
                    className={`rounded-xl border p-4 shadow-inner flex items-center justify-between ${accent}`}
                  >
                    <div>
                      <p className="text-[10px] uppercase font-bold tracking-wider opacity-85">{severity} Risk</p>
                      <p className="mt-1 text-2xl font-black">{count}</p>
                    </div>
                    <div className="h-3 w-3 rounded-full bg-current animate-pulse" />
                  </div>
                )
              })
            ) : (
              <div className="text-xs text-slate-500 leading-relaxed text-center">No risk alerts detected.</div>
            )}
          </div>
        </div>

        {/* Right Side: Alerts log table */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-1.5 animate-pulse">
                <Activity size={16} className="text-rose-500" />
                Live Audits log
              </h2>
              <p className="text-xs text-slate-400">Review credential padding, overlapping periods, and outlier models.</p>
            </div>
            <span className="rounded-xl bg-slate-900 border border-slate-800 px-3.5 py-1.5 text-xs text-slate-400">
              {loading ? 'Analyzing...' : `${alerts?.total_alerts ?? 0} Compliance Issues`}
            </span>
          </div>

          <div className="mt-6 overflow-hidden rounded-xl border border-slate-900 bg-slate-950/20">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-900/80 text-left text-xs text-slate-300">
                <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider font-bold">
                  <tr>
                    <th className="px-5 py-3.5">Candidate ID</th>
                    <th className="px-5 py-3.5">Anomaly Classification</th>
                    <th className="px-5 py-3.5 text-center">Threat Level</th>
                    <th className="px-5 py-3.5 text-center">Audit Confidence</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/40">
                  {loading ? (
                    Array.from({ length: 4 }).map((_, idx) => (
                      <tr key={idx}>
                        <td className="px-5 py-4" colSpan={4}>
                          <div className="h-6 rounded-lg shimmer-placeholder w-full" />
                        </td>
                      </tr>
                    ))
                  ) : alerts?.recent_alerts.length ? (
                    alerts.recent_alerts.map((alert) => {
                      const isHigh = alert.severity.toLowerCase() === 'high' || alert.severity.toLowerCase() === 'critical'
                      const isMed = alert.severity.toLowerCase() === 'medium'
                      
                      const severityBadge = isHigh
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : isMed
                        ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
                        : 'bg-slate-900 text-slate-400 border border-slate-800'

                      return (
                        <tr 
                          key={alert.id} 
                          className="transition hover:bg-slate-900/35 group"
                        >
                          <td className="px-5 py-4 font-mono font-bold text-slate-300">
                            {alert.candidate_id}
                          </td>
                          <td className="px-5 py-4">
                            <div className="font-bold text-white group-hover:text-rose-400 transition">
                              {alert.alert_type}
                            </div>
                            <div className="text-[10px] text-slate-500 mt-0.5 max-w-md truncate">
                              {alert.description}
                            </div>
                          </td>
                          <td className="px-5 py-4 text-center">
                            <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-bold capitalize ${severityBadge}`}>
                              {alert.severity}
                            </span>
                          </td>
                          <td className="px-5 py-4 text-center">
                            <span className="inline-flex rounded-lg bg-indigo-500/5 border border-indigo-500/10 px-2 py-0.5 font-bold font-mono text-indigo-400">
                              {Math.round(alert.confidence_score * 100)}%
                            </span>
                          </td>
                        </tr>
                      )
                    })
                  ) : (
                    <tr>
                      <td className="px-5 py-10 text-slate-500 text-center" colSpan={4}>
                        No active anomalies detected inside rosters. Sandbox workspace clean.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
