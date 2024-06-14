import re
from typing import Dict, List

from nodriver import Tab

from src.core.browser import init_browser
from src.core.redis import REDIS_KEYS, RedisProvider
from src.models import GetSeriePage, SerieBase, SerieMetadata, SeriePageEpisode


class DizipalSeriePage:
    async def get_serie_page(self, serie: str) -> GetSeriePage:
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

    async def _get_episodes(
        self, page: Tab, metadata: SerieMetadata, seasons: List[str]
    ) -> SeriePageEpisode:
        _seasons = await page.query_selector_all(".last-episodes .episodes")
        _season_episodes: Dict[int, List[SerieBase]] = {}
        season_num = 0

        for season in _seasons:
            season_num += 1
            _episodes = await page.query_selector_all(".episode-item a", _node=season)
            _season_episodes[season_num] = []
            for episode in _episodes:
                _episode = await page.query_selector(".episode", _node=episode)
                _image = await page.query_selector("img", _node=episode)
                _date = await page.query_selector(".date", _node=episode)
                dict = SerieBase(
                    href=episode.attrs.get("href"),
                    image=_image.attrs.get("src"),  # type: ignore
                    name=f"{_episode.text.strip()} - {_date.text.strip()}",  # type: ignore
                    desc="metadata.desc",
                    video_url="",
                )

                _season_episodes[season_num].append(dict)

        return SeriePageEpisode(episodes=_season_episodes)

    async def _get_serie_page(self, serie: str) -> GetSeriePage:
        browser = await init_browser()
        page = await browser.get(f"https://dizipal736.com/dizi/{serie}")
        await page.wait_for(".user-menu")

        metadata = await self._get_metadata(page)
        seasons = await self._get_seasons(page)
        episodes = await self._get_episodes(page, metadata, seasons)

        await page.close()

        data = GetSeriePage(episodes=episodes, seasons=seasons, metadata=metadata)

        RedisProvider.set(REDIS_KEYS.SERIE.value.format(serie=serie), data)

        return data
