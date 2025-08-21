from fastapi import APIRouter

from app.api.api_v1.endpoints import regions

api_router = APIRouter()

# Include region endpoints
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
