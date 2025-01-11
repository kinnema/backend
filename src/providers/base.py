from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = (2,)
    MEDIUM = 1
    HIGH = 0


class BaseProvider(ABC):

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
    def get_dizi(self, dizi: str, sezon: int, bolum: int) -> Optional[str]:
        pass
