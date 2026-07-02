import { Link, useLocation } from 'react-router-dom'
import {
  BarChart3,
  Search,
  Zap,
  Gem,
  AlertTriangle,
  MessageCircle,
  HelpCircle,
  TrendingUp,
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
    <aside className="sticky top-0 h-screen flex w-72 flex-col border-r border-slate-800/40 bg-slate-950/60 p-5 backdrop-blur-2xl z-30">
      {/* Branding Hub */}
      <div className="mb-8 rounded-2xl border border-slate-800/60 bg-slate-900/30 p-4 ring-1 ring-white/5">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-400 to-violet-600 font-extrabold text-white shadow-lg shadow-sky-500/15">
            TG
          </div>
          <div>
            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">Platform</span>
            <h2 className="text-base font-bold text-white tracking-tight">TalentGraph AI</h2>
          </div>
        </div>
        <p className="mt-3 text-xs leading-relaxed text-slate-400">
          Decentralized explainable multi-agent candidate ranking framework.
        </p>
      </div>

      {/* Menu Navigation */}
      <nav className="flex-1 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive =
            location.pathname === item.path ||
            (item.path !== '/' && location.pathname.startsWith(item.path.split('/')[1]))

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold transition-all duration-300 ${
                isActive
                  ? 'bg-gradient-to-r from-sky-500/10 to-violet-600/10 text-white border border-sky-500/20 shadow-md shadow-sky-950/20 glow-card'
                  : 'text-slate-400 border border-transparent hover:bg-slate-900/40 hover:text-slate-100 hover:border-slate-800/50'
              }`}
            >
              <span
                className={`inline-flex h-9 w-9 items-center justify-center rounded-lg transition-all duration-300 ${
                  isActive
                    ? 'bg-gradient-to-br from-sky-500 to-violet-600 text-white shadow-md'
                    : 'bg-slate-900 border border-slate-800/60 text-slate-500 group-hover:bg-slate-800 group-hover:text-slate-300'
                }`}
              >
                <Icon size={16} />
              </span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Recruiter Deck widgets */}
      <div className="mt-8 rounded-2xl border border-slate-800/50 bg-slate-900/20 p-4 ring-1 ring-white/5 relative overflow-hidden">
        {/* Glow Element */}
        <div className="absolute top-0 right-0 h-10 w-10 bg-indigo-500/10 rounded-full blur-xl pointer-events-none" />
        
        <div className="flex items-center gap-1.5 text-xs text-sky-400 font-bold uppercase tracking-wider">
          <TrendingUp size={12} />
          <span>Realtime Insights</span>
        </div>
        <p className="mt-2 text-xs leading-relaxed text-slate-400">
          Rank jobs to compute SHAP explanations and locate hidden gems.
        </p>
        <Link
          to="/search"
          className="mt-4 flex w-full items-center justify-center rounded-xl bg-slate-900 hover:bg-slate-800 text-xs font-bold text-slate-200 py-2.5 transition border border-slate-800"
        >
          Begin Search Flow
        </Link>
      </div>

      {/* Footer Branding line */}
      <div className="mt-4 flex items-center justify-between px-2 text-[10px] text-slate-500 font-semibold border-t border-slate-900 pt-4">
        <span>© TalentGraph AI</span>
        <a href="#help" className="hover:text-slate-300 flex items-center gap-1">
          <HelpCircle size={10} /> Support
        </a>
      </div>
    </aside>
  )
}
