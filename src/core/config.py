from typing import Optional

from pydantic import (
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: Optional[int] = 0
    REDIS_PASSWORD: Optional[str] = ""
    REDIS_USER: Optional[str] = ""

    MONGODB_URL: str = "mongodb://root:example@db:27017"

    CORS_ORIGINS: list[str]

    @computed_field  # type: ignore[misc]
    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()  # type: ignore
