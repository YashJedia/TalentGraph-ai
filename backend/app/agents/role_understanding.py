from typing import Any, Dict, List
from app.services.embeddings import get_embedding_service
from app.services.qdrant import get_qdrant_service
from app.models.database import Job
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


TECHNICAL_KEYWORDS = [
    'python', 'java', 'react', 'node', 'docker', 'kubernetes', 'sql', 'nosql', 'graphql', 'aws', 'azure',
    'gcp', 'microservices', 'rest', 'api', 'backend', 'frontend', 'devops', 'ci/cd', 'cloud', 'data'
]
SOFT_KEYWORDS = [
    'communication', 'leadership', 'collaboration', 'problem solving', 'adaptability', 'creativity',
    'ownership', 'coaching', 'mentoring', 'stakeholder', 'teamwork', 'influence', 'empathy'
]
CULTURE_PATTERNS = {
    'remote': 'remote_first',
    'flexible': 'flexible_work',
    'startup': 'innovation',
    'fast-paced': 'innovation',
    'diverse': 'inclusive',
    'inclusive': 'inclusive',
    'customer': 'customer_focus',
}


def _extract_keywords(text: str, keywords: List[str]) -> List[str]:
    normalized = text.lower()
    return [keyword for keyword in keywords if keyword in normalized]


def _build_leadership_requirements(required_skills: List[Dict[str, Any]], job: Job) -> Dict[str, Any]:
    critical_skills = [item.get('skill') for item in required_skills if item.get('priority') == 'critical']
    return {
        'team_size': max(1, job.required_experience_years or 1),
        'required_experience': job.required_experience_years or 0,
        'competencies': critical_skills or ['leadership', 'communication', 'execution'],
    }


def _build_culture_signals(job: Job) -> List[str]:
    text = ' '.join(
        filter(None, [
            job.job_title,
            job.job_description,
            job.location,
            job.remote_option,
        ])
    ).lower()
    signals = set()
    for pattern, signal in CULTURE_PATTERNS.items():
        if pattern in text:
            signals.add(signal)
    if 'team' in text and 'collabor' in text:
        signals.add('collaborative')
    if not signals:
        signals.add('execution_focus')
    return list(signals)


class RoleUnderstandingAgent:
    """Agent that extracts job intelligence from job postings."""

    async def analyze(self, job: Job, session: AsyncSession) -> Job:
        required_skills = job.required_skills or []
        skills = [item.get('skill') for item in required_skills if item.get('skill')]

        technical_skills = [
            {
                'skill': item.get('skill'),
                'importance': 0.9 if item.get('priority') == 'critical' else 0.7,
                'category': 'technical',
            }
            for item in required_skills
            if item.get('skill') and item.get('priority') != 'nice_to_have'
        ]

        soft_skills = [
            {
                'skill': skill,
                'importance': 0.8,
            }
            for item in required_skills
            if item.get('skill') and item.get('priority') == 'nice_to_have'
        ]

        if not technical_skills and skills:
            technical_skills = [{'skill': item.get('skill'), 'importance': 0.75, 'category': 'technical'} for item in required_skills if item.get('skill')]

        if not soft_skills:
            soft_skills = [
                {'skill': keyword, 'importance': 0.65}
                for keyword in _extract_keywords(job.job_description or '', SOFT_KEYWORDS)
            ]

        culture_signals = _build_culture_signals(job)
        leadership_requirements = _build_leadership_requirements(required_skills, job)

        job.technical_skills = {'skills': technical_skills}
        job.soft_skills = {'skills': soft_skills}
        job.leadership_requirements = leadership_requirements
        job.culture_signals = culture_signals

        text = f"{job.job_title}. {job.job_description or ''}"
        embedding = get_embedding_service().embed(text)

        job.job_embedding = embedding
        session.add(job)
        await session.commit()
        await session.refresh(job)

        try:
            get_qdrant_service().add_vector(
                settings.QDRANT_COLLECTION_JOBS,
                str(job.id),
                embedding,
                {
                    'job_title': job.job_title,
                    'company_name': job.company_name,
                    'location': job.location,
                },
            )
        except Exception:
            # Qdrant is optional for Phase 3 ranking and search
            pass

        return job
