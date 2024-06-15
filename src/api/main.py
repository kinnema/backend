from fastapi import APIRouter

from src.api.routes import app, auth, serie, user

api_router = APIRouter()
api_router.include_router(app.router, tags=["app"], prefix="/app")
api_router.include_router(serie.router, tags=["serie"])
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(user.router, tags=["user"], prefix="/user")
