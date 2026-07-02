from typing import List, Dict, Any, Optional
from app.models.database import Candidate
from app.services.embeddings import get_embedding_service
from app.services.bm25_search import get_bm25_service
from app.config.settings import settings


class HybridSearchService:
    """Hybrid search combining BM25 (keyword) and embedding (semantic) retrieval."""

    async def search(
        self,
        query: str,
        candidates: List[Candidate],
        limit: int = 10,
        embedding_weight: Optional[float] = None,
        bm25_weight: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search on candidates.

        :param query: Search query string
        :param candidates: List of candidates to search
        :param limit: Max results to return
        :param embedding_weight: Weight for embedding similarity (default: settings.WEIGHT_EMBEDDING_SIMILARITY)
        :param bm25_weight: Weight for BM25 score (default: settings.WEIGHT_BM25)
        :return: List of candidates with hybrid scores, sorted by relevance
        """
        if not embedding_weight:
            embedding_weight = settings.WEIGHT_EMBEDDING_SIMILARITY
        if not bm25_weight:
            bm25_weight = settings.WEIGHT_BM25

        embedding_service = get_embedding_service()
        bm25_service = get_bm25_service()

        # Build BM25 index if needed
        if not bm25_service.bm25_model or not bm25_service.candidates_corpus:
            await bm25_service.build_index(None, candidates)

        # Get BM25 scores
        bm25_results = await bm25_service.search(query, limit=len(candidates))
        bm25_scores = {result["candidate"].id: result["score"] for result in bm25_results}

        # Normalize BM25 scores to 0-1 range
        max_bm25_score = max(bm25_scores.values()) if bm25_scores else 1.0
        bm25_normalized = {
            cid: score / max(max_bm25_score, 1.0) for cid, score in bm25_scores.items()
        }

        # Get embedding similarity scores
        query_embedding = embedding_service.embed(query)
        embedding_scores = {}
        for candidate in candidates:
            if candidate.profile_embedding:
                similarity = embedding_service.similarity(query_embedding, candidate.profile_embedding)
                embedding_scores[candidate.id] = float(similarity)
            else:
                embedding_scores[candidate.id] = 0.0

        # Combine scores with weights
        hybrid_results = []
        for candidate in candidates:
            bm25_score = bm25_normalized.get(candidate.id, 0.0)
            embedding_score = embedding_scores.get(candidate.id, 0.0)

            hybrid_score = (embedding_weight * embedding_score) + (bm25_weight * bm25_score)

            hybrid_results.append(
                {
                    "candidate": candidate,
                    "hybrid_score": round(hybrid_score, 3),
                    "embedding_score": round(embedding_score, 3),
                    "bm25_score": round(bm25_score, 3),
                }
            )

        # Sort by hybrid score
        hybrid_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return hybrid_results[:limit]


def get_hybrid_search_service() -> HybridSearchService:
    """Singleton hybrid search service."""
    if not hasattr(get_hybrid_search_service, "_instance"):
        get_hybrid_search_service._instance = HybridSearchService()
    return get_hybrid_search_service._instance
