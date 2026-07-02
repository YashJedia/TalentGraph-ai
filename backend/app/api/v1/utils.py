import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy import desc

from app.config.settings import settings
from app.models.database import Candidate, CandidateJobRanking, FraudAlert, Job
from app.models.schemas import CandidateResponse, FraudAlert as FraudAlertSchema, RankingResponse


def _get_repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _get_default_dataset_path() -> Path:
    root = _get_repository_root()
    container_path = Path("/app/data/candidate_dataset/candidates.jsonl")
    if container_path.exists():
        return container_path
    return root.joinpath("..", "India_runs_data_and_ai_challenge", "India_runs_data_and_ai_challenge", "candidates.jsonl").resolve()


def _load_jsonl_file(file_path: Path) -> List[Dict[str, Any]]:
    candidates = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            candidates.append(json.loads(raw))
    return candidates


def _parse_date(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                return None
    return None


def _normalize_skill(skill: Dict[str, Any]) -> Dict[str, Any]:
    duration_months = skill.get("duration_months")
    years = None
    if isinstance(duration_months, (int, float)):
        years = round(float(duration_months) / 12.0, 1)
    return {
        "skill_name": skill.get("name"),
        "proficiency": skill.get("proficiency", "intermediate"),
        "endorsements": int(skill.get("endorsements", 0) or 0),
        "category": "technical",
        "years_of_experience": years,
    }


def _normalize_career_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "company": entry.get("company"),
        "title": entry.get("title"),
        "start_date": _parse_date(entry.get("start_date")),
        "end_date": _parse_date(entry.get("end_date")),
        "duration_months": int(entry.get("duration_months", 0) or 0),
        "is_current": bool(entry.get("is_current", False)),
        "industry": entry.get("industry"),
        "company_size": entry.get("company_size"),
        "description": entry.get("description"),
        "responsibilities": entry.get("responsibilities"),
        "achievements": entry.get("achievements"),
    }


def _normalize_education_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "institution": entry.get("institution"),
        "degree": entry.get("degree"),
        "field_of_study": entry.get("field_of_study"),
        "start_year": int(entry.get("start_year", 0) or 0),
        "end_year": int(entry.get("end_year", 0) or 0),
        "grade": entry.get("grade"),
        "tier": entry.get("tier", "unknown"),
    }


def _map_dataset_candidate(raw: Dict[str, Any]) -> Dict[str, Any]:
    profile = raw.get("profile", {}) or {}
    redrob_signals = raw.get("redrob_signals", {}) or {}
    years_of_experience = profile.get("years_of_experience")
    completeness_score = redrob_signals.get("profile_completeness_score")

    candidate_payload = {
        "candidate_id": raw.get("candidate_id"),
        "anonymized_name": profile.get("anonymized_name"),
        "headline": profile.get("headline"),
        "summary": profile.get("summary"),
        "location": profile.get("location"),
        "country": profile.get("country"),
        "years_of_experience": float(years_of_experience) if years_of_experience is not None else None,
        "current_title": profile.get("current_title"),
        "current_company": profile.get("current_company"),
        "current_company_size": profile.get("current_company_size"),
        "current_industry": profile.get("current_industry"),
        "raw_data": raw,
    }

    if completeness_score is not None:
        try:
            candidate_payload["profile_completeness"] = min(1.0, max(0.0, float(completeness_score) / 100.0))
        except (TypeError, ValueError):
            pass

    if isinstance(redrob_signals.get("recruiter_response_rate"), (int, float)):
        candidate_payload["recruiter_response_rate"] = float(redrob_signals.get("recruiter_response_rate"))

    return candidate_payload


def _candidate_summary(candidate: Candidate) -> Optional[Dict[str, Any]]:
    if candidate is None:
        return None
    return {
        "id": candidate.id,
        "candidate_id": candidate.candidate_id,
        "anonymized_name": candidate.anonymized_name,
        "headline": candidate.headline,
        "current_title": candidate.current_title,
        "current_company": candidate.current_company,
        "years_of_experience": float(candidate.years_of_experience or 0.0) if candidate.years_of_experience is not None else None,
        "growth_score": float(candidate.growth_score or 0.0) if candidate.growth_score is not None else None,
        "behavioral_score": float(candidate.behavioral_score or 0.0) if candidate.behavioral_score is not None else None,
        "fraud_risk_score": float(candidate.fraud_risk_score or 0.0) if candidate.fraud_risk_score is not None else None,
        "profile_completeness": float(candidate.profile_completeness or 0.0) if candidate.profile_completeness is not None else None,
    }


def _ranking_to_response(ranking: CandidateJobRanking, candidate: Optional[Candidate] = None) -> RankingResponse:
    return RankingResponse(
        id=ranking.id,
        job_id=ranking.job_id,
        candidate_id=ranking.candidate_id,
        candidate=CandidateResponse.model_validate(candidate) if candidate else None,
        final_score=float(ranking.final_score or 0.0),
        rank=ranking.rank or 0,
        percentile=float(ranking.percentile or 0.0),
        top_strengths=ranking.top_strengths or [],
        potential_risks=ranking.potential_risks or [],
        hidden_gem_indicators=ranking.hidden_gem_indicators or [],
        is_hidden_gem=ranking.is_hidden_gem or False,
        is_fraud_flagged=ranking.is_fraud_flagged or False,
    )


def _fraud_alert_to_response(alert: FraudAlert) -> FraudAlertSchema:
    return FraudAlertSchema(
        id=alert.id,
        candidate_id=alert.candidate_id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        description=alert.description or "",
        confidence_score=float(alert.confidence_score or 0.0),
        evidence=alert.evidence or {},
        created_at=alert.created_at,
    )


def _update_model_from_dict(instance: Any, data: Dict[str, Any]) -> None:
    for field, value in data.items():
        if hasattr(instance, field):
            setattr(instance, field, value)
