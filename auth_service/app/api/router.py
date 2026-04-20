from fastapi import APIRouter
from app.api.routes_auth import router as auth_router

# сборка роутеров
def create_api_router():
    api_router = APIRouter()
    api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
    
    return api_router
