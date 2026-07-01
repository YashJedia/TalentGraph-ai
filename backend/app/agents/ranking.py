from typing import List, Dict, Optional
from decimal import Decimal
from app.config.settings import settings
from app.services.embeddings import get_embedding_service
from app.services.qdrant import get_qdrant_service
from app.models.database import Candidate, Job, CandidateJobRanking
from sqlalchemy.ext.asyncio import AsyncSession


def _normalize_score(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    if value is None:
        return 0.0
    return float(max(min(value, max_value), min_value))


def _culture_similarity(job: Job, candidate: Candidate) -> float:
    job_signals = set(job.culture_signals or [])
    candidate_signals = set()
    if candidate.current_industry:
        candidate_signals.add(candidate.current_industry.lower())
    if candidate.location:
        candidate_signals.add(candidate.location.lower())
    if candidate.current_company_size:
        candidate_signals.add(candidate.current_company_size.lower())
    if not job_signals or not candidate_signals:
        return 0.45
    overlap = len(job_signals.intersection(candidate_signals))
    return round(min(1.0, overlap / max(1, len(job_signals))), 2)


def _semantic_similarity(job: Job, candidate: Candidate) -> float:
    if job.job_embedding and candidate.profile_embedding:
        return get_embedding_service().similarity(job.job_embedding, candidate.profile_embedding)

    if job.job_description and candidate.summary:
        return get_embedding_service().similarity(job.job_description, candidate.summary)
    return 0.45


def _experience_match(job: Job, candidate: Candidate) -> float:
    if job.required_experience_years and candidate.years_of_experience is not None:
        return round(min(1.0, float(candidate.years_of_experience) / job.required_experience_years), 2)
    return 0.5


def _behavioral_score(candidate: Candidate) -> float:
    return _normalize_score(float(candidate.behavioral_score or 0.5))


def _career_growth_score(candidate: Candidate) -> float:
    return _normalize_score(float(candidate.growth_score or 0.5))


def _leadership_score(candidate: Candidate) -> float:
    return _normalize_score(float(candidate.leadership_score or 0.5))


class RankingAgent:
    """Agent that scores candidates for a job and stores rank intelligence."""

    async def rank_job(self, job: Job, candidates: List[Candidate], session: AsyncSession, limit: Optional[int] = None) -> List[CandidateJobRanking]:
        rankings: List[CandidateJobRanking] = []

        for candidate in candidates:
            semantic_score = _normalize_score(_semantic_similarity(job, candidate))
            experience_score = _experience_match(job, candidate)
            behavioral_score = _behavioral_score(candidate)
            career_growth_score = _career_growth_score(candidate)
            leadership_score = _leadership_score(candidate)
            culture_fit_score = _normalize_score(_culture_similarity(job, candidate))

            final_score = (
                settings.WEIGHT_SEMANTIC_MATCH * semantic_score
                + settings.WEIGHT_EXPERIENCE_MATCH * experience_score
                + settings.WEIGHT_BEHAVIORAL_SCORE * behavioral_score
                + settings.WEIGHT_CAREER_GROWTH * career_growth_score
                + settings.WEIGHT_LEADERSHIP * leadership_score
                + settings.WEIGHT_CULTURE_FIT * culture_fit_score
            )
            final_score = round(min(max(final_score, 0.0), 1.0), 2)

            hidden_gem_indicators = []
            if final_score >= 0.8 and semantic_score < 0.7:
                hidden_gem_indicators.append('high_growth_low_semantic_match')
            if candidate.growth_score and candidate.growth_score > 0.7:
                hidden_gem_indicators.append('strong_career_trajectory')

            strengths = []
            if semantic_score > 0.75:
                strengths.append('semantic fit')
            if experience_score > 0.8:
                strengths.append('experience alignment')
            if career_growth_score > 0.65:
                strengths.append('career growth')
            if leadership_score > 0.7:
                strengths.append('leadership potential')

            risks = []
            if semantic_score < 0.5:
                risks.append('skill mismatch')
            if experience_score < 0.5:
                risks.append('experience gap')
            if behavioral_score < 0.5:
                risks.append('behavioral risk')

            ranking = CandidateJobRanking(
                job_id=job.id,
                candidate_id=candidate.id,
                semantic_match_score=semantic_score,
                experience_match_score=experience_score,
                behavioral_score=behavioral_score,
                career_growth_score=career_growth_score,
                leadership_score=leadership_score,
                culture_fit_score=culture_fit_score,
                final_score=final_score,
                top_strengths=strengths,
                potential_risks=risks,
                hidden_gem_indicators=hidden_gem_indicators,
                transferable_skills_analysis={
                    'skills': [skill.skill_name for skill in candidate.skills or []][:5]
                },
                career_trajectory_fit={
                    'growth_score': career_growth_score,
                    'promotions': float(candidate.promotion_velocity or 0.0),
                },
                is_hidden_gem=final_score >= 0.85 and float(candidate.fraud_risk_score or 0.0) < settings.FRAUD_RISK_THRESHOLD,
                is_fraud_flagged=float(candidate.fraud_risk_score or 0.0) >= settings.FRAUD_RISK_THRESHOLD,
                bm25_score=0.5,
                embedding_similarity=semantic_score,
                hybrid_retrieval_score=0.5,
            )
            rankings.append(ranking)

        rankings.sort(key=lambda r: float(r.final_score or 0.0), reverse=True)
        total = len(rankings)
        for index, ranking in enumerate(rankings, start=1):
            ranking.rank = index
            ranking.percentile = round(100.0 * (total - index) / total, 2) if total else 0.0
            session.add(ranking)

        if limit:
            rankings = rankings[:limit]

        await session.commit()
        return rankings

    def explain_ranking(self, ranking: CandidateJobRanking) -> Dict[str, object]:
        return {
            'feature_importance': {
                'semantic_match': float(ranking.semantic_match_score or 0.0),
                'experience_match': float(ranking.experience_match_score or 0.0),
                'behavioral_score': float(ranking.behavioral_score or 0.0),
                'career_growth': float(ranking.career_growth_score or 0.0),
                'leadership': float(ranking.leadership_score or 0.0),
                'culture_fit': float(ranking.culture_fit_score or 0.0),
            },
            'top_strengths': ranking.top_strengths or [],
            'potential_risks': ranking.potential_risks or [],
            'hidden_gem_indicators': ranking.hidden_gem_indicators or [],
        }
