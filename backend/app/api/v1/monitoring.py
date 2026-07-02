from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.database import Candidate, CandidateJobRanking, FraudAlert, Job
from app.models.schemas import HealthResponse, SystemStatsResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(session: AsyncSession = Depends(get_db_session)) -> HealthResponse:
    await session.execute(select(1))
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        database="ok",
        vector_db="unverified",
        version="1.0.0",
    )


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(session: AsyncSession = Depends(get_db_session)) -> SystemStatsResponse:
    total_jobs = int((await session.scalar(select(func.count(Job.id)))) or 0)
    total_candidates = int((await session.scalar(select(func.count(Candidate.id)))) or 0)
    total_rankings = int((await session.scalar(select(func.count(CandidateJobRanking.id)))) or 0)
    fraud_alerts_pending = int(
        (await session.scalar(select(func.count(FraudAlert.id)).where(FraudAlert.is_reviewed.is_(False)))) or 0
    )
    average_ranking_score = float((await session.scalar(select(func.avg(CandidateJobRanking.final_score)))) or 0.0)
    return SystemStatsResponse(
        total_jobs=total_jobs,
        total_candidates=total_candidates,
        total_rankings=total_rankings,
        fraud_alerts_pending=fraud_alerts_pending,
        average_ranking_score=average_ranking_score,
        processing_time_ms=0.0,
    )
