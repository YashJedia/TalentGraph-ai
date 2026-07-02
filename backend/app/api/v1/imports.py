from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.db.repository import JobRepository, CandidateRepository
from app.models.schemas import JobResponse, CandidateResponse
from app.models.database import Job
from app.api.v1.utils import _get_default_dataset_path, _load_jsonl_file, _map_dataset_candidate, _normalize_skill, _normalize_career_entry, _normalize_education_entry

router = APIRouter()
job_repo = JobRepository()
candidate_repo = CandidateRepository()


@router.post("/jobs/import-sample", response_model=List[JobResponse])
async def import_sample_jobs(session: AsyncSession = Depends(get_db_session)) -> List[JobResponse]:
    existing_jobs = await job_repo.list(session, skip=0, limit=1)
    if existing_jobs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Jobs already exist in the database")

    sample_jobs = [
        {
            "job_title": "Senior Data Engineer",
            "company_name": "Redrob Analytics",
            "job_description": "Build and optimize data pipelines for analytics and machine learning workloads. Strong Python, SQL, Spark, and cloud experience required.",
            "required_skills": [
                {"skill": "Python", "proficiency": "expert", "priority": "critical", "years_required": 4},
                {"skill": "SQL", "proficiency": "advanced", "priority": "critical", "years_required": 4},
                {"skill": "Apache Spark", "proficiency": "advanced", "priority": "important", "years_required": 2},
            ],
            "nice_to_have_skills": [
                {"skill": "Airflow", "proficiency": "intermediate", "priority": "nice_to_have", "years_required": 1},
            ],
            "required_experience_years": 5,
            "seniority_level": "Senior",
            "location": "Bengaluru",
            "remote_option": "hybrid",
            "salary_range": {"min": 20, "max": 35, "currency": "INR"},
        },
        {
            "job_title": "AI/ML Engineer",
            "company_name": "Redrob Labs",
            "job_description": "Develop machine learning models and productionize AI solutions using modern model tooling, NLP, and cloud infrastructure.",
            "required_skills": [
                {"skill": "Machine Learning", "proficiency": "advanced", "priority": "critical", "years_required": 3},
                {"skill": "NLP", "proficiency": "advanced", "priority": "important", "years_required": 2},
                {"skill": "PyTorch", "proficiency": "intermediate", "priority": "important", "years_required": 2},
            ],
            "nice_to_have_skills": [
                {"skill": "Cloud", "proficiency": "intermediate", "priority": "nice_to_have", "years_required": 1},
            ],
            "required_experience_years": 4,
            "seniority_level": "Mid-Senior",
            "location": "Remote",
            "remote_option": "remote",
            "salary_range": {"min": 25, "max": 45, "currency": "INR"},
        },
    ]

    created_jobs: List[Job] = []
    for payload in sample_jobs:
        created_jobs.append(await job_repo.create(session, payload))

    return [JobResponse.model_validate(job) for job in created_jobs]


@router.post("/candidates/import-dataset", response_model=List[CandidateResponse])
async def import_candidate_dataset(
    limit: Optional[int] = None,
    file_path: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session),
) -> List[CandidateResponse]:
    dataset_path = Path(file_path) if file_path else _get_default_dataset_path()
    if not dataset_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset file not found: {dataset_path}")

    raw_candidates = _load_jsonl_file(dataset_path)
    if limit is not None and limit > 0:
        raw_candidates = raw_candidates[:limit]

    candidates_payloads = []
    for raw in raw_candidates:
        if not isinstance(raw, dict):
            continue
        candidate_payload = _map_dataset_candidate(raw)
        if not candidate_payload.get("candidate_id"):
            continue

        normalized_skills = [_normalize_skill(skill) for skill in raw.get("skills", [])]
        normalized_career = [_normalize_career_entry(entry) for entry in raw.get("career_history", [])]
        normalized_education = [_normalize_education_entry(entry) for entry in raw.get("education", [])]

        candidate_payload["skills"] = normalized_skills
        candidate_payload["career_history"] = normalized_career
        candidate_payload["education"] = normalized_education
        candidates_payloads.append(candidate_payload)

    created_candidates = await candidate_repo.bulk_create(session, candidates_payloads)
    return [CandidateResponse.model_validate(candidate) for candidate in created_candidates]
