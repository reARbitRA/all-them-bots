"""Runtime settings, loaded from the environment rather than source control."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .exceptions import ConfigurationError


class Settings(BaseSettings):
    """Settings for the worker and optional FastAPI control plane."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    cdp_endpoint: str = "http://localhost:9222"
    cdp_connect_timeout_seconds: int = Field(default=20, ge=1, le=120)
    enabled_platforms: str = "ponisha,karlancer,parscoders"
    automation_enabled: bool = False
    auto_submit_bids: bool = False
    max_jobs_per_platform: int = Field(default=20, ge=1, le=100)
    poll_interval_seconds: int = Field(default=300, ge=30, le=86_400)
    automation_min_delay_seconds: float = Field(default=2.0, ge=0.0, le=60.0)
    navigation_timeout_seconds: int = Field(default=30, ge=5, le=120)

    llm_api_url: str | None = None
    llm_api_key: SecretStr | None = None
    llm_model: str = "fast-model"
    llm_timeout_seconds: int = Field(default=45, ge=5, le=180)
    llm_min_automation_confidence: float = Field(default=0.92, ge=0.5, le=1.0)

    arena_executor_url: str | None = None
    arena_executor_token: SecretStr | None = None
    arena_executor_timeout_seconds: int = Field(default=1800, ge=30, le=14_400)
    arena_executor_poll_seconds: float = Field(default=5.0, ge=1.0, le=60.0)

    github_token: SecretStr | None = None
    github_owner: str | None = None
    github_private: bool = False
    github_delivery_repository: str | None = None
    github_branch: str = "main"

    database_path: Path = Path("var/pipeline.sqlite3")
    artifact_root: Path = Path("artifacts")
    log_level: str = "INFO"
    service_api_key: SecretStr | None = None

    @field_validator("cdp_endpoint")
    @classmethod
    def cdp_endpoint_is_http(cls, value: str) -> str:
        if not value.startswith(("http://", "https://", "ws://", "wss://")):
            raise ValueError("CDP_ENDPOINT must be an http(s) or ws(s) endpoint")
        return value.rstrip("/")

    @property
    def platform_names(self) -> tuple[str, ...]:
        return tuple(name.strip().lower() for name in self.enabled_platforms.split(",") if name.strip())

    def require_classifier(self) -> None:
        if not self.llm_api_url or not self.llm_api_key:
            raise ConfigurationError("LLM_API_URL and LLM_API_KEY are required to classify or bid")

    def require_execution(self) -> None:
        missing = [
            name
            for name, value in (
                ("ARENA_EXECUTOR_URL", self.arena_executor_url),
                ("ARENA_EXECUTOR_TOKEN", self.arena_executor_token),
                ("GITHUB_TOKEN", self.github_token),
                ("GITHUB_OWNER", self.github_owner),
            )
            if not value
        ]
        if missing:
            raise ConfigurationError(f"Execution/delivery requires: {', '.join(missing)}")

    def secret_value(self, value: SecretStr | None) -> str | None:
        return value.get_secret_value() if value else None
