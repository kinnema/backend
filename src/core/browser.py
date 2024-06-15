import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import nodriver as uc

from src.core.config import ROOT_DIR, settings
from src.helpers.repeated_timer import RepeatTimer


class Browser:
    browser: uc.Browser
    last_request_thread: RepeatTimer
    last_request: Optional[datetime] = datetime.now(tz=timezone.utc)

    async def init_browser(self):
        config = uc.Config()
        config.add_extension(os.path.join(ROOT_DIR, "extensions", "ublock.crx"))
        config.add_extension(os.path.join(ROOT_DIR, "extensions", "image-blocker.crx"))

        self.browser = await uc.start(config=config)

        self.init_timer()

    def init_timer(self):
        self.start_background_task()

    def _background_task(self):
        if self.last_request:
            last_request_expire = self.last_request + timedelta(
                minutes=settings.BROWSER_IDLE_TIMEOUT_IN_MINUTES
            )
            date_now = datetime.now(tz=timezone.utc)

            if date_now > last_request_expire:
                self.stop_browser()
                print("Last request expired")

    def start_background_task(self):
        timer = RepeatTimer(
            settings.BROWSER_CHECK_IDLE_TIMEOUT_IN_SECONDS, self._background_task
        )
        timer.start()

        self.last_request_thread = timer

    def set_last_request(self, last_request: datetime):
        self.last_request = last_request

    def stop_browser(self):
        self.last_request = None
        self.browser.stop()
        self.last_request_thread.stop()


browser = Browser()
