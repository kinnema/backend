from fastapi import APIRouter
from src.api.routes import serie



api_router = APIRouter()
api_router.include_router(serie.router, tags=["serie"])