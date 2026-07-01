# TalentGraph AI - System Architecture

## Overview

TalentGraph AI is a modular candidate intelligence platform that combines semantic search, candidate analysis, and machine learning to assist recruiters in evaluating and ranking candidates. The application follows a layered architecture with separate frontend, backend, database, and AI processing components.

---

## System Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                 Frontend (React + TailwindCSS)                  │
│ Dashboard | Search | Ranking | Hidden Gems | Fraud | Copilot   │
└────────────────────┬────────────────────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                    │
│                                                                │
│  API Layer                                                     │
│  /jobs | /candidates | /rankings | /copilot | /fraud           │
│                                                                │
│  Processing Layer                                              │
│  • Role Understanding                                          │
│  • Candidate Intelligence                                      │
│  • Behavioral Analysis                                         │
│  • Career Trajectory                                           │
│  • Fraud Detection                                             │
│  • Ranking Engine                                              │
│  • Recruiter Copilot                                           │
│                                                                │
│  Embedding & Retrieval                                         │
│  Sentence Transformers | Hybrid Search                         │
└────────────────┬──────────────────────┬─────────────────────────┘
                 │                      │
        ┌────────▼───────────┐   ┌──────▼─────────────┐
        │ PostgreSQL         │   │ Qdrant            │
        │ Relational Data    │   │ Vector Database   │
        └────────────────────┘   └───────────────────┘
```

---

## Architecture Components

### Frontend

The frontend provides the user interface for recruiters and administrators. It is responsible for candidate search, ranking visualization, fraud alerts, and interaction with the recruiter assistant.

**Technology**

- React
- TypeScript
- TailwindCSS
- ShadCN UI

---

### Backend

The backend exposes REST APIs and coordinates communication between the database, AI modules, and frontend.

Primary responsibilities include:

- API request handling
- Candidate processing
- Ranking generation
- Fraud analysis
- Embedding generation
- Recruiter assistant integration

---

### Database Layer

Two storage systems are used.

| Component | Purpose |
|----------|---------|
| PostgreSQL | Stores structured application data such as jobs, candidates, rankings, and user records |
| Qdrant | Stores vector embeddings for semantic similarity search |

---

## AI Processing Modules

| Module | Responsibility |
|---------|----------------|
| Role Understanding | Extracts required skills and role information from job descriptions |
| Candidate Intelligence | Processes candidate profiles and generates embeddings |
| Behavioral Analysis | Evaluates profile quality and activity signals |
| Career Trajectory | Analyzes career progression and professional growth |
| Fraud Detection | Detects anomalous or inconsistent candidate profiles |
| Ranking Engine | Combines evaluation metrics into a final ranking |
| Recruiter Copilot | Provides contextual responses using Retrieval-Augmented Generation (RAG) |

---

## Candidate Ranking

Candidate ranking combines semantic similarity with additional evaluation metrics.

### Ranking Formula

```text
Final Score =
0.35 × Semantic Match +
0.20 × Experience Match +
0.15 × Behavioral Score +
0.10 × Career Growth +
0.10 × Leadership +
0.10 × Culture Fit
```

### Score Distribution

| Component | Weight |
|-----------|-------:|
| Semantic Match | 0.35 |
| Experience Match | 0.20 |
| Behavioral Score | 0.15 |
| Career Growth | 0.10 |
| Leadership | 0.10 |
| Culture Fit | 0.10 |

The weighted score is normalized before generating the final ranking.

---

## Candidate Retrieval

The retrieval pipeline combines semantic similarity with keyword-based search.

```text
                Query
                  │
                  ▼
        Embedding Generation
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
Vector Search          Keyword Search
(Qdrant)              (PostgreSQL BM25)
      │                       │
      └───────────┬───────────┘
                  ▼
           Combined Ranking
```

---

## Data Flow

### Job Processing

```text
Job Description
        │
        ▼
Role Understanding
        │
        ▼
Embedding Generation
        │
        ▼
PostgreSQL + Qdrant
```

### Candidate Processing

```text
Candidate Profile
        │
        ▼
Candidate Analysis
        │
        ├── Behavioral Analysis
        ├── Career Evaluation
        ├── Fraud Detection
        └── Embedding Generation
                │
                ▼
        PostgreSQL + Qdrant
```

### Ranking Process

```text
Job Request
      │
      ▼
Hybrid Retrieval
      │
      ▼
Score Calculation
      │
      ▼
Ranked Candidates
```

### Recruiter Interaction

```text
Recruiter Query
        │
        ▼
Retrieve Context
        │
        ▼
LLM Response
```

---

## Deployment

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | PostgreSQL (Supabase) |
| Vector Database | Qdrant |

---

## Technology Stack

| Layer | Technology |
|------|------------|
| Frontend | React, TypeScript, TailwindCSS, ShadCN UI |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| Vector Database | Qdrant |
| Embeddings | Sentence Transformers |
| Machine Learning | Scikit-learn, SHAP, NetworkX |
| LLM | Gemini / OpenAI |
| Deployment | Docker, Vercel, Render, Supabase |

---

## Project Structure

```text
talentgraph-ai/
│
├── backend/
│   ├── api/
│   ├── agents/
│   ├── config/
│   ├── db/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── styles/
│   └── App.tsx
│
├── docker/
├── DATABASE_SCHEMA.sql
├── docker-compose.yml
├── README.md
└── ARCHITECTURE.md
```

---

## Summary

TalentGraph AI follows a modular architecture that separates presentation, business logic, AI processing, and data storage into independent layers. This design simplifies maintenance, enables future feature additions, and supports semantic candidate search, intelligent ranking, and recruiter assistance through a scalable backend architecture.