from typing import Annotated

from fastapi import Depends
from odmantic import AIOEngine

from src.core.database import mongoEngine


def get_db() -> AIOEngine:
    return mongoEngine


SessionDep = Annotated[AIOEngine, Depends(get_db)]
