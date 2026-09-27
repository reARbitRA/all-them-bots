"""Ponisha DOM adapter. Selectors are ordered from stable semantic attributes to fallbacks."""

from __future__ import annotations

from urllib.parse import urlparse

from .base import FreelancePlatform, PlatformSelectors


class PonishaPlatform(FreelancePlatform):
    name = "ponisha"
    base_url = "https://ponisha.ir"
    selectors = PlatformSelectors(
        listing_url="https://ponisha.ir/projects",
        job_card=("[data-testid='project-card']", ".project-card", "article.project", "article"),
        job_link=("a[href*='/project/']", "a[href*='/projects/']", "a"),
        title=("h1", "[data-testid='project-title']", ".project-title"),
        description=(
            "[data-testid='project-description']",
            "#project-description",
            ".project-description",
            ".description",
        ),
        budget=("[data-testid='project-budget']", ".project-budget", ".budget"),
        status=("[data-testid='project-status']", ".project-status", ".status"),
        bid_message=(
            "textarea[name='proposal']",
            "textarea[name='description']",
            "[data-testid='proposal-message'] textarea",
            "textarea",
        ),
        bid_submit=(
            "button[type='submit'][data-testid*='proposal']",
            "button:has-text('ارسال پیشنهاد')",
            "button:has-text('ثبت پیشنهاد')",
        ),
        bid_success=("[role='alert']:has-text('ثبت')", ".toast-success", ".alert-success"),
        chat_button=(
            "a[href*='chat']",
            "button:has-text('گفتگو')",
            "button:has-text('پیام')",
        ),
        chat_message=("textarea[name='message']", "textarea", "[contenteditable='true']"),
        chat_send=("button[type='submit']", "button:has-text('ارسال')"),
        awarded_markers=("پذیرفته", "برنده", "انجام پروژه", "در حال انجام", "awarded", "accepted"),
    )

    def accepts_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.hostname in {"ponisha.ir", "www.ponisha.ir"} and "/project" in parsed.path
