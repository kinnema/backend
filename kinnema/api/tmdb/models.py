from dataclasses import dataclass
from typing import Optional, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TmdbChangeResults:
    id: int
    adult: Optional[bool] = None


@dataclass_json
@dataclass
class TmdbChangeResponse:
    results: List[TmdbChangeResults]
    page: int
    totalpages: int
    totalresults: int
