import axios from 'axios'

const rawApiUrl = (import.meta as any).env.VITE_API_URL
const API_URL = (() => {
  if (!rawApiUrl || rawApiUrl.trim() === '') {
    return '/api/v1'
  }

  try {
    const parsed = new URL(rawApiUrl)
    if (['backend', 'localhost', '127.0.0.1'].includes(parsed.hostname)) {
      return '/api/v1'
    }
  } catch {
    // Not a full URL, continue with the raw string
  }

  const normalized = rawApiUrl.replace(/\/+$|\?/g, '')
  return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`
})()

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
})

export const api = {
  // Jobs
  getJobs: () => apiClient.get('/jobs'),
  getJob: (jobId: string) => apiClient.get(`/jobs/${jobId}`),
  createJob: (jobData: any) => apiClient.post('/jobs', jobData),

  // Candidates
  getCandidates: () => apiClient.get('/candidates'),
  getCandidate: (candidateId: string) => apiClient.get(`/candidates/${candidateId}`),
  createCandidate: (candidateData: any) => apiClient.post('/candidates', candidateData),
  uploadCandidates: (candidates: any) => apiClient.post('/candidates/bulk', candidates),

  // Rankings
  getRankings: (jobId: string, limit?: number) =>
    apiClient.get(`/rankings/job/${jobId}`, { params: { limit } }),
  getTopCandidates: (jobId: string) => apiClient.get(`/rankings/${jobId}/top10`),
  getHiddenGems: (jobId: string) => apiClient.get(`/rankings/${jobId}/hidden-gems`),
  getAllHiddenGems: () => apiClient.get('/rankings/hidden-gems'),
  searchCandidates: (searchParams: any) => apiClient.post('/search', searchParams),
  getSystemStats: () => apiClient.get('/stats'),

  // Fraud Detection
  getFraudAlerts: () => apiClient.get('/fraud/alerts'),
  getFraudAlert: (alertId: string) => apiClient.get(`/fraud/alerts/${alertId}`),

  // Comparison
  compareCandidates: (candidateIds: string[], jobId: string) =>
    apiClient.post('/comparison', { candidate_ids: candidateIds, job_id: jobId }),

  // Copilot
  askCopilot: (message: string, context?: any) =>
    apiClient.post('/copilot/ask', { content: message, context }),

  // Imports & workflows
  importSampleJobs: () => apiClient.post('/jobs/import-sample'),
  importCandidateDataset: (limit?: number) =>
    apiClient.post('/candidates/import-dataset', null, { params: { limit } }),
  rankCandidatesForJob: (jobId: string, limit?: number) =>
    apiClient.post(`/rankings/job/${jobId}`, null, { params: { limit } }),

  // Health
  health: () => apiClient.get('/health'),
}

export default apiClient
