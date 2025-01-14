import re
import aiohttp
from bs4 import BeautifulSoup
from src.providers.base import BaseProvider, Priority


class DizipalV1Provider(BaseProvider):
    @property
    def NAME(self) -> str:
        raise NotImplementedError

    @property
    def PRIORITY(self) -> str:
        return Priority.HIGH

    @property
    def PROVIDER_URL(self) -> str:
        return 'https://dizipal845-dotcom.gateway.web.tr'
    
    def _request_headers(self):
        return {
            "Accept-Language":"tr,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Sec-Ch-Ua-Platform":"Windows",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Cookie":"dizipal845_com=%7B%22HttpHost%22%3A%22dizipal845.com%22%2C%22Protokol%22%3A%22https%22%2C%22Port%22%3A443%2C%22KulAdSifre%22%3Anull%2C%22UrlAdresi%22%3A%22%5C%2F%22%2C%22GetVeri%22%3Anull%2C%22GitOpjeId%22%3Anull%2C%22DnsAdresi%22%3A0%2C%22URL_Adresi%22%3A%22https%3A%5C%2F%5C%2Fdizipal845.com%5C%2F%22%2C%22GirisIP%22%3A%22188.114.97.7%22%7D",
            "Origin":self.PROVIDER_URL,
            "Referer":self.PROVIDER_URL,
        }

    async def get_dizi(self, dizi: str, sezon: int, bolum: int) -> str | None:
        async with aiohttp.ClientSession() as client:
            headers = self._request_headers()
            url = f"{self.PROVIDER_URL}/dizi/{dizi}/sezon-{sezon}/bolum-{bolum}"
            response = await client.get(url, headers=headers)
            response_body = await response.text()
            bs4 = BeautifulSoup(response_body, "html.parser")
            videoLink = bs4.select_one("#vast_new > iframe").attrs.get("src");
            
            if videoLink:
                response = await client.get(
                        videoLink,
                        headers={"Referer": url},
                    )
                text = await response.text()
                x = re.findall(r"file:\"([^\"]+)", text)

                if len(x) > 0:
                    url = x[0]

                    return url

    @property
    def ENABLED(self) -> bool:
        return True



            
            




