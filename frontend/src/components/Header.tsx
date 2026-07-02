import { useAppStore } from '../context/store'

export default function Header() {
  const { darkMode, toggleDarkMode } = useAppStore()

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/60 bg-slate-900/95 backdrop-blur-2xl px-8 py-4 shadow-sm shadow-slate-950/10">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-3xl bg-gradient-to-br from-sky-500 to-violet-600 text-xl font-black text-white shadow-xl shadow-sky-500/20">
            TG
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-slate-500">TalentGraph AI</p>
            <h1 className="text-lg font-semibold text-white">Recruiter intelligence console</h1>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={toggleDarkMode}
            className="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-slate-200 shadow-sm shadow-slate-950/10 transition hover:bg-slate-800"
          >
            {darkMode ? '🌙 Dark' : '☀️ Light'}
          </button>
          <button className="rounded-2xl bg-gradient-to-r from-sky-500 to-violet-600 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500">
            New candidate flow
          </button>
        </div>
      </div>
    </header>
  )
}
