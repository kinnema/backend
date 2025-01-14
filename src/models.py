from pydantic import BaseModel
from sqlmodel import SQLModel

from src.schemas import LastWachedBase


class GetSerieResult(BaseModel):
    url: str


class TokenPayload(SQLModel):
    sub: int | None = None


class LastWatchedCreate(LastWachedBase):
    pass
