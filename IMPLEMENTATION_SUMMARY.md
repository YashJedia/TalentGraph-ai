# TalentGraph AI - Implementation Summary

## Overview

This document provides a summary of the implemented components of the TalentGraph AI project. The application is organized into separate frontend, backend, AI processing, and database layers to support candidate analysis, semantic search, ranking, and recruiter assistance.

---

## Project Structure

```text
talentgraph-ai/
│
├── backend/
├── frontend/
├── docker/
├── DATABASE_SCHEMA.sql
├── docker-compose.yml
├── ARCHITECTURE.md
├── README.md
└── .env.example
```

---

## Backend

The backend is developed using **FastAPI** and provides the APIs required by the application.

Implemented components include:

- FastAPI application structure
- SQLAlchemy database models
- Pydantic validation schemas
- Database session management
- Configuration management
- Embedding service
- Qdrant integration

The backend is responsible for candidate processing, ranking, retrieval, and communication with AI modules.

---

## Frontend

The frontend is built using **React**, **TypeScript**, and **TailwindCSS**.

Implemented pages include:

- Dashboard
- Candidate Search
- Candidate Ranking
- Hidden Gems
- Fraud Alerts
- Recruiter Copilot
- Candidate Comparison

Reusable components include:

- Header
- Sidebar
- Layout
- Shared UI components

---

## Database

The application uses two storage systems.

| Component  | Purpose                                           |
| ---------- | ------------------------------------------------- |
| PostgreSQL | Stores structured application data                |
| Qdrant     | Stores vector embeddings used for semantic search |

Primary data stored includes:

- Jobs
- Candidates
- Rankings
- User activity
- Fraud records

---

## AI Modules

The backend includes dedicated modules for candidate evaluation.

| Module                 | Responsibility                             |
| ---------------------- | ------------------------------------------ |
| Role Understanding     | Extracts information from job descriptions |
| Candidate Intelligence | Processes candidate profiles               |
| Behavioral Analysis    | Evaluates profile quality                  |
| Career Trajectory      | Measures professional growth               |
| Fraud Detection        | Detects anomalous profiles                 |
| Ranking Engine         | Computes final candidate scores            |
| Recruiter Copilot      | Generates contextual responses using RAG   |

---

## Candidate Ranking

Candidate scores are calculated using multiple evaluation factors.

```text
Final Score =
0.35 × Semantic Match +
0.20 × Experience Match +
0.15 × Behavioral Score +
0.10 × Career Growth +
0.10 × Leadership +
0.10 × Culture Fit
```

The weighted score is normalized before ranking candidates.

---

## Retrieval Pipeline

Candidate retrieval combines semantic similarity with keyword matching.

```text
Query
   │
   ▼
Embedding Generation
   │
   ├── Vector Search (Qdrant)
   ├── BM25 Search (PostgreSQL)
   │
   ▼
Combined Candidate Ranking
```

---

## Project Directory

```text
backend/
│
├── app/
│   ├── api/
│   ├── agents/
│   ├── config/
│   ├── db/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── tests/
├── alembic/
└── requirements.txt

frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── context/
│   ├── styles/
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## Docker Services

The project can be started using Docker Compose.

Available services:

- PostgreSQL
- Qdrant
- Redis
- FastAPI
- React

Start all services:

```bash
docker compose up -d
```

Check running services:

```bash
docker compose ps
```

View backend logs:

```bash
docker compose logs -f backend
```

---

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation:

```text
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Application:

```text
http://localhost:5173
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

---

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

---

### Ranking Workflow

```text
Candidate Retrieval
        │
        ▼
Hybrid Search
        │
        ▼
Score Calculation
        │
        ▼
Ranked Candidates
```

---

## Technology Stack

| Layer            | Technology                       |
| ---------------- | -------------------------------- |
| Frontend         | React, TypeScript, TailwindCSS   |
| Backend          | FastAPI, Python                  |
| Database         | PostgreSQL                       |
| Vector Database  | Qdrant                           |
| Embeddings       | Sentence Transformers            |
| Machine Learning | Scikit-learn, SHAP, NetworkX     |
| LLM              | Gemini / OpenAI                  |
| Deployment       | Docker, Vercel, Render, Supabase |

---

## Current Status

| Component            | Status   |
| -------------------- | -------- |
| Backend Structure    | Complete |
| Frontend Structure   | Complete |
| Database Schema      | Complete |
| Embedding Service    | Complete |
| Qdrant Integration   | Complete |
| Docker Configuration | Complete |
| Documentation        | Complete |

---

## Summary

TalentGraph AI is implemented as a modular full-stack application that combines semantic search, candidate evaluation, ranking, and recruiter assistance. The separation of frontend, backend, AI modules, and database layers allows the system to be maintained and extended while keeping responsibilities clearly defined.
