from fastapi import APIRouter

from src.api.routes import auth, serie

api_router = APIRouter()
api_router.include_router(serie.router, tags=["serie"])
api_router.include_router(auth.router, tags=["auth"],prefix="/auth")