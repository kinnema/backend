from fastapi import APIRouter


from src.core.browser import browser

router = APIRouter()


@router.get("/warmup")
async def warmup():
    if browser.browser.stopped:
        await browser.init_browser()

    return {"status": "ok"}
