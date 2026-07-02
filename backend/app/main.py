"""FastAPI application initialization"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config.settings import settings
from app.db.session import init_db, close_db

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("🚀 Starting TalentGraph AI Backend")
    await init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down TalentGraph AI Backend")
    await close_db()


def create_app() -> FastAPI:
    """Create FastAPI application"""

    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # Register Phase 2 API routes
    from app.api.v1 import api_router
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.API_VERSION,
            "environment": settings.FASTAPI_ENV,
        }

    logger.info("✅ FastAPI application created successfully")
    return app


# Create the application
app = create_app()
