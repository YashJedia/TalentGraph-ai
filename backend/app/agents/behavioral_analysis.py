from datetime import datetime
from app.models.database import Candidate
from sqlalchemy.ext.asyncio import AsyncSession


class BehavioralAnalysisAgent:
    """Agent that calculates behavioral signals from candidate profiles."""

    async def analyze(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        fields = [
            candidate.headline,
            candidate.summary,
            candidate.location,
            candidate.country,
            candidate.current_title,
            candidate.current_company,
            candidate.current_industry,
        ]
        non_empty = [field for field in fields if field]
        completeness = len(non_empty) / len(fields) if fields else 0.0

        candidate.profile_completeness = round(min(1.0, completeness + 0.1), 2)
        last_update = candidate.updated_at or candidate.created_at or datetime.utcnow()
        candidate.activity_recency = last_update
        candidate.recruiter_response_rate = round(min(1.0, 0.5 + completeness * 0.3), 2)

        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)
        return candidate
