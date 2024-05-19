from typing import Annotated, Generator

from fastapi import Depends
from nodriver import Browser
from sqlmodel import Session

from src.core.browser import init_browser
from src.core.database import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


async def get_browser() -> Browser:
    return await init_browser()


SessionDep = Annotated[Session, Depends(get_db)]
BrowserDep = Annotated[Browser, Depends(get_browser)]
