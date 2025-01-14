import json
import re
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

from src.providers.base import BaseProvider, Priority


class HdFilmCehennemiProvider(BaseProvider):

    @property
    def NAME(self) -> str:
        return "Hdfilmcehennemi"

    async def get_dizi(self, dizi: str, sezon: int, bolum: int) -> Optional[str]:
        name, href = await self._search(dizi)
        episode = await self._find_episode(href, sezon, bolum)

        if episode is not None:
            video_hash = await self._get_video_hash(episode)

            if video_hash is not None:
                return await self._get_video(video_hash)

        return None

    @property
    def PROVIDER_URL(self) -> str:
        return ""

    @property
    def PRIORITY(self) -> str:
        return Priority.HIGH

    async def _get_video(self, hash: str):
        url = "https://cehennemstream.click/player/index.php"
        params = {"data": "d10ec7c16cbe9de8fbb1c42787c3ec26", "do": "getVideo"}

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "fireplayer_player=ec3d80n6codmlluku437v1pleg",
            "Origin": "https://cehennemstream.click",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }

        async with aiohttp.ClientSession() as session:
            payload = f"hash={hash}&r=https%3A%2F%2Fhdfilmcehennemi3.com%2F"
            async with session.post(
                f"{url}?data={hash}&do=getVideo", headers=headers, data=payload
            ) as response:
                to_json = json.loads(await response.text())
                video_source_url = to_json["videoSource"]

                source_response = await session.post(video_source_url, headers=headers)
                ss = await source_response.text()

                # Regex pattern
                pattern = r"#EXT-X-STREAM-INF:.*?BANDWIDTH=(\d+).*?\n(https?://[^\s]+)"

                # Find all matches
                matches = re.findall(pattern, ss)

                # Convert matches to a list of tuples (bandwidth, url) and find the max
                highest_bandwidth_url = max(matches, key=lambda x: int(x[0]))[1]

                print("URL with highest bandwidth:", highest_bandwidth_url)

                return highest_bandwidth_url

    async def _search(self, search_text: str) -> tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://hdfilmcehennemi3.com/?s={search_text}"
            )

            text = await response.text()
            bs4 = BeautifulSoup(text, features="html.parser")

            items = bs4.select(".single-item")
            for item in items:
                serie = item.select_one(".categorytitle a")
                serie_name = serie.text
                serie_href = serie.attrs.get("href")

                if serie_name.lower() == search_text.lower():
                    return serie_name, serie_href

    async def _find_episode(
        self, href: str, season: int, episode: int
    ) -> Optional[str]:
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(href)

                text = await response.text()
                bs4 = BeautifulSoup(text, features="html.parser")

                items = bs4.select(".bolumust")
                for item in items:
                    episode_tag = item.select_one(".baslik")
                    episode_href = item.select_one("a").attrs.get("href")
                    # Extract all integers
                    numbers = re.findall(r"\d+", episode_tag.text)
                    numbers = list(map(int, numbers))
                    found_season = numbers[0]
                    found_episode = numbers[1]

                    if found_episode == episode and found_season == season:
                        return episode_href
        except Exception:
            return None

    async def _get_video_hash(self, href: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(href)

            text = await response.text()
            bs4 = BeautifulSoup(text, features="html.parser")

            iframe_source = bs4.select_one(".video-container iframe").attrs.get("src")
            splitted_source = iframe_source.split("/video/")
            hash = splitted_source[1]

            return hash

    @property
    def ENABLED(self) -> bool:
        return False

