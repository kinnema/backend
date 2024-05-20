from typing import Union

from fastapi import APIRouter, HTTPException

from src.models import (
    GetHomeResults,
    GetSeriePage,
    GetSerieResult,
)
from src.providers.dizipal import Dizipal

router = APIRouter()


# @router.get("/collection/{collection}")
# async def collection(
#     collection: str,
#     provider: Union[str, None] = None,
# ) -> SerieResults:
#     if provider is None:
#         provider = "dizipal"

#     async def get_() -> Optional[List[SerieBase]]:
#         if provider == "dizipal":
#             dizipal = Dizipal(browser)
#             series = await dizipal.collection(collection)

#             return series

#         return None

#     collections = await get_()

#     if collections is None:
#         raise HTTPException(status_code=404, detail="Serie not found")

#     return SerieResults(results=collections)


@router.post("/search/{query}")
async def search(query: str, provider: Union[str, None] = None):
    if provider is None:
        provider = "dizipal"

    async def get_():
        if provider == "dizipal":
            dizipal = Dizipal()
            return await dizipal.search(query)

        return None

    url = await get_()
    return {"results": url}


@router.get("/watch/{dizi}/{sezon}/{bolum}")
async def get_serie(dizi: str, sezon: int, bolum: int) -> GetSerieResult:
    url = await Dizipal().get_dizi(dizi, sezon, bolum)

    if url is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return GetSerieResult(url=url)


@router.get("/home")
async def get_home() -> GetHomeResults:
    data = await Dizipal().get_home()

    return data


@router.get("/serie/{name}")
async def get_serie_page(name: str) -> GetSeriePage:
    data = await Dizipal.get_serie_page_instance().get_serie_page(name)

    return data
