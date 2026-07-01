from typing import Dict
from app.models.database import Candidate
from sqlalchemy.ext.asyncio import AsyncSession


class CareerTrajectoryAgent:
    """Agent that analyzes career trajectory and growth patterns."""

    def _count_promotions(self, candidate: Candidate) -> int:
        return sum(
            1
            for entry in candidate.career_history or []
            if entry.title and any(keyword in entry.title.lower() for keyword in ['senior', 'lead', 'manager', 'director', 'principal'])
        )

    def _quality_score(self, value: float) -> float:
        return round(min(1.0, max(0.0, value)), 2)

    async def analyze(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        total_years = float(candidate.years_of_experience or 0.0)
        promotions = self._count_promotions(candidate)
        experience_factor = max(total_years, 1.0)

        candidate.promotion_velocity = round(promotions / experience_factor, 2)
        candidate.career_growth_trend = {
            'responsibility_progression': self._quality_score(0.6 + len(candidate.career_history or []) * 0.05),
            'salary_growth_rate': self._quality_score(0.08 + 0.01 * promotions),
            'skill_accumulation': self._quality_score(0.5 + len(candidate.skills or []) * 0.03),
            'tenure_progression': self._quality_score(0.5 + 0.05 * min(len(candidate.career_history or []), 10)),
        }
        candidate.skill_evolution = {
            'new_skills_per_year': round(min(2.0, max(0.0, len(candidate.skills or []) / experience_factor)), 2),
            'skill_depth_growth': self._quality_score(0.4 + len(candidate.skills or []) * 0.02),
            'technology_adoption': self._quality_score(0.5 + 0.03 * len(candidate.skills or [])),
            'breadth_expansion': self._quality_score(0.4 + 0.03 * len(candidate.skills or [])),
        }
        candidate.responsibility_growth = {
            'team_lead_experience': round(min(10.0, promotions * 1.0), 1),
            'project_complexity': self._quality_score(0.5 + promotions * 0.05),
            'scope_increase': self._quality_score(0.5 + len(candidate.career_history or []) * 0.03),
            'impact_level': self._quality_score(0.55 + len(candidate.career_history or []) * 0.02),
        }
        candidate.career_growth_score = round(
            min(
                1.0,
                (
                    candidate.promotion_velocity * 0.15
                    + candidate.career_growth_trend['responsibility_progression'] * 0.25
                    + candidate.skill_evolution['skill_depth_growth'] * 0.25
                    + candidate.responsibility_growth['impact_level'] * 0.35
                )
            ),
            2,
        )

        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)
        return candidate
