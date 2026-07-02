from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.db.repository import CandidateRepository
from app.models.schemas import CandidateBulkUpload, CandidateCreate, CandidateResponse, CandidateUpdate
from app.models.database import Candidate, CareerHistory, Education, Skill
from app.agents.orchestrator import TalentGraphOrchestrator

router = APIRouter()
candidate_repo = CandidateRepository()
orchestrator = TalentGraphOrchestrator()


@router.get("", response_model=List[CandidateResponse])
async def list_candidates(limit: int = 20, offset: int = 0, session: AsyncSession = Depends(get_db_session)) -> List[CandidateResponse]:
    candidates = await candidate_repo.list(session, skip=offset, limit=limit)
    return [CandidateResponse.model_validate(candidate) for candidate in candidates]


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await candidate_repo.get_by_id(session, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return CandidateResponse.model_validate(candidate)


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate_create: CandidateCreate, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await candidate_repo.create(session, candidate_create.model_dump(exclude_none=True))
    return CandidateResponse.model_validate(candidate)


@router.post("/bulk", response_model=List[CandidateResponse], status_code=status.HTTP_201_CREATED)
async def bulk_upload_candidates(payload: CandidateBulkUpload, session: AsyncSession = Depends(get_db_session)) -> List[CandidateResponse]:
    candidates = await candidate_repo.bulk_create(session, [candidate.model_dump(exclude_none=True) for candidate in payload.candidates])
    return [CandidateResponse.model_validate(candidate) for candidate in candidates]


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(candidate_id: UUID, candidate_update: CandidateUpdate, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await candidate_repo.get_by_id(session, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")

    update_data = candidate_update.model_dump(exclude_none=True)
    if update_data.get("career_history") is not None:
        await session.execute(delete(CareerHistory).where(CareerHistory.candidate_id == candidate.id))
    if update_data.get("education") is not None:
        await session.execute(delete(Education).where(Education.candidate_id == candidate.id))
    if update_data.get("skills") is not None:
        await session.execute(delete(Skill).where(Skill.candidate_id == candidate.id))

    for field, value in update_data.items():
        if field not in ["career_history", "education", "skills"] and hasattr(candidate, field):
            setattr(candidate, field, value)

    for item in update_data.get("career_history", []):
        session.add(CareerHistory(**item.model_dump(exclude_none=True), candidate_id=candidate.id))
    for item in update_data.get("education", []):
        session.add(Education(**item.model_dump(exclude_none=True), candidate_id=candidate.id))
    for item in update_data.get("skills", []):
        session.add(Skill(**item.model_dump(exclude_none=True), candidate_id=candidate.id))

    await session.commit()
    await session.refresh(candidate)
    return CandidateResponse.model_validate(candidate)


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> None:
    candidate = await candidate_repo.get_by_id(session, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    await candidate_repo.delete(session, candidate)


@router.post("/{candidate_id}/analyze", response_model=CandidateResponse)
async def analyze_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await candidate_repo.get_by_id(session, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    candidate = await orchestrator.analyze_candidate(candidate, session)
    return CandidateResponse.model_validate(candidate)
