from fastapi import APIRouter, HTTPException

from src.models import GetSerieResult
from src.providers.dizipal.dizipal import Dizipal

router = APIRouter()


@router.get("/watch/{dizi}/{sezon}/{bolum}")
async def get_serie(dizi: str, sezon: int, bolum: int) -> GetSerieResult:
    url = await Dizipal().get_dizi(dizi, sezon, bolum)

    if url is None:
        raise HTTPException(status_code=404, detail="Serie not found")

    return GetSerieResult(url=url)
