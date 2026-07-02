from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.schemas import CandidateSearchQuery, SearchResponse
from app.models.database import Candidate, CandidateJobRanking
from app.models.schemas import CandidateResponse

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_candidates(query: CandidateSearchQuery, session: AsyncSession = Depends(get_db_session)) -> SearchResponse:
    ranking_query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == query.job_id)
    if query.exclude_fraud_flagged:
        ranking_query = ranking_query.where(CandidateJobRanking.is_fraud_flagged.is_(False))
    if query.min_score is not None:
        ranking_query = ranking_query.where(CandidateJobRanking.final_score >= query.min_score)
    if not query.include_hidden_gems:
        ranking_query = ranking_query.where(CandidateJobRanking.is_hidden_gem.is_(False))

    ranking_query = ranking_query.order_by(desc(CandidateJobRanking.final_score)).limit(query.limit).offset(query.offset)
    result = await session.execute(ranking_query)
    rankings = result.scalars().all()

    results = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        if not candidate:
            continue
        results.append(
            {
                "candidate": CandidateResponse.model_validate(candidate),
                "score": float(ranking.final_score or 0.0),
            }
        )

    return SearchResponse(total_results=len(results), results=results)
