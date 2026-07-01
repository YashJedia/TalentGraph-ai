# TalentGraph AI

An AI-assisted candidate intelligence platform designed to improve the recruitment process through semantic search, profile analysis, candidate ranking, and recruiter assistance.

The project combines traditional information retrieval with vector search and machine learning techniques to evaluate candidate profiles beyond keyword matching.

---

## Features

- Semantic candidate search using vector embeddings
- Hybrid retrieval with keyword and semantic matching
- Multi-factor candidate ranking
- Candidate profile analysis
- Fraud detection for profile inconsistencies
- Recruiter copilot for contextual assistance
- Explainable ranking workflow

---

## System Architecture

```text
Frontend (React)
        │
        ▼
 FastAPI Backend
        │
 ┌──────┴─────────┐
 │                │
 ▼                ▼
PostgreSQL     Qdrant
(Relational)   (Vector DB)
        │
        ▼
 AI Processing Modules
        │
        ▼
 Candidate Ranking
```

---

## Technology Stack

| Layer | Technology |
|------|------------|
| Frontend | React, TypeScript, TailwindCSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| Vector Database | Qdrant |
| Embeddings | Sentence Transformers |
| Machine Learning | Scikit-learn, SHAP, NetworkX |
| LLM | Gemini / OpenAI |
| Deployment | Docker, Vercel, Render |

---

## Project Structure

```text
talentgraph-ai/
│
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

## Core Modules

| Module | Description |
|----------|-------------|
| Role Understanding | Extracts role requirements from job descriptions |
| Candidate Intelligence | Processes candidate profiles |
| Behavioral Analysis | Evaluates profile quality and engagement |
| Career Trajectory | Measures professional growth |
| Fraud Detection | Identifies anomalous profiles |
| Ranking Engine | Computes final candidate rankings |
| Recruiter Copilot | Generates contextual recruiter assistance |

---

## Candidate Ranking

The ranking engine combines several evaluation metrics.

```text
Final Score =
0.35 × Semantic Match +
0.20 × Experience Match +
0.15 × Behavioral Score +
0.10 × Career Growth +
0.10 × Leadership +
0.10 × Culture Fit
```

The weighted score is normalized before generating the final ranking.

---

## Getting Started

Clone the repository.

```bash
git clone <repository-url>
cd talentgraph-ai
```

Create the environment configuration.

```bash
cp .env.example .env
```

Start the application.

```bash
docker compose up -d
```

The application will be available at:

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## Documentation

| File | Purpose |
|------|---------|
| QUICKSTART.md | Local setup instructions |
| ARCHITECTURE.md | System architecture |
| IMPLEMENTATION_SUMMARY.md | Implementation overview |
| DATABASE_SCHEMA.sql | Database schema |

---

## Repository Structure

The project follows a modular architecture where the frontend, backend, AI processing modules, and data storage are organized into separate components. This structure allows each layer to be developed and maintained independently while supporting semantic retrieval, candidate evaluation, and recruiter workflows.

---

## Future Improvements

Possible enhancements include:

- Improved candidate recommendation strategies
- Additional recruiter analytics
- Expanded explainability for ranking decisions
- Support for larger candidate datasets
- Performance optimization for large-scale retrieval

---

## License

This project was developed as part of a hackathon submission.