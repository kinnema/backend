import os

import nodriver as uc

from src.core.config import ROOT_DIR


async def init_browser():
    global browser
    config = uc.Config()
    config.add_extension(os.path.join(ROOT_DIR, "extensions", "ublock.crx"))
    config.add_extension(os.path.join(ROOT_DIR, "extensions", "image-blocker.crx"))

    browser = await uc.start(config=config)
