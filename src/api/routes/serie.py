import asyncio
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.core.redis import RedisProvider
from src.models import GetSerieResult
from src.providers import available_providers

router = APIRouter()

async def fetch_serie_from_providers(serie_name: str, season: int, episode: int):
    fromDatabase = RedisProvider.get(
        f"episode-watch:{serie_name}:{season}:{episode}", GetSerieResult
    )

    if fromDatabase is not None:
        data = json.dumps({'url': fromDatabase.url})
        yield f"{data}\n"
        return

    providers = available_providers.get_providers()
    tasks = [provider.get_dizi(serie_name, season, episode) for provider in providers]
    found_url = False

    for task in asyncio.as_completed(tasks):
        try:
            url = await asyncio.wait_for(task, timeout=5)
            if url:
                RedisProvider.set(
                    f"episode-watch:{serie_name}:{season}:{episode}", GetSerieResult(url=url)
                )
                data = json.dumps({'url': url})
                yield f"{data}\n"
                found_url = True
                break
        except asyncio.TimeoutError:
            print(f"Provider {task} timed out.")
        except Exception as e:
            print(f"Error fetching from provider: {e}")

    if not found_url:
        yield f"{json.dumps({'error': 'No URL found for the requested episode'})}\n"


@router.get("/watch")
async def get_serie(serie_name: str, season: int, episode: int):
    serie_name = serie_name.lower()
    return StreamingResponse(
        content=fetch_serie_from_providers(serie_name, season, episode),
        media_type="application/json"
    )