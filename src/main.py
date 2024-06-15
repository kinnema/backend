from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.core.browser as browser
from src.api.main import api_router
from src.core.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    await browser.init_browser()


@app.on_event("shutdown")
async def shutdown():
    if browser.browser:
        browser.browser.stop()


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
