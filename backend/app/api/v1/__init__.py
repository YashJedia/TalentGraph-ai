from fastapi import APIRouter

from app.api.v1.jobs import router as jobs_router
from app.api.v1.candidates import router as candidates_router
from app.api.v1.rankings import router as rankings_router
from app.api.v1.search import router as search_router
from app.api.v1.fraud import router as fraud_router
from app.api.v1.comparison import router as comparison_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.imports import router as imports_router
from app.api.v1.monitoring import router as monitoring_router

api_router = APIRouter()
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(candidates_router, prefix="/candidates", tags=["candidates"])
api_router.include_router(rankings_router, prefix="/rankings", tags=["rankings"])
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(fraud_router, prefix="/fraud", tags=["fraud"])
api_router.include_router(comparison_router, prefix="", tags=["comparison"])
api_router.include_router(copilot_router, prefix="/copilot", tags=["copilot"])
api_router.include_router(imports_router, prefix="", tags=["imports"])
api_router.include_router(monitoring_router, prefix="", tags=["monitoring"])
