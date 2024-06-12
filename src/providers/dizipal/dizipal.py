import re
from typing import Optional

import bs4
from fastapi import HTTPException

from src.core.config import settings
from src.core.http import get_html
from src.core.redis import RedisProvider
from src.models import GetSerieResult


class Dizipal:
    async def get_dizi(self, dizi, sezon, bolum) -> Optional[str]:
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
        url = f"https://webcache.googleusercontent.com/search?q=cache:{settings.DIZIPAL_URL}/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}"
        r = await get_html(url)

        soup = bs4.BeautifulSoup(r, "html.parser")

        iframe_src: Optional[str] = soup.select_one("#vast_new iframe").get("src")  # type: ignore

        if iframe_src is not None:
            iframe_html = await get_html(iframe_src)
            x = re.findall(r"file:\"([^\"]+)", iframe_html)
            url = x[0]

            return url

        raise HTTPException(status_code=404, detail="Serie not found")
