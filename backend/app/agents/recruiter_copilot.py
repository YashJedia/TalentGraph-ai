from typing import Dict, Optional, List
from app.services.embeddings import get_embedding_service
from app.services.llm_service import LLMService
from app.services.qdrant import get_qdrant_service
from app.models.database import CandidateJobRanking, Candidate, Job
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class RecruiterCopilotAgent:
    """Conversational agent for recruiter support."""

    def __init__(self):
        self.llm = LLMService()

    async def ask(self, user_query: str, session: AsyncSession, context: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        query_vector = None
        related_candidates: List[str] = []
        related_summaries = []

        try:
            qdrant = get_qdrant_service()
            query_vector = get_embedding_service().embed(user_query)
        except Exception:
            query_vector = None

        # Use existing job or candidate context to populate response hints
        context_data = context or {}
        if context_data.get('job_id'):
            job = await session.get(Job, context_data['job_id'])
            if job:
                context_data['job_title'] = job.job_title
                context_data['job_description'] = job.job_description

        if context_data.get('candidate_id'):
            candidate = await session.get(Candidate, context_data['candidate_id'])
            if candidate:
                context_data['candidate_name'] = candidate.anonymized_name or ''
                context_data['candidate_title'] = candidate.current_title or ''

        if query_vector and isinstance(query_vector, list):
            try:
                search_results = qdrant.search(settings.QDRANT_COLLECTION_CANDIDATES, query_vector, limit=5)
                for hit in search_results:
                    related_candidates.append(hit.get('id'))
                    related_summaries.append(str(hit.get('payload', {})))
            except Exception:
                pass

        response_text = self.llm.generate_response(user_query, context_data)
        confidence = 0.7
        suggestions = [
            'Compare the top-ranked candidates for this job.',
            'Review any candidates with hidden gem indicators.',
            'Ask for an explanation of the ranking model.',
        ]

        return {
            'message': response_text,
            'suggestions': suggestions,
            'related_candidates': related_candidates,
            'confidence': confidence,
        }
