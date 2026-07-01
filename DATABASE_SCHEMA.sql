-- TalentGraph AI - Complete Database Schema
-- PostgreSQL 14+

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================
-- Core Tables
-- ============================================

-- Jobs Table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_description TEXT NOT NULL,
    required_skills JSONB,
    nice_to_have_skills JSONB,
    required_experience_years INT,
    seniority_level VARCHAR(50),
    location VARCHAR(255),
    remote_option VARCHAR(50),
    salary_range JSONB,
    job_embedding JSONB,
    
    -- Role Understanding Agent Output
    technical_skills JSONB,
    soft_skills JSONB,
    leadership_requirements JSONB,
    seniority_analysis JSONB,
    culture_signals JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID
);

-- Candidates Table
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id VARCHAR(50) UNIQUE NOT NULL,
    anonymized_name VARCHAR(255),
    headline VARCHAR(255),
    summary TEXT,
    location VARCHAR(255),
    country VARCHAR(100),
    years_of_experience DECIMAL(5, 1),
    current_title VARCHAR(255),
    current_company VARCHAR(255),
    current_company_size VARCHAR(50),
    current_industry VARCHAR(100),
    
    -- Candidate Intelligence Agent Output
    profile_embedding JSONB,
    skill_depth JSONB,
    experience_level JSONB,
    leadership_score DECIMAL(3, 2),
    growth_score DECIMAL(3, 2),
    behavioral_score DECIMAL(3, 2),
    communication_score DECIMAL(3, 2),
    
    -- Career Trajectory Analysis
    promotion_velocity DECIMAL(5, 2),
    career_growth_trend JSONB,
    skill_evolution JSONB,
    responsibility_growth JSONB,
    
    -- Fraud Detection
    fraud_risk_score DECIMAL(3, 2),
    fraud_signals JSONB,
    anomaly_flags JSONB,
    
    -- Profile Quality
    profile_completeness DECIMAL(3, 2),
    activity_recency TIMESTAMP,
    recruiter_response_rate DECIMAL(3, 2),
    assessment_completion_rate DECIMAL(3, 2),
    
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Career History Table
CREATE TABLE career_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    company VARCHAR(255),
    title VARCHAR(255),
    start_date DATE,
    end_date DATE,
    duration_months INT,
    is_current BOOLEAN,
    industry VARCHAR(100),
    company_size VARCHAR(50),
    description TEXT,
    responsibilities JSONB,
    achievements JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Education Table
CREATE TABLE education (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    institution VARCHAR(255),
    degree VARCHAR(100),
    field_of_study VARCHAR(255),
    start_year INT,
    end_year INT,
    grade VARCHAR(50),
    tier VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills Table
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    skill_name VARCHAR(255),
    proficiency VARCHAR(50), -- beginner, intermediate, advanced, expert
    endorsements INT DEFAULT 0,
    last_used_date DATE,
    category VARCHAR(100), -- technical, soft, leadership, domain
    years_of_experience DECIMAL(5, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Ranking & Matching Tables
-- ============================================

-- Candidate-Job Rankings (Ranking Agent Output)
CREATE TABLE candidate_job_rankings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    -- Individual Scores
    semantic_match_score DECIMAL(3, 2),
    experience_match_score DECIMAL(3, 2),
    behavioral_score DECIMAL(3, 2),
    career_growth_score DECIMAL(3, 2),
    leadership_score DECIMAL(3, 2),
    culture_fit_score DECIMAL(3, 2),
    
    -- Final Composite Score
    final_score DECIMAL(3, 2) NOT NULL,
    rank INT,
    percentile DECIMAL(5, 2),
    
    -- Explanations & Insights
    top_strengths JSONB,
    potential_risks JSONB,
    hidden_gem_indicators JSONB,
    transferable_skills_analysis JSONB,
    career_trajectory_fit JSONB,
    
    is_hidden_gem BOOLEAN DEFAULT false,
    is_fraud_flagged BOOLEAN DEFAULT false,
    
    bm25_score DECIMAL(3, 2),
    embedding_similarity DECIMAL(3, 2),
    hybrid_retrieval_score DECIMAL(3, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(job_id, candidate_id)
);

-- Explainability Table
CREATE TABLE ranking_explanations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ranking_id UUID NOT NULL REFERENCES candidate_job_rankings(id) ON DELETE CASCADE,
    
    -- SHAP Explanations
    feature_importance JSONB,
    top_contributing_factors JSONB,
    
    -- Narrative Explanations
    why_selected_narrative TEXT,
    risks_narrative TEXT,
    opportunities_narrative TEXT,
    
    -- Visual Explanations
    radar_chart_data JSONB,
    comparison_metrics JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Behavioral Signals & Conversation History
-- ============================================

-- Recruiter Interactions
CREATE TABLE recruiter_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recruiter_id UUID NOT NULL,
    candidate_id UUID REFERENCES candidates(id) ON DELETE SET NULL,
    job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,
    interaction_type VARCHAR(100), -- view, contact, interview, reject, offer
    interaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_seconds INT,
    notes TEXT
);

-- Copilot Conversations
CREATE TABLE copilot_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recruiter_id UUID NOT NULL,
    session_id VARCHAR(255),
    
    conversation_history JSONB,
    context_data JSONB, -- current candidates, jobs being evaluated
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation Messages
CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES copilot_conversations(id) ON DELETE CASCADE,
    
    message_type VARCHAR(20), -- user, assistant
    content TEXT,
    embedded_query JSONB,
    
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Analytics & Audit Tables
-- ============================================

-- Audit Log
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    entity_type VARCHAR(100),
    entity_id UUID,
    action VARCHAR(50), -- create, update, delete, view
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Analytics
CREATE TABLE ranking_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    
    total_candidates_ranked INT,
    top_10_hired INT,
    top_25_hired INT,
    hidden_gems_hired INT,
    false_positives INT,
    false_negatives INT,
    
    precision_at_10 DECIMAL(3, 2),
    recall_at_10 DECIMAL(3, 2),
    map_score DECIMAL(3, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Fraud & Anomaly Detection
-- ============================================

CREATE TABLE fraud_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    alert_type VARCHAR(100), -- skill_stuffing, timeline_inconsistency, unrealistic_claims, etc.
    severity VARCHAR(20), -- low, medium, high, critical
    description TEXT,
    evidence JSONB,
    confidence_score DECIMAL(3, 2),
    
    is_reviewed BOOLEAN DEFAULT false,
    reviewer_id UUID,
    reviewer_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP
);

-- Anomaly Scores (Isolation Forest Results)
CREATE TABLE anomaly_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    
    anomaly_score DECIMAL(5, 4),
    is_anomaly BOOLEAN,
    anomaly_features JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- System & Cache Tables
-- ============================================

-- Cached Rankings (for faster retrieval)
CREATE TABLE ranking_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    
    cached_rankings JSONB,
    cache_hit_count INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Text search indexes
CREATE INDEX idx_candidates_fulltext ON candidates USING GIN (to_tsvector('english', summary));
CREATE INDEX idx_jobs_fulltext ON jobs USING GIN (to_tsvector('english', job_description));

-- BRIN indexes for timestamp columns
CREATE INDEX idx_candidates_created_brin ON candidates USING BRIN (created_at);
CREATE INDEX idx_rankings_created_brin ON candidate_job_rankings USING BRIN (created_at);

-- ============================================
-- Views
-- ============================================

-- Top Candidates by Job
CREATE VIEW top_candidates_by_job AS
SELECT 
    j.job_title,
    j.company_name,
    c.anonymized_name,
    c.current_title,
    cjr.final_score,
    cjr.rank,
    cjr.is_hidden_gem,
    cjr.is_fraud_flagged
FROM candidate_job_rankings cjr
JOIN jobs j ON cjr.job_id = j.id
JOIN candidates c ON cjr.candidate_id = c.id
WHERE cjr.rank <= 10
ORDER BY j.id, cjr.rank;

-- Hidden Gems
CREATE VIEW hidden_gems_view AS
SELECT 
    c.anonymized_name,
    c.current_title,
    c.years_of_experience,
    cjr.job_id,
    cjr.final_score,
    cjr.hidden_gem_indicators
FROM candidate_job_rankings cjr
JOIN candidates c ON cjr.candidate_id = c.id
WHERE cjr.is_hidden_gem = true
ORDER BY cjr.final_score DESC;

-- Fraud Alerts Summary
CREATE VIEW fraud_alerts_summary AS
SELECT 
    alert_type,
    severity,
    COUNT(*) as count,
    COUNT(*) FILTER (WHERE is_reviewed = false) as unreviewed_count
FROM fraud_alerts
GROUP BY alert_type, severity;
