import re
from typing import List
from nodriver import Browser
from providers import AvailableProviders, Provider

class Dizipal(Provider):

    def __init__(self, browser: Browser):
        self.browser = browser

    async def collection(self, collection: str):
        return await self.search(collection)


    async def search(self, query: str):
        series: List["dict"] = []
        page = await self.browser.get(f"https://dizipal735.com/diziler?kelime={query}")
        await page.wait_for(".type2")
        all_series = await page.query_selector_all(".type2 ul li a")

        for serie in all_series:
            _image = await page.query_selector("img", _node=serie)
            name = await page.query_selector(".detail .title", _node=serie)
            provider = AvailableProviders.DIZIPAL
            image = _image.attrs.get("src")
            href = serie.attrs.get("href")

            print(name)
            dict = {
                "name": name.text,
                "image": image,
                "provider": provider,
                "href": href
            }

            series.append(dict)



        await page.close()
        return series





    async def get_dizi(self, dizi, sezon, bolum):
        self.dizi = dizi
        self.sezon = sezon
        self.bolum = bolum

        page = await self.browser.get(f'https://dizipal735.com/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}')
        await page.wait_for(".user-menu")
        iframe = await page.query_selector("div#vast_new iframe")
        iframe_source = iframe.attrs.get("src")
        iframe_browser = await self.browser.get(iframe_source)
        page_content =  await iframe_browser.get_content()

        x = re.findall(r"file:\"([^\"]+)", page_content) 

        await page.close()

        if (len(x) > 0):
            return x[0]
        