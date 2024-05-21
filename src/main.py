from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.main import api_router
from src.core.config import settings

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
