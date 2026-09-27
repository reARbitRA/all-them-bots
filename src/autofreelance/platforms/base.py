"""DOM strategy contract for a freelance platform.

Adapters use semantic locator fallbacks rather than brittle JavaScript or synthetic
fingerprint tricks.  Update a platform's selector manifest after a permitted UI change.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from hashlib import sha256
from urllib.parse import urljoin, urlparse

from playwright.async_api import Locator, Page

from ..browser import CdpBrowser
from ..config import Settings
from ..exceptions import PlatformInteractionError
from ..models import FreelanceJob
from ..text import normalize_text, url_fingerprint

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PlatformSelectors:
    listing_url: str
    job_card: tuple[str, ...]
    job_link: tuple[str, ...]
    title: tuple[str, ...]
    description: tuple[str, ...]
    budget: tuple[str, ...]
    status: tuple[str, ...]
    bid_message: tuple[str, ...]
    bid_submit: tuple[str, ...]
    bid_success: tuple[str, ...]
    chat_button: tuple[str, ...]
    chat_message: tuple[str, ...]
    chat_send: tuple[str, ...]
    bid_amount: tuple[str, ...] = ()
    bid_days: tuple[str, ...] = ()
    awarded_markers: tuple[str, ...] = ()


class FreelancePlatform(ABC):
    """Strategy interface for one authorized freelance platform session."""

    name: str
    base_url: str
    selectors: PlatformSelectors

    def __init__(self, browser: CdpBrowser, settings: Settings) -> None:
        self.browser = browser
        self.settings = settings

    @abstractmethod
    def accepts_url(self, url: str) -> bool:
        """Return true when a URL belongs to this platform's job detail view."""

    async def discover_jobs(self) -> list[FreelanceJob]:
        """Read at most the configured number of visible jobs from the public listing."""
        page = await self.browser.new_page()
        try:
            await self.browser.navigate(page, self.selectors.listing_url)
            cards = await self._visible_job_cards(page)
            candidate_urls: list[str] = []
            seen: set[str] = set()
            for card in cards:
                href = await self._read_href(card, self.selectors.job_link)
                if not href:
                    continue
                absolute_url = urljoin(page.url, href)
                if absolute_url in seen or not self.accepts_url(absolute_url):
                    continue
                seen.add(absolute_url)
                candidate_urls.append(absolute_url)
                if len(candidate_urls) >= self.settings.max_jobs_per_platform:
                    break

            semaphore = asyncio.Semaphore(3)

            async def extract(url: str) -> FreelanceJob | None:
                async with semaphore:
                    try:
                        return await self._extract_job(url)
                    except PlatformInteractionError as exc:
                        logger.warning(
                            "job_extraction_failed",
                            extra={"platform": self.name, "url": url, "error": str(exc)},
                        )
                        return None

            results = await asyncio.gather(*(extract(url) for url in candidate_urls))
            return [job for job in results if job is not None]
        finally:
            if not page.is_closed():
                await page.close()

    async def submit_bid(self, job: FreelanceJob, proposal_fa: str) -> None:
        """Submit one short proposal through the authorized, visible site UI."""
        if not self.settings.automation_enabled or not self.settings.auto_submit_bids:
            raise PlatformInteractionError("Bid submission is disabled by configuration")
        proposal = normalize_text(proposal_fa, max_length=900)
        if len(proposal) < 20:
            raise PlatformInteractionError("Proposal is too short to submit safely")
        page = await self.browser.new_page()
        try:
            await self._open_job(page, job.url)
            await self._fill_first(page, self.selectors.bid_message, proposal, "proposal textarea")
            await self._pause()
            await self._click_first(page, self.selectors.bid_submit, "submit bid")
            await self._wait_for_any(page, self.selectors.bid_success, "bid submission confirmation")
        finally:
            if not page.is_closed():
                await page.close()

    async def is_awarded(self, job: FreelanceJob) -> bool:
        """Check the job detail UI for a platform-specific award state."""
        page = await self.browser.new_page()
        try:
            await self._open_job(page, job.url)
            status = (await self._read_first(page, self.selectors.status)).casefold()
            return bool(status) and any(marker.casefold() in status for marker in self.selectors.awarded_markers)
        finally:
            if not page.is_closed():
                await page.close()

    async def send_delivery(self, job: FreelanceJob, github_url: str) -> None:
        """Send the exact required Persian delivery message in the platform UI."""
        if not github_url.startswith("https://github.com/"):
            raise PlatformInteractionError("Delivery URL must be an HTTPS GitHub repository URL")
        message = (
            "پروژه انجام شد. سورس کد و راهنمای اجرا در این لینک گیت‌هاب قرار دارد: "
            f"{github_url}"
        )
        page = await self.browser.new_page()
        try:
            await self._open_job(page, job.url)
            before_pages = set(self.browser.context.pages)
            await self._click_first(page, self.selectors.chat_button, "project chat")
            await page.wait_for_timeout(400)
            chat_page = next(
                (candidate for candidate in self.browser.context.pages if candidate not in before_pages), page
            )
            self.browser.track_worker_page(chat_page) if chat_page is not page else None
            await self.browser.assert_no_access_challenge(chat_page)
            await self._fill_first(chat_page, self.selectors.chat_message, message, "chat message")
            await self._pause()
            await self._click_first(chat_page, self.selectors.chat_send, "send delivery message")
        finally:
            # A popup is included in worker pages and will be closed by the browser lifecycle.
            if not page.is_closed():
                await page.close()

    async def _extract_job(self, url: str) -> FreelanceJob:
        page = await self.browser.new_page()
        try:
            await self._open_job(page, url)
            title = await self._read_first(page, self.selectors.title)
            description = await self._read_first(page, self.selectors.description)
            budget = await self._read_first(page, self.selectors.budget)
            if not title or not description:
                raise PlatformInteractionError("Job title or description was not present in the DOM")
            external_id = self._external_id(page.url)
            return FreelanceJob(
                platform=self.name,
                external_id=external_id,
                url=page.url,
                title=normalize_text(title, max_length=300),
                description=normalize_text(description, max_length=40_000),
                budget_text=normalize_text(budget, max_length=500) or None,
            )
        finally:
            if not page.is_closed():
                await page.close()

    async def _open_job(self, page: Page, url: str) -> None:
        if not self.accepts_url(url):
            raise PlatformInteractionError(f"Refusing a non-{self.name} job URL: {url}")
        await self.browser.navigate(page, url)
        if not self.accepts_url(page.url):
            raise PlatformInteractionError(f"Job redirected outside {self.name}: {page.url}")

    async def _visible_job_cards(self, page: Page) -> list[Locator]:
        for selector in self.selectors.job_card:
            locator = page.locator(selector)
            try:
                await locator.first.wait_for(state="visible", timeout=7_000)
                count = min(await locator.count(), self.settings.max_jobs_per_platform * 2)
                if count:
                    return [locator.nth(index) for index in range(count)]
            except Exception:
                continue
        raise PlatformInteractionError("No job cards found; verify login and selector manifest")

    async def _read_href(self, scope: Locator | Page, selectors: Iterable[str]) -> str:
        for selector in selectors:
            try:
                item = scope.locator(selector).first
                if await item.count():
                    value = await item.get_attribute("href")
                    if value:
                        return value
            except Exception:
                continue
        return ""

    async def _read_first(self, scope: Locator | Page, selectors: Iterable[str]) -> str:
        for selector in selectors:
            try:
                item = scope.locator(selector).first
                if await item.count():
                    text = normalize_text(await item.inner_text(timeout=3_000))
                    if text:
                        return text
            except Exception:
                continue
        return ""

    async def _fill_first(
        self, page: Page, selectors: Iterable[str], value: str, action_name: str
    ) -> None:
        for selector in selectors:
            try:
                item = page.locator(selector).first
                if await item.count() and await item.is_visible():
                    await item.fill(value, timeout=8_000)
                    return
            except Exception:
                continue
        raise PlatformInteractionError(f"Could not find {action_name} control")

    async def _click_first(self, page: Page, selectors: Iterable[str], action_name: str) -> None:
        for selector in selectors:
            try:
                item = page.locator(selector).first
                if await item.count() and await item.is_visible():
                    await item.click(timeout=8_000)
                    return
            except Exception:
                continue
        raise PlatformInteractionError(f"Could not find {action_name} control")

    async def _wait_for_any(self, page: Page, selectors: Iterable[str], action_name: str) -> None:
        for selector in selectors:
            try:
                await page.locator(selector).first.wait_for(state="visible", timeout=8_000)
                return
            except Exception:
                continue
        raise PlatformInteractionError(f"No {action_name} was detected after action")

    def _external_id(self, url: str) -> str:
        path_parts = [part for part in urlparse(url).path.split("/") if part]
        candidate = path_parts[-1] if path_parts else ""
        return candidate if 3 <= len(candidate) <= 120 else url_fingerprint(url)

    async def _pause(self) -> None:
        if self.settings.automation_min_delay_seconds:
            await asyncio.sleep(self.settings.automation_min_delay_seconds)

    def stable_id_for_url(self, url: str) -> str:
        return sha256(url.encode()).hexdigest()[:20]
