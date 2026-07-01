# TalentGraph AI - Quick Start

## Overview

This guide provides the minimum steps required to set up and run the TalentGraph AI project in a local development environment.

---

## Prerequisites

Ensure the following software is installed before starting:

- Git
- Docker and Docker Compose
- Python 3.11 or later
- Node.js 18 or later

---

## Clone the Repository

```bash
git clone <repository-url>
cd talentgraph-ai
```

---

## Configure Environment

Create a local environment file from the template.

```bash
cp .env.example .env
```

Update any required environment variables before running the application.

---

# Running with Docker

Docker is the recommended way to start all project services.

Start the application:

```bash
docker compose up -d
```

Verify that all containers are running:

```bash
docker compose ps
```

Stop all services:

```bash
docker compose down
```

---

# Manual Setup

## Backend

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the development server.

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

## Frontend

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

```
http://localhost:5173
```

---

# Project Structure

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
├── README.md
└── .env.example
```

---

# Common Commands

Start all services.

```bash
docker compose up -d
```

Stop all services.

```bash
docker compose down
```

Check running containers.

```bash
docker compose ps
```

View backend logs.

```bash
docker compose logs -f backend
```

Restart the backend service.

```bash
docker compose restart backend
```

---

# Verify the Installation

After startup, the following services should be accessible.

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

# Project Documentation

| File | Description |
|------|-------------|
| README.md | Project overview |
| ARCHITECTURE.md | System architecture |
| IMPLEMENTATION_SUMMARY.md | Implementation summary |
| DATABASE_SCHEMA.sql | Database schema |

---

# Troubleshooting

## Docker services are not running

Check the container status.

```bash
docker compose ps
```

View service logs.

```bash
docker compose logs
```

---

## Backend is unavailable

Verify that:

- Docker containers are running.
- Environment variables are configured.
- Python dependencies have been installed.

---

## Frontend is unavailable

Verify that:

- Node.js dependencies are installed.
- The backend server is running.
- API configuration is correct.

---

# Next Steps

Once the application is running successfully:

1. Review the project overview in `README.md`.
2. Read `ARCHITECTURE.md` to understand the system design.
3. Refer to `IMPLEMENTATION_SUMMARY.md` for implementation details.
4. Explore the API using the Swagger documentation.