from pydantic import BaseModel
from sqlmodel import SQLModel


class GetSerieResult(BaseModel):
    url: str


class TokenPayload(SQLModel):
    sub: int | None = None
