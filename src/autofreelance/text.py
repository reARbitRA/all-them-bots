"""Text and identifier helpers."""

from __future__ import annotations

import hashlib
import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")
_SAFE_REPO = re.compile(r"[^a-z0-9-]+")


def normalize_text(value: str, max_length: int | None = None) -> str:
    cleaned = _WHITESPACE.sub(" ", unicodedata.normalize("NFKC", value)).strip()
    return cleaned[:max_length].strip() if max_length else cleaned


def url_fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]


def repository_slug(title: str, external_id: str) -> str:
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    base = _SAFE_REPO.sub("-", ascii_title).strip("-") or "freelance-delivery"
    return f"{base[:45].rstrip('-')}-{external_id[-8:]}".strip("-")


def has_persian_text(value: str) -> bool:
    return any("\u0600" <= char <= "\u06ff" for char in value)
