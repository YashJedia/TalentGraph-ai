from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application configuration"""

    # FastAPI
    FASTAPI_ENV: str = os.getenv("FASTAPI_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    API_TITLE: str = "TalentGraph AI"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Explainable Multi-Agent Candidate Intelligence Platform"
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/talentgraph_ai"
    )
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "0"))

    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_JOBS: str = "jobs_embeddings"
    QDRANT_COLLECTION_CANDIDATES: str = "candidates_embeddings"

    # AI Models
    PRIMARY_AI_PROVIDER: str = os.getenv("PRIMARY_AI_PROVIDER", "gemini")  # gemini or openai
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Embeddings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/talentgraph.log")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"

    # Batch Processing
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "32"))
    PROCESSING_TIMEOUT: int = int(os.getenv("PROCESSING_TIMEOUT", "300"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))

    # Scoring Weights (Ranking Agent)
    WEIGHT_SEMANTIC_MATCH: float = 0.35
    WEIGHT_EXPERIENCE_MATCH: float = 0.20
    WEIGHT_BEHAVIORAL_SCORE: float = 0.15
    WEIGHT_CAREER_GROWTH: float = 0.10
    WEIGHT_LEADERSHIP: float = 0.10
    WEIGHT_CULTURE_FIT: float = 0.10

    # Fraud Detection Thresholds
    FRAUD_RISK_THRESHOLD: float = 0.7
    ANOMALY_THRESHOLD: float = 0.5

    # Hybrid Retrieval Weights
    WEIGHT_EMBEDDING_SIMILARITY: float = 0.5
    WEIGHT_BM25: float = 0.5

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
