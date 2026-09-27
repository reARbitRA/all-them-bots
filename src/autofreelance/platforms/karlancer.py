"""Karlancer DOM adapter."""

from __future__ import annotations

from urllib.parse import urlparse

from .base import FreelancePlatform, PlatformSelectors


class KarlancerPlatform(FreelancePlatform):
    name = "karlancer"
    base_url = "https://www.karlancer.com"
    selectors = PlatformSelectors(
        listing_url="https://www.karlancer.com/projects",
        job_card=("[data-testid='project-card']", ".project-card", ".project-item", "article"),
        job_link=("a[href*='/projects/']", "a[href*='/project/']", "a"),
        title=("h1", ".project-title", "[data-testid='project-title']"),
        description=("#project-description", ".project-description", ".project-detail__description", ".description"),
        budget=(".project-budget", ".budget", "[data-testid='project-budget']"),
        status=(".project-status", ".status", "[data-testid='project-status']"),
        bid_message=(
            "textarea[name='description']",
            "textarea[name='proposal']",
            "textarea[placeholder*='پیشنهاد']",
            "textarea",
        ),
        bid_submit=("button:has-text('ارسال پیشنهاد')", "button:has-text('ثبت پیشنهاد')", "button[type='submit']"),
        bid_success=(".toast-success", ".alert-success", "[role='alert']:has-text('موفق')"),
        chat_button=("a[href*='chat']", "a[href*='message']", "button:has-text('گفتگو')", "button:has-text('پیام')"),
        chat_message=("textarea[name='message']", "textarea", "[contenteditable='true']"),
        chat_send=("button:has-text('ارسال')", "button[type='submit']"),
        awarded_markers=("پذیرفته", "برنده", "در حال انجام", "انتخاب شده", "awarded", "accepted"),
    )

    def accepts_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.hostname in {"karlancer.com", "www.karlancer.com"} and "/project" in parsed.path
