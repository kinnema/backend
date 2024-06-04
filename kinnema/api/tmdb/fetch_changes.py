import aiohttp
from django.conf import settings

from .models import TmdbChangeResponse


async def fetch_last_changes() -> TmdbChangeResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.themoviedb.org/3/tv/changes",
            headers={"Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}"},
        ) as response:
            return TmdbChangeResponse(**await response.json())
