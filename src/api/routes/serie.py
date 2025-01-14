from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from starlette.responses import PlainTextResponse

from src.providers import available_providers

router = APIRouter()


async def fetch_serie_from_providers(serie_name: str, season: int, episode: int):
    providers = available_providers.get_providers()

    
    print(providers)
    for provider in providers:
        url = await provider.get_dizi(serie_name, season, episode)

        if url:
            yield f"{url}\n\n"
            # break


@router.get("/watch")
async def get_serie(serie_name: str, season: int, episode: int):
    return EventSourceResponse(
        content=fetch_serie_from_providers(serie_name, season, episode),
    )