import re
from typing import Optional

import aiohttp
from fastapi import HTTPException

from src.core.browser import browser
from src.core.config import settings
from src.core.redis import RedisProvider
from src.models import GetSerieResult


class Dizipal:
    async def get_dizi(
        self,
        dizi,
        sezon,
        bolum,
    ) -> Optional[str]:
        fromDatabase = RedisProvider.get(
            f"episode-watch:{dizi}:{sezon}:{bolum}", GetSerieResult
        )

        if fromDatabase is not None:
            return fromDatabase.url

        url = await self._get_dizi(dizi, sezon, bolum)

        if url is None:
            raise HTTPException(status_code=404, detail="Serie not found")

        RedisProvider.set(
            f"episode-watch:{dizi}:{sezon}:{bolum}", GetSerieResult(url=url)
        )

        return url

    async def _get_dizi(self, dizi, sezon, bolum) -> Optional[str]:
        try:
            url = f"{settings.PROVIDER_URL}/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}"
            page = await browser.browser.get(url, True)

            await page.wait_for(".container")
            iframe = await page.query_selector("div#vast_new iframe")
            iframe_source = iframe.attrs.get("src")  # type: ignore

            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    iframe_source,  # type: ignore
                    headers={"Referer": url},
                )
                text = await response.text()
                x = re.findall(r"file:\"([^\"]+)", text)

                await session.close()
                await page.close()

                if len(x) > 0:
                    url = x[0]

                    return url
        except Exception:
            await page.close()
