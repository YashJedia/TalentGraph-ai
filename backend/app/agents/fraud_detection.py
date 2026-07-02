from typing import Dict, List
from datetime import datetime
from app.models.database import Candidate, FraudAlert
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class FraudDetectionAgent:
    """Agent that detects suspicious candidate profiles and generates alerts."""

    def _detect_skill_stuffing(self, candidate: Candidate) -> tuple[bool, float, str]:
        """Detect unrealistic skill counts or proficiency claims."""
        skills_count = len(candidate.skills or [])
        years_of_experience = float(candidate.years_of_experience or 0.0)
        
        # Too many skills for experience level
        if skills_count > 50:
            return True, 0.85, "Too many skills for reported experience"
        
        if years_of_experience > 0 and skills_count > 0:
            skills_per_year = skills_count / years_of_experience
            if skills_per_year > 10:  # More than 10 skills per year is suspicious
                return True, 0.72, "Unusually high skill acquisition rate"
        
        return False, 0.0, ""

    def _detect_timeline_inconsistencies(self, candidate: Candidate) -> tuple[bool, float, str]:
        """Detect overlapping roles, missing gaps, or suspicious dates."""
        career_history = candidate.career_history or []
        
        if len(career_history) < 2:
            return False, 0.0, ""
        
        # Sort by start date
        sorted_history = sorted(career_history, key=lambda x: x.start_date or datetime.min)
        
        for i in range(len(sorted_history) - 1):
            current_role = sorted_history[i]
            next_role = sorted_history[i + 1]
            
            # Check for overlapping dates
            if current_role.end_date and next_role.start_date:
                if current_role.end_date > next_role.start_date:
                    return True, 0.88, "Overlapping employment periods detected"
        
        # Check timeline vs reported experience
        timeline_months = sum((entry.duration_months or 0) for entry in career_history)
        timeline_years = timeline_months / 12.0 if timeline_months else 0.0
        reported_years = float(candidate.years_of_experience or 0.0)
        timeline_gap = max(0.0, timeline_years - reported_years)
        
        if timeline_gap > 2.0:  # More than 2 years discrepancy
            return True, 0.78, "Career timeline exceeds reported experience"
        
        return False, 0.0, ""

    def _detect_unrealistic_claims(self, candidate: Candidate) -> tuple[bool, float, str]:
        """Detect claims inconsistent with role, experience, or timeline."""
        years_of_experience = float(candidate.years_of_experience or 0.0)
        
        # Check for seniority inflation
        has_senior_title = any(
            entry.title and any(
                keyword in entry.title.lower() 
                for keyword in ['senior', 'lead', 'manager', 'director', 'principal', 'architect']
            )
            for entry in candidate.career_history or []
        )
        
        if has_senior_title and years_of_experience < 4:
            return True, 0.82, "Senior-level title with insufficient experience"
        
        return False, 0.0, ""

    async def _detect_isolation_forest_anomalies(self, candidate: Candidate) -> tuple[bool, float, str]:
        """Use IsolationForest for statistical anomaly detection."""
        if not HAS_SKLEARN:
            return False, 0.0, ""
        
        try:
            years_of_experience = float(candidate.years_of_experience or 0.0)
            num_skills = float(len(candidate.skills or []))
            
            career_history = candidate.career_history or []
            avg_tenure_months = (
                sum(entry.duration_months or 0 for entry in career_history) / len(career_history)
                if career_history else 0.0
            )
            
            promotion_count = sum(
                1 for entry in career_history
                if entry.title and any(
                    keyword in entry.title.lower() 
                    for keyword in ['senior', 'lead', 'manager', 'director', 'principal']
                )
            )
            promotion_velocity = promotion_count / max(years_of_experience, 1.0)
            
            profile_completeness = 0.0
            fields_present = 0
            total_fields = 10
            if candidate.summary: fields_present += 1
            if candidate.skills: fields_present += 1
            if candidate.career_history: fields_present += 1
            if candidate.education: fields_present += 1
            if candidate.current_title: fields_present += 1
            if candidate.current_company: fields_present += 1
            if candidate.location: fields_present += 1
            if candidate.country: fields_present += 1
            if candidate.current_industry: fields_present += 1
            if candidate.headline: fields_present += 1
            profile_completeness = fields_present / total_fields
            
            # Simplified activity recency (0.0-1.0)
            activity_recency = 0.5
            
            # Build feature vector
            features = [[
                years_of_experience,
                num_skills,
                avg_tenure_months,
                promotion_velocity,
                profile_completeness,
                activity_recency,
            ]]
            
            # Fit and predict
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            prediction = iso_forest.fit_predict(features)[0]
            
            # -1 indicates anomaly, 1 indicates normal
            if prediction == -1:
                anomaly_score = iso_forest.score_samples(features)[0]
                # Convert score to 0-1 range (more negative = more anomalous)
                confidence = min(1.0, abs(anomaly_score) / 2.0)
                return True, confidence, "Statistical anomaly detected in profile features"
        except Exception:
            # Fallback if sklearn fails
            pass
        
        return False, 0.0, ""

    async def analyze(self, candidate: Candidate, session: AsyncSession) -> Candidate:
        alerts: List[Dict[str, object]] = []
        max_confidence = 0.0
        
        # Run all detection methods
        skill_stuff_detected, skill_score, skill_msg = self._detect_skill_stuffing(candidate)
        if skill_stuff_detected:
            alerts.append({
                'type': 'skill_stuffing',
                'severity': 'high',
                'confidence': skill_score,
                'detail': skill_msg
            })
            max_confidence = max(max_confidence, skill_score)
        
        timeline_detected, timeline_score, timeline_msg = self._detect_timeline_inconsistencies(candidate)
        if timeline_detected:
            alerts.append({
                'type': 'timeline_inconsistency',
                'severity': 'medium',
                'confidence': timeline_score,
                'detail': timeline_msg
            })
            max_confidence = max(max_confidence, timeline_score)
        
        unrealistic_detected, unrealistic_score, unrealistic_msg = self._detect_unrealistic_claims(candidate)
        if unrealistic_detected:
            alerts.append({
                'type': 'unrealistic_claims',
                'severity': 'high',
                'confidence': unrealistic_score,
                'detail': unrealistic_msg
            })
            max_confidence = max(max_confidence, unrealistic_score)
        
        # IsolationForest anomaly detection
        iso_detected, iso_score, iso_msg = await self._detect_isolation_forest_anomalies(candidate)
        if iso_detected:
            alerts.append({
                'type': 'profile_anomaly',
                'severity': 'low',
                'confidence': iso_score,
                'detail': iso_msg
            })
            max_confidence = max(max_confidence, iso_score)
        
        # Calculate composite fraud score
        fraud_score = min(1.0, max_confidence)
        
        # Build fraud signals list (simpler version)
        signals: List[Dict[str, object]] = [
            {'type': alert['type'], 'detail': alert['detail']}
            for alert in alerts
        ]
        
        candidate.fraud_risk_score = round(fraud_score, 2)
        candidate.fraud_signals = signals
        candidate.anomaly_flags = {
            'total_alerts': len(alerts),
            'alert_types': [alert['type'] for alert in alerts],
            'max_confidence': round(max_confidence, 2),
        }

        session.add(candidate)
        await session.commit()
        await session.refresh(candidate)

        # Create fraud alert if threshold exceeded
        if fraud_score >= settings.FRAUD_RISK_THRESHOLD and alerts:
            alert = FraudAlert(
                candidate_id=candidate.id,
                alert_type='fraud_risk_detected',
                severity='high' if fraud_score >= 0.8 else 'medium' if fraud_score >= 0.5 else 'low',
                description=f"Candidate profile shows potential anomalies. Detected issues: {', '.join([a['type'] for a in alerts])}",
                evidence={
                    'fraud_score': fraud_score,
                    'alerts': alerts,
                },
                confidence_score=fraud_score,
                created_at=datetime.utcnow(),
            )
            session.add(alert)
            await session.commit()

        return candidate

