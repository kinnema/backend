import re
from asyncio import sleep
from typing import List, Optional

import aiohttp
from fastapi import HTTPException
from nodriver import Browser, Tab
from odmantic import AIOEngine
from redis import Redis

from src.api.deps import SessionDep
from src.core.browser import init_browser
from src.core.redis import REDIS_KEYS, RedisProvider
from src.models import GetHomeResults, GetSerieResult, HomeTrends, SerieBase, SerieWatch
from src.providers import AvailableProviders
from src.providers.dizipal.serie_page import DizipalSeriePage


class Dizipal:
    @classmethod
    def get_serie_page_instance(cls) -> DizipalSeriePage:
        """
        Create a DizipalSeriePage instance. This function is optimized for speed
        by using a class method instead of a static method.
        """

        return DizipalSeriePage()

    async def get_home(self) -> GetHomeResults:
        return (
            RedisProvider.get(
                REDIS_KEYS.HOME,
                GetHomeResults,
            )
            or await self._get_home()
        )

    async def collection(self, collection: str) -> List[SerieBase]:
        return await self.search(collection)

    async def search(self, query: str) -> List[SerieBase]:
        series: List[SerieBase] = []
        browser = await init_browser()

        page = await browser.get(f"https://dizipal736.com/diziler?kelime={query}")
        await page.wait_for(".type2")
        all_series = await page.query_selector_all(".type2 ul li a")

        for serie in all_series:
            _image = await page.query_selector("img", _node=serie)
            name = await page.query_selector(".detail .title", _node=serie)
            image = _image.attrs.get("src")  # type: ignore
            href = serie.attrs.get("href")

            dict = SerieBase(
                name=name.text,  # type: ignore
                image=image,  # type: ignore
                href=href,
            )

            series.append(dict)

        await page.close()

        return series

    async def get_dizi(self, dizi, sezon, bolum, session: AIOEngine) -> Optional[str]:
        fromDatabase = RedisProvider.get(
            f"episode-watch:{dizi}:{sezon}:{bolum}", GetSerieResult
        )

        if fromDatabase is not None:
            return fromDatabase.url

        url = await self._get_dizi(dizi, sezon, bolum)

        if url is None:
            raise HTTPException(status_code=404, detail="Serie not found")

        RedisProvider.set(
            f"episode-watch:{dizi}:{sezon}:{bolum}", GetSerieResult(url=url)
        )

        return url

    async def _get_dizi(self, dizi, sezon, bolum) -> Optional[str]:
        browser = await init_browser()
        url = f"https://dizipal736.com/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}"
        page = await browser.get(url)

        await page.wait_for(".user-menu")
        iframe = await page.query_selector("div#vast_new iframe")
        iframe_source = iframe.attrs.get("src")  # type: ignore

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                iframe_source,  # type: ignore
                headers={"Referer": url},
            )
            text = await response.text()
            x = re.findall(r"file:\"([^\"]+)", text)

            await session.close()
            await page.close()
            browser.stop()

            if len(x) > 0:
                url = x[0]

                return url

    async def _get_home(self) -> GetHomeResults:
        browser = await init_browser()
        page = await browser.get("https://dizipal736.com")
        await page.wait_for(".user-menu")

        trends = await self._fetch_home_trends(page)
        new_series = await self._fetch_home_new_series(page)
        last_episodes = await self._fetch_last_episodes(page)

        await page.close()

        results = GetHomeResults(
            trends=trends, new_series=new_series, last_episodes=last_episodes
        )

        RedisProvider.set(REDIS_KEYS.HOME, results)

        return results

    async def _fetch_home_trends(self, page: Tab) -> List[HomeTrends]:
        _trends = await page.query_selector_all(".trends li a")
        trends = []
        for trend in _trends:
            _image = await page.query_selector("img", _node=trend)
            trends.append(
                {
                    "image": _image.attrs.get("src"),  # type: ignore
                    "href": trend.attrs.get("href"),
                    "name": _image.attrs.get("alt"),  # type: ignore
                }
            )

        return trends

    async def _fetch_home_new_series(self, page: Tab) -> List[HomeTrends]:
        new_series = []
        _new_series_el = await page.query_selector_all(".movie-type-genres")
        _new_series = await page.query_selector_all("ul li a", _node=_new_series_el[1])

        for new_serie in _new_series:
            _image = await page.query_selector("img", _node=new_serie)
            new_series.append(
                {
                    "image": _image.attrs.src,  # type: ignore
                    "href": new_serie.attrs.get("href"),
                    "name": _image.attrs.get("alt"),  # type: ignore
                }
            )

        return new_series

    async def _fetch_last_episodes(self, page: Tab) -> List[SerieBase]:
        last_episodes: List[SerieBase] = []
        _last_episodes = await page.query_selector_all(".last-episodes .episode-item a")

        for episode in _last_episodes:
            _image = await page.query_selector("img", _node=episode)
            _name = await page.query_selector(".name", _node=episode)
            _episode = await page.query_selector(".episode", _node=episode)
            # _date = await page.query_selector(".date", _node=episode)

            last_episodes.append(
                SerieBase(
                    href=episode.attrs.get("href"),
                    image=_image.attrs.get("src"),  # type: ignore
                    name=f"{_name.text.strip()} - {_episode.text.strip()}",  # type: ignore
                    desc=_name.text.strip(),  # type: ignore
                )
            )

        return last_episodes
