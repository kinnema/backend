from src.providers.base import Priority, BaseProvider
from src.providers.dizipal.dizipal import Dizipal
from src.providers.dizipalv1 import DizipalV1Provider
from src.providers.hdfilmcehennemi3.hdfilmcehennemi import HdFilmCehennemiProvider


class AvailableProviders:
    @property
    def providers(self) -> list[BaseProvider]:
        return [Dizipal(), HdFilmCehennemiProvider(), DizipalV1Provider()]

    def get_providers(self) -> list[BaseProvider]:
        filtered_providers = filter(lambda x:x.ENABLED, self.providers)
        sorted_providers = sorted(filtered_providers, key=lambda x: x.PRIORITY)

        return sorted_providers


available_providers = AvailableProviders()
