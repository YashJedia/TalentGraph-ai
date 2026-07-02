from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database import Candidate


class BM25SearchService:
    """BM25 ranking algorithm for keyword-based retrieval."""

    def __init__(self):
        self.bm25_model: BM25Okapi = None
        self.candidates_corpus: List[Candidate] = []

    def _candidate_to_text(self, candidate: Candidate) -> str:
        """Convert candidate profile to searchable text."""
        lines = [
            candidate.anonymized_name or "",
            candidate.headline or "",
            candidate.summary or "",
            candidate.current_title or "",
            candidate.current_company or "",
            candidate.location or "",
            candidate.country or "",
            candidate.current_industry or "",
        ]

        for skill in candidate.skills or []:
            lines.append(skill.skill_name or "")

        for entry in candidate.career_history or []:
            lines.extend(
                [
                    entry.title or "",
                    entry.company or "",
                    entry.industry or "",
                    entry.description or "",
                ]
            )

        for entry in candidate.education or []:
            lines.extend(
                [
                    entry.institution or "",
                    entry.degree or "",
                    entry.field_of_study or "",
                ]
            )

        return " ".join([line for line in lines if line])

    async def build_index(self, session: AsyncSession, candidates: List[Candidate]) -> None:
        """Build BM25 index from candidates."""
        self.candidates_corpus = candidates
        corpus_texts = [self._candidate_to_text(candidate) for candidate in candidates]
        tokenized_corpus = [text.lower().split() for text in corpus_texts]
        self.bm25_model = BM25Okapi(tokenized_corpus)

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search candidates using BM25."""
        if not self.bm25_model or not self.candidates_corpus:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25_model.get_scores(tokenized_query)

        scored_candidates = [
            {"candidate": candidate, "score": float(score)} for candidate, score in zip(self.candidates_corpus, scores)
        ]

        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        return scored_candidates[:limit]


def get_bm25_service() -> BM25SearchService:
    """Singleton BM25 service."""
    if not hasattr(get_bm25_service, "_instance"):
        get_bm25_service._instance = BM25SearchService()
    return get_bm25_service._instance
