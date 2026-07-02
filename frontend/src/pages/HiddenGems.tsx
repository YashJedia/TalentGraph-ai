import { useEffect, useState } from 'react'
import { api } from '../services/api'

type CandidateSummary = {
  id: string
  candidate_id: string
  anonymized_name?: string
  current_title?: string
  current_company?: string
}

type Ranking = {
  id: string
  job_id?: string
  candidate_id: string
  candidate?: CandidateSummary
  final_score: number
  rank: number
  percentile: number
}

export default function HiddenGems() {
  const [hiddenGems, setHiddenGems] = useState<Ranking[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadHiddenGems() {
      try {
        const response = await api.getAllHiddenGems()
        setHiddenGems(response.data)
      } catch (error) {
        console.error('Hidden gems load failed', error)
      } finally {
        setLoading(false)
      }
    }
    loadHiddenGems()
  }, [])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-semibold text-white">Hidden Gems</h1>
        <p className="mt-3 text-slate-400 max-w-2xl">Discover candidates with strong long-term potential and under-the-radar signals.</p>
      </div>

      <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-white">Hidden gems pipeline</h2>
            <p className="mt-2 text-sm text-slate-400">Showcase the top-ranked hidden gem candidates from across your active roles.</p>
          </div>
          <span className="inline-flex rounded-2xl bg-slate-800 px-4 py-2 text-sm text-slate-200 shadow-inner shadow-slate-950/20">{loading ? 'Loading...' : `${hiddenGems.length} candidates`}</span>
        </div>

        <div className="mt-8 overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/95 shadow-inner shadow-slate-950/10">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
              <thead className="bg-slate-900 text-slate-400">
                <tr>
                  <th className="px-4 py-4">Rank</th>
                  <th className="px-4 py-4">Candidate</th>
                  <th className="px-4 py-4">Score</th>
                  <th className="px-4 py-4">Percentile</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {loading ? (
                  <tr>
                    <td className="px-4 py-10 text-slate-500" colSpan={4}>
                      Loading hidden gem candidates...
                    </td>
                  </tr>
                ) : hiddenGems.length === 0 ? (
                  <tr>
                    <td className="px-4 py-10 text-slate-500" colSpan={4}>
                      No hidden gems found. Run ranking workflows for candidate pools to populate this view.
                    </td>
                  </tr>
                ) : (
                  hiddenGems.map((item) => (
                    <tr key={item.id} className="transition hover:bg-slate-900/80">
                      <td className="px-4 py-4 font-semibold text-white">{item.rank}</td>
                      <td className="px-4 py-4">
                        <div className="font-semibold text-white">{item.candidate?.anonymized_name ?? item.candidate_id}</div>
                        <div className="text-slate-400">{item.candidate?.current_title ?? 'Candidate profile'}</div>
                      </td>
                      <td className="px-4 py-4">{Math.round(item.final_score * 100)}%</td>
                      <td className="px-4 py-4">{item.percentile.toFixed(1)}%</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
