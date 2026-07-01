# TalentGraph AI Backend - README

## Phase 1: Project Setup Complete ✅

### Structure
```
backend/
├── app/
│   ├── api/           # API routes
│   ├── agents/        # AI agents
│   ├── db/            # Database models & sessions
│   ├── models/        # Pydantic models
│   ├── utils/         # Utility functions
│   └── config/        # Configuration
├── alembic/           # Database migrations
├── tests/             # Unit tests
├── main.py            # Application entry
└── requirements.txt   # Dependencies
```

### Database
- **SQL Schema**: See `DATABASE_SCHEMA.sql`
- **Tables**: 20+ tables for jobs, candidates, rankings, fraud, interactions
- **Vector DB**: Qdrant for embeddings (1024 dimensions)
- **Indexes**: Optimized for fast retrieval

### AI Agents (To be implemented in Phase 3)
1. Role Understanding Agent - Parse job descriptions
2. Candidate Intelligence Agent - Profile analysis
3. Behavioral Analysis Agent - Signal extraction
4. Career Trajectory Agent - Growth metrics
5. Fraud Detection Agent - Anomaly detection
6. Ranking Agent - Candidate scoring
7. Recruiter Copilot Agent - LLM-based Q&A

### Scoring Algorithm
```
Final Score = 
  0.35 × Semantic Match +
  0.20 × Experience Match +
  0.15 × Behavioral Score +
  0.10 × Career Growth +
  0.10 × Leadership +
  0.10 × Culture Fit
```

### Tech Stack
- FastAPI - REST framework
- PostgreSQL - Relational database
- Qdrant - Vector database
- Sentence Transformers - Embeddings
- Gemini/OpenAI - LLM APIs
- Scikit-Learn, SHAP - ML tools

## Next Steps
- Phase 2: Backend API Implementation
- Phase 3: AI Agents & Scoring
- Phase 4: React Frontend
- Phase 5: Deployment
