from datetime import datetime, timezone

import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.main import api_router
from src.core.browser import browser
from src.core.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    await browser.init_browser()


@app.on_event("shutdown")
async def shutdown():
    if browser.browser:
        browser.stop_browser()


@app.middleware("http")
async def last_request_expire(request: fastapi.Request, call_next):
    last_request = datetime.now(tz=timezone.utc)
    browser.set_last_request(last_request)

    if not browser.last_request_thread.is_alive():
        browser.start_background_task()

    response = await call_next(request)

    return response


@app.middleware("http")
async def check_browser(request: fastapi.Request, call_next):
    if browser.browser.stopped:
        print("create_browser")
        await browser.init_browser()

    response = await call_next(request)

    return response


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
