"""Attachment to an account-holder's existing Chromium session via CDP.

No browser is launched here and this module never attempts to evade access controls.  A
challenge page is a hard stop that the account holder must resolve outside the worker.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    TimeoutError,
    async_playwright,
)

from .config import Settings
from .exceptions import AccessChallengeDetected, BrowserUnavailable, PlatformInteractionError

logger = logging.getLogger(__name__)

_CHALLENGE_WORDS = (
    "just a moment",
    "attention required",
    "verify you are human",
    "verify you are a human",
    "security check",
    "captcha",
    "checking your browser",
)
_CHALLENGE_SELECTORS = (
    "iframe[src*='challenges.cloudflare.com']",
    "iframe[title*='challenge' i]",
    "[data-sitekey]",
    "#cf-chl-widget",
)


class CdpBrowser:
    """Small lifecycle wrapper around :meth:`BrowserType.connect_over_cdp`.

    Chrome is owned by the human operator.  ``close`` only closes tabs created by
    this worker and detaches Playwright; it never asks Chrome to terminate.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._created_pages: list[Page] = []

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            raise BrowserUnavailable("CDP browser is not connected")
        return self._context

    async def connect(self) -> None:
        if self._browser is not None:
            return
        self._playwright = await async_playwright().start()
        try:
            self._browser = await self._playwright.chromium.connect_over_cdp(
                self._settings.cdp_endpoint,
                timeout=self._settings.cdp_connect_timeout_seconds * 1000,
            )
            if not self._browser.contexts:
                raise BrowserUnavailable("The CDP browser has no default context")
            self._context = self._browser.contexts[0]
            logger.info("attached_to_cdp_browser", extra={"endpoint": self._settings.cdp_endpoint})
        except Exception as exc:
            await self._detach_playwright()
            raise BrowserUnavailable(
                "Could not attach to approved Chrome CDP endpoint. Start Chrome with "
                "--remote-debugging-port=9222 and sign in manually."
            ) from exc

    async def new_page(self) -> Page:
        await self.connect()
        page = await self.context.new_page()
        self.track_worker_page(page)
        return page

    def track_worker_page(self, page: Page) -> None:
        if page not in self._created_pages:
            self._created_pages.append(page)

    async def navigate(self, page: Page, url: str) -> None:
        try:
            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=self._settings.navigation_timeout_seconds * 1000,
            )
            if response and response.status >= 500:
                raise PlatformInteractionError(f"Platform returned HTTP {response.status} for {url}")
            await self.assert_no_access_challenge(page)
        except TimeoutError as exc:
            await self.assert_no_access_challenge(page)
            raise PlatformInteractionError(f"Timed out loading {url}") from exc

    async def assert_no_access_challenge(self, page: Page) -> None:
        """Fail closed when an access-control challenge is present.

        Detection is intentionally followed only by a clear error, never by solving,
        fingerprinting, proxy rotation, retries intended to evade, or CAPTCHA services.
        """
        current_url = page.url.lower()
        if any(fragment in current_url for fragment in ("/cdn-cgi/", "challenge", "captcha")):
            raise AccessChallengeDetected(f"Access challenge URL detected at {page.url}")
        for selector in _CHALLENGE_SELECTORS:
            try:
                if await page.locator(selector).count():
                    raise AccessChallengeDetected(f"Access challenge element detected at {page.url}")
            except AccessChallengeDetected:
                raise
            except Exception:
                continue
        try:
            body = (await page.locator("body").inner_text(timeout=3_000)).lower()
        except Exception:
            return
        if any(phrase in body for phrase in _CHALLENGE_WORDS):
            raise AccessChallengeDetected(f"Access challenge content detected at {page.url}")

    @staticmethod
    def same_site(url: str, expected_base_url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        expected = (urlparse(expected_base_url).hostname or "").lower()
        return host == expected or host.endswith(f".{expected}")

    async def close_worker_pages(self) -> None:
        for page in reversed(self._created_pages):
            try:
                if not page.is_closed():
                    await page.close()
            except Exception:  # Browser already disappeared; nothing safe to recover.
                logger.debug("worker_page_close_failed", exc_info=True)
        self._created_pages.clear()

    async def _detach_playwright(self) -> None:
        if self._playwright is not None:
            try:
                await self._playwright.stop()
            finally:
                self._playwright = None
                self._browser = None
                self._context = None

    async def close(self) -> None:
        await self.close_worker_pages()
        # Do not call Browser.close(): this is an externally-owned Chrome process.
        await self._detach_playwright()
