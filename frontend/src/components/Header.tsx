import { useAppStore } from '../context/store'

export default function Header() {
  const { darkMode, toggleDarkMode } = useAppStore()

  return (
    <header className="sticky top-0 z-20 bg-slate-900/95 backdrop-blur border-b border-slate-700/80 px-8 py-5 flex items-center justify-between shadow-lg shadow-slate-950/20">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-gradient-to-br from-blue-500 to-indigo-500 shadow-xl shadow-blue-500/20 text-lg font-bold text-white">
          TG
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-400">TalentGraph AI</p>
          <h1 className="text-2xl font-semibold text-white">Recruiter Intelligence</h1>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={toggleDarkMode}
          className="rounded-2xl bg-slate-800 px-4 py-2 text-slate-300 shadow-sm shadow-slate-950/10 hover:bg-slate-700"
        >
          {darkMode ? '🌙 Dark' : '☀️ Light'}
        </button>
        <button className="rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-2 text-white shadow-lg shadow-blue-500/20 hover:from-blue-500 hover:to-indigo-500">
          Logout
        </button>
      </div>
    </header>
  )
}
