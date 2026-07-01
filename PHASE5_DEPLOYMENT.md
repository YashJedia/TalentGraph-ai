# PHASE 5: Deployment & Documentation

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         GitHub/GitLab Repository        │
└──────────────────┬──────────────────────┘
                   │ Push
          ┌────────▼────────┐
          │   CI/CD Pipeline │
          │   (GitHub Actions)
          └────────┬────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    ┌───▼──┐  ┌───▼──┐  ┌───▼──┐
    │Tests │  │Build │  │Lint  │
    └───┬──┘  └───┬──┘  └───┬──┘
        │         │         │
        └─────────┼─────────┘
                  │
        ┌─────────▼─────────┐
        │   Docker Build    │
        │   & Push to GCR   │
        └─────────┬─────────┘
                  │
        ┌─────────┴──────────────────┐
        │                            │
    ┌───▼──────┐            ┌───────▼───┐
    │  Render  │            │  Vercel   │
    │(Backend) │            │(Frontend) │
    └──────────┘            └───────────┘
```

## 5.1 Backend Deployment (Render)

### Docker Setup
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Run migrations
RUN alembic upgrade head

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Render Deployment
1. Connect GitHub repository
2. Create web service:
   - Name: talentgraph-ai-backend
   - Environment: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Environment variables (.env):
   ```
   DATABASE_URL=postgresql://...
   QDRANT_HOST=...
   QDRANT_PORT=6333
   GEMINI_API_KEY=...
   REDIS_URL=...
   ```
4. Auto-deploy on push

### Health Check
```python
@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
```

## 5.2 Frontend Deployment (Vercel)

### Vercel Configuration
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "react",
  "env": {
    "VITE_API_URL": "@db_api_url"
  }
}
```

### Deployment Steps
1. Connect GitHub repo to Vercel
2. Set environment variables
3. Configure build settings
4. Auto-deploy on main branch push

## 5.3 Database Deployment (Supabase)

### PostgreSQL Setup
```sql
-- Run DATABASE_SCHEMA.sql in Supabase console
```

### Connection String
```
postgresql://user:password@host:5432/talentgraph_ai
```

### Backups
- Automated daily backups (Supabase)
- Point-in-time recovery (14 days)
- Custom backup schedule

## 5.4 Vector Database (Qdrant)

### Qdrant Cloud Setup
1. Create account on qdrant.io
2. Create cluster
3. Set API key
4. Configure collections:
   ```
   - jobs_embeddings
   - candidates_embeddings
   ```

### Alternative: Self-hosted
```bash
# Docker
docker run -p 6333:6333 qdrant/qdrant:latest
```

## 5.5 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      # Backend tests
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      
      - name: Run tests
        run: pytest backend/tests -v --cov
      
      # Frontend tests
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install frontend deps
        run: cd frontend && npm install
      
      - name: Build frontend
        run: cd frontend && npm run build
      
      - name: Frontend tests
        run: cd frontend && npm test

  build-backend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: gcr.io/project/talentgraph-backend:latest

  deploy:
    needs: [test, build-backend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/svc/${{ secrets.RENDER_SERVICE_ID }}
          
      - name: Deploy to Vercel
        run: |
          vercel deploy --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## 5.6 Monitoring & Logging

### Application Monitoring
```python
# backend/app/middleware/monitoring.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {duration:.2f}s"
    )
    
    return response
```

### Logging Strategy
```
Level      Use Case
----------+----------------------------------------
DEBUG      Detailed debugging info
INFO       General information (requests, status)
WARNING    Warnings (deprecated, slow queries)
ERROR      Errors (API failures, exceptions)
CRITICAL   Critical failures (service down)
```

### Log Aggregation
- **Local**: File-based (JSON format)
- **Cloud**: Send to LogRocket or Sentry
- **Retention**: 30 days

### Error Tracking
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production"
)
```

## 5.7 Scalability & Performance

### Auto-scaling
```yaml
# Render auto-scaling
Max number of instances: 5
Min number of instances: 1
Scale up at: 80% CPU
Scale down at: 30% CPU
```

### Caching Strategy
```python
# Redis caching
CACHE_KEYS = {
    "rankings:{job_id}": 3600,        # 1 hour
    "candidate:{candidate_id}": 7200,  # 2 hours
    "job:{job_id}": 86400              # 1 day
}

@cache.cached(timeout=3600, key_prefix='rankings')
async def get_rankings(job_id: str):
    pass
```

### Database Optimization
- Connection pooling (20 connections)
- Query optimization (indexes)
- Materialized views for reports
- Partitioning large tables by date

## 5.8 Documentation

### Architecture Documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) ✅
- [DATABASE_SCHEMA.sql](./DATABASE_SCHEMA.sql) ✅

### Setup Guide
```markdown
# TalentGraph AI - Setup Guide

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 16
- Qdrant

## Local Development

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/your-repo/talentgraph-ai.git
cd talentgraph-ai
\`\`\`

### 2. Environment Setup
\`\`\`bash
cp .env.example .env
# Edit .env with your values
\`\`\`

### 3. Start Services
\`\`\`bash
docker-compose up -d
\`\`\`

### 4. Initialize Database
\`\`\`bash
docker-compose exec backend alembic upgrade head
\`\`\`

### 5. Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# API: http://localhost:8000
\`\`\`

### 6. Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
\`\`\`

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing
\`\`\`bash
# Backend
pytest backend/tests -v

# Frontend
npm test
\`\`\`

## Deployment
See [DEPLOYMENT.md](#) for production setup
```

### API Documentation (Auto-generated)
- Swagger UI (FastAPI)
- Request/response examples
- Error codes and explanations
- Authentication requirements

### Developer Guide
```markdown
## Development Guidelines

### Code Style
- Python: PEP 8
- JavaScript: Prettier
- Git commits: Conventional commits

### Branch Strategy
- main: Production
- develop: Development
- feature/: Feature branches
- fix/: Bug fixes

### Pull Request Process
1. Create feature branch
2. Make changes
3. Write tests
4. Submit PR with description
5. Wait for CI/CD to pass
6. Get 2 approvals
7. Merge to develop
```

### User Documentation
- Feature tutorials
- Video walkthroughs
- FAQ section
- Troubleshooting guide

## 5.9 Security Checklist

- ✅ Environment variables in .env (not committed)
- ✅ HTTPS/TLS for all communications
- ✅ Rate limiting on API endpoints
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS properly configured
- ✅ JWT token expiration
- ✅ Password hashing (bcrypt)
- ✅ Audit logging for sensitive actions
- ✅ Data encryption at rest
- ✅ Regular dependency updates
- ✅ Security headers (X-Frame-Options, etc.)

## 5.10 Monitoring Dashboards

### Key Metrics
```
Backend:
- Requests/sec
- Average response time
- Error rate
- API availability
- Database connections
- Redis cache hit rate

Frontend:
- Page load time
- Time to interactive
- JavaScript errors
- API error rate
- User session duration
```

### Alerts
```
Alert          Threshold       Action
─────────────────────────────────────────
High Error Rate    >5%         Page on-call
High Latency      >2s          Investigate DB
Server Down        Any         Immediate restart
Low Disk Space    >90%         Alert DevOps
```

## Success Criteria

✅ Deployment automated (CI/CD)
✅ Zero-downtime deployments
✅ Automated backups
✅ Comprehensive monitoring
✅ Error tracking operational
✅ 99.95% uptime SLA
✅ Full documentation
✅ Security audit passed
