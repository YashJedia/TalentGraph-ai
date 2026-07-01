# TalentGraph AI

Candidate Intelligence Platform for Semantic Search, Profile Analysis and Explainable Ranking.

---

## Overview

TalentGraph AI is designed to improve candidate discovery by combining semantic search, structured profile analysis, and explainable ranking. Instead of relying solely on keyword matching, the platform evaluates multiple aspects of a candidate profile to generate more relevant recommendations.

The project follows a modular architecture with separate frontend, backend, data storage, and AI processing components.

---

## Core Capabilities

- Semantic candidate search using vector embeddings
- Hybrid candidate retrieval
- Multi-factor candidate ranking
- Candidate profile analysis
- Explainable ranking workflow
- Recruiter assistance through LLM integration
- Fraud and anomaly detection support

---

## Architecture Overview

```
                React Frontend
                       │
                       ▼
                FastAPI Backend
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
   PostgreSQL                    Qdrant
(Relational Data)            (Vector Storage)
        │
        ▼
   AI Processing Modules
        │
        ▼
 Candidate Ranking & Insights
```

---

## Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| Vector Database | Qdrant |
| Embeddings | Sentence Transformers |
| Machine Learning | Scikit-learn, SHAP |
| LLM | Gemini / OpenAI |
| Deployment | Docker |

---

## Project Structure

```text
talentgraph-ai/
├── backend/
├── frontend/
├── docker/
├── ARCHITECTURE.md
├── IMPLEMENTATION_SUMMARY.md
├── QUICKSTART.md
├── DATABASE_SCHEMA.sql
├── docker-compose.yml
└── README.md
```

---

## Candidate Evaluation

Candidate ranking is generated using multiple evaluation factors, including semantic similarity, relevant experience, behavioral indicators, career progression, leadership signals, and organizational fit.

```
Final Score =
0.35 × Semantic Match +
0.20 × Experience Match +
0.15 × Behavioral Score +
0.10 × Career Growth +
0.10 × Leadership +
0.10 × Culture Fit
```

The final score is normalized before ranking candidates.

---

## Getting Started

### Using Docker

```bash
docker compose up -d
```

### Manual Setup

Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Services

| Service | Address |
|----------|---------|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## Documentation

| File | Description |
|------|-------------|
| README.md | Project overview |
| QUICKSTART.md | Setup instructions |
| ARCHITECTURE.md | System architecture |
| IMPLEMENTATION_SUMMARY.md | Implementation overview |
| DATABASE_SCHEMA.sql | Database schema |

---

## Design Principles

- Modular architecture
- Explainable candidate ranking
- Separation of frontend and backend
- Scalable data storage
- Containerized development environment
- Extensible AI processing pipeline

---

## Future Enhancements

Potential areas for future improvement include:

- Enhanced ranking strategies
- Additional recruiter analytics
- Improved explainability
- Performance optimization
- Expanded dataset support

---

## License

Developed as part of a hackathon project.