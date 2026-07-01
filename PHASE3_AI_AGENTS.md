# PHASE 3: AI Agents & Scoring Intelligence

## Overview
Implement the 7 AI agents that drive candidate intelligence and ranking.

## Agent Architecture

### Agent 1: Role Understanding Agent

**Purpose**: Parse job descriptions and extract requirements

**Input**:
```json
{
  "job_title": "Senior Full Stack Engineer",
  "job_description": "...",
  "required_skills": [],
  "seniority_level": "Senior"
}
```

**Processing**:
1. NLP analysis of job description
2. Extract entities (skills, responsibilities)
3. Categorize skills (technical vs soft)
4. Identify leadership requirements
5. Detect culture signals
6. Generate job embedding

**Output**:
```python
{
    "technical_skills": [
        {"skill": "Python", "importance": 0.95, "category": "backend"},
        {"skill": "React", "importance": 0.85, "category": "frontend"},
        ...
    ],
    "soft_skills": [
        {"skill": "Communication", "importance": 0.8},
        {"skill": "Leadership", "importance": 0.7},
    ],
    "leadership_requirements": {
        "team_size": 5,
        "required_experience": 3,
        "competencies": [...]
    },
    "seniority": "Senior",
    "culture_signals": ["innovation", "startup_mindset", "remote_first"],
    "job_embedding": [...]  # Vector(1024)
}
```

**Implementation**:
```python
# backend/app/agents/role_understanding.py
class RoleUnderstandingAgent:
    async def analyze(self, job: Job) -> JobAnalysis:
        # Use LLM + regex/NLP for extraction
        # Generate embedding
        # Store results
        pass
```

---

### Agent 2: Candidate Intelligence Agent

**Purpose**: Holistically analyze candidate profiles

**Input**: Candidate profile (name, headline, summary, career history, skills, education)

**Processing**:
1. Parse career history
2. Assess skill depth per domain
3. Calculate experience level
4. Evaluate communication signals
5. Detect leadership patterns
6. Generate candidate embedding

**Skill Depth Calculation**:
```python
skill_depth = {
    "Python": {
        "proficiency": "expert",
        "years": 8,
        "breadth": 0.9,  # Used in multiple roles
        "depth_score": 0.92
    },
    "React": {
        "proficiency": "intermediate",
        "years": 3,
        "breadth": 0.6,
        "depth_score": 0.65
    }
}
```

**Output**:
```python
{
    "skill_depth": {...},
    "experience_level": {"total_years": 8, "seniority": "Senior"},
    "leadership_score": 0.75,
    "growth_score": 0.82,
    "behavioral_score": 0.78,
    "communication_score": 0.85,
    "profile_embedding": [...]  # Vector(1024)
}
```

---

### Agent 3: Behavioral Analysis Agent

**Purpose**: Extract behavioral signals from profile

**Metrics**:
```python
behavioral_metrics = {
    "profile_completeness": 0.92,      # % of fields filled
    "activity_recency": 30,             # Days since last update
    "recruiter_response_rate": 0.85,    # Historical response rate
    "assessment_completion": 0.90,      # Assessment completion rate
    "profile_update_frequency": 0.6,    # How often updated
    "engagement_score": 0.78
}
```

**Behavioral Score Calculation**:
```
behavioral_score = (
    0.3 * profile_completeness +
    0.2 * (1 - activity_recency/365) +  # Recent = good
    0.2 * recruiter_response_rate +
    0.2 * assessment_completion +
    0.1 * engagement_score
)
```

---

### Agent 4: Career Trajectory Agent

**Purpose**: Analyze career growth patterns

**Metrics**:

1. **Promotion Velocity**
   ```
   promotions_per_year = (number_of_promotions) / (total_years)
   ```

2. **Career Growth Trend**
   ```python
   career_growth = {
       "responsibility_progression": 0.85,   # Scope expansion
       "salary_growth_rate": 0.12,           # Yearly growth
       "skill_accumulation": 0.78,           # New skills over time
       "tenure_progression": 0.8             # Career stability
   }
   ```

3. **Skill Evolution**
   ```python
   skill_evolution = {
       "new_skills_per_year": 1.5,
       "skill_depth_growth": 0.75,
       "technology_adoption": 0.82,
       "breadth_expansion": 0.65
   }
   ```

4. **Responsibility Growth**
   ```python
   responsibility_growth = {
       "team_lead_experience": 3,      # Years
       "project_complexity": 0.85,
       "scope_increase": 0.78,
       "impact_level": 0.88
   }
   ```

**Output**:
```python
{
    "promotion_velocity": 1.2,              # promotions/year
    "career_growth_trend": {...},
    "skill_evolution": {...},
    "responsibility_growth": {...},
    "career_growth_score": 0.81
}
```

---

### Agent 5: Fraud Detection Agent

**Purpose**: Identify suspicious/fraudulent profiles

**Detection Methods**:

1. **Skill Stuffing Detection**
   ```python
   # Too many skills, unusual proficiency claims
   if candidate.total_skills > 50:
       anomaly_score += 0.3
   if sum(proficiency=="expert" for skill in skills) > 20:
       anomaly_score += 0.4
   ```

2. **Timeline Inconsistencies**
   ```python
   # Overlapping roles, missing gaps, suspicious dates
   for role in career_history:
       if role.end_date < role.start_date:
           alert_type = "timeline_inconsistency"
   ```

3. **Unrealistic Claims**
   ```python
   # Claims inconsistent with role/timeline
   # E.g., "10 years Python" but only 3 years total experience
   if skill_years > total_years:
       alert_type = "unrealistic_claims"
   ```

4. **Isolation Forest Anomaly Detection**
   ```python
   from sklearn.ensemble import IsolationForest
   
   features = [
       years_of_experience,
       num_skills,
       avg_tenure_months,
       promotion_velocity,
       profile_completeness,
       activity_recency
   ]
   
   iso_forest = IsolationForest(contamination=0.1)
   anomaly_scores = iso_forest.fit_predict(features)
   ```

**Fraud Alert Types**:
```python
fraud_alerts = [
    {"type": "skill_stuffing", "severity": "high", "confidence": 0.85},
    {"type": "timeline_inconsistency", "severity": "medium", "confidence": 0.72},
    {"type": "unrealistic_claims", "severity": "high", "confidence": 0.88},
    {"type": "profile_anomaly", "severity": "low", "confidence": 0.65}
]
```

---

### Agent 6: Ranking Agent

**Purpose**: Calculate final composite score and rank candidates

**Scoring Formula**:
```
Final Score = 
  0.35 × Semantic Match Score +
  0.20 × Experience Match Score +
  0.15 × Behavioral Score +
  0.10 × Career Growth Score +
  0.10 × Leadership Score +
  0.10 × Culture Fit Score
```

**Component Calculations**:

1. **Semantic Match** (embedding similarity)
   ```python
   semantic_score = cosine_similarity(job_embedding, candidate_embedding)
   ```

2. **Experience Match**
   ```python
   experience_score = min(
       candidate_years / job_required_years,
       skill_match_percentage,
       depth_in_required_skills
   ) * 0.95
   ```

3. **Leadership Match** (if required)
   ```python
   leadership_score = candidate.leadership_score * job.leadership_weight
   ```

4. **Culture Fit** (company alignment)
   ```python
   culture_signals_match = len(intersection(job_signals, candidate_signals)) / \
                          len(union(job_signals, candidate_signals))
   ```

**Hidden Gem Detection**:
```python
# Candidates with high potential but non-obvious match
is_hidden_gem = (
    final_score >= 0.7 AND
    semantic_score < 0.6 AND  # Not direct match
    skill_evolution > 0.8 AND # Strong growth
    career_trajectory_fit > 0.75  # Career path aligns
)
```

---

### Agent 7: Recruiter Copilot Agent

**Purpose**: Conversational AI for recruiter support

**Capabilities**:
1. Answer ranking questions with context
2. Compare candidates side-by-side
3. Explain ranking decisions
4. Suggest hidden gems
5. Generate job descriptions
6. Interview question recommendations

**RAG (Retrieval-Augmented Generation)**:
```
User Query → Embed Query → Retrieve relevant candidates/rankings
→ Pass to LLM with context → Generate response
```

**Implementation**:
```python
# backend/app/agents/recruiter_copilot.py
class RecruiterCopilotAgent:
    async def ask(self, query: str, context: Dict) -> CopilotResponse:
        # 1. Embed user query
        # 2. Retrieve relevant candidates/rankings from vector DB
        # 3. Get ranking explanations
        # 4. Format context
        # 5. Call LLM API (Gemini/OpenAI)
        # 6. Generate response with suggestions
        pass
```

**Example Interactions**:
```
Q: Why is Candidate A ranked higher than B?
A: Candidate A has [explanation based on scores and SHAP values]

Q: Find engineers who can transition to AI roles
A: [Query for high career_growth + ML-adjacent skills]

Q: Compare these 3 candidates
A: [Radar charts + detailed comparison]
```

---

## Implementation Steps

1. **Data Preparation**
   - Load candidate dataset (JSONL)
   - Parse and validate schema
   - Store in PostgreSQL

2. **Role Understanding Agent**
   - Parse job descriptions
   - Extract requirements
   - Generate job embeddings
   - Store analysis

3. **Candidate Intelligence Agent**
   - Analyze profiles
   - Calculate skill depth
   - Generate candidate embeddings
   - Store scores

4. **Behavioral Analysis Agent**
   - Calculate metrics
   - Generate behavioral score

5. **Career Trajectory Agent**
   - Calculate growth metrics
   - Trend analysis

6. **Fraud Detection Agent**
   - Implement detection rules
   - Isolation Forest
   - Generate alerts

7. **Ranking Agent**
   - Implement scoring formula
   - Rank candidates
   - Detect hidden gems
   - Generate SHAP explanations

8. **Recruiter Copilot Agent**
   - Implement RAG
   - LLM integration
   - Response generation

## Files to Create

```
backend/app/agents/
├── base_agent.py                    # Base class
├── role_understanding.py            # Agent 1
├── candidate_intelligence.py        # Agent 2
├── behavioral_analysis.py           # Agent 3
├── career_trajectory.py             # Agent 4
├── fraud_detection.py               # Agent 5
├── ranking.py                       # Agent 6
├── recruiter_copilot.py            # Agent 7
└── orchestrator.py                  # Coordinate agents

backend/app/services/
├── bm25_search.py
├── hybrid_search.py                 # BM25 + embedding
├── llm_service.py                   # Gemini/OpenAI
├── shap_explainer.py               # SHAP explanations
└── fraud_detector.py
```

## Success Criteria
✅ All agents functional
✅ Scoring matches formula exactly
✅ Explainability working (SHAP)
✅ Fraud detection accurate
✅ LLM responses coherent
✅ < 500ms ranking time
✅ Comprehensive test coverage
