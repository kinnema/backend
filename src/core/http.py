import aiohttp


async def get_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        finally:
            await session.close()
