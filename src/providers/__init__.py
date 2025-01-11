from src.providers.base import Priority, BaseProvider
from src.providers.dizipal.dizipal import Dizipal
from src.providers.hdfilmcehennemi3.hdfilmcehennemi import HdFilmCehennemiProvider


class AvailableProviders:
    @property
    def providers(self) -> list[BaseProvider]:
        return [Dizipal(), HdFilmCehennemiProvider()]

    def get_providers(self) -> list[BaseProvider]:
        sorted_providers = sorted(self.providers, key=lambda x: x.PRIORITY)

        return sorted_providers


available_providers = AvailableProviders()
