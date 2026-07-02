from datetime import datetime
from typing import Dict, List
from app.services.embeddings import get_embedding_service
from app.services.qdrant import get_qdrant_service
from app.models.database import Candidate
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class CandidateIntelligenceAgent:
    """Agent that analyzes candidate profiles and generates intelligence signals."""

    def _make_profile_text(self, candidate: Candidate) -> str:
        lines = [
            candidate.anonymized_name or '',
            candidate.headline or '',
            candidate.summary or '',
            candidate.location or '',
            candidate.country or '',
            candidate.current_title or '',
            candidate.current_company or '',
        ]

        loaded_skills = candidate.__dict__.get('skills') or []
        if loaded_skills:
            lines.extend([skill.skill_name or '' for skill in loaded_skills])
        elif candidate.raw_data:
            lines.extend(
                [skill.get('name') for skill in candidate.raw_data.get('skills', []) if skill.get('name')]
            )

        loaded_career = candidate.__dict__.get('career_history') or []
        if loaded_career:
            lines.extend([career.title or '' for career in loaded_career])
        elif candidate.raw_data:
            lines.extend(
                [entry.get('title') for entry in candidate.raw_data.get('career_history', []) if entry.get('title')]
            )

        return ' | '.join([line for line in lines if line])

    def _calculate_skill_depth(self, candidate: Candidate) -> Dict[str, Dict[str, object]]:
        depth: Dict[str, Dict[str, object]] = {}
        for skill in candidate.skills or []:
            proficiency = skill.proficiency or 'intermediate'
            years = float(skill.years_of_experience or 0.0)
            score = min(1.0, 0.3 + years * 0.1 + (0.2 if proficiency.lower() in ['advanced', 'expert'] else 0.0))
            depth[skill.skill_name] = {
                'proficiency': proficiency,
                'years': years,
                'breadth': min(1.0, 0.5 + years * 0.05),
                'depth_score': round(score, 2),
            }
        return depth

    def _calculate_experience_level(self, candidate: Candidate) -> Dict[str, object]:
        total_years = float(candidate.years_of_experience or 0.0)
        seniority = 'Mid' if total_years >= 3 else 'Junior'
        if total_years >= 8:
            seniority = 'Senior'
        return {
            'total_years': round(total_years, 1),
            'seniority': seniority,
        }

    async def analyze(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        summary_text = self._make_profile_text(candidate)
        embedding = get_embedding_service().embed(summary_text)

        candidate.profile_embedding = embedding
        candidate.skill_depth = self._calculate_skill_depth(candidate)
        candidate.experience_level = self._calculate_experience_level(candidate)

        candidate.leadership_score = round(
            min(1.0, 0.6 + 0.1 * len([skill for skill in candidate.skills or [] if skill.category == 'leadership'])),
            2,
        )
        candidate.growth_score = round(
            min(1.0, 0.5 + 0.05 * len(candidate.career_history or [])),
            2,
        )
        candidate.behavioral_score = round(min(1.0, 0.55 + 0.05 * len(candidate.skills or [])), 2)
        candidate.communication_score = round(
            min(1.0, 0.5 + 0.05 * len([skill for skill in candidate.skills or [] if 'commun' in (skill.skill_name or '').lower()])),
            2,
        )

        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)

        try:
            get_qdrant_service().add_vector(
                settings.QDRANT_COLLECTION_CANDIDATES,
                str(candidate.id),
                embedding,
                {
                    'candidate_id': candidate.candidate_id,
                    'current_title': candidate.current_title,
                    'current_company': candidate.current_company,
                },
            )
        except Exception:
            pass

        return candidate
