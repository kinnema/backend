from fastapi import APIRouter

from src.core.browser import browser

router = APIRouter()


@router.post("/warmup")
async def warmup():
    if browser.browser.stopped:
        await browser.init_browser()

    return {"status": "ok"}
