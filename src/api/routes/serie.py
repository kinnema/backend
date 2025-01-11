from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from starlette.responses import PlainTextResponse

from src.providers import available_providers

router = APIRouter()


async def fetch_serie_from_providers(serie_name: str, season: int, episode: int):
    providers = available_providers.get_providers()

    for provider in providers:
        url = await provider.get_dizi(serie_name, season, episode)

        if url:
            yield f"{url}\n\n"
            # break


@router.get("/watch")
async def get_serie(serie_name: str, season: int, episode: int):
    return EventSourceResponse(
        content=fetch_serie_from_providers(serie_name, season, episode),
    )


@router.get("/ss.m3u8", response_class=PlainTextResponse)
async def ss():
    playlist_string = """
#EXTM3U
#EXT-X-VERSION:3
## [ FirePlayer ] by Neron (c) 2018~ | firevideoplayer.com | Skype : neronsilence ☪ ##
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",LANGUAGE="tur",NAME="Turkish",DEFAULT=NO,AUTOSELECT=YES,URI="http://localhost:3001/?destination=https://cehennemstream.click/m3/cjJMeHRpL1FnbUVDajBpL3c1ejF2c2hNYUNMc1haZy9xNmhxM0VheU5TbFNuM0p0RTJKT2JIV0U2ajZVcGp4a2p1TW9VdEJiYys2WjBodWJDVWJxZmYxYmtyQ0R0WXZyNlh2VWxoKzQzRGJxVE0rU3ArWUYvdDRqSFEwWUVMbjhELzNMbTBLdnVieVFXUEQ0Yk1MR21EZnZ0cFRQN0pHVlN5TlF0MTM3cElyV0s1Q3FCV2pPMkZhYmROVmpseXZVUzhxZ2Q2Z2FrWXZzQ2RJSWo1TnZWTzZVQzBnQ0lpZ0VMMGlDdi9WenVNYmtoZGpYaHZSbHFNams0OGZzN3NFSmx0eTQ1Q2lCdnQxQzlFSWV2UkNOV0JrUDVyUzFRRGFMcldyc0lNUEEwWGM9"
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=276000,RESOLUTION=640x360,NAME="360p",CODECS="avc1.4D4015,mp4a.40.2",AUDIO="audio"
http://localhost:3001/?destination=https://cehennemstream.click/m3/cjJMeHRpL1FnbUVDajBpL3c1ejF2c2hNYUNMc1haZy9xNmhxM0VheU5TbFNuM0p0RTJKT2JIV0U2ajZVcGp4a25USFlBNEhZSW1UY3p0VCtMYTRiNko1elBsdGlaUTYxS2p1MFI5S25EYjBKaTZuOXJBTmdGR05xNHNuUlg5bzNXbjVtK0VvYnM3eXlnRitHeVY5UkFiOGRCamtHQ21aRWVuTXV2UjFmNXhjNm1LVWwyR1JlMHNVMjJPTWNSdDNndlhPWCtFUElzOVEvbStINi9kWWxXcE5hNXdpa1kzL2F6SlQvS3BtRC9GQ3BJcGt3aGNpUzBLeWIwUGs3SHYrcnNkakhXQ2pxUXdrMmJsS3FETDdJTWV1T3FsZlpSWVp3cTZzb0dDWWdZSTA9
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2048000,RESOLUTION=1280x720,NAME="720p",CODECS="avc1.4D401F,mp4a.40.2",AUDIO="audio"
http://localhost:3001/?destination=https://cehennemstream.click/m3/cjJMeHRpL1FnbUVDajBpL3c1ejF2c2hNYUNMc1haZy9xNmhxM0VheU5TbFNuM0p0RTJKT2JIV0U2ajZVcGp4a2VnQXFCNisybnNhanFiVFp6UmtKeTVpNkdpQnlvaCtJcGZQQ2VyM29aaVNub1NtMmxHOW11Ykd4SnNxL05aeC9YL1h3SmUzOFdqWHAyTFVRL0VLa0R1ajFnVDRqTm1YWHMvYjNydldPREw3aDNDRVZoRmNvMXpTeFlEM2w4UWo5SmVPaFRRbUxFNUFySFRmUkt3VmZtVlBtR2xqSjlZR2IzM2pWbXlLSUR4cU5PclpqRmlsWGhCTzFzNjAxWFhtRXpUQ0N6a1duSThDSWswZlAxRTNVSmRoNkpGNTk3cEhYQmhZUEdTcHB0QmM9
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4096000,RESOLUTION=1920x1080,NAME="1080p",CODECS="avc1.640028,mp4a.40.2",AUDIO="audio"
http://localhost:3001/?destination=https://cehennemstream.click/m3/cjJMeHRpL1FnbUVDajBpL3c1ejF2c2hNYUNMc1haZy9xNmhxM0VheU5TbFNuM0p0RTJKT2JIV0U2ajZVcGp4a0dqRitLSmY4RHFLWTZtYWYvSzBPbHhwOG9WN2F1YTU4TE9wdkw4UStYaGovR0tSeDd6K1Q5WHJjWnhabTMxSlBjblQ2UjRUeE5KdFhmeGFxa215Zm5xRFFQQW5qNWpNb2I2RGpjdSttYXA4d0FWdlBVcEkrYzNNV0EyalNJY3dmTk5kVmlQY1QrempwVGxudmYvazdkT3V5ZCszR2p2a1pOdGxsNGp3a3k5TG5oNGwxUk9zdU5hZ1ZKWjNMckphajF0Z0lhcTNuN2s3ektYSTkzWGZ5SkdHZjFSSnd2aitFcEZIQXY3WHBQUHJCYTU4bUxXOW53R21UTUlBN1g1bWE%3D
    """
    # Strip leading/trailing whitespaces/newlines before returning
    playlist_string = playlist_string.encode("utf-8").decode("utf-8-sig")
    return playlist_string.strip()
