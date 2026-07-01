"""Embedding service using a lightweight deterministic vectorizer."""

import hashlib
import logging
from typing import List, Union

import numpy as np
from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating deterministic embeddings."""

    _instance: "EmbeddingService" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.dimension = settings.EMBEDDING_DIMENSION
        logger.info(
            f"Initializing lightweight embedding service: {settings.EMBEDDING_MODEL}"
        )
        self._initialized = True

    def _normalize_text(self, text: str) -> str:
        return (text or "").strip().lower()

    def _text_to_vector(self, text: str) -> np.ndarray:
        if not text:
            return np.zeros(self.dimension, dtype=np.float32)

        normalized_text = self._normalize_text(text)
        digest = hashlib.sha256(normalized_text.encode("utf-8")).digest()
        values = np.frombuffer(digest, dtype=np.uint8).astype(np.float32)
        values = values / 255.0

        if values.shape[0] >= self.dimension:
            result = values[: self.dimension]
        else:
            result = np.tile(values, int(np.ceil(self.dimension / values.shape[0])))[: self.dimension]

        return result.astype(np.float32)

    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for text(s)."""
        if isinstance(text, str):
            return self._text_to_vector(text).tolist()

        return [self._text_to_vector(item).tolist() for item in text]

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        return [self._text_to_vector(text).tolist() for text in texts]

    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        try:
            emb1 = np.array(embedding1, dtype=np.float32)
            emb2 = np.array(embedding2, dtype=np.float32)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            if norm1 == 0.0 or norm2 == 0.0:
                return 0.0
            return float(np.dot(emb1, emb2) / (norm1 * norm2))
        except Exception as e:
            logger.error(f"❌ Error calculating similarity: {e}")
            return 0.0


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
