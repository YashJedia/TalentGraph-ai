from typing import Optional, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.schemas import CopilotMessage, CopilotResponse
from app.agents.orchestrator import TalentGraphOrchestrator

router = APIRouter()
orchestrator = TalentGraphOrchestrator()


@router.post("/ask", response_model=CopilotResponse)
async def ask_copilot(request: CopilotMessage, session: AsyncSession = Depends(get_db_session)) -> CopilotResponse:
    result = await orchestrator.ask_copilot(request.content, session, request.context or {})
    return CopilotResponse(
        message=result.get("message", ""),
        suggestions=result.get("suggestions", []),
        related_candidates=result.get("related_candidates", []),
        confidence=float(result.get("confidence", 0.0)),
    )
