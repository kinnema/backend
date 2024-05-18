from typing import List, Optional, TypedDict

class Serie(TypedDict):
    name: str
    image: str
    href: str
    provider: Optional[str]


class SerieResults(TypedDict):
    results: List[Serie]

class GetSerieResult(TypedDict):
    url: str