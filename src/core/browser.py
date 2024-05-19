import nodriver as uc


async def init_browser() -> uc.Browser:
    browser = await uc.start()

    return browser
