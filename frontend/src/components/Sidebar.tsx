import { Link, useLocation } from 'react-router-dom'
import {
  BarChart3,
  Search,
  Zap,
  Gem,
  AlertTriangle,
  MessageCircle,
  Settings,
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
    <aside className="w-72 bg-slate-950/95 border-r border-slate-700 p-6 flex flex-col shadow-2xl shadow-slate-950/30">
      <div className="mb-10 rounded-[28px] border border-slate-800 bg-slate-900 p-5">
        <div className="inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-gradient-to-br from-blue-500 to-indigo-500 text-lg font-bold text-white shadow-lg shadow-blue-500/20">
          TG
        </div>
        <p className="mt-4 text-xs uppercase tracking-[0.24em] text-slate-400">TalentGraph AI</p>
        <p className="mt-2 text-sm text-slate-300">Recruiter console and candidate intelligence.</p>
      </div>

      <nav className="space-y-3 flex-1">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center gap-3 rounded-3xl px-4 py-3 text-sm font-medium transition ${
                isActive
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/10'
                  : 'text-slate-300 hover:bg-slate-900 hover:text-white'
              }`}
            >
              <span className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-slate-300 group-hover:bg-slate-800">
                <Icon size={18} />
              </span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <button className="mt-6 flex items-center justify-center gap-2 rounded-3xl border border-slate-800 bg-slate-900 py-3 text-sm text-slate-300 transition hover:border-slate-600 hover:bg-slate-800">
        <Settings size={18} />
        <span>Settings</span>
      </button>
    </aside>
  )
}
