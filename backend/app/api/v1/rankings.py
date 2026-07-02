from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.db.repository import RankingRepository
from app.models.schemas import RankingExplanationResponse, RankingListResponse, RankingResponse
from app.models.database import Candidate, CandidateJobRanking, Job, RankingExplanation
from app.agents.orchestrator import TalentGraphOrchestrator
from app.services.shap_explainer import SHAPExplainer

router = APIRouter()
ranking_repo = RankingRepository()
orchestrator = TalentGraphOrchestrator()


@router.get("/job/{job_id}", response_model=RankingListResponse)
async def get_rankings(job_id: UUID, limit: int = 20, session: AsyncSession = Depends(get_db_session)) -> RankingListResponse:
    rankings = await ranking_repo.get_by_job(session, job_id, limit=limit)
    ranked_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        ranked_models.append(RankingResponse.model_validate({
            **ranking.__dict__,
            'candidate': candidate,
        }))
    return RankingListResponse(
        total_candidates=len(ranked_models),
        ranked_candidates=ranked_models,
        top_10_percentile=ranked_models[:10],
        hidden_gems=[r for r in ranked_models if r.is_hidden_gem],
    )


@router.get("/{job_id}/top10", response_model=List[RankingResponse])
async def get_top_rankings(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    rankings = await ranking_repo.get_top_for_job(session, job_id, limit=10)
    results = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        results.append(RankingResponse.model_validate({
            **ranking.__dict__,
            'candidate': candidate,
        }))
    return results


@router.get("/hidden-gems", response_model=List[RankingResponse])
async def get_all_hidden_gems(session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    rankings = await ranking_repo.get_hidden_gems(session)
    results = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        results.append(RankingResponse.model_validate({
            **ranking.__dict__,
            'candidate': candidate,
        }))
    return results


@router.get("/{job_id}/hidden-gems", response_model=List[RankingResponse])
async def get_hidden_gems(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    rankings = await ranking_repo.get_hidden_gems(session, job_id=job_id)
    results = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        results.append(RankingResponse.model_validate({
            **ranking.__dict__,
            'candidate': candidate,
        }))
    return results


@router.post("/job/{job_id}", response_model=RankingListResponse)
async def rank_candidates_for_job(job_id: UUID, limit: int = 50, session: AsyncSession = Depends(get_db_session)) -> RankingListResponse:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    await ranking_repo.delete_by_job(session, job_id)
    candidates_query = select(Candidate).options(
        selectinload(Candidate.skills),
        selectinload(Candidate.career_history),
        selectinload(Candidate.education),
    )
    candidates = (await session.execute(candidates_query)).scalars().all()
    if not candidates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No candidates available for ranking")

    rankings = await orchestrator.rank_job(job, candidates, session, limit=limit)
    ranked_models = [RankingResponse.model_validate({**ranking.__dict__, 'candidate': next((c for c in candidates if c.id == ranking.candidate_id), None)}) for ranking in rankings]

    return RankingListResponse(
        total_candidates=len(rankings),
        ranked_candidates=ranked_models,
        top_10_percentile=ranked_models[:10],
        hidden_gems=[r for r in ranked_models if r.is_hidden_gem],
    )


@router.get("/{ranking_id}", response_model=RankingResponse)
async def get_ranking(ranking_id: UUID, session: AsyncSession = Depends(get_db_session)) -> RankingResponse:
    ranking = await session.get(CandidateJobRanking, ranking_id)
    if ranking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ranking not found")
    candidate = await session.get(Candidate, ranking.candidate_id)
    return RankingResponse.model_validate({**ranking.__dict__, 'candidate': candidate})


@router.post("/{ranking_id}/explain", response_model=RankingExplanationResponse)
async def explain_ranking(ranking_id: UUID, session: AsyncSession = Depends(get_db_session)) -> RankingExplanationResponse:
    ranking = await session.get(CandidateJobRanking, ranking_id)
    if ranking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ranking not found")
    
    candidate = await session.get(Candidate, ranking.candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

    explanation_dict = SHAPExplainer.explain_ranking(ranking, candidate)
    
    explanation = RankingExplanation(
        ranking_id=ranking.id,
        feature_importance=explanation_dict["feature_importance"],
        top_contributing_factors=explanation_dict["top_contributing_factors"],
        why_selected_narrative=explanation_dict["why_selected_narrative"],
        risks_narrative=explanation_dict["risks_narrative"],
        opportunities_narrative=explanation_dict["opportunities_narrative"],
    )
    session.add(explanation)
    await session.commit()
    
    return RankingExplanationResponse(
        ranking_id=ranking.id,
        summary=explanation.why_selected_narrative,
        top_strengths=explanation_dict["top_strengths"],
        potential_risks=explanation_dict["potential_risks"],
        narrative=explanation.opportunities_narrative,
    )
