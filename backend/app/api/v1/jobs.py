from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.db.session import get_db_session
from app.db.repository import JobRepository
from app.models.schemas import JobCreate, JobResponse, JobUpdate
from app.models.database import Job
from app.agents.orchestrator import TalentGraphOrchestrator

router = APIRouter()
job_repo = JobRepository()
orchestrator = TalentGraphOrchestrator()


@router.get("", response_model=List[JobResponse])
async def list_jobs(limit: int = 20, offset: int = 0, session: AsyncSession = Depends(get_db_session)) -> List[JobResponse]:
    jobs = await job_repo.list(session, skip=offset, limit=limit)
    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await job_repo.get_by_id(session, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobResponse.model_validate(job)


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job_create: JobCreate, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await job_repo.create(session, job_create.model_dump(exclude_none=True))
    return JobResponse.model_validate(job)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(job_id: UUID, job_update: JobUpdate, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await job_repo.get_by_id(session, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    job = await job_repo.update(session, job, job_update.model_dump(exclude_none=True))
    return JobResponse.model_validate(job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> None:
    job = await job_repo.get_by_id(session, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    await job_repo.delete(session, job)


@router.post("/{job_id}/analyze", response_model=JobResponse)
async def analyze_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await job_repo.get_by_id(session, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    job = await orchestrator.analyze_job(job, session)
    return JobResponse.model_validate(job)
