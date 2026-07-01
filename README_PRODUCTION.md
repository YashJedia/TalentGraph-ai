# 🚀 TalentGraph AI - Production-Ready Candidate Intelligence Platform

> **Explainable Multi-Agent AI System for Intelligent Candidate Ranking**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue)](https://react.dev/)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16-orange)](https://www.postgresql.org/)
[![Status](https://img.shields.io/badge/Phase-1%20%E2%9C%85-success)](./PROJECT_INDEX.md)

---

## 🎯 Overview

**TalentGraph AI** is a complete SaaS platform for intelligent candidate ranking that goes far beyond keyword matching. Using 7 specialized AI agents, it:

- 🧠 **Understands** job descriptions semantically
- 👥 **Analyzes** candidate profiles holistically  
- 🎯 **Explains** ranking decisions with SHAP
- 💎 **Discovers** hidden gem candidates
- 🔒 **Detects** fraudulent profiles
- 📊 **Tracks** career growth trajectories
- 💬 **Converses** via LLM-powered copilot

---

## ✨ Key Features

| Feature | Technology | Status |
|---------|-----------|--------|
| **Semantic Ranking** | BAAI/bge-large-en embeddings | ✅ Built |
| **Hybrid Retrieval** | BM25 + Vector similarity | 🏗️ Phase 2 |
| **7 AI Agents** | Multi-agent orchestration | 🏗️ Phase 3 |
| **Explainability** | SHAP + Natural language | 🏗️ Phase 3 |
| **Fraud Detection** | Isolation Forest | 🏗️ Phase 3 |
| **Career Analysis** | Growth metrics & trends | 🏗️ Phase 3 |
| **Recruiter Copilot** | Gemini/OpenAI + RAG | 🏗️ Phase 3 |
| **Modern UI** | React + TailwindCSS | 🏗️ Phase 4 |

---

## 🏗️ Architecture

```
Frontend (React)              Backend (FastAPI)           Data Layer
├── Dashboard                ├── Job API                 ├── PostgreSQL
├── Search                   ├── Candidate API           ├── Qdrant (Vector DB)
├── Ranking                  ├── Ranking API             └── Redis (Cache)
├── Hidden Gems              ├── 7 AI Agents
├── Fraud Alerts             ├── Copilot API
├── Copilot                  └── Scoring Engine
└── Comparison
```

---

## 📊 Scoring Formula

```
Final Score = 
  0.35 × Semantic Match       +
  0.20 × Experience Match     +
  0.15 × Behavioral Score     +
  0.10 × Career Growth        +
  0.10 × Leadership           +
  0.10 × Culture Fit
```

**Scale**: 0-100 | **Hidden Gems**: Non-obvious matches with high potential

---

## 🚀 Quick Start

### Option 1: Docker (Recommended) ⭐
```bash
# Start all services
docker-compose up -d

# Access:
# Frontend:  http://localhost:5173
# API Docs:  http://localhost:8000/docs
# Qdrant:    http://localhost:6333/dashboard
```

### Option 2: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

👉 **[See Full Setup Guide](./QUICKSTART.md)**

---

## 📁 Project Structure

```
talentgraph-ai/
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/         # Routes (Phase 2)
│   │   ├── agents/      # AI agents (Phase 3)
│   │   ├── models/      # Database models ✅
│   │   ├── services/    # Embeddings, Vector DB ✅
│   │   └── config/      # Settings ✅
│   └── requirements.txt  # Dependencies ✅
│
├── frontend/            # React + TypeScript
│   ├── src/
│   │   ├── pages/      # 7 pages ✅
│   │   ├── components/ # Components ✅
│   │   └── services/   # API client ✅
│   └── package.json    # Dependencies ✅
│
├── docker-compose.yml   # Multi-container setup ✅
├── DATABASE_SCHEMA.sql  # Full database schema ✅
├── ARCHITECTURE.md      # System design ✅
│
├── QUICKSTART.md        # 5-minute setup
├── PROJECT_INDEX.md     # Complete guide
├── IMPLEMENTATION_SUMMARY.md  # What's built
│
├── PHASE1_SETUP.md           # ✅ Complete
├── PHASE2_BACKEND_INFRASTRUCTURE.md  # Next
├── PHASE3_AI_AGENTS.md              # Then
├── PHASE4_FRONTEND.md               # Then
└── PHASE5_DEPLOYMENT.md             # Finally
```

---

## 🤖 7 AI Agents (Phase 3)

| Agent | Purpose | Output |
|-------|---------|--------|
| **Role Understanding** | Parse job descriptions | Skills, requirements |
| **Candidate Intelligence** | Analyze profiles | Skill depth, experience |
| **Behavioral Analysis** | Extract signals | Engagement scores |
| **Career Trajectory** | Growth metrics | Growth score, trends |
| **Fraud Detection** | Find anomalies | Risk score, alerts |
| **Ranking** | Calculate scores | Final score, rank |
| **Recruiter Copilot** | Conversational AI | Context-aware responses |

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](./QUICKSTART.md) | 5-minute setup ⭐ |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design |
| [PROJECT_INDEX.md](./PROJECT_INDEX.md) | Full guide |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | What's built |
| PHASE*_*.md | Phase specifications |

---

## 💻 Tech Stack

**Backend**: FastAPI • Python 3.11+ • SQLAlchemy • PostgreSQL • Qdrant  
**Frontend**: React 18 • TypeScript • TailwindCSS • ShadCN UI  
**AI/ML**: Sentence Transformers • Gemini • SHAP • Scikit-Learn  
**Infrastructure**: Docker • PostgreSQL • Redis • Qdrant

---

## 📊 Phase Status

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Setup & Infrastructure | 1 day | ✅ COMPLETE |
| 2 | Backend APIs | 3-4 days | 🏗️ READY |
| 3 | AI Agents & Scoring | 5-7 days | 🏗️ READY |
| 4 | Frontend Implementation | 4-5 days | 🏗️ READY |
| 5 | Deployment & Docs | 2-3 days | 🏗️ READY |

**Total**: ~15-20 days to production

---

## 🎓 What's Built (Phase 1) ✅

✅ 30+ directories created
✅ 20+ database tables
✅ FastAPI application with health checks
✅ 8 SQLAlchemy models
✅ 15+ Pydantic schemas
✅ Embedding service (Sentence Transformers)
✅ Qdrant vector DB client
✅ React structure with routing
✅ 7 page components
✅ API client service
✅ State management (Zustand)
✅ Dark mode UI (TailwindCSS)
✅ Docker multi-container setup
✅ Complete documentation

**~5000+ lines of production-ready code**

---

## 🚀 Next Steps

1. **Read [QUICKSTART.md](./QUICKSTART.md)** (5 min)
2. **Start Docker** (5 min)
3. **Explore Interfaces** (5 min)
4. **Read [PHASE2_BACKEND_INFRASTRUCTURE.md](./PHASE2_BACKEND_INFRASTRUCTURE.md)**
5. **Start Building APIs** (Phase 2)

---

## 📞 Support

- **Quick Setup**: [QUICKSTART.md](./QUICKSTART.md)
- **Architecture**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Database**: [DATABASE_SCHEMA.sql](./DATABASE_SCHEMA.sql)
- **All Guides**: [PROJECT_INDEX.md](./PROJECT_INDEX.md)

---

**Ready to build? Start with [QUICKSTART.md](./QUICKSTART.md)! 🚀**
