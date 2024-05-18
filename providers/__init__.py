from enum import Enum
from nodriver import Browser


class Provider:
    def __init__(self, browser: Browser, provider: str):
        self.browser = browser
        self.provider = provider

class AvailableProviders(Enum):
    DIZIPAL = "dizipal"