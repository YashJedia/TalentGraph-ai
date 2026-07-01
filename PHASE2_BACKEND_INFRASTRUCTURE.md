# PHASE 2: Backend Infrastructure Implementation

## Overview
Build the core API endpoints, database layer, and service integrations for TalentGraph AI.

## Deliverables

### 2.1 API Routes Structure

```
backend/app/api/
├── routes.py                    # Main router setup
├── v1/
│   ├── jobs.py                 # Job endpoints
│   ├── candidates.py           # Candidate endpoints
│   ├── rankings.py             # Ranking endpoints
│   ├── search.py               # Hybrid search
│   ├── fraud.py                # Fraud detection
│   ├── comparison.py           # Candidate comparison
│   ├── copilot.py              # LLM copilot
│   └── health.py               # Health checks
```

### 2.2 Job Endpoints

```python
POST   /api/v1/jobs              # Create job
GET    /api/v1/jobs              # List jobs
GET    /api/v1/jobs/{job_id}     # Get job details
PUT    /api/v1/jobs/{job_id}     # Update job
DELETE /api/v1/jobs/{job_id}     # Delete job
POST   /api/v1/jobs/{job_id}/analyze  # Trigger Role Understanding Agent
```

### 2.3 Candidate Endpoints

```python
POST   /api/v1/candidates                # Create candidate
GET    /api/v1/candidates                # List candidates
GET    /api/v1/candidates/{candidate_id} # Get candidate details
POST   /api/v1/candidates/bulk           # Bulk upload from JSONL
PUT    /api/v1/candidates/{candidate_id} # Update candidate
DELETE /api/v1/candidates/{candidate_id} # Delete candidate
POST   /api/v1/candidates/{candidate_id}/analyze # Trigger analysis
```

### 2.4 Ranking Endpoints

```python
POST   /api/v1/rankings/job/{job_id}      # Rank candidates for job
GET    /api/v1/rankings/job/{job_id}      # Get all rankings
GET    /api/v1/rankings/job/{job_id}/top10    # Top 10 candidates
GET    /api/v1/rankings/job/{job_id}/hidden-gems # Hidden gems
GET    /api/v1/rankings/{ranking_id}      # Get ranking details
POST   /api/v1/rankings/{ranking_id}/explain  # Get explanations
```

### 2.5 Key Implementation Files

#### Database Operations (`app/db/repository.py`)
```python
class JobRepository:
    async def create(self, job_data: JobCreate) -> Job
    async def get_by_id(self, job_id: UUID) -> Job
    async def list(self, skip: int = 0, limit: int = 20) -> List[Job]
    async def update(self, job_id: UUID, job_data: JobUpdate) -> Job
    async def delete(self, job_id: UUID) -> bool

class CandidateRepository:
    async def create(self, candidate_data: CandidateCreate) -> Candidate
    async def bulk_create(self, candidates: List[CandidateCreate]) -> List[Candidate]
    async def get_by_id(self, candidate_id: UUID) -> Candidate
    async def list(self, skip: int = 0, limit: int = 20) -> List[Candidate]

class RankingRepository:
    async def create(self, ranking_data: RankingCreate) -> CandidateJobRanking
    async def get_by_job(self, job_id: UUID) -> List[CandidateJobRanking]
    async def get_by_job_sorted(self, job_id: UUID, limit: int = 10)
    async def get_hidden_gems(self, job_id: UUID) -> List[CandidateJobRanking]
```

#### Services (`app/services/`)
- `embeddings.py` - Sentence Transformers integration ✅
- `qdrant.py` - Vector DB operations ✅
- `bm25_search.py` - BM25 ranking algorithm
- `hybrid_search.py` - Hybrid retrieval (BM25 + embedding)
- `llm.py` - Gemini/OpenAI integration

### 2.6 JSONL Data Import

Create endpoint to import from dataset:
```python
@router.post("/candidates/import-dataset")
async def import_from_dataset(
    file_path: str = "[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/candidates.jsonl"
):
    """Import candidates from dataset"""
    # Parse JSONL
    # Validate schema
    # Create candidate records
    # Generate embeddings
    # Store in Qdrant
    # Return statistics
```

### 2.7 Error Handling & Validation

```python
# Create custom exceptions
class TalentGraphException(Exception): pass
class CandidateNotFound(TalentGraphException): pass
class JobNotFound(TalentGraphException): pass
class RankingException(TalentGraphException): pass
class EmbeddingException(TalentGraphException): pass

# Global exception handler in main.py
@app.exception_handler(TalentGraphException)
async def talent_graph_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

### 2.8 Testing Setup (`backend/tests/`)

```python
# test_jobs_api.py
def test_create_job(): pass
def test_get_job(): pass
def test_list_jobs(): pass
def test_update_job(): pass

# test_candidates_api.py
def test_create_candidate(): pass
def test_bulk_import_candidates(): pass

# test_rankings_api.py
def test_rank_candidates(): pass
```

## Implementation Steps

1. ✅ Create database models
2. Create repository pattern layer
3. Create service layer (BM25, hybrid search, LLM)
4. Create API endpoints
5. Create error handling middleware
6. Create request/response validation
7. Add logging throughout
8. Create unit tests
9. Create integration tests
10. Add API documentation (Swagger)

## Tech Stack
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Pydantic 2.5+
- Qdrant Python client
- rank-bm25
- Sentence Transformers
- Gemini/OpenAI APIs

## Success Criteria
✅ All endpoints functional
✅ Data validated against schema
✅ Embeddings generated and stored
✅ Tests passing (>90% coverage)
✅ API documentation complete
✅ 99.9% uptime SLA on health checks
