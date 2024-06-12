import json
from enum import Enum
from typing import Optional, Type

import redis
from pydantic import BaseModel
from typing_extensions import TypeVar

from src.core.config import settings

redisClient = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB or 0,
    password=settings.REDIS_PASSWORD,
    username=settings.REDIS_USER,
    decode_responses=True,
)


class REDIS_KEYS(Enum):
    HOME = "home"
    SERIE = "serie:{serie}"


T = TypeVar("T")


class RedisProvider:
    @staticmethod
    def get(key: REDIS_KEYS | str, model: Type[T]) -> Optional[T]:
        cached = redisClient.get((key.value if isinstance(key, REDIS_KEYS) else key))

        if cached is None:
            return None

        return model(**json.loads(cached))  # type: ignore

    @staticmethod
    def set(key: REDIS_KEYS | str, value: BaseModel, expire: int = 60 * 60 * 24):
        k = key.value if isinstance(key, REDIS_KEYS) else key
        redisClient.set(k, value.model_dump_json())

        if expire:
            redisClient.expire(k, expire)
