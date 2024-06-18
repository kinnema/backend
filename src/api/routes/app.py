from fastapi import APIRouter

from src.core.browser import browser
from src.core.config import settings

router = APIRouter()


@router.post("/warmup")
async def warmup():
    if browser.browser.stopped:
        await browser.init_browser()
        page = await browser.browser.get(settings.PROVIDER_URL, True)

        await page.wait_for(".container")
        await page.close()

    return {"status": "ok"}
