from typing import List, Optional, Union

import nodriver as uc
from fastapi import APIRouter, HTTPException

from src import crud
from src.deps import BrowserDep, SessionDep
from src.models import (
    GetHomeResults,
    GetSeriePage,
    GetSerieResult,
    SerieBase,
    SerieCreate,
    SerieResults,
)
from src.providers.dizipal import Dizipal

router = APIRouter()


@router.get("/collection/{collection}")
async def collection(
    collection: str,
    session: SessionDep,
    browser: BrowserDep,
    provider: Union[str, None] = None,
) -> SerieResults:
    if provider is None:
        provider = "dizipal"

    async def get_() -> Optional[List[SerieBase]]:
        if provider == "dizipal":
            dizipal = Dizipal(browser)
            series = await dizipal.collection(collection)

            for serie in series:
                create_serie = SerieCreate(**serie, collection=collection)  # type: ignore
                crud.create_serie(session=session, serie=create_serie)  # type: ignore

            return series

        return None

    collections = await get_()

    if collections is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return SerieResults(results=collections)


@router.post("/search/{query}")
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


@router.get("/watch/{dizi}/{sezon}/{bolum}")
async def get_serie(
    dizi: str, sezon: int, bolum: int, provider: Union[str, None] = None
) -> GetSerieResult:
    browser = await uc.start()

    if provider is None:
        provider = "dizipal"

    async def get_() -> Optional[str]:
        if provider == "dizipal":
            dizipal = Dizipal(browser)
            return await dizipal.get_dizi(dizi, sezon, bolum)

        return None

    url = await get_()

    if url is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return GetSerieResult(url=url)


@router.get("/home")
async def get_home(browser: BrowserDep) -> GetHomeResults:
    data = await Dizipal(browser).get_home()

    return data


@router.get("/serie/{name}")
async def get_serie_page(name: str, browser: BrowserDep) -> GetSeriePage:
    data = await Dizipal.get_serie_page_instance(browser).get_serie_page(name)

    return data
