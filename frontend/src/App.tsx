import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import CandidateSearch from './pages/CandidateSearch'
import CandidateRanking from './pages/CandidateRanking'
import HiddenGems from './pages/HiddenGems'
import FraudAlerts from './pages/FraudAlerts'
import RecruiterCopilot from './pages/RecruiterCopilot'
import CandidateComparison from './pages/CandidateComparison'
import Layout from './components/Layout'
import './styles/globals.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/search" element={<CandidateSearch />} />
          <Route path="/ranking/new" element={<CandidateRanking />} />
          <Route path="/ranking/:jobId" element={<CandidateRanking />} />
          <Route path="/hidden-gems" element={<HiddenGems />} />
          <Route path="/fraud-alerts" element={<FraudAlerts />} />
          <Route path="/copilot" element={<RecruiterCopilot />} />
          <Route path="/comparison" element={<CandidateComparison />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
