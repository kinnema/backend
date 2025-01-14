from abc import ABC, ABCMeta, abstractmethod
from enum import Enum
from typing import Awaitable, Optional


class Priority(str, Enum):
    LOW = (2,)
    MEDIUM = 1
    HIGH = 0


class BaseProvider(metaclass=ABCMeta):

    @property
    @abstractmethod
    def ENABLED(self) -> bool:
        return True
    
    @property
    @abstractmethod
    def NAME(self) -> str:
        pass

    @property
    @abstractmethod
    def PRIORITY(self) -> str:
        pass

    @property
    @abstractmethod
    def PROVIDER_URL(self) -> str:
        pass

    @abstractmethod
    def get_dizi(self, dizi: str, sezon: int, bolum: int) -> Awaitable[Optional[str]]:
        pass
