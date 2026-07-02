import asyncio
from app.agents.ranking import RankingAgent


class DummySkill:
    def __init__(self, skill_name: str, proficiency: str = "intermediate", years_of_experience: float = 1.0):
        self.skill_name = skill_name
        self.proficiency = proficiency
        self.years_of_experience = years_of_experience


class DummyCandidate:
    def __init__(self):
        self.id = "00000000-0000-0000-0000-000000000001"
        self.summary = "Experienced data engineer with cloud and ETL expertise."
        self.years_of_experience = 5.0
        self.behavioral_score = 0.7
        self.growth_score = 0.6
        self.leadership_score = 0.4
        self.fraud_risk_score = 0.1
        self.current_industry = "analytics"
        self.location = "Bengaluru"
        self.current_company_size = "medium"
        self.skills = [DummySkill("Python", "expert", 4.0)]
        self.profile_embedding = [0.01] * 1024


class DummyJob:
    def __init__(self):
        self.id = "00000000-0000-0000-0000-000000000010"
        self.job_description = "Looking for a data engineer with strong Python, SQL, and cloud data experience."
        self.required_experience_years = 4
        self.culture_signals = ["innovation"]


class StubSession:
    async def add(self, item):
        pass

    async def commit(self):
        pass


def test_ranking_agent_assigns_rank_and_scores():
    agent = RankingAgent()
    job = DummyJob()
    candidate = DummyCandidate()
    session = StubSession()

    rankings = asyncio.run(agent.rank_job(job, [candidate], session, limit=1))

    assert len(rankings) == 1
    ranking = rankings[0]
    assert ranking.rank == 1
    assert 0.0 <= ranking.final_score <= 1.0
    assert isinstance(ranking.hidden_gem_indicators, list)
    assert ranking.is_fraud_flagged is False
