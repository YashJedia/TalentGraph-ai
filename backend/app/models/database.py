"""SQLAlchemy database models"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, ForeignKey, Index, UUID as SQLALCHEMY_UUID, func, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from uuid import uuid4
import datetime

from app.db.session import Base


class Job(Base):
    """Job posting model"""

    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_title = Column(String(255), nullable=False, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    job_description = Column(Text, nullable=False)
    required_skills = Column(JSONB, nullable=True)
    nice_to_have_skills = Column(JSONB, nullable=True)
    required_experience_years = Column(Integer, nullable=True)
    seniority_level = Column(String(50), nullable=True, index=True)
    location = Column(String(255), nullable=True)
    remote_option = Column(String(50), nullable=True)
    salary_range = Column(JSONB, nullable=True)

    # Role Understanding Agent Output
    technical_skills = Column(JSONB, nullable=True)
    soft_skills = Column(JSONB, nullable=True)
    leadership_requirements = Column(JSONB, nullable=True)
    seniority_analysis = Column(JSONB, nullable=True)
    culture_signals = Column(JSONB, nullable=True)

    # Embeddings
    job_embedding = Column(JSONB, nullable=True)  # Store as JSON array, use pgvector in future

    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    rankings = relationship("CandidateJobRanking", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_job_created", "created_at"),
    )


class Candidate(Base):
    """Candidate profile model"""

    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    candidate_id = Column(String(50), unique=True, nullable=False, index=True)
    anonymized_name = Column(String(255), nullable=True)
    headline = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    years_of_experience = Column(DECIMAL(5, 1), nullable=True, index=True)
    current_title = Column(String(255), nullable=True, index=True)
    current_company = Column(String(255), nullable=True, index=True)
    current_company_size = Column(String(50), nullable=True)
    current_industry = Column(String(100), nullable=True)

    # Candidate Intelligence Agent Output
    profile_embedding = Column(JSONB, nullable=True)
    skill_depth = Column(JSONB, nullable=True)
    experience_level = Column(JSONB, nullable=True)
    leadership_score = Column(DECIMAL(3, 2), nullable=True)
    growth_score = Column(DECIMAL(3, 2), nullable=True)
    behavioral_score = Column(DECIMAL(3, 2), nullable=True)
    communication_score = Column(DECIMAL(3, 2), nullable=True)

    # Career Trajectory Analysis
    promotion_velocity = Column(DECIMAL(5, 2), nullable=True)
    career_growth_trend = Column(JSONB, nullable=True)
    skill_evolution = Column(JSONB, nullable=True)
    responsibility_growth = Column(JSONB, nullable=True)

    # Fraud Detection
    fraud_risk_score = Column(DECIMAL(3, 2), nullable=True)
    fraud_signals = Column(JSONB, nullable=True)
    anomaly_flags = Column(JSONB, nullable=True)

    # Profile Quality
    profile_completeness = Column(DECIMAL(3, 2), nullable=True)
    activity_recency = Column(DateTime, nullable=True)
    recruiter_response_rate = Column(DECIMAL(3, 2), nullable=True)
    assessment_completion_rate = Column(DECIMAL(3, 2), nullable=True)

    raw_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    career_history = relationship("CareerHistory", back_populates="candidate", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    rankings = relationship("CandidateJobRanking", back_populates="candidate", cascade="all, delete-orphan")
    fraud_alerts = relationship("FraudAlert", back_populates="candidate", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_candidate_created", "created_at"),
    )


class CareerHistory(Base):
    """Career history model"""

    __tablename__ = "career_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True, index=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    duration_months = Column(Integer, nullable=True)
    is_current = Column(Boolean, default=False)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    responsibilities = Column(JSONB, nullable=True)
    achievements = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    candidate = relationship("Candidate", back_populates="career_history")


class Education(Base):
    """Education model"""

    __tablename__ = "education"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    institution = Column(String(255), nullable=True, index=True)
    degree = Column(String(100), nullable=True)
    field_of_study = Column(String(255), nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    grade = Column(String(50), nullable=True)
    tier = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    candidate = relationship("Candidate", back_populates="education")


class Skill(Base):
    """Candidate skills model"""

    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(255), nullable=False, index=True)
    proficiency = Column(String(50), nullable=True)  # beginner, intermediate, advanced, expert
    endorsements = Column(Integer, default=0)
    last_used_date = Column(DateTime, nullable=True)
    category = Column(String(100), nullable=True, index=True)  # technical, soft, leadership, domain
    years_of_experience = Column(DECIMAL(5, 1), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    candidate = relationship("Candidate", back_populates="skills")


class CandidateJobRanking(Base):
    """Candidate-Job ranking model (Ranking Agent Output)"""

    __tablename__ = "candidate_job_rankings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)

    # Individual Scores
    semantic_match_score = Column(DECIMAL(3, 2), nullable=True)
    experience_match_score = Column(DECIMAL(3, 2), nullable=True)
    behavioral_score = Column(DECIMAL(3, 2), nullable=True)
    career_growth_score = Column(DECIMAL(3, 2), nullable=True)
    leadership_score = Column(DECIMAL(3, 2), nullable=True)
    culture_fit_score = Column(DECIMAL(3, 2), nullable=True)

    # Final Score
    final_score = Column(DECIMAL(3, 2), nullable=False, index=True)
    rank = Column(Integer, nullable=True, index=True)
    percentile = Column(DECIMAL(5, 2), nullable=True)

    # Explanations
    top_strengths = Column(JSONB, nullable=True)
    potential_risks = Column(JSONB, nullable=True)
    hidden_gem_indicators = Column(JSONB, nullable=True)
    transferable_skills_analysis = Column(JSONB, nullable=True)
    career_trajectory_fit = Column(JSONB, nullable=True)

    # Flags
    is_hidden_gem = Column(Boolean, default=False)
    is_fraud_flagged = Column(Boolean, default=False)

    # Hybrid Retrieval Scores
    bm25_score = Column(DECIMAL(3, 2), nullable=True)
    embedding_similarity = Column(DECIMAL(3, 2), nullable=True)
    hybrid_retrieval_score = Column(DECIMAL(3, 2), nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="rankings")
    candidate = relationship("Candidate", back_populates="rankings")
    explanations = relationship("RankingExplanation", back_populates="ranking", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_ranking_job_candidate", "job_id", "candidate_id", unique=True),
    )


class RankingExplanation(Base):
    """Ranking explanations (SHAP, narratives, etc.)"""

    __tablename__ = "ranking_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    ranking_id = Column(UUID(as_uuid=True), ForeignKey("candidate_job_rankings.id", ondelete="CASCADE"), nullable=False, index=True)

    # SHAP Explanations
    feature_importance = Column(JSONB, nullable=True)
    top_contributing_factors = Column(JSONB, nullable=True)

    # Narrative Explanations
    why_selected_narrative = Column(Text, nullable=True)
    risks_narrative = Column(Text, nullable=True)
    opportunities_narrative = Column(Text, nullable=True)

    # Visual Explanations
    radar_chart_data = Column(JSONB, nullable=True)
    comparison_metrics = Column(JSONB, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    ranking = relationship("CandidateJobRanking", back_populates="explanations")


class FraudAlert(Base):
    """Fraud alerts model"""

    __tablename__ = "fraud_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)

    alert_type = Column(String(100), nullable=False)  # skill_stuffing, timeline_inconsistency, etc.
    severity = Column(String(20), nullable=False, index=True)  # low, medium, high, critical
    description = Column(Text, nullable=True)
    evidence = Column(JSONB, nullable=True)
    confidence_score = Column(DECIMAL(3, 2), nullable=True)

    is_reviewed = Column(Boolean, default=False, index=True)
    reviewer_id = Column(UUID(as_uuid=True), nullable=True)
    reviewer_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="fraud_alerts")


# Export all models
__all__ = [
    "Base",
    "Job",
    "Candidate",
    "CareerHistory",
    "Education",
    "Skill",
    "CandidateJobRanking",
    "RankingExplanation",
    "FraudAlert",
]
