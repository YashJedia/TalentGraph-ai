"""Database configuration and session management"""

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, StaticPool
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

_is_sqlite = settings.DATABASE_URL.startswith("sqlite")


def _get_async_url(url: str) -> str:
    """Convert a sync DB URL to an async one."""
    if url.startswith("sqlite"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return url.replace("postgresql://", "postgresql+asyncpg://")


# Sync database engine
if _is_sqlite:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.DEBUG,
    )

# Async database engine
if _is_sqlite:
    async_engine = create_async_engine(
        _get_async_url(settings.DATABASE_URL),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG,
    )
else:
    async_engine = create_async_engine(
        _get_async_url(settings.DATABASE_URL),
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.DEBUG,
    )

# Session maker
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Declarative base for models
Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()


@event.listens_for(Engine, "connect")
def set_pragma(dbapi_conn, connection_record):
    """Enable foreign keys and optimizations"""
    if _is_sqlite:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    elif "postgresql" in settings.DATABASE_URL:
        cursor = dbapi_conn.cursor()
        cursor.execute("SET client_encoding TO 'utf8'")
        cursor.close()


async def init_db():
    """Initialize database"""
    async with async_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")


async def close_db():
    """Close database connection"""
    await async_engine.dispose()
    logger.info("Database connection closed")
