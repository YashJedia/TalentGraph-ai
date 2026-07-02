import { Link, useLocation } from 'react-router-dom'
import {
  BarChart3,
  Search,
  Zap,
  Gem,
  AlertTriangle,
  MessageCircle,
} from 'lucide-react'

const menuItems = [
  { label: 'Dashboard', path: '/', icon: BarChart3 },
  { label: 'Search', path: '/search', icon: Search },
  { label: 'Ranking', path: '/ranking/new', icon: Zap },
  { label: 'Hidden Gems', path: '/hidden-gems', icon: Gem },
  { label: 'Fraud Alerts', path: '/fraud-alerts', icon: AlertTriangle },
  { label: 'Copilot', path: '/copilot', icon: MessageCircle },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="flex w-72 flex-col border-r border-slate-800/60 bg-slate-900/95 p-6 shadow-xl shadow-slate-950/10">
      <div className="mb-10 rounded-[32px] border border-slate-800/60 bg-slate-900/90 p-5 shadow-lg shadow-slate-950/10">
        <div className="inline-flex h-14 w-14 items-center justify-center rounded-3xl bg-gradient-to-br from-sky-500 to-violet-600 text-xl font-black text-white shadow-lg shadow-sky-500/20">
          TG
        </div>
        <p className="mt-4 text-xs uppercase tracking-[0.35em] text-slate-500">TalentGraph AI</p>
        <p className="mt-2 text-sm text-slate-300">Recruiter console for modern talent intelligence.</p>
      </div>

      <nav className="flex-1 space-y-3">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center gap-3 rounded-3xl px-4 py-3 text-sm font-semibold transition ${
                isActive
                  ? 'bg-gradient-to-r from-sky-500 to-violet-600 text-white shadow-lg shadow-sky-500/20'
                  : 'text-slate-300 hover:bg-slate-900 hover:text-slate-100'
              }`}
            >
              <span className={`inline-flex h-11 w-11 items-center justify-center rounded-2xl ${
                isActive ? 'bg-white/10 text-white' : 'bg-slate-900 text-slate-400 group-hover:bg-slate-800 group-hover:text-white'
              }`}>
                <Icon size={18} />
              </span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="mt-8 rounded-[28px] border border-slate-800 bg-slate-900/80 p-5 text-sm text-slate-300 shadow-xl shadow-slate-950/20">
        <p className="font-semibold text-white">Recruiter toolkit</p>
        <p className="mt-2 text-slate-400">Import data, run rankings, and keep fraud alerts under control.</p>
        <Link
          to="/search"
          className="mt-4 inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-sky-500 to-violet-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500"
        >
          Start search
        </Link>
      </div>
    </aside>
  )
}
