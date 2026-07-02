import pytest
from app.services.embeddings import get_embedding_service


def test_embedding_service_returns_fixed_dimension():
    service = get_embedding_service()
    embedding = service.embed("TalentGraph AI")

    assert isinstance(embedding, list)
    assert len(embedding) == service.dimension
    assert all(isinstance(value, float) for value in embedding)


def test_embedding_service_is_deterministic():
    service = get_embedding_service()
    embedding_a = service.embed("candidate matching")
    embedding_b = service.embed("candidate matching")

    assert embedding_a == embedding_b
