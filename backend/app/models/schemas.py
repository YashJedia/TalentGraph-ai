"""Pydantic models for API requests/responses"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


# ============================================
# Job Models
# ============================================

class SkillRequirement(BaseModel):
    skill: str
    proficiency: str = "intermediate"  # beginner, intermediate, advanced, expert
    priority: str = "nice_to_have"  # critical, important, nice_to_have
    years_required: int = 0


class JobBase(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    required_skills: Optional[List[SkillRequirement]] = None
    nice_to_have_skills: Optional[List[SkillRequirement]] = None
    required_experience_years: Optional[int] = None
    seniority_level: Optional[str] = None
    location: Optional[str] = None
    remote_option: Optional[str] = None
    salary_range: Optional[Dict[str, Any]] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_description: Optional[str] = None
    required_skills: Optional[List[SkillRequirement]] = None
    nice_to_have_skills: Optional[List[SkillRequirement]] = None
    required_experience_years: Optional[int] = None
    seniority_level: Optional[str] = None
    location: Optional[str] = None
    remote_option: Optional[str] = None
    salary_range: Optional[Dict[str, Any]] = None


class JobResponse(JobBase):
    id: UUID
    technical_skills: Optional[Dict[str, Any]] = None
    soft_skills: Optional[Dict[str, Any]] = None
    leadership_requirements: Optional[Dict[str, Any]] = None
    culture_signals: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Candidate Models
# ============================================

class EducationDetail(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int
    grade: Optional[str] = None
    tier: Optional[str] = None


class CareerEntry(BaseModel):
    company: str
    title: str
    start_date: datetime
    end_date: Optional[datetime] = None
    duration_months: int
    is_current: bool
    industry: str
    company_size: str
    description: str
    responsibilities: Optional[List[str]] = None
    achievements: Optional[List[str]] = None


class CandidateSkill(BaseModel):
    skill_name: str
    proficiency: str  # beginner, intermediate, advanced, expert
    endorsements: int = 0
    category: str = "technical"  # technical, soft, leadership, domain
    years_of_experience: Optional[float] = None


class CandidateUpdate(BaseModel):
    candidate_id: Optional[str] = None
    anonymized_name: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    years_of_experience: Optional[float] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    current_company_size: Optional[str] = None
    current_industry: Optional[str] = None
    career_history: Optional[List[CareerEntry]] = None
    education: Optional[List[EducationDetail]] = None
    skills: Optional[List[CandidateSkill]] = None


class CandidateBase(BaseModel):
    candidate_id: str
    anonymized_name: str
    headline: str
    summary: str
    location: str
    country: str
    years_of_experience: float
    current_title: str
    current_company: str
    current_company_size: str
    current_industry: str


class CandidateCreate(CandidateBase):
    career_history: List[CareerEntry]
    education: List[EducationDetail]
    skills: List[CandidateSkill]


class CandidateResponse(CandidateBase):
    id: UUID
    skill_depth: Optional[Dict[str, Any]] = None
    experience_level: Optional[Dict[str, Any]] = None
    leadership_score: Optional[float] = None
    growth_score: Optional[float] = None
    behavioral_score: Optional[float] = None
    communication_score: Optional[float] = None
    fraud_risk_score: Optional[float] = None
    profile_completeness: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateBulkUpload(BaseModel):
    candidates: List[CandidateCreate]


# ============================================
# Ranking Models
# ============================================

class RankingScores(BaseModel):
    semantic_match_score: float
    experience_match_score: float
    behavioral_score: float
    career_growth_score: float
    leadership_score: float
    culture_fit_score: float


class RankingResponse(BaseModel):
    id: UUID
    job_id: UUID
    candidate_id: UUID
    final_score: float
    rank: int
    percentile: float
    top_strengths: List[str]
    potential_risks: List[str]
    hidden_gem_indicators: Optional[List[str]] = None
    is_hidden_gem: bool
    is_fraud_flagged: bool

    class Config:
        from_attributes = True


class RankingExplanationResponse(BaseModel):
    ranking_id: UUID
    summary: str
    top_strengths: List[str]
    potential_risks: List[str]
    narrative: str


class RankingListResponse(BaseModel):
    total_candidates: int
    ranked_candidates: List[RankingResponse]
    top_10_percentile: List[RankingResponse]
    hidden_gems: List[RankingResponse]


class SearchResult(BaseModel):
    candidate: CandidateResponse
    score: float


class SearchResponse(BaseModel):
    total_results: int
    results: List[SearchResult]


# ============================================
# Search & Query Models
# ============================================

class CandidateSearchQuery(BaseModel):
    job_id: UUID
    limit: int = Field(default=10, le=100)
    offset: int = Field(default=0, ge=0)
    include_hidden_gems: bool = True
    exclude_fraud_flagged: bool = True
    min_score: Optional[float] = Field(default=0.5, ge=0, le=1)


class ComparisonRequest(BaseModel):
    candidate_ids: List[UUID]
    job_id: UUID


class CandidateComparisonResponse(BaseModel):
    candidates: List[RankingResponse]
    comparison_metrics: Dict[str, Any]
    recommendations: List[str]


# ============================================
# Fraud Detection Models
# ============================================

class FraudAlert(BaseModel):
    id: UUID
    candidate_id: UUID
    alert_type: str
    severity: str
    description: str
    confidence_score: float
    evidence: Dict[str, Any]
    created_at: datetime


class FraudAlertsResponse(BaseModel):
    total_alerts: int
    by_severity: Dict[str, int]
    recent_alerts: List[FraudAlert]


# ============================================
# Copilot Models
# ============================================

class CopilotMessage(BaseModel):
    content: str
    context: Optional[Dict[str, Any]] = None


class CopilotResponse(BaseModel):
    message: str
    suggestions: Optional[List[str]] = None
    related_candidates: Optional[List[UUID]] = None
    confidence: float


# ============================================
# Health & Analytics
# ============================================

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    vector_db: str
    version: str


class SystemStatsResponse(BaseModel):
    total_jobs: int
    total_candidates: int
    total_rankings: int
    fraud_alerts_pending: int
    average_ranking_score: float
    processing_time_ms: float
