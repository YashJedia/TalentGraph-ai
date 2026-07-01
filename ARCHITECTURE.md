# TalentGraph AI - System Architecture

## 🏗️ Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React + TailwindCSS)              │
│  Dashboard | Search | Ranking | Hidden Gems | Fraud | Copilot  │
└────────────────────┬────────────────────────────────────────────┘
                     │ REST API / WebSocket
┌────────────────────▼────────────────────────────────────────────┐
│                   FastAPI Backend (Python)                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │            API Layer (Routes)                              │ │
│  │  /jobs | /candidates | /rankings | /copilot | /fraud      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │           AI Agents Layer                                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │Role          │  │Candidate     │  │Behavioral        │ │ │
│  │  │Understanding │  │Intelligence  │  │Analysis          │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │Career        │  │Fraud         │  │Ranking           │ │ │
│  │  │Trajectory    │  │Detection     │  │                  │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │      Recruiter Copilot (LLM + RAG)                 │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │         Scoring & Analysis Engine                         │ │
│  │  Hybrid Retrieval | Career Analysis | Fraud Scoring       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │         Embeddings Layer (SentenceTransformer)            │ │
│  │  BAAI/bge-large-en-v1.5 (1024 dimensions)                │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────┬──────────────────────┬──────────────────────────┘
                 │                      │
        ┌────────▼───────────┐   ┌─────▼──────────────┐
        │  PostgreSQL        │   │  Qdrant Vector DB  │
        │  (Relational Data) │   │  (Embeddings)      │
        │                    │   │                    │
        │ • Jobs             │   │ • Job embeddings   │
        │ • Candidates       │   │ • Candidate        │
        │ • Rankings         │   │   embeddings       │
        │ • Interactions     │   │ • Query results    │
        │ • Fraud Alerts     │   │                    │
        └────────────────────┘   └────────────────────┘
```

## 🤖 AI Agents Architecture

### 1. **Role Understanding Agent**
- **Input**: Job Description
- **Process**:
  - Parse JD semantically
  - Extract technical requirements
  - Identify soft skills needed
  - Detect leadership requirements
  - Analyze culture signals
- **Output**:
```python
{
    "technical_skills": [
        {"skill": "Python", "proficiency": "expert", "priority": "critical"},
        ...
    ],
    "soft_skills": [...],
    "leadership_requirements": {...},
    "seniority": "Senior",
    "culture_signals": [...],
    "job_embedding": Vector(1024)
}
```

### 2. **Candidate Intelligence Agent**
- **Input**: Candidate Profile
- **Process**:
  - Analyze profile holistically
  - Extract skills with proficiency
  - Assess experience level
  - Calculate depth in each domain
  - Generate behavioral indicators
- **Output**:
```python
{
    "skill_depth": {...},
    "experience_level": {...},
    "leadership_score": 0.85,
    "growth_score": 0.72,
    "behavioral_score": 0.78,
    "communication_score": 0.81,
    "profile_embedding": Vector(1024)
}
```

### 3. **Behavioral Analysis Agent**
- **Metrics Tracked**:
  - Profile Completeness
  - Activity Recency
  - Recruiter Response Rate
  - Assessment Completion
- **Output**: `behavioral_score` (0-1)

### 4. **Career Trajectory Agent**
- **Metrics Calculated**:
  - Promotion Velocity (promotions per year)
  - Career Growth (salary/responsibility trend)
  - Skill Evolution (skill progression)
  - Responsibility Growth (scope expansion)
- **Output**: `career_growth_score`, trajectory analysis

### 5. **Fraud Detection Agent**
- **Methods**: Isolation Forest Algorithm
- **Detects**:
  - Skill Stuffing (excessive skills listed)
  - Timeline Inconsistencies (gaps/overlaps)
  - Unrealistic Claims
  - Suspicious Patterns
- **Output**: `fraud_risk_score`, `anomaly_flags`

### 6. **Ranking Agent**
- **Input**: Job, Candidates, Scores
- **Scoring Formula**:
```
Final Score = 
  0.35 × Semantic Match +
  0.20 × Experience Match +
  0.15 × Behavioral Score +
  0.10 × Career Growth +
  0.10 × Leadership +
  0.10 × Culture Fit
```
- **Output**: Ranked candidates with explanations

### 7. **Recruiter Copilot Agent**
- **Capabilities**:
  - Answer ranking questions
  - Compare candidates
  - Suggest hidden gems
  - Provide contextual recommendations
- **Tech Stack**: RAG + LLM (Gemini/OpenAI)

## 🔍 Hybrid Retrieval System

```
Query → Embedding Generation → Parallel Search
                               ├→ Vector Search (Qdrant) → Embedding Similarity
                               ├→ BM25 Search (PostgreSQL) → Keyword Match
                               └→ Hybrid Score Combination
                                   Score = 0.5 × Embedding_Sim + 0.5 × BM25
```

## 📊 Scoring System

### Individual Component Scores (0-1 scale):
1. **Semantic Match (0.35 weight)**: How well candidate profile matches job requirements semantically
2. **Experience Match (0.20 weight)**: Years of relevant experience + depth
3. **Behavioral Score (0.15 weight)**: Profile completeness + activity + engagement
4. **Career Growth (0.10 weight)**: Promotion velocity + skill evolution
5. **Leadership (0.10 weight)**: Leadership experience + responsibility growth
6. **Culture Fit (0.10 weight)**: Industry alignment + company size adaptation

### Final Score Normalization:
- All scores normalized to 0-100 scale
- Top candidates highlighted
- Percentile rankings calculated

## 🔐 Security & Privacy

- JWT authentication
- Rate limiting on API endpoints
- Data encryption at rest & in transit
- Audit logging for all actions
- GDPR compliance ready

## 🚀 Deployment Architecture

### Frontend (Vercel)
- Automatic deployments from Git
- CDN edge caching
- Environment-specific configs

### Backend (Render)
- Docker containerization
- Auto-scaling
- Health checks

### Database (Supabase)
- PostgreSQL managed
- Automatic backups
- Connection pooling

### Vector DB (Self-hosted/Qdrant Cloud)
- High-availability setup
- Vector index optimization
- Snapshot backup strategy

## 📈 Performance Metrics

- **Retrieval Speed**: <500ms for top 10 candidates
- **Embedding Generation**: <100ms per profile
- **Ranking Calculation**: <200ms for 100 candidates
- **API Response Time**: <1s for complex queries

## 🗄️ Data Flow

```
1. Job Upload
   ├→ Parse & Normalize
   ├→ Role Understanding Agent
   ├→ Generate Job Embedding
   └→ Store in PostgreSQL + Qdrant

2. Candidate Ingestion
   ├→ Validate Schema
   ├→ Candidate Intelligence Agent
   ├→ Career Trajectory Analysis
   ├→ Fraud Detection
   ├→ Generate Embeddings
   └→ Store in PostgreSQL + Qdrant

3. Ranking Process
   ├→ Hybrid Retrieval (BM25 + Embedding)
   ├→ Score Calculation
   ├→ Hidden Gems Detection
   ├→ Generate Explanations (SHAP)
   └→ Store Rankings

4. Recruiter Interaction
   ├→ User Query
   ├→ Copilot Retrieval (RAG)
   ├→ LLM Generation
   └→ Stream Response
```

## 🔄 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React, TailwindCSS, ShadCN | UI/UX |
| Backend | FastAPI, Python | APIs, Business Logic |
| Database | PostgreSQL | Relational Data |
| Vector DB | Qdrant | Embeddings, Similarity Search |
| Embeddings | Sentence Transformers | Text to Vector |
| LLM | Gemini/OpenAI | Agent Intelligence, Copilot |
| ML | Scikit-Learn, SHAP, NetworkX | Fraud Detection, Explainability |
| Deployment | Vercel, Render, Supabase | Cloud Infrastructure |
