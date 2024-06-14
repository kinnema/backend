from typing import Dict, List, Optional

from odmantic import Model
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class SerieWatch(Model):
    serie: str
    season: int
    episode: int
    watch_url: str


class SerieBase(BaseModel):
    name: str
    desc: str
    image: str
    href: str
    video_url: Optional[str] = None


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


class SeriePageEpisode(BaseModel):
    episodes: Dict[int, List[SerieBase]]


class GetSeriePage(BaseModel):
    episodes: SeriePageEpisode
    seasons: List[str]
    metadata: SerieMetadata


class SeriePageModel(Model):
    episodes: SeriePageEpisode
    seasons: List[str]
    metadata: SerieMetadata

class TokenPayload(SQLModel):
    sub: int | None = None
