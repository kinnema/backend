from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_ASYNC_DATABASE_URI.__str__(), echo=True, future=True
)
