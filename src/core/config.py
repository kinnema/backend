from typing import Optional

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
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

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PASSWORD: str = "kinnema"
    POSTGRES_USER: str = "kinnema"
    POSTGRES_DB: str = "kinnema"
    POSTGRES_PORT: int = 5432

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = "key"

    CORS_ORIGINS: list[str] = ["*"]

    @computed_field  # type: ignore[misc]
    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_ASYNC_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
