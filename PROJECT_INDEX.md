# 🚀 TalentGraph AI - Complete Project Guide

**Explainable Multi-Agent Candidate Intelligence Platform**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Phase Breakdown](#phase-breakdown)
5. [Key Technologies](#key-technologies)
6. [Dataset Integration](#dataset-integration)
7. [Next Steps](#next-steps)

---

## 🎯 Project Overview

**TalentGraph AI** is a production-ready platform for intelligent candidate ranking that goes beyond keyword matching. Using multi-agent AI, it:

- 🧠 **Understands Requirements**: Semantically analyzes job descriptions
- 👥 **Evaluates Holistically**: Analyzes candidate profiles beyond skills
- 🎯 **Explains Decisions**: Provides recruiter-friendly explanations
- 💎 **Finds Hidden Gems**: Discovers non-obvious matches
- 🔒 **Detects Fraud**: Identifies suspicious profiles
- 📊 **Tracks Trajectories**: Analyzes career growth patterns
- 💬 **Converses**: LLM-powered recruiter assistant

### Key Features

| Feature | How It Works |
|---------|-----------|
| **Semantic Ranking** | Job & candidate embeddings with hybrid BM25+cosine retrieval |
| **7 AI Agents** | Specialized agents for different aspects of evaluation |
| **Explainability** | SHAP values, feature importance, natural language explanations |
| **Hidden Gems** | Detect career transition potential, transferable skills |
| **Fraud Detection** | Isolation Forest + rule-based anomaly detection |
| **Recruiter Copilot** | Conversational AI with RAG for context-aware responses |

---

## ⚡ Quick Start

### Local Development (Docker)

```bash
# 1. Clone & navigate
git clone <repo>
cd talentgraph-ai

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be healthy
docker-compose ps

# 4. Access applications
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Qdrant: http://localhost:6333
```

### Manual Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
talentgraph-ai/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                      # API routes (Phase 2)
│   │   ├── agents/                   # AI agents (Phase 3)
│   │   ├── db/
│   │   │   ├── session.py           # Database configuration ✅
│   │   │   └── models/
│   │   ├── models/
│   │   │   ├── database.py          # SQLAlchemy models ✅
│   │   │   └── schemas.py           # Pydantic schemas ✅
│   │   ├── services/
│   │   │   ├── embeddings.py        # Sentence Transformers ✅
│   │   │   ├── qdrant.py            # Vector DB client ✅
│   │   │   ├── bm25_search.py       # BM25 search (Phase 2)
│   │   │   └── llm.py               # LLM integration (Phase 3)
│   │   ├── config/
│   │   │   └── settings.py          # Configuration ✅
│   │   └── main.py                  # App entry point ✅
│   ├── requirements.txt              # Dependencies ✅
│   ├── alembic/                      # Database migrations
│   └── tests/                        # Unit tests
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/              # Reusable components ✅
│   │   │   ├── Layout.tsx           # Main layout ✅
│   │   │   ├── Header.tsx           # Header component ✅
│   │   │   ├── Sidebar.tsx          # Navigation sidebar ✅
│   │   │   └── Card.tsx             # Card components ✅
│   │   ├── pages/                   # Page components ✅
│   │   │   ├── Dashboard.tsx
│   │   │   ├── CandidateSearch.tsx
│   │   │   ├── CandidateRanking.tsx
│   │   │   ├── HiddenGems.tsx
│   │   │   ├── FraudAlerts.tsx
│   │   │   ├── RecruiterCopilot.tsx
│   │   │   └── CandidateComparison.tsx
│   │   ├── services/
│   │   │   └── api.ts               # API client ✅
│   │   ├── context/
│   │   │   └── store.ts             # State management ✅
│   │   ├── styles/
│   │   │   └── globals.css          # Global styles ✅
│   │   ├── App.tsx                  # Main app ✅
│   │   └── main.tsx                 # Entry point ✅
│   ├── package.json                 # Dependencies ✅
│   ├── vite.config.ts               # Vite config ✅
│   └── tsconfig.json                # TypeScript config ✅
│
├── docker/
│   └── Dockerfile.backend            # Backend Docker image ✅
│
├── docker-compose.yml                # Multi-container setup ✅
│
├── DATABASE_SCHEMA.sql               # Full database schema ✅
├── ARCHITECTURE.md                   # System architecture ✅
├── README.md                         # Project README ✅
│
├── PHASE1_SETUP.md                  # ✅ COMPLETE
├── PHASE2_BACKEND_INFRASTRUCTURE.md # IN PROGRESS
├── PHASE3_AI_AGENTS.md              # PLANNED
├── PHASE4_FRONTEND.md               # PLANNED
└── PHASE5_DEPLOYMENT.md             # PLANNED
```

---

## 🎯 Phase Breakdown

### ✅ **PHASE 1: Project Setup & Infrastructure**

**Status**: COMPLETE ✅

**Deliverables**:
- ✅ Complete folder structure
- ✅ Database schema (20+ tables)
- ✅ Configuration management
- ✅ Base FastAPI app
- ✅ Frontend structure
- ✅ Docker setup
- ✅ Documentation

**Files Created**:
- Database: `DATABASE_SCHEMA.sql`
- Architecture: `ARCHITECTURE.md`
- Config: `.env.example`, `settings.py`
- Models: `database.py`, `schemas.py`
- Services: `embeddings.py`, `qdrant.py`

---

### 📌 **PHASE 2: Backend Infrastructure** 

**Status**: TO START

**Estimated Duration**: 3-4 days

**Key Deliverables**:
- Implement all API endpoints
- Create repository pattern (database layer)
- Build service layer (BM25, hybrid search)
- JSONL dataset import
- Error handling & validation
- Comprehensive tests

**Files to Create**:
```
backend/app/
├── api/
│   ├── routes.py
│   └── v1/
│       ├── jobs.py
│       ├── candidates.py
│       ├── rankings.py
│       ├── search.py
│       ├── fraud.py
│       ├── comparison.py
│       ├── copilot.py
│       └── health.py
├── db/
│   ├── repository.py
│   └── queries.py
└── services/
    ├── bm25_search.py
    ├── hybrid_search.py
    └── crud.py
```

**See**: [PHASE2_BACKEND_INFRASTRUCTURE.md](./PHASE2_BACKEND_INFRASTRUCTURE.md)

---

### 🤖 **PHASE 3: AI Agents & Scoring**

**Status**: PLANNED

**Estimated Duration**: 5-7 days

**7 AI Agents**:
1. Role Understanding Agent
2. Candidate Intelligence Agent
3. Behavioral Analysis Agent
4. Career Trajectory Agent
5. Fraud Detection Agent
6. Ranking Agent
7. Recruiter Copilot Agent

**Key Features**:
- Semantic analysis with embeddings
- Career trajectory metrics
- Fraud detection (Isolation Forest)
- Hybrid retrieval (BM25 + embedding)
- SHAP explainability
- LLM integration (Gemini/OpenAI)
- RAG-based copilot

**See**: [PHASE3_AI_AGENTS.md](./PHASE3_AI_AGENTS.md)

---

### 🎨 **PHASE 4: Frontend Implementation**

**Status**: PLANNED

**Estimated Duration**: 4-5 days

**7 Pages**:
1. Dashboard
2. Candidate Search
3. Candidate Ranking
4. Hidden Gems
5. Fraud Alerts
6. Recruiter Copilot
7. Candidate Comparison

**Tech Stack**:
- React 18
- TypeScript
- TailwindCSS
- ShadCN UI
- Zustand (state management)
- Recharts (visualizations)

**See**: [PHASE4_FRONTEND.md](./PHASE4_FRONTEND.md)

---

### 🚀 **PHASE 5: Deployment & Documentation**

**Status**: PLANNED

**Estimated Duration**: 2-3 days

**Deployment Targets**:
- Backend: Render
- Frontend: Vercel
- Database: Supabase
- Vector DB: Qdrant Cloud

**CI/CD**:
- GitHub Actions pipeline
- Automated testing
- Docker builds
- Zero-downtime deployments

**Documentation**:
- Setup guide
- API documentation
- Developer guide
- User manual

**See**: [PHASE5_DEPLOYMENT.md](./PHASE5_DEPLOYMENT.md)

---

## 🔧 Key Technologies

### Backend
```
Framework:     FastAPI 0.104+
Language:      Python 3.11+
Database:      PostgreSQL 16+
Vector DB:     Qdrant
ORM:           SQLAlchemy 2.0+
API Docs:      Swagger/ReDoc
```

### AI & ML
```
Embeddings:    Sentence Transformers (BAAI/bge-large-en-v1.5)
LLM:           Gemini API (primary), OpenAI (fallback)
Search:        rank-bm25 + vector similarity
Anomaly:       Scikit-Learn Isolation Forest
Explainability: SHAP
```

### Frontend
```
Framework:     React 18
Language:      TypeScript
Styling:       TailwindCSS
Components:    ShadCN UI
State:         Zustand
Charts:        Recharts
HTTP:          Axios
```

### Infrastructure
```
Containers:    Docker & Docker Compose
Frontend:      Vercel
Backend:       Render
Database:      Supabase (PostgreSQL)
Vector DB:     Qdrant Cloud
CI/CD:         GitHub Actions
```

---

## 📊 Dataset Integration

### Data Source
```
[PUB] India_runs_data_and_ai_challenge/
└── India_runs_data_and_ai_challenge/
    ├── candidates.jsonl              # Main dataset
    ├── candidate_schema.json          # Schema definition
    ├── sample_candidates.json         # Sample data
    ├── sample_submission.csv
    ├── job_description.docx
    └── validate_submission.py
```

### Data Import Flow

```
1. JSONL Upload
   ↓
2. Schema Validation
   ↓
3. Parse Candidate Data
   ├── Profile
   ├── Career History
   ├── Education
   └── Skills
   ↓
4. Generate Embeddings (Sentence Transformers)
   ↓
5. Store in PostgreSQL + Qdrant
   ├── Relational data → PostgreSQL
   └── Vector embeddings → Qdrant
   ↓
6. Run Analysis Agents
   ├── Candidate Intelligence
   ├── Career Trajectory
   ├── Fraud Detection
   └── Generate scores
   ↓
7. Ready for Ranking
```

### Example Candidate Record
```json
{
  "candidate_id": "CAND_0000001",
  "profile": {
    "anonymized_name": "Ira Vora",
    "headline": "Backend Engineer | SQL, Spark, Cloud",
    "years_of_experience": 6.9,
    "current_title": "Backend Engineer",
    "current_company": "Mindtree"
  },
  "career_history": [...],
  "education": [...],
  "skills": [
    {
      "name": "Python",
      "proficiency": "expert",
      "endorsements": 45
    }
  ]
}
```

---

## 🚀 Next Steps

### Immediate (This Week)
- [x] Phase 1: Project Setup ✅
- [ ] Start Phase 2: Backend API endpoints
- [ ] Create repository pattern
- [ ] Implement CRUD operations
- [ ] Setup database migrations

### Short Term (Next 2 Weeks)
- [ ] Complete Phase 2: All endpoints working
- [ ] Start Phase 3: AI agents
- [ ] Dataset import functionality
- [ ] Hybrid search implementation

### Medium Term (Next Month)
- [ ] Complete Phase 3: All agents functional
- [ ] Complete Phase 4: Frontend pages
- [ ] Full integration testing
- [ ] Performance optimization

### Long Term (Months 2-3)
- [ ] Complete Phase 5: Deployment
- [ ] Security audit
- [ ] Production launch
- [ ] User feedback & iterations

---

## 📖 Documentation Index

| Document | Purpose | Status |
|----------|---------|--------|
| [README.md](./README.md) | Project overview | ✅ |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System architecture | ✅ |
| [DATABASE_SCHEMA.sql](./DATABASE_SCHEMA.sql) | Database design | ✅ |
| [PHASE1_SETUP.md](./README.md) | Phase 1 details | ✅ |
| [PHASE2_BACKEND_INFRASTRUCTURE.md](./PHASE2_BACKEND_INFRASTRUCTURE.md) | Phase 2 guide | ⏳ |
| [PHASE3_AI_AGENTS.md](./PHASE3_AI_AGENTS.md) | AI agents specification | ⏳ |
| [PHASE4_FRONTEND.md](./PHASE4_FRONTEND.md) | Frontend guide | ⏳ |
| [PHASE5_DEPLOYMENT.md](./PHASE5_DEPLOYMENT.md) | Deployment guide | ⏳ |

---

## 💡 Key Insights

### Why This Architecture?

1. **Modular Design**: Each agent is independent and testable
2. **Scalability**: Microservices-ready, can be deployed separately
3. **Explainability**: SHAP values + narrative explanations
4. **Hybrid Search**: BM25 + semantic for best relevance
5. **AI-First**: Multi-agent orchestration for complex reasoning
6. **Modern Stack**: Latest stable versions of all dependencies

### Scoring Formula

```
Final Score = 
  0.35 × Semantic Match +
  0.20 × Experience Match +
  0.15 × Behavioral Score +
  0.10 × Career Growth +
  0.10 × Leadership +
  0.10 × Culture Fit

Each component: 0-1 scale
Final score: 0-100 scale
```

### Hidden Gem Detection

```
is_hidden_gem = (
    final_score >= 0.7 AND
    semantic_score < 0.6 AND      // Not obvious match
    skill_evolution > 0.8 AND      // Strong growth
    career_trajectory_fit > 0.75   // Career path aligns
)
```

---

## 📞 Support & Questions

For questions about specific phases or components:
- See the phase-specific documentation
- Check ARCHITECTURE.md for system design
- Review DATABASE_SCHEMA.sql for data model

---

## 📝 License & Attribution

TalentGraph AI - Production Ready Candidate Intelligence Platform
2024 - All Rights Reserved

---

**Last Updated**: June 26, 2024
**Project Status**: Phase 1 Complete ✅ | Phase 2 Starting
**Maintained by**: AI Architecture Team
