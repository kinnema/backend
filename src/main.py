
from fastapi import FastAPI
from src.api.main import api_router
from src.core.database import init_db


app = FastAPI()

init_db()
app.include_router(api_router)