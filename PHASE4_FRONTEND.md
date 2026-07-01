# PHASE 4: Frontend React Application

## Overview
Build the modern, professional React frontend with TailwindCSS and ShadCN components.

## Page Specifications

### 1. Dashboard (`/`)

**Components**:
- Stats Cards (4 columns)
  - Total Jobs
  - Total Candidates
  - Pending Rankings
  - Fraud Alerts
- Recent Rankings Section
- Top Candidates Section
- System Health Status

**Metrics to Display**:
```json
{
  "total_jobs": 0,
  "total_candidates": 0,
  "pending_rankings": 0,
  "fraud_alerts_pending": 0,
  "average_ranking_score": 0.0,
  "processing_time_ms": 0
}
```

### 2. Candidate Search (`/search`)

**Components**:
- Advanced Search Form
  - Job title filter
  - Company filter
  - Location filter
  - Skills multi-select
  - Experience range slider
  - Seniority level select
- Search Results Table
  - Candidate name (anonymized)
  - Current title
  - Experience
  - Match score
  - Actions (view, compare, rank)
- Pagination

**Features**:
- Real-time search (debounced)
- Faceted search
- Quick filters
- Saved searches

### 3. Candidate Ranking (`/ranking/:jobId`)

**Components**:
- Job Details Card
  - Job title, company, description
  - Required skills
  - Seniority level
- Ranking Results Table (sorted by score)
  - Rank (1-10)
  - Candidate name
  - Final score (0-100)
  - Component scores (radar mini)
  - Status (hidden gem, fraud flagged)
  - Actions

- Detailed Score Breakdown
  - Semantic Match: 90
  - Experience Match: 85
  - Behavioral Score: 78
  - Career Growth: 82
  - Leadership: 75
  - Culture Fit: 88

- Candidate Card (expandable)
  - Full profile details
  - Career history timeline
  - Skills with proficiency
  - Education
  - Explanations (SHAP values)

### 4. Hidden Gems (`/hidden-gems`)

**Components**:
- Filter sidebar
  - Target roles
  - Min score
  - Max score
  - Industry
- Hidden Gems Grid
  - Card per candidate
  - Why they're a hidden gem
  - Relevant skills
  - Career trajectory chart
  - Match score

**Hidden Gem Indicators**:
- Strong transferable skills
- Non-obvious career paths
- High potential transitions

### 5. Fraud Alerts (`/fraud-alerts`)

**Components**:
- Alert Statistics
  - Total alerts
  - By severity
  - Resolved vs pending
- Alert Table
  - Candidate name
  - Alert type (skill_stuffing, etc.)
  - Severity (critical, high, medium, low)
  - Confidence score
  - Status (reviewed, pending)
  - Evidence (expandable)

- Alert Details Modal
  - Full evidence
  - Manual review option
  - Notes field
  - Approve/Reject actions

**Alert Types**:
- Skill Stuffing
- Timeline Inconsistencies
- Unrealistic Claims
- Profile Anomalies

### 6. Recruiter Copilot (`/copilot`)

**Components**:
- Chat Interface
  - Message history
  - User input area
  - Send button
  - Clear conversation

- Right Sidebar
  - Context candidates
  - Recent jobs
  - Suggested questions

**Suggested Questions**:
- Why is Candidate A ranked higher?
- Find candidates who can transition to AI?
- Compare these candidates
- Explain this ranking
- Generate interview questions

**Features**:
- Streaming responses
- Context awareness
- Code syntax highlighting
- Download transcripts
- Save favorite conversations

### 7. Candidate Comparison (`/comparison`)

**Components**:
- Candidate Selection
  - Multi-select (up to 5)
  - Search by name/ID
- Comparison Table
  - Vertical layout with candidates as columns
  - Metrics as rows
  - Color coding (green for advantages)
- Side-by-Side Details
  - Career timeline
  - Skills comparison
  - Education comparison
- Radar Chart (superimposed)
- Recommendations Section

**Comparison Metrics**:
- Experience (years)
- Skill Match %
- All component scores
- Career trajectory
- Behavioral signals

## UI/UX Specifications

### Design System

**Colors**:
```css
--primary: #3b82f6          /* Blue */
--secondary: #8b5cf6        /* Purple */
--success: #10b981          /* Green */
--warning: #f59e0b          /* Amber */
--error: #ef4444            /* Red */
--background: #0f172a       /* Dark blue */
--surface: #1a2332          /* Slate */
--border: #334155           /* Border gray */
```

**Typography**:
- Heading: 24px, 700 weight
- Subheading: 18px, 600 weight
- Body: 14px, 400 weight
- Small: 12px, 400 weight

**Components**:
- Button: Blue primary, 36px height
- Input: Slate surface, 8px border-radius
- Card: Slate surface, 1px border, shadow
- Modal: Overlay + card

### Responsive Design
- Mobile: 320px+
- Tablet: 768px+
- Desktop: 1024px+

## Implementation Files

```
frontend/src/
├── components/
│   ├── Layout.tsx
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── Card.tsx
│   ├── Table.tsx
│   ├── Chart/
│   │   ├── RadarChart.tsx
│   │   ├── TimelineChart.tsx
│   │   └── ComparisonChart.tsx
│   ├── Forms/
│   │   ├── SearchForm.tsx
│   │   ├── RankingForm.tsx
│   │   └── JobForm.tsx
│   ├── Modals/
│   │   ├── CandidateModal.tsx
│   │   ├── ComparisonModal.tsx
│   │   └── AlertModal.tsx
│   └── Copilot/
│       ├── ChatWindow.tsx
│       ├── MessageList.tsx
│       └── InputArea.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── CandidateSearch.tsx
│   ├── CandidateRanking.tsx
│   ├── HiddenGems.tsx
│   ├── FraudAlerts.tsx
│   ├── RecruiterCopilot.tsx
│   └── CandidateComparison.tsx
├── hooks/
│   ├── useApi.ts                # Data fetching
│   ├── usePagination.ts         # Pagination logic
│   ├── useSearch.ts             # Search logic
│   └── useLocalStorage.ts       # Persist state
├── services/
│   └── api.ts                   # API client ✅
├── context/
│   ├── store.ts                 # Zustand store ✅
│   └── AuthContext.tsx          # Auth management
├── lib/
│   ├── utils.ts                 # Helper functions
│   └── api-client.ts
├── styles/
│   ├── globals.css              # Global styles ✅
│   └── tailwind.config.js
├── types/
│   └── index.ts                 # TypeScript types
├── App.tsx                      # Main app ✅
└── main.tsx                     # Entry point ✅
```

## Key Implementation Patterns

### Data Fetching Hook
```typescript
function useGetRankings(jobId: string) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    // Fetch rankings
  }, [jobId])
  
  return { data, loading }
}
```

### Form Component
```typescript
function SearchForm() {
  const [formData, setFormData] = useState({})
  const { mutate } = useSearch()
  
  const onSubmit = (e) => {
    e.preventDefault()
    mutate(formData)
  }
  
  return <form onSubmit={onSubmit}>...</form>
}
```

### Chart Component
```typescript
function RadarChart({ data }) {
  return (
    <ResponsiveRadar
      data={data}
      keys={['semantic', 'experience', 'behavior', ...]}
      ...
    />
  )
}
```

## API Integration

Each page calls specific API endpoints:

| Page | Endpoints |
|------|-----------|
| Dashboard | GET /health, GET /stats |
| Search | GET /candidates, GET /jobs |
| Ranking | GET /rankings/{jobId}, GET /rankings/{id}/explain |
| Hidden Gems | GET /rankings/{jobId}/hidden-gems |
| Fraud Alerts | GET /fraud/alerts |
| Copilot | POST /copilot/ask |
| Comparison | POST /comparison |

## Testing (`frontend/tests/`)

```typescript
// Dashboard.test.tsx
describe('Dashboard', () => {
  it('displays stats cards', () => {})
  it('loads rankings', () => {})
})

// CandidateSearch.test.tsx
describe('CandidateSearch', () => {
  it('searches candidates', () => {})
  it('filters by skills', () => {})
})
```

## Performance Optimization

1. **Code Splitting**
   ```typescript
   const Dashboard = lazy(() => import('./pages/Dashboard'))
   ```

2. **Memoization**
   ```typescript
   const CandidateCard = memo(({ candidate }) => ...)
   ```

3. **Virtual Scrolling** (for large lists)
   ```typescript
   import { FixedSizeList } from 'react-window'
   ```

4. **Lazy Images**
   ```typescript
   <img loading="lazy" src="..." />
   ```

5. **Service Worker** (PWA)
   ```typescript
   if ('serviceWorker' in navigator) {
     navigator.serviceWorker.register('/sw.js')
   }
   ```

## Success Criteria
✅ All 7 pages functional
✅ Real-time data updates
✅ Responsive on mobile/tablet/desktop
✅ < 2s initial load
✅ Smooth animations
✅ Accessibility (WCAG 2.1 AA)
✅ > 90 Lighthouse score
