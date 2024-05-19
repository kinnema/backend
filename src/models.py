from typing import List

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.providers import AvailableProviders


class SerieBase(SQLModel):
    name: str
    image: str
    href: str
    provider: AvailableProviders


class SerieCreate(SerieBase):
    pass


class Serie(SerieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    collection: str


class SerieResults(BaseModel):
    results: List[SerieBase]


class GetSerieResult(BaseModel):
    url: str


class HomeTrends(BaseModel):
    image: str
    href: str
    name: str


class GetHomeResults(BaseModel):
    trends: List[HomeTrends]
    new_series: List[HomeTrends]
    last_episodes: List[SerieBase]


class SerieMetadata(BaseModel):
    name: str
    desc: str
    image: str


class GetSeriePage(BaseModel):
    episodes: List[SerieBase]
    seasons: List[str]
    metadata: SerieMetadata
