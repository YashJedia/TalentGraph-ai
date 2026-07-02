import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'

type Candidate = {
  id: string
  candidate_id: string
  anonymized_name?: string
  headline?: string
  current_title?: string
  current_company?: string
  location?: string
  current_industry?: string
  years_of_experience?: number
}

type Job = {
  id: string
  job_title: string
  company_name: string
}

type SearchResult = {
  candidate: Candidate
  score: number
}

export default function CandidateSearch() {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [jobs, setJobs] = useState<Job[]>([])
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedJob, setSelectedJob] = useState('')
  const [loading, setLoading] = useState(true)
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    async function loadData() {
      try {
        const [candidatesResponse, jobsResponse] = await Promise.all([
          api.getCandidates(),
          api.getJobs(),
        ])
        setCandidates(candidatesResponse.data)
        setJobs(jobsResponse.data)
      } catch (error) {
        console.error('Candidate search load failed', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  useEffect(() => {
    async function fetchSearchResults() {
      if (!selectedJob) {
        setSearchResults([])
        return
      }
      setSearching(true)
      try {
        const response = await api.searchCandidates({
          job_id: selectedJob,
          limit: 50,
          offset: 0,
          include_hidden_gems: true,
          exclude_fraud_flagged: true,
          min_score: 0.4,
        })
        setSearchResults(response.data.results)
      } catch (error) {
        console.error('Candidate search API failed', error)
        setSearchResults([])
      } finally {
        setSearching(false)
      }
    }

    fetchSearchResults()
  }, [selectedJob])

  const filteredCandidates = useMemo(() => {
    const lowerSearch = searchTerm.toLowerCase()
    const source = selectedJob ? searchResults.map((item) => item.candidate) : candidates

    return source.filter((candidate) => {
      const candidateText = [
        candidate.anonymized_name,
        candidate.headline,
        candidate.current_title,
        candidate.current_company,
        candidate.location,
        candidate.current_industry,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()

      return candidateText.includes(lowerSearch)
    })
  }, [candidates, searchResults, searchTerm, selectedJob])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-semibold text-white">Candidate Search</h1>
        <p className="mt-3 text-slate-400 max-w-2xl">Filter and inspect candidate profiles across the TalentGraph database.</p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[300px_1fr]">
        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <div className="space-y-6">
            <div>
              <label className="text-sm font-semibold text-slate-300">Search candidates</label>
              <input
                className="mt-4 w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-4 text-slate-100 outline-none focus:border-sky-500"
                placeholder="Name, title, location or skill"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-semibold text-slate-300">Filter by job</label>
              <select
                className="mt-4 w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-4 text-slate-100 outline-none focus:border-sky-500"
                value={selectedJob}
                onChange={(event) => setSelectedJob(event.target.value)}
              >
                <option value="">All jobs</option>
                {jobs.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.job_title} at {job.company_name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white">Search results</h2>
              <p className="mt-2 text-sm text-slate-400">Browse candidates and explore their profile summaries.</p>
            </div>
            <span className="inline-flex rounded-2xl bg-slate-800 px-4 py-2 text-sm text-slate-200 shadow-inner shadow-slate-950/20">
              {loading || searching ? 'Loading...' : `${filteredCandidates.length} results`}
            </span>
          </div>
          <div className="mt-8 overflow-hidden rounded-3xl border border-slate-800 bg-slate-950/95 shadow-inner shadow-slate-950/10">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-800 text-left text-sm text-slate-300">
                <thead className="bg-slate-900 text-slate-400">
                  <tr>
                    <th className="px-4 py-4">Candidate</th>
                    <th className="px-4 py-4">Title</th>
                    <th className="px-4 py-4">Location</th>
                    <th className="px-4 py-4">Experience</th>
                    <th className="px-4 py-4">Company</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {(loading || searching) && selectedJob ? (
                    <tr>
                      <td className="px-4 py-10 text-slate-500" colSpan={5}>
                        Loading search results...
                      </td>
                    </tr>
                  ) : filteredCandidates.length === 0 ? (
                    <tr>
                      <td className="px-4 py-10 text-slate-500" colSpan={5}>
                        {loading ? 'Loading candidates…' : 'No candidates match your search criteria.'}
                      </td>
                    </tr>
                  ) : (
                    filteredCandidates.map((candidate) => (
                      <tr key={candidate.id} className="transition hover:bg-slate-900/80">
                        <td className="px-4 py-4">
                          <div className="font-semibold text-white">{candidate.anonymized_name}</div>
                          <div className="text-xs text-slate-500">{candidate.candidate_id}</div>
                        </td>
                        <td className="px-4 py-4">{candidate.current_title || candidate.headline || '—'}</td>
                        <td className="px-4 py-4">{candidate.location || '—'}</td>
                        <td className="px-4 py-4">{candidate.years_of_experience ?? '—'} yrs</td>
                        <td className="px-4 py-4">{candidate.current_company || '—'}</td>
                      </tr>
                    ))
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
