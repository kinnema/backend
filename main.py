import asyncio
import nodriver as uc
import re
from typing import Union
from fastapi import FastAPI

from models import GetSerieResult, SerieResults
from providers.dizipal import Dizipal

app = FastAPI()


@app.get("/collection/{collection}")
async def collection(collection: str, provider: Union[str, None] = None) -> SerieResults:
    browser = await uc.start()
    if provider is None:
        provider = "dizipal"


    async def get_():
        if provider == "dizipal":
            dizipal = Dizipal(browser)
            return await dizipal.collection(collection)

        return None

    url = await get_()
    return {"results": url}

@app.get("/search/{query}")
async def search(query: str, provider: Union[str, None] = None):
    browser = await uc.start()
    if provider is None:
        provider = "dizipal"


    async def get_():
        if provider == "dizipal":
            dizipal = Dizipal(browser)
            return await dizipal.search(query)

        return None

    url = await get_()
    return {"results": url}



@app.get("/dizi/{dizi}/{sezon}/{bolum}")
async def get_serie(dizi: str, sezon: int, bolum: int, provider: Union[str, None] = None) -> GetSerieResult:
    browser = await uc.start()

    if provider is None:
        provider = "dizipal"

    
    async def get_():
        if provider == "dizipal":
            dizipal = Dizipal(browser)
            return await dizipal.get_dizi(dizi, sezon, bolum)

        return None


    url = await get_()
    return {"url": url}
