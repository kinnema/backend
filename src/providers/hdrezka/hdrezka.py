
import json
import re
from typing import Dict, List, Optional, Union

import aiohttp
from bs4 import BeautifulSoup
from click import Option

from src.providers.base import BaseProvider, Priority

class NotFoundError(Exception):
    pass


rezka_base = 'https://rezka.ag'
base_headers = {
    'X-Hdrezka-Android-App': '1',
    'X-Hdrezka-Android-App-Version': '2.2.0',
}


class MediaType:
    MOVIE = 'movie'
    SHOW = 'show'


class HdRezkaProvider(BaseProvider):


    @property
    def PRIORITY(self) -> str:
       return Priority.LOW

    @property
    def REQUIRES_BROWSER(self) -> bool:
        return False


    @property
    def PROVIDER_URL(self) -> str:
        return ""

    async def get_dizi(self, dizi: str, sezon: int, bolum: int) -> str | None:
        s = await universal_scraper(dizi, MediaType.SHOW, None, sezon, bolum)

        print(s[-1])
        for item in s[-1]:
            return s[-1][item]




def extract_title_and_year(title_and_year: str) -> Optional[Dict[str, Union[str, int]]]:
    try:
        parts = title_and_year.strip().split()
        year = int(parts[-1])
        title = ' '.join(parts[:-1])
        return {'title': title, 'year': year}
    except (ValueError, IndexError):
        return None

def generate_random_favs() -> str:
    import random
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))

def _extract_video_urls(link: str) -> Dict[str, Optional[str]]:
    bracket_pattern = r'\[(.*?)\]'
    url_pattern = r'https?://[^\s]+\.mp4'  # Updated to match video file extensions

    bracket_match = re.search(bracket_pattern, link)
    bracket_content = bracket_match.group(1) if bracket_match else None
    quality = bracket_content if bracket_content is not None else ""

    if bracket_content is None:
        raise Exception()

    try:
        quality = BeautifulSoup(bracket_content, features="html.parser").text
    except:
        print("no html")

    url_match = re.search(url_pattern, link)

    if url_match is None:
        return { quality: None }

    return {
        quality: url_match.group(0)
    }

def parse_video_links(links: str) -> List[Dict[str, Optional[str]]]:
    l = links.split(',')
    

    return list(map((lambda x: _extract_video_urls(x)), l))

def parse_subtitle_links(subtitles: Optional[str]) -> List[str]:
    if not subtitles:
        return []

    return subtitles.split(',')

async def search_and_find_media_id(title: str, media_type: str, release_year: Optional[int] = None) -> Optional[Dict]:
    """
    Searches for the media ID based on the title, type, and optional release year using BeautifulSoup.
    
    Args:
        title (str): Title of the media.
        media_type (str): Type of the media ('movie' or 'show').
        release_year (Optional[int]): Year of the media release (optional for shows).

    Returns:
        Optional[Dict]: A dictionary with media data if found, otherwise None.
    """
    async with aiohttp.ClientSession(headers=base_headers) as session:
        async with session.get(f"{rezka_base}/engine/ajax/search.php", params={'q': title}) as response:
            search_data = await response.text()

    soup = BeautifulSoup(search_data, 'html.parser')
    
    # Find all links with media details inside <a> tags
    item_links = soup.find_all('a', href=True)
    movie_data = []

    for link in item_links:
        title_and_year = link.get_text(strip=True)
        print(f"Checking title: {title_and_year}")  # Debugging line

        # Adjusted regex to match the new format
        match = re.search(r'\(([^)]+)\)', title_and_year)
        if match:
            # Extract the year or year range
            year_text = match.group(1).split(',')[-1].strip()  # "2024 - ..." or "2005-2009"
            print(f"Extracted year text: {year_text}")  # Debugging line
            
            # Match for a single year or a range
            year_match = re.match(r'(\d{4})', year_text)
            if year_match:
                year = int(year_match.group(1))
            else:
                print(f"Skipping due to invalid year format: {year_text}")  # Debugging line
                continue  # Skip if the year format is not valid

            # Normalize the title to match
            media_title = title_and_year.split(' (')[0]
            print(f"Extracted title: {media_title}")  # Debugging line

            # Check if the title matches (case-insensitive)
            if title.lower() in media_title.lower():  # Changed to use 'in' for partial matching
                print(f"Title match found: {media_title}")  # Debugging line
                match_id = re.search(r'/(\d+)-[^/]+\.html$', link['href'])
                if match_id:
                    movie_data.append({
                        'id': match_id.group(1),
                        'year': year,
                        'type': media_type,
                        'url': link['href']
                    })

    # If the release_year is provided, filter based on the year; otherwise, return the first match
    if release_year:
        filtered_items = [item for item in movie_data if item['type'] == media_type and item['year'] == release_year]
    else:
        filtered_items = [item for item in movie_data if item['type'] == media_type]

    print(f"Filtered items: {filtered_items}")  # Debugging line
    return filtered_items[0] if filtered_items else None

async def get_translator_id(url: str, movie_id: str, media_type: str) -> Optional[str]:
    async with aiohttp.ClientSession(headers=base_headers) as session:
        async with session.get(f"http://localhost:3000/?destination={url}") as response:
            response_text = await response.text()

    if 'data-translator_id="238"' in response_text:
        return '238'

    function_name = '   ' if media_type == MediaType.MOVIE else 'initCDNSeriesEvents'
    regex_pattern = re.compile(rf'sof\.tv\.{function_name}\({movie_id}, ([^,]+)', re.IGNORECASE)
    match = regex_pattern.search(response_text)
    
    return match.group(1) if match else None

async def get_stream(movie_id: str, translator_id: str, media_type: str, season: Optional[int] = None, episode: Optional[int] = None) -> Dict:
    search_params = {
        'id': movie_id,
        'translator_id': translator_id,
        'favs': generate_random_favs(),
        'action': 'get_movie' if media_type == MediaType.MOVIE else 'get_stream'
    }

    if media_type == MediaType.SHOW:
        if season is not None and episode is not None:
            search_params.update({'season': str(season), 'episode': str(episode)})
    else:
        search_params.update({'is_camprip': '0', 'is_ads': '0', 'is_director': '0'})

    async with aiohttp.ClientSession(headers=base_headers) as session:
        async with session.post(f"http://localhost:3000/?destination={rezka_base}/ajax/get_cdn_series/", data=search_params) as response:
            response_text = await response.text()

    return json.loads(response_text)

async def universal_scraper(title: str, media_type: str, release_year: Optional[int] = None, season: Optional[int] = None, episode: Optional[int] = None) -> List[Dict[str,Optional[str]]]:
    result = await search_and_find_media_id(title, media_type, release_year)
    if not result or not result.get('id'):
        raise NotFoundError('No result found')

    translator_id = await get_translator_id(result['url'], result['id'], media_type)
    if not translator_id:
        raise NotFoundError('No translator id found')

    stream_data = await get_stream(result['id'], translator_id, media_type, season, episode)
    parsed_videos = parse_video_links(stream_data.get('url', ''))
    parsed_subtitles = parse_subtitle_links(stream_data.get('subtitle', False))
    
    return parsed_videos