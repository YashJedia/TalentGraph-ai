from typing import List, Dict, Optional
from app.models.database import Job, Candidate, CandidateJobRanking
from app.services.embeddings import get_embedding_service
from app.agents.role_understanding import RoleUnderstandingAgent
from app.agents.candidate_intelligence import CandidateIntelligenceAgent
from app.agents.behavioral_analysis import BehavioralAnalysisAgent
from app.agents.career_trajectory import CareerTrajectoryAgent
from app.agents.fraud_detection import FraudDetectionAgent
from app.agents.ranking import RankingAgent
from app.agents.recruiter_copilot import RecruiterCopilotAgent
from sqlalchemy.ext.asyncio import AsyncSession


class TalentGraphOrchestrator:
    """Coordinator for TalentGraph AI agents."""

    def __init__(self):
        self.role_agent = RoleUnderstandingAgent()
        self.candidate_agent = CandidateIntelligenceAgent()
        self.behavior_agent = BehavioralAnalysisAgent()
        self.career_agent = CareerTrajectoryAgent()
        self.fraud_agent = FraudDetectionAgent()
        self.ranking_agent = RankingAgent()
        self.copilot_agent = RecruiterCopilotAgent()

    async def analyze_job(self, job: Job, session: AsyncSession) -> Job:
        return await self.role_agent.analyze(job, session)

    async def analyze_candidate(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        candidate = await self.candidate_agent.analyze(candidate, session)
        candidate = await self.behavior_agent.analyze(candidate, session)
        candidate = await self.career_agent.analyze(candidate, session)
        candidate = await self.fraud_agent.analyze(candidate, session)
        return candidate

    async def rank_job(self, job: Job, candidates: List[Candidate], session: AsyncSession, limit: Optional[int] = None) -> List[CandidateJobRanking]:
        analyzed_candidates = []
        for candidate in candidates:
            if candidate.profile_embedding is None:
                candidate = await self.candidate_agent.analyze(candidate, session)
            if candidate.behavioral_score is None or candidate.growth_score is None:
                candidate = await self.behavior_agent.analyze(candidate, session)
            if candidate.career_growth_score is None:
                candidate = await self.career_agent.analyze(candidate, session)
            if candidate.fraud_risk_score is None:
                candidate = await self.fraud_agent.analyze(candidate, session)
            analyzed_candidates.append(candidate)

        if job.job_embedding is None:
            job = await self.role_agent.analyze(job, session)

        return await self.ranking_agent.rank_job(job, analyzed_candidates, session, limit=limit)

    async def ask_copilot(self, message: str, session: AsyncSession, context: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        return await self.copilot_agent.ask(message, session, context)
