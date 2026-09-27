"""Platform strategy registration; third parties can register another adapter at startup."""

from __future__ import annotations

from collections.abc import Callable

from ..browser import CdpBrowser
from ..config import Settings
from ..exceptions import ConfigurationError
from .base import FreelancePlatform
from .karlancer import KarlancerPlatform
from .parscoders import ParsCodersPlatform
from .ponisha import PonishaPlatform

PlatformFactory = Callable[[CdpBrowser, Settings], FreelancePlatform]

_REGISTRY: dict[str, PlatformFactory] = {
    "ponisha": PonishaPlatform,
    "karlancer": KarlancerPlatform,
    "parscoders": ParsCodersPlatform,
}


def register_platform(name: str, factory: PlatformFactory) -> None:
    normalized = name.strip().lower()
    if not normalized:
        raise ValueError("Platform name cannot be empty")
    _REGISTRY[normalized] = factory


def create_platforms(browser: CdpBrowser, settings: Settings) -> dict[str, FreelancePlatform]:
    missing = [name for name in settings.platform_names if name not in _REGISTRY]
    if missing:
        available = ", ".join(sorted(_REGISTRY))
        raise ConfigurationError(f"Unknown platform(s): {', '.join(missing)}. Available: {available}")
    return {name: _REGISTRY[name](browser, settings) for name in settings.platform_names}
