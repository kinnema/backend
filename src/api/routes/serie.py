import asyncio
from csv import Error
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.core.redis import RedisProvider
from src.models import GetSerieResult
from src.providers import available_providers

router = APIRouter()

async def fetch_serie_from_providers(serie_name: str, season: int, episode: int) -> GetSerieResult:
    data = GetSerieResult(url=None, error=None)
    fromDatabase = RedisProvider.get(
        f"episode-watch:{serie_name}:{season}:{episode}", GetSerieResult
    )

    if fromDatabase is not None:
        data = GetSerieResult(url=fromDatabase.url, error=None)
        return data

    providers = available_providers.get_providers()
    tasks = [provider.get_dizi(serie_name, season, episode) for provider in providers]
    found_url = False

    for task in asyncio.as_completed(tasks):
        try:
            url = await asyncio.wait_for(task, timeout=5)
            if url:
                RedisProvider.set(
                    f"episode-watch:{serie_name}:{season}:{episode}", GetSerieResult(url=url, error=None)
                )
                data = GetSerieResult(url=url, error=None)
                found_url = True
                break
        except asyncio.TimeoutError:
            print(f"Provider {task} timed out.")
        except Exception as e:
            print(f"Error fetching from provider: {e}")

    if not found_url:
        return GetSerieResult(url=None, error='No URL found for the requested episode')
    
    return data


@router.get("/watch")
async def get_serie(serie_name: str, season: int, episode: int) -> GetSerieResult:
    serie_name = serie_name.lower()
    response = await fetch_serie_from_providers(serie_name, season, episode)
    
    return response