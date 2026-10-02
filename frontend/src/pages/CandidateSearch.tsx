import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import { Search, SlidersHorizontal, Briefcase, MapPin, Award } from 'lucide-react'

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

  // Get initials for name avatar
  const getInitials = (name?: string) => {
    if (!name) return 'C'
    const parts = name.trim().split(/\s+/)
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    }
    return parts[0][0].toUpperCase()
  }

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
          Candidate Search
        </h1>
        <p className="mt-2 text-sm text-slate-400 max-w-2xl">
          Filter and inspect candidate profiles with active semantic attributes and experience qualifiers.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[320px_1fr]">
        {/* Left filter card */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6 flex flex-col gap-6 h-fit">
          <h2 className="text-lg font-bold text-white flex items-center gap-1.5 border-b border-slate-900 pb-3">
            <SlidersHorizontal size={16} className="text-sky-400" />
            Search Filters
          </h2>
          
          <div className="space-y-5">
            {/* Search inputs */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <Search size={11} className="text-sky-400" /> Keyword query
              </label>
              <input
                className="w-full rounded-xl border border-slate-800 bg-slate-900/30 px-3.5 py-3 text-sm text-slate-100 placeholder:text-slate-500 outline-none focus:border-sky-500"
                placeholder="Name, skills, title, location"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
              />
            </div>

            {/* Job role matches */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <Briefcase size={11} className="text-sky-400" /> Job Matching Profile
              </label>
              <select
                className="w-full rounded-xl border border-slate-800 bg-slate-900/30 px-3.5 py-3 text-sm text-slate-100 outline-none focus:border-sky-500"
                value={selectedJob}
                onChange={(event) => setSelectedJob(event.target.value)}
              >
                <option value="" className="bg-slate-950">All Candidates</option>
                {jobs.map((job) => (
                  <option key={job.id} value={job.id} className="bg-slate-950">
                    {job.job_title} ({job.company_name})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Right results grid */}
        <div className="glass-card rounded-[24px] border border-slate-800 bg-slate-950/40 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-900 pb-4">
            <div>
              <h2 className="text-lg font-bold text-white">Ingested Rosters</h2>
              <p className="text-xs text-slate-400">Match credentials across vectors index and local lists.</p>
            </div>
            <span className="rounded-xl bg-slate-900 px-3.5 py-2 text-xs font-bold text-slate-300 border border-slate-800/80 shadow-md">
              {loading || searching ? (
                <span className="flex items-center gap-1.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-sky-500 animate-ping" />
                  Resolving...
                </span>
              ) : (
                `${filteredCandidates.length} Active Records`
              )}
            </span>
          </div>

          {/* Table list */}
          <div className="mt-6 overflow-hidden rounded-xl border border-slate-900 bg-slate-950/20">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-900/80 text-left text-xs text-slate-300">
                <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider font-bold">
                  <tr>
                    <th className="px-5 py-3.5">Candidate name</th>
                    <th className="px-5 py-3.5">Current Role</th>
                    <th className="px-5 py-3.5"><span className="flex items-center gap-1"><MapPin size={12} /> Location</span></th>
                    <th className="px-5 py-3.5"><span className="flex items-center gap-1"><Award size={12} /> Tenures</span></th>
                    <th className="px-5 py-3.5">Enterprise</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/40">
                  {loading || searching ? (
                    // Shimmer rows
                    Array.from({ length: 5 }).map((_, idx) => (
                      <tr key={idx}>
                        <td className="px-5 py-4" colSpan={5}>
                          <div className="h-5 rounded-lg shimmer-placeholder w-full" />
                        </td>
                      </tr>
                    ))
                  ) : filteredCandidates.length === 0 ? (
                    <tr>
                      <td className="px-5 py-10 text-slate-500 text-center" colSpan={5}>
                        No candidates match your queries in the database. Try adjusting your filter tags.
                      </td>
                    </tr>
                  ) : (
                    filteredCandidates.map((candidate) => (
                      <tr 
                        key={candidate.id} 
                        className="transition hover:bg-slate-900/35 group"
                      >
                        {/* Name Block with Avatar initials */}
                        <td className="px-5 py-4 flex items-center gap-3">
                          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500/10 to-violet-500/10 border border-sky-500/15 text-sky-400 font-extrabold text-xs shadow-inner">
                            {getInitials(candidate.anonymized_name)}
                          </div>
                          <div>
                            <div className="font-bold text-white group-hover:text-sky-400 transition">
                              {candidate.anonymized_name || 'Anonymous Profile'}
                            </div>
                            <div className="text-[10px] text-slate-500 font-mono mt-0.5">{candidate.candidate_id}</div>
                          </div>
                        </td>
                        <td className="px-5 py-4 font-semibold text-slate-300">
                          {candidate.current_title || candidate.headline || '—'}
                        </td>
                        <td className="px-5 py-4 text-slate-400 text-xs">
                          {candidate.location || 'Remote'}
                        </td>
                        <td className="px-5 py-4">
                          <span className="inline-flex items-center gap-1.5 rounded-lg bg-sky-500/5 border border-sky-500/10 px-2 py-1 text-slate-300 font-bold font-mono">
                            {candidate.years_of_experience ?? 0} yrs
                          </span>
                        </td>
                        <td className="px-5 py-4 text-slate-400">
                          {candidate.current_company || 'Freelance'}
                        </td>
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
