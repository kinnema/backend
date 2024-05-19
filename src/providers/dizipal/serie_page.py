import re
from typing import List

from nodriver import Browser, Tab

from src.core.redis import REDIS_KEYS, RedisProvider
from src.models import GetSeriePage, SerieBase, SerieMetadata
from src.providers import AvailableProviders


class DizipalSeriePage:
    def __init__(self, browser: Browser):
        self.browser = browser

    async def get_serie_page(self, serie: str) -> GetSeriePage:
        print(REDIS_KEYS.SERIE.value.format(serie=serie))
        return RedisProvider.get(
            REDIS_KEYS.SERIE.value.format(serie=serie), GetSeriePage
        ) or await self._get_serie_page(serie)

    async def _get_metadata(self, page: Tab) -> SerieMetadata:
        _name = await page.query_selector(".cover h5")
        _desc = await page.query_selector(".summary p")
        _image_el = await page.query_selector(".cover")
        _image = _image_el.attrs.get("style")  # type: ignore
        _image_regex = re.search(r"url\((.*?)\)", _image)  # type: ignore

        image = _image_regex.group(1) if _image_regex else ""
        desc = _desc.text.strip()  # type: ignore
        name = _name.text.strip()  # type: ignore

        return SerieMetadata(name=name, desc=desc, image=image)

    async def _get_seasons(self, page: Tab) -> List[str]:
        _seasons = await page.query_selector_all(".season-selectbox select option")
        seasons: List[str] = []

        for season in _seasons:
            seasons.append(season.attrs.get("value"))

        return seasons

    async def _get_episodes(self, page: Tab, serie: str) -> List[SerieBase]:
        _episodes = await page.query_selector_all(".episodes .episode-item a")
        episodes: List[SerieBase] = []

        for episode in _episodes:
            _image = await page.query_selector("img", _node=episode)
            _date = await page.query_selector(".date", _node=episode)
            _episode = await page.query_selector(".episode", _node=episode)

            dict = SerieBase(
                href=episode.attrs.get("href"),
                image=_image.attrs.get("src"),  # type: ignore
                name=f"{_episode.text.strip()} - {_date.text.strip()}",  # type: ignore
                provider=AvailableProviders.DIZIPAL,
            )

            episodes.append(dict)

        return episodes

    async def _get_serie_page(self, serie: str) -> GetSeriePage:
        page = await self.browser.get(f"https://dizipal735.com/dizi/{serie}")
        await page.wait_for(".user-menu")

        episodes = await self._get_episodes(page, serie)
        seasons = await self._get_seasons(page)
        metadata = await self._get_metadata(page)

        await page.close()

        data = GetSeriePage(episodes=episodes, seasons=seasons, metadata=metadata)

        RedisProvider.set(REDIS_KEYS.SERIE.value.format(serie=serie), data)

        return data
