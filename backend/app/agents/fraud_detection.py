from typing import Dict, List
from datetime import datetime
from app.models.database import Candidate, FraudAlert
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


class FraudDetectionAgent:
    """Agent that detects suspicious candidate profiles and generates alerts."""

    async def analyze(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        years_of_experience = float(candidate.years_of_experience or 0.0)
        skills_count = len(candidate.skills or [])
        career_history = candidate.career_history or []

        has_senior_title = any(
            entry.title and any(keyword in entry.title.lower() for keyword in ['senior', 'lead', 'manager', 'director', 'principal'])
            for entry in career_history
        )

        timeline_months = sum((entry.duration_months or 0) for entry in career_history)
        timeline_years = timeline_months / 12.0 if timeline_months else 0.0
        timeline_gap = max(0.0, timeline_years - years_of_experience)

        skill_density = min(1.0, skills_count / max(1.0, years_of_experience or 1.0))
        seniority_inflation = 1.0 if has_senior_title and years_of_experience < 4 else 0.0
        timeline_inconsistency = min(1.0, timeline_gap / max(1.0, years_of_experience or 1.0))
        suspicious_pattern = 1.0 if skills_count > 50 and years_of_experience < 3 else 0.0

        fraud_score = round(
            min(
                1.0,
                0.4 * skill_density + 0.3 * timeline_inconsistency + 0.2 * seniority_inflation + 0.1 * suspicious_pattern,
            ),
            2,
        )

        signals: List[Dict[str, object]] = []
        if skill_density > 4.0:
            signals.append({'type': 'skill_density', 'detail': 'Many skills for reported years of experience'})
        if timeline_inconsistency > 0.25:
            signals.append({'type': 'timeline_inconsistency', 'detail': 'Career timeline exceeds reported experience by more than 3 months per year'})
        if seniority_inflation > 0.0:
            signals.append({'type': 'seniority_inflation', 'detail': 'Senior-level role with low experience'})
        if suspicious_pattern > 0.0:
            signals.append({'type': 'suspicious_skill_pattern', 'detail': 'Unusually high number of skills for early-career candidate'})

        candidate.fraud_risk_score = fraud_score
        candidate.fraud_signals = signals
        candidate.anomaly_flags = {
            'timeline_years': round(timeline_years, 2),
            'skill_density': round(skill_density, 2),
            'seniority_inflation': seniority_inflation,
        }

        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)

        if fraud_score >= settings.FRAUD_RISK_THRESHOLD and signals:
            alert = FraudAlert(
                candidate_id=candidate.id,
                alert_type='fraud_risk_detected',
                severity='high' if fraud_score >= 0.8 else 'medium',
                description='Candidate profile shows potential anomalies in experience or skills data.',
                evidence={
                    'fraud_score': fraud_score,
                    'signals': signals,
                },
                confidence_score=fraud_score,
                created_at=datetime.utcnow(),
            )
            session.add(alert)
            await session.commit()

        return candidate
