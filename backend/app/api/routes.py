"""API router definitions for TalentGraph AI backend."""

from datetime import datetime
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, desc, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.models.database import (
    Candidate,
    CareerHistory,
    Education,
    FraudAlert,
    Job,
    CandidateJobRanking,
    RankingExplanation,
    Skill,
)
from app.agents.orchestrator import TalentGraphOrchestrator
from app.models.schemas import (
    CandidateBulkUpload,
    CandidateCreate,
    CandidateResponse,
    CandidateUpdate,
    CandidateComparisonResponse,
    CandidateSearchQuery,
    ComparisonRequest,
    CopilotMessage,
    CopilotResponse,
    FraudAlert as FraudAlertSchema,
    FraudAlertsResponse,
    HealthResponse,    SystemStatsResponse,    JobCreate,
    JobResponse,
    JobUpdate,
    RankingExplanationResponse,
    RankingListResponse,
    RankingResponse,
    SearchResponse,
)
from app.config.settings import settings

api_router = APIRouter()
orchestrator = TalentGraphOrchestrator()


class TalentGraphException(Exception):
    pass


class ResourceNotFound(TalentGraphException):
    pass


class InvalidRequest(TalentGraphException):
    pass


def _candidate_summary(candidate: Candidate) -> Optional[Dict[str, Any]]:
    if candidate is None:
        return None
    return {
        'id': candidate.id,
        'candidate_id': candidate.candidate_id,
        'anonymized_name': candidate.anonymized_name,
        'headline': candidate.headline,
        'current_title': candidate.current_title,
        'current_company': candidate.current_company,
        'years_of_experience': float(candidate.years_of_experience or 0.0) if candidate.years_of_experience is not None else None,
        'growth_score': float(candidate.growth_score or 0.0) if candidate.growth_score is not None else None,
        'behavioral_score': float(candidate.behavioral_score or 0.0) if candidate.behavioral_score is not None else None,
        'fraud_risk_score': float(candidate.fraud_risk_score or 0.0) if candidate.fraud_risk_score is not None else None,
        'profile_completeness': float(candidate.profile_completeness or 0.0) if candidate.profile_completeness is not None else None,
    }


def _ranking_to_response(ranking: CandidateJobRanking, candidate: Optional[Candidate] = None) -> RankingResponse:
    return RankingResponse(
        id=ranking.id,
        job_id=ranking.job_id,
        candidate_id=ranking.candidate_id,
        candidate=_candidate_summary(candidate) if candidate else None,
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


def _update_model_from_dict(instance, data: Dict[str, Any]) -> None:
    for field, value in data.items():
        if hasattr(instance, field):
            setattr(instance, field, value)


async def _get_candidate_or_404(candidate_id: UUID, session: AsyncSession) -> Candidate:
    candidate = await session.get(Candidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


async def _get_job_or_404(job_id: UUID, session: AsyncSession) -> Job:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


def _get_repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


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


@api_router.get("/health", response_model=HealthResponse)
async def api_health(session: AsyncSession = Depends(get_db_session)) -> HealthResponse:
    """Health check for API and PostgreSQL connectivity."""
    await session.execute(select(1))
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        database="ok",
        vector_db="unverified",
        version=settings.API_VERSION,
    )


@api_router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(session: AsyncSession = Depends(get_db_session)) -> SystemStatsResponse:
    total_jobs = int((await session.scalar(select(func.count(Job.id)))) or 0)
    total_candidates = int((await session.scalar(select(func.count(Candidate.id)))) or 0)
    total_rankings = int((await session.scalar(select(func.count(CandidateJobRanking.id)))) or 0)
    fraud_alerts_pending = int(
        (await session.scalar(select(func.count(FraudAlert.id)).where(FraudAlert.is_reviewed.is_(False)))) or 0
    )
    average_ranking_score = float((await session.scalar(select(func.avg(CandidateJobRanking.final_score)))) or 0.0)
    return SystemStatsResponse(
        total_jobs=total_jobs,
        total_candidates=total_candidates,
        total_rankings=total_rankings,
        fraud_alerts_pending=fraud_alerts_pending,
        average_ranking_score=average_ranking_score,
        processing_time_ms=0.0,
    )


@api_router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db_session),
) -> List[JobResponse]:
    query = select(Job).limit(limit).offset(offset).order_by(desc(Job.created_at))
    result = await session.execute(query)
    jobs = result.scalars().all()
    return [JobResponse.model_validate(job) for job in jobs]


@api_router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobResponse.model_validate(job)


@api_router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job_create: JobCreate, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = Job(**job_create.model_dump(exclude_none=True))
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return JobResponse.model_validate(job)


@api_router.post("/jobs/import-sample", response_model=List[JobResponse])
async def import_sample_jobs(session: AsyncSession = Depends(get_db_session)) -> List[JobResponse]:
    existing = int((await session.scalar(select(func.count(Job.id)))) or 0)
    if existing > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Jobs already exist in the database")

    sample_jobs = [
        {
            "job_title": "Senior Data Engineer",
            "company_name": "Redrob Analytics",
            "job_description": "Build and optimize data pipelines for analytics and machine learning workloads. Strong Python, SQL, Spark, and cloud experience required.",
            "required_skills": [
                {"skill": "Python", "proficiency": "expert", "priority": "critical", "years_required": 4},
                {"skill": "SQL", "proficiency": "advanced", "priority": "critical", "years_required": 4},
                {"skill": "Apache Spark", "proficiency": "advanced", "priority": "important", "years_required": 2},
            ],
            "nice_to_have_skills": [
                {"skill": "Airflow", "proficiency": "intermediate", "priority": "nice_to_have", "years_required": 1},
            ],
            "required_experience_years": 5,
            "seniority_level": "Senior",
            "location": "Bengaluru",
            "remote_option": "hybrid",
            "salary_range": {"min": 20, "max": 35, "currency": "INR"},
        },
        {
            "job_title": "AI/ML Engineer",
            "company_name": "Redrob Labs",
            "job_description": "Develop machine learning models and productionize AI solutions using modern model tooling, NLP, and cloud infrastructure.",
            "required_skills": [
                {"skill": "Machine Learning", "proficiency": "advanced", "priority": "critical", "years_required": 3},
                {"skill": "NLP", "proficiency": "advanced", "priority": "important", "years_required": 2},
                {"skill": "PyTorch", "proficiency": "intermediate", "priority": "important", "years_required": 2},
            ],
            "nice_to_have_skills": [
                {"skill": "Cloud", "proficiency": "intermediate", "priority": "nice_to_have", "years_required": 1},
            ],
            "required_experience_years": 4,
            "seniority_level": "Mid-Senior",
            "location": "Remote",
            "remote_option": "remote",
            "salary_range": {"min": 25, "max": 45, "currency": "INR"},
        },
    ]

    created_jobs = []
    for payload in sample_jobs:
        job = Job(**payload)
        session.add(job)
        created_jobs.append(job)

    await session.commit()
    for job in created_jobs:
        await session.refresh(job)

    return [JobResponse.model_validate(job) for job in created_jobs]


@api_router.get("/candidates", response_model=List[CandidateResponse])
async def list_candidates(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db_session),
) -> List[CandidateResponse]:
    query = select(Candidate).limit(limit).offset(offset).order_by(desc(Candidate.created_at))
    result = await session.execute(query)
    candidates = result.scalars().all()
    return [CandidateResponse.model_validate(candidate) for candidate in candidates]


@api_router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await session.get(Candidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return CandidateResponse.model_validate(candidate)


@api_router.post("/candidates", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate_create: CandidateCreate, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate_payload = candidate_create.model_dump(exclude_none=True)
    skills_data = candidate_payload.pop("skills", [])
    career_history_data = candidate_payload.pop("career_history", [])
    education_data = candidate_payload.pop("education", [])

    candidate = Candidate(**candidate_payload)
    session.add(candidate)
    await session.flush()

    for item in skills_data:
        session.add(Skill(**item, candidate_id=candidate.id))

    for item in career_history_data:
        session.add(CareerHistory(**item, candidate_id=candidate.id))

    for item in education_data:
        session.add(Education(**item, candidate_id=candidate.id))

    await session.commit()
    await session.refresh(candidate)
    return CandidateResponse.model_validate(candidate)


@api_router.post("/candidates/bulk", response_model=List[CandidateResponse], status_code=status.HTTP_201_CREATED)
async def bulk_upload_candidates(
    payload: CandidateBulkUpload, session: AsyncSession = Depends(get_db_session)
) -> List[CandidateResponse]:
    created_candidates = []
    for candidate_data in payload.candidates:
        candidate_payload = candidate_data.model_dump(exclude_none=True)
        skills_data = candidate_payload.pop("skills", [])
        career_history_data = candidate_payload.pop("career_history", [])
        education_data = candidate_payload.pop("education", [])

        candidate = Candidate(**candidate_payload)
        session.add(candidate)
        await session.flush()

        for item in skills_data:
            skill = Skill(**item, candidate_id=candidate.id)
            session.add(skill)

        for item in career_history_data:
            career = CareerHistory(**item, candidate_id=candidate.id)
            session.add(career)

        for item in education_data:
            education = Education(**item, candidate_id=candidate.id)
            session.add(education)

        created_candidates.append(candidate)

    await session.commit()
    for candidate in created_candidates:
        await session.refresh(candidate)

    return [CandidateResponse.model_validate(candidate) for candidate in created_candidates]


@api_router.get("/rankings/job/{job_id}", response_model=RankingListResponse)
async def get_rankings(job_id: UUID, limit: int = 20, session: AsyncSession = Depends(get_db_session)) -> RankingListResponse:
    query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == job_id).order_by(desc(CandidateJobRanking.final_score)).limit(limit)
    result = await session.execute(query)
    rankings = result.scalars().all()

    ranked_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        ranked_models.append(_ranking_to_response(ranking, candidate=candidate))

    top_10 = ranked_models[:10]
    hidden_gems = [ranking for ranking in ranked_models if ranking.is_hidden_gem]
    return RankingListResponse(
        total_candidates=len(ranked_models),
        ranked_candidates=ranked_models,
        top_10_percentile=top_10,
        hidden_gems=hidden_gems,
    )


@api_router.get("/rankings/{job_id}/top10", response_model=List[RankingResponse])
async def get_top_rankings(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == job_id).order_by(desc(CandidateJobRanking.final_score)).limit(10)
    result = await session.execute(query)
    rankings = result.scalars().all()

    ranked_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        ranked_models.append(_ranking_to_response(ranking, candidate=candidate))
    return ranked_models


@api_router.get("/rankings/hidden-gems", response_model=List[RankingResponse])
async def get_all_hidden_gems(session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    query = select(CandidateJobRanking).where(
        CandidateJobRanking.is_hidden_gem.is_(True),
    ).order_by(desc(CandidateJobRanking.final_score)).limit(50)
    result = await session.execute(query)
    rankings = result.scalars().all()

    ranked_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        ranked_models.append(_ranking_to_response(ranking, candidate=candidate))
    return ranked_models


@api_router.get("/rankings/{job_id}/hidden-gems", response_model=List[RankingResponse])
async def get_hidden_gems(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> List[RankingResponse]:
    query = select(CandidateJobRanking).where(
        CandidateJobRanking.job_id == job_id,
        CandidateJobRanking.is_hidden_gem.is_(True),
    ).order_by(desc(CandidateJobRanking.final_score))
    result = await session.execute(query)
    rankings = result.scalars().all()

    ranked_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        ranked_models.append(_ranking_to_response(ranking, candidate=candidate))
    return ranked_models


@api_router.get("/fraud/alerts", response_model=FraudAlertsResponse)
async def list_fraud_alerts(session: AsyncSession = Depends(get_db_session)) -> FraudAlertsResponse:
    query = select(FraudAlert).order_by(desc(FraudAlert.created_at)).limit(50)
    result = await session.execute(query)
    alerts = result.scalars().all()
    alert_models = [_fraud_alert_to_response(alert) for alert in alerts]
    severity_counts = {}
    for alert in alert_models:
        severity_counts[alert.severity] = severity_counts.get(alert.severity, 0) + 1

    return FraudAlertsResponse(
        total_alerts=len(alert_models),
        by_severity=severity_counts,
        recent_alerts=alert_models,
    )


@api_router.get("/fraud/alerts/{alert_id}", response_model=FraudAlertSchema)
async def get_fraud_alert(alert_id: UUID, session: AsyncSession = Depends(get_db_session)) -> FraudAlertSchema:
    alert = await session.get(FraudAlert, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fraud alert not found")
    return _fraud_alert_to_response(alert)


@api_router.post("/comparison", response_model=CandidateComparisonResponse)
async def compare_candidates(
    request: ComparisonRequest, session: AsyncSession = Depends(get_db_session)
) -> CandidateComparisonResponse:
    query = select(CandidateJobRanking).where(
        CandidateJobRanking.job_id == request.job_id,
        CandidateJobRanking.candidate_id.in_(request.candidate_ids),
    ).order_by(desc(CandidateJobRanking.final_score))
    result = await session.execute(query)
    rankings = result.scalars().all()

    comparison_metrics = {
        "job_id": str(request.job_id),
        "candidate_count": len(request.candidate_ids),
        "ranked_count": len(rankings),
    }
    recommendations = [
        "Review the top-ranked candidates first.",
        "Check candidate fit against required skills and seniority level.",
    ]

    comparison_models = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        comparison_models.append(_ranking_to_response(ranking, candidate=candidate))

    return CandidateComparisonResponse(
        candidates=comparison_models,
        comparison_metrics=comparison_metrics,
        recommendations=recommendations,
    )


@api_router.post("/copilot/ask", response_model=CopilotResponse)
async def ask_copilot(request: CopilotMessage, session: AsyncSession = Depends(get_db_session)) -> CopilotResponse:
    """Recruiter copilot endpoint using the TalentGraph AI agent orchestrator."""
    result = await orchestrator.ask_copilot(request.content, session, request.context or {})
    return CopilotResponse(
        message=result.get('message', ''),
        suggestions=result.get('suggestions', []),
        related_candidates=result.get('related_candidates', []),
        confidence=float(result.get('confidence', 0.0)),
    )


@api_router.put("/jobs/{job_id}", response_model=JobResponse)
async def update_job(job_id: UUID, job_update: JobUpdate, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await _get_job_or_404(job_id, session)
    update_data = job_update.model_dump(exclude_none=True)
    _update_model_from_dict(job, update_data)
    await session.commit()
    await session.refresh(job)
    return JobResponse.model_validate(job)


@api_router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> Response:
    job = await _get_job_or_404(job_id, session)
    await session.delete(job)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api_router.post("/jobs/{job_id}/analyze", response_model=JobResponse)
async def analyze_job(job_id: UUID, session: AsyncSession = Depends(get_db_session)) -> JobResponse:
    job = await _get_job_or_404(job_id, session)
    job = await orchestrator.analyze_job(job, session)
    return JobResponse.model_validate(job)


@api_router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(candidate_id: UUID, candidate_update: CandidateUpdate, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await _get_candidate_or_404(candidate_id, session)
    update_data = candidate_update.model_dump(exclude_none=True)
    if update_data.get("career_history") is not None:
        await session.execute(delete(CareerHistory).where(CareerHistory.candidate_id == candidate.id))
    if update_data.get("education") is not None:
        await session.execute(delete(Education).where(Education.candidate_id == candidate.id))
    if update_data.get("skills") is not None:
        await session.execute(delete(Skill).where(Skill.candidate_id == candidate.id))
    _update_model_from_dict(candidate, {k: v for k, v in update_data.items() if k not in ["career_history", "education", "skills"]})

    for item in update_data.get("career_history", []):
        session.add(CareerHistory(**item.model_dump(exclude_none=True), candidate_id=candidate.id))
    for item in update_data.get("education", []):
        session.add(Education(**item.model_dump(exclude_none=True), candidate_id=candidate.id))
    for item in update_data.get("skills", []):
        session.add(Skill(**item.model_dump(exclude_none=True), candidate_id=candidate.id))

    await session.commit()
    await session.refresh(candidate)
    return CandidateResponse.model_validate(candidate)


@api_router.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> Response:
    candidate = await _get_candidate_or_404(candidate_id, session)
    await session.delete(candidate)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api_router.post("/candidates/{candidate_id}/analyze", response_model=CandidateResponse)
async def analyze_candidate(candidate_id: UUID, session: AsyncSession = Depends(get_db_session)) -> CandidateResponse:
    candidate = await _get_candidate_or_404(candidate_id, session)
    candidate = await orchestrator.analyze_candidate(candidate, session)
    return CandidateResponse.model_validate(candidate)


@api_router.post("/candidates/import-dataset", response_model=List[CandidateResponse])
async def import_candidate_dataset(
    file_path: Optional[str] = None,
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_db_session),
) -> List[CandidateResponse]:
    default_path = _get_default_dataset_path()
    effective_path = Path(file_path) if file_path else default_path
    if not effective_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset file not found: {effective_path}")

    raw_candidates = _load_jsonl_file(effective_path)
    if limit is not None and limit > 0:
        raw_candidates = raw_candidates[:limit]
    created_candidates = []
    for raw in raw_candidates:
        if not isinstance(raw, dict):
            continue
        candidate_payload = _map_dataset_candidate(raw)
        if not candidate_payload.get("candidate_id"):
            continue

        candidate = Candidate(**candidate_payload)
        session.add(candidate)
        await session.flush()

        for skill in raw.get("skills", []):
            normalized_skill = _normalize_skill(skill)
            session.add(Skill(**normalized_skill, candidate_id=candidate.id))

        for entry in raw.get("career_history", []):
            session.add(CareerHistory(**_normalize_career_entry(entry), candidate_id=candidate.id))

        for entry in raw.get("education", []):
            session.add(Education(**_normalize_education_entry(entry), candidate_id=candidate.id))

        created_candidates.append(candidate)

    await session.commit()

    enriched_candidates = []
    for candidate in created_candidates:
        await session.refresh(candidate)
        try:
            candidate = await orchestrator.analyze_candidate(candidate, session)
        except Exception:
            # Continue even if analysis fails for a particular candidate
            pass
        enriched_candidates.append(candidate)

    return [CandidateResponse.model_validate(candidate) for candidate in enriched_candidates]


@api_router.post("/rankings/job/{job_id}", response_model=RankingListResponse)
async def rank_candidates_for_job(job_id: UUID, limit: int = 50, session: AsyncSession = Depends(get_db_session)) -> RankingListResponse:
    job = await _get_job_or_404(job_id, session)
    candidates_query = select(Candidate).options(
        selectinload(Candidate.skills),
        selectinload(Candidate.career_history),
        selectinload(Candidate.education),
    )
    candidates_result = await session.execute(candidates_query)
    candidates = candidates_result.scalars().all()
    if not candidates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No candidates available for ranking")

    await session.execute(delete(CandidateJobRanking).where(CandidateJobRanking.job_id == job.id))
    await session.commit()

    rankings = await orchestrator.rank_job(job, candidates, session, limit=limit)
    ranked_models = []
    for ranking in rankings:
        candidate = next((candidate for candidate in candidates if candidate.id == ranking.candidate_id), None)
        ranked_models.append(_ranking_to_response(ranking, candidate=candidate))

    top_10 = ranked_models[:10]
    hidden_gems = [ranking for ranking in ranked_models if ranking.is_hidden_gem]
    return RankingListResponse(
        total_candidates=len(rankings),
        ranked_candidates=ranked_models,
        top_10_percentile=top_10,
        hidden_gems=hidden_gems,
    )


@api_router.get("/rankings/{ranking_id}", response_model=RankingResponse)
async def get_ranking(ranking_id: UUID, session: AsyncSession = Depends(get_db_session)) -> RankingResponse:
    ranking = await session.get(CandidateJobRanking, ranking_id)
    if ranking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ranking not found")
    candidate = await session.get(Candidate, ranking.candidate_id)
    return _ranking_to_response(ranking, candidate=candidate)


@api_router.post("/rankings/{ranking_id}/explain", response_model=RankingExplanationResponse)
async def explain_ranking(ranking_id: UUID, session: AsyncSession = Depends(get_db_session)) -> RankingExplanationResponse:
    ranking = await session.get(CandidateJobRanking, ranking_id)
    if ranking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ranking not found")

    explanation = RankingExplanation(
        ranking_id=ranking.id,
        feature_importance={
            "semantic_match": float(ranking.semantic_match_score or 0.0),
            "experience": float(ranking.experience_match_score or 0.0),
            "leadership": float(ranking.leadership_score or 0.0),
        },
        top_contributing_factors=["experience", "communication", "culture"],
        why_selected_narrative=f"Candidate {ranking.candidate_id} scored {ranking.final_score} for job {ranking.job_id}.",
        risks_narrative="Potential risk from skill gap or lack of domain experience.",
        opportunities_narrative="Strong fit for collaborative teams and growth roles.",
    )
    session.add(explanation)
    await session.commit()
    return RankingExplanationResponse(
        ranking_id=ranking.id,
        summary=explanation.why_selected_narrative,
        top_strengths=ranking.top_strengths or [],
        potential_risks=ranking.potential_risks or [],
        narrative=explanation.opportunities_narrative or "",
    )


@api_router.post("/search", response_model=SearchResponse)
async def search_candidates(query: CandidateSearchQuery, session: AsyncSession = Depends(get_db_session)) -> SearchResponse:
    ranking_query = select(CandidateJobRanking).where(CandidateJobRanking.job_id == query.job_id)
    if query.exclude_fraud_flagged:
        ranking_query = ranking_query.where(CandidateJobRanking.is_fraud_flagged.is_(False))
    if query.min_score is not None:
        ranking_query = ranking_query.where(CandidateJobRanking.final_score >= query.min_score)
    if not query.include_hidden_gems:
        ranking_query = ranking_query.where(CandidateJobRanking.is_hidden_gem.is_(False))

    ranking_query = ranking_query.order_by(desc(CandidateJobRanking.final_score)).limit(query.limit).offset(query.offset)
    result = await session.execute(ranking_query)
    rankings = result.scalars().all()
    results = []
    for ranking in rankings:
        candidate = await session.get(Candidate, ranking.candidate_id)
        if not candidate:
            continue
        results.append(
            {
                "candidate": CandidateResponse.model_validate(candidate),
                "score": float(ranking.final_score or 0.0),
            }
        )
    return SearchResponse(
        total_results=len(results),
        results=results,
    )
