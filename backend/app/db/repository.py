from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import Candidate, CandidateJobRanking, FraudAlert, Job, Skill, CareerHistory, Education


class JobRepository:
    async def list(self, session: AsyncSession, skip: int = 0, limit: int = 20) -> List[Job]:
        query = select(Job).order_by(desc(Job.created_at)).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, job_id: UUID) -> Optional[Job]:
        return await session.get(Job, job_id)

    async def create(self, session: AsyncSession, job_data: Dict[str, Any]) -> Job:
        job = Job(**job_data)
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    async def update(self, session: AsyncSession, job: Job, updates: Dict[str, Any]) -> Job:
        for field, value in updates.items():
            if hasattr(job, field):
                setattr(job, field, value)
        await session.commit()
        await session.refresh(job)
        return job

    async def delete(self, session: AsyncSession, job: Job) -> None:
        await session.delete(job)
        await session.commit()

    async def count(self, session: AsyncSession) -> int:
        result = await session.scalar(select(func.count(Job.id)))
        return int(result or 0)


class CandidateRepository:
    async def list(self, session: AsyncSession, skip: int = 0, limit: int = 20) -> List[Candidate]:
        query = select(Candidate).order_by(desc(Candidate.created_at)).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, candidate_id: UUID) -> Optional[Candidate]:
        return await session.get(Candidate, candidate_id)

    async def create(self, session: AsyncSession, candidate_data: Dict[str, Any]) -> Candidate:
        skills_data = candidate_data.pop("skills", [])
        career_history_data = candidate_data.pop("career_history", [])
        education_data = candidate_data.pop("education", [])

        candidate = Candidate(**candidate_data)
        session.add(candidate)
        await session.flush()

        for item in skills_data:
            session.add(Skill(**item, candidate_id=candidate.id))
        for item in career_history_data:
            session.add(CareerHistory(**item, candidate_id=candidate.id))
        for item in education_data:
            session.add(Education(**item, candidate_id=candidate.id))

        await session.commit()
        await session.refresh(candidate)
        return candidate

    async def bulk_create(self, session: AsyncSession, candidates_data: List[Dict[str, Any]]) -> List[Candidate]:
        created_candidates = []
        for candidate_data in candidates_data:
            candidate_payload = candidate_data.copy()
            skills_data = candidate_payload.pop("skills", [])
            career_history_data = candidate_payload.pop("career_history", [])
            education_data = candidate_payload.pop("education", [])

            candidate = Candidate(**candidate_payload)
            session.add(candidate)
            await session.flush()

            for item in skills_data:
                session.add(Skill(**item, candidate_id=candidate.id))
            for item in career_history_data:
                session.add(CareerHistory(**item, candidate_id=candidate.id))
            for item in education_data:
                session.add(Education(**item, candidate_id=candidate.id))

            created_candidates.append(candidate)

        await session.commit()
        for candidate in created_candidates:
            await session.refresh(candidate)
        return created_candidates

    async def delete(self, session: AsyncSession, candidate: Candidate) -> None:
        await session.delete(candidate)
        await session.commit()


class RankingRepository:
    async def get_by_job(self, session: AsyncSession, job_id: UUID, limit: int = 20) -> List[CandidateJobRanking]:
        query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == job_id).order_by(desc(CandidateJobRanking.final_score)).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_top_for_job(self, session: AsyncSession, job_id: UUID, limit: int = 10) -> List[CandidateJobRanking]:
        query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == job_id).order_by(desc(CandidateJobRanking.final_score)).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_hidden_gems(self, session: AsyncSession, job_id: Optional[UUID] = None) -> List[CandidateJobRanking]:
        query = select(CandidateJobRanking).where(CandidateJobRanking.is_hidden_gem.is_(True))
        if job_id:
            query = query.where(CandidateJobRanking.job_id == job_id)
        query = query.order_by(desc(CandidateJobRanking.final_score))
        result = await session.execute(query)
        return result.scalars().all()

    async def delete_by_job(self, session: AsyncSession, job_id: UUID) -> None:
        await session.execute(delete(CandidateJobRanking).where(CandidateJobRanking.job_id == job_id))
        await session.commit()


class FraudRepository:
    async def list_alerts(self, session: AsyncSession, limit: int = 50) -> List[FraudAlert]:
        query = select(FraudAlert).order_by(desc(FraudAlert.created_at)).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_alert(self, session: AsyncSession, alert_id: UUID) -> Optional[FraudAlert]:
        return await session.get(FraudAlert, alert_id)
