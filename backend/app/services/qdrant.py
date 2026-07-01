"""Qdrant Vector Database Service"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.config.settings import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for Qdrant vector database operations"""

    _instance: "QdrantService" = None
    _client: Optional[QdrantClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
        return cls._instance

    def _ensure_client(self):
        if self._client is None:
            logger.info(f"Connecting to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            try:
                self._client = QdrantClient(
                    host=settings.QDRANT_HOST,
                    port=settings.QDRANT_PORT,
                    api_key=settings.QDRANT_API_KEY,
                )
                logger.info("✅ Connected to Qdrant")
                self._initialize_collections()
            except Exception as e:
                logger.error(f"❌ Failed to connect to Qdrant: {e}")
                raise

    def _initialize_collections(self):
        """Initialize required collections if they don't exist"""
        collections = [
            (settings.QDRANT_COLLECTION_JOBS, "Job embeddings"),
            (settings.QDRANT_COLLECTION_CANDIDATES, "Candidate embeddings"),
        ]

        for collection_name, description in collections:
            try:
                collections_response = self._client.get_collections()
                existing_names = [c.name for c in collections_response.collections]

                if collection_name not in existing_names:
                    logger.info(f"Creating collection: {collection_name}")
                    self._client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=settings.EMBEDDING_DIMENSION,
                            distance=Distance.COSINE,
                        ),
                    )
                    logger.info(f"✅ Collection created: {collection_name}")
            except Exception as e:
                logger.error(f"❌ Error initializing collection {collection_name}: {e}")
                raise

    def _point_id(self, point_id: str) -> str:
        return str(point_id)

    def add_vector(
        self,
        collection_name: str,
        point_id: str,
        vector: List[float],
        payload: Dict[str, Any],
    ):
        """Add a single vector to collection"""
        try:
            self._ensure_client()
            point = PointStruct(id=self._point_id(point_id), vector=vector, payload=payload)
            self._client.upsert(
                collection_name=collection_name,
                points=[point],
            )
            logger.debug(f"✅ Vector added to {collection_name}: {point_id}")
        except Exception as e:
            logger.error(f"❌ Error adding vector: {e}")
            raise

    def add_vectors(
        self,
        collection_name: str,
        point_ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ):
        """Add multiple vectors to collection"""
        try:
            self._ensure_client()
            points = [
                PointStruct(
                    id=self._point_id(pid),
                    vector=vector,
                    payload=payload,
                )
                for pid, vector, payload in zip(point_ids, vectors, payloads)
            ]
            self._client.upsert(
                collection_name=collection_name,
                points=points,
            )
            logger.info(f"✅ {len(points)} vectors added to {collection_name}")
        except Exception as e:
            logger.error(f"❌ Error adding vectors: {e}")
            raise

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            self._ensure_client()
            results = self._client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )

            search_results = []
            for result in results:
                search_results.append(
                    {
                        "id": result.id,
                        "score": result.score,
                        "payload": result.payload,
                    }
                )

            logger.debug(f"✅ Search completed in {collection_name}: {len(results)} results")
            return search_results

        except Exception as e:
            logger.error(f"❌ Error searching vectors: {e}")
            raise

    def delete_vector(self, collection_name: str, point_id: str):
        """Delete a vector from collection"""
        try:
            self._ensure_client()
            self._client.delete(
                collection_name=collection_name,
                points_selector=[self._point_id(point_id)],
            )
            logger.debug(f"✅ Vector deleted from {collection_name}: {point_id}")
        except Exception as e:
            logger.error(f"❌ Error deleting vector: {e}")
            raise

    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get collection information"""
        try:
            self._ensure_client()
            info = self._client.get_collection(collection_name)
            return {
                "name": info.name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
            }
        except Exception as e:
            logger.error(f"❌ Error getting collection info: {e}")
            raise


def get_qdrant_service() -> QdrantService:
    return QdrantService()
