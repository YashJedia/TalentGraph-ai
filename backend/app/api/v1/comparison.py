from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.database import CandidateJobRanking, Candidate
from app.models.schemas import ComparisonRequest, CandidateComparisonResponse, RankingResponse

router = APIRouter()


@router.post("/comparison", response_model=CandidateComparisonResponse)
async def compare_candidates(request: ComparisonRequest, session: AsyncSession = Depends(get_db_session)) -> CandidateComparisonResponse:
    query = select(CandidateJobRanking).where(
        CandidateJobRanking.job_id == request.job_id,
        CandidateJobRanking.candidate_id.in_(request.candidate_ids),
    ).order_by(desc(CandidateJobRanking.final_score))
    result = await session.execute(query)
    rankings = result.scalars().all()

    comparison_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        comparison_models.append(
            RankingResponse.model_validate(
                {
                    **ranking.__dict__,
                    "candidate": candidate,
                }
            )
        )

    comparison_metrics = {
        "job_id": str(request.job_id),
        "candidate_count": len(request.candidate_ids),
        "ranked_count": len(rankings),
    }

    recommendations = [
        "Review the top-ranked candidates first.",
        "Check candidate fit against required skills and seniority level.",
    ]

    return CandidateComparisonResponse(
        candidates=comparison_models,
        comparison_metrics=comparison_metrics,
        recommendations=recommendations,
    )
