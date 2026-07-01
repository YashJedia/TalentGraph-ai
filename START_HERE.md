# Getting Started

## Overview

This document explains how to set up and run the TalentGraph AI project locally.

---

## Prerequisites

Make sure the following tools are installed before starting.

- Python 3.11 or later
- Node.js 18 or later
- Docker and Docker Compose
- Git

---

## Clone the Repository

```bash
git clone <repository-url>
cd talentgraph-ai
```

---

## Environment Configuration

Create a `.env` file using the provided template.

```bash
cp .env.example .env
```

Update the required environment variables before starting the application.

---

## Running with Docker

The recommended way to run the project is with Docker Compose.

```bash
docker compose up -d
```

Verify that all containers are running.

```bash
docker compose ps
```

Stop all services.

```bash
docker compose down
```

---

## Running the Backend

Navigate to the backend directory.

```bash
cd backend
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

API documentation is available at:

```text
http://localhost:8000/docs
```

---

## Running the Frontend

Navigate to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

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
├── DATABASE_SCHEMA.sql
├── docker-compose.yml
└── README.md
```

---

## Main Components

| Component | Description |
|-----------|-------------|
| Frontend | User interface built with React |
| Backend | REST API developed using FastAPI |
| PostgreSQL | Stores application data |
| Qdrant | Stores vector embeddings |
| AI Modules | Candidate analysis and ranking |

---

## Useful Commands

Start all services.

```bash
docker compose up -d
```

Stop all services.

```bash
docker compose down
```

View running containers.

```bash
docker compose ps
```

View backend logs.

```bash
docker compose logs -f backend
```

---

## Documentation

| File | Purpose |
|------|---------|
| README.md | Project overview |
| ARCHITECTURE.md | System architecture |
| IMPLEMENTATION_SUMMARY.md | Implementation overview |
| DATABASE_SCHEMA.sql | Database schema |

---

## Troubleshooting

### Docker containers are not starting

Check container status.

```bash
docker compose ps
```

Inspect logs.

```bash
docker compose logs
```

---

### Backend is unavailable

Verify that:

- PostgreSQL is running.
- Environment variables are configured.
- Required Python packages are installed.

---

### Frontend is unavailable

Verify that:

- Node.js dependencies are installed.
- The backend server is running.
- API configuration is correct.

---

## Next Steps

After the project is running successfully:

1. Review the project structure.
2. Explore the API documentation.
3. Read `ARCHITECTURE.md` for the system design.
4. Refer to `IMPLEMENTATION_SUMMARY.md` for implementation details.