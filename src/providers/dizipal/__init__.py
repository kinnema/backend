import re
from typing import List, Optional

from nodriver import Browser, Tab

from src.core.redis import REDIS_KEYS, RedisProvider
from src.models import GetHomeResults, HomeTrends, SerieBase
from src.providers import AvailableProviders
from src.providers.dizipal.serie_page import DizipalSeriePage


class Dizipal:
    @classmethod
    def get_serie_page_instance(cls, browser: Browser) -> DizipalSeriePage:
        """
        Create a DizipalSeriePage instance. This function is optimized for speed
        by using a class method instead of a static method.
        """

        print(type(browser))
        return DizipalSeriePage(browser)

    def __init__(self, browser: Browser):
        self.browser = browser

    async def get_home(self) -> GetHomeResults:
        return (
            RedisProvider.get(
                REDIS_KEYS.HOME,
            )
            or await self._get_home()
        )

    async def collection(self, collection: str) -> List[SerieBase]:
        return await self.search(collection)

    async def search(self, query: str) -> List[SerieBase]:
        series: List[SerieBase] = []
        page = await self.browser.get(f"https://dizipal735.com/diziler?kelime={query}")
        await page.wait_for(".type2")
        all_series = await page.query_selector_all(".type2 ul li a")

        for serie in all_series:
            _image = await page.query_selector("img", _node=serie)
            name = await page.query_selector(".detail .title", _node=serie)
            provider = AvailableProviders.DIZIPAL
            image = _image.attrs.get("src")  # type: ignore
            href = serie.attrs.get("href")

            dict = SerieBase(
                name=name.text,  # type: ignore
                image=image,  # type: ignore
                provider=provider,
                href=href,
            )

            series.append(dict)

        await page.close()

        return series

    async def get_dizi(self, dizi, sezon, bolum) -> Optional[str]:
        self.dizi = dizi
        self.sezon = sezon
        self.bolum = bolum

        page = await self.browser.get(
            f"https://dizipal735.com/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}"
        )
        await page.wait_for(".user-menu")
        iframe = await page.query_selector("div#vast_new iframe")
        iframe_source = iframe.attrs.get("src")  # type: ignore
        iframe_browser = await self.browser.get(iframe_source)  # type: ignore
        page_content = await iframe_browser.get_content()

        x = re.findall(r"file:\"([^\"]+)", page_content)

        await page.close()

        if len(x) > 0:
            return x[0]

    async def _get_home(self) -> GetHomeResults:
        page = await self.browser.get("https://dizipal735.com")
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
                    provider=AvailableProviders.DIZIPAL,
                )
            )

        return last_episodes
