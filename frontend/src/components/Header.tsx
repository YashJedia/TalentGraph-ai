import { useEffect, useState } from 'react'
import { useAppStore } from '../context/store'
import { api } from '../services/api'
import { Activity, Moon, Sun, Cpu, Sparkles } from 'lucide-react'

export default function Header() {
  const { darkMode, toggleDarkMode } = useAppStore()
  const [dbStatus, setDbStatus] = useState<'online' | 'offline' | 'checking'>('checking')
  const [latency, setLatency] = useState<number | null>(null)

  useEffect(() => {
    async function checkHealth() {
      const startTime = performance.now()
      try {
        await api.getSystemStats()
        const duration = Math.round(performance.now() - startTime)
        setDbStatus('online')
        setLatency(duration)
      } catch (error) {
        setDbStatus('offline')
        setLatency(null)
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 15000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/40 bg-slate-950/80 backdrop-blur-2xl px-6 py-4">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Cpu size={16} className="text-sky-400" />
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">TalentGraph AI Platform</p>
            <span className="flex h-1.5 w-1.5 rounded-full bg-sky-500/50 animate-ping" />
          </div>
          <h1 className="mt-1 text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            Recruiter Intelligence console
            <span className="ml-1 rounded px-1.5 py-0.5 text-[10px] font-semibold bg-violet-500/10 text-violet-400 border border-violet-500/20 uppercase tracking-wider flex items-center gap-1">
              <Sparkles size={8} /> Multi-Agent
            </span>
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-4">
          {/* Telemetry Status Monitor */}
          <div className="hidden md:flex items-center gap-3 rounded-2xl border border-slate-800 bg-slate-900/40 px-3.5 py-1.5 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <span className={`h-2.5 w-2.5 rounded-full ${
                dbStatus === 'online' ? 'bg-emerald-500 indicator-pulse' : dbStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
              }`} />
              <span className="font-semibold text-slate-300">
                {dbStatus === 'online' ? 'Gateway Active' : dbStatus === 'offline' ? 'Disconnected' : 'Checking Status'}
              </span>
            </div>
            {latency !== null && (
              <>
                <span className="h-3 w-px bg-slate-800" />
                <span className="font-mono text-[10px] text-slate-500">{latency}ms latency</span>
              </>
            )}
          </div>

          <div className="flex items-center gap-2">
            {/* Theme Toggle Button */}
            <button
              onClick={toggleDarkMode}
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-800 bg-slate-900/60 text-slate-300 transition hover:bg-slate-800 hover:text-white"
              title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>

            {/* Quick action button */}
            <button className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-violet-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500 hover:scale-[1.02]">
              <Activity size={16} />
              <span>Diagnostic Sync</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
