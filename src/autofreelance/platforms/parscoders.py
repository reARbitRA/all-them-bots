"""ParsCoders DOM adapter."""

from __future__ import annotations

from urllib.parse import urlparse

from .base import FreelancePlatform, PlatformSelectors


class ParsCodersPlatform(FreelancePlatform):
    name = "parscoders"
    base_url = "https://parscoders.com"
    selectors = PlatformSelectors(
        listing_url="https://parscoders.com/projects",
        job_card=("[data-testid='project-card']", ".project-card", ".project-item", ".project-list-item", "article"),
        job_link=("a[href*='/project/']", "a[href*='/projects/']", "a"),
        title=("h1", ".project-title", ".title"),
        description=("#project-description", ".project-description", ".project-details", ".description"),
        budget=(".project-budget", ".budget", ".price"),
        status=(".project-status", ".status", ".project-state"),
        bid_message=("textarea[name='proposal']", "textarea[name='description']", "textarea", "[contenteditable='true']"),
        bid_submit=("button:has-text('ارسال پیشنهاد')", "button:has-text('ثبت پیشنهاد')", "button[type='submit']"),
        bid_success=(".toast-success", ".alert-success", "[role='alert']:has-text('موفق')"),
        chat_button=("a[href*='chat']", "a[href*='message']", "button:has-text('گفتگو')", "button:has-text('پیام')"),
        chat_message=("textarea[name='message']", "textarea", "[contenteditable='true']"),
        chat_send=("button:has-text('ارسال')", "button[type='submit']"),
        awarded_markers=("پذیرفته", "برنده", "در حال انجام", "انتخاب شده", "awarded", "accepted"),
    )

    def accepts_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.hostname in {"parscoders.com", "www.parscoders.com"} and "/project" in parsed.path
