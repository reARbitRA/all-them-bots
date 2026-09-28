"""
Fable-Omega TMA (Telegram Mini App) Cryptographic Authentication Gate
Protects endpoints against forgery and timing attacks via constant-time HMAC-SHA256.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import urllib.parse
from typing import Any


class TMACryptoGate:
    """Cryptographic authorization validator for Telegram Mini App initData."""

    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token.strip()
        self._secret_key = hmac.new(
            key=b"WebAppData",
            msg=self.bot_token.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()

    def validate_init_data(self, init_data_raw: str) -> tuple[bool, dict[str, Any] | None]:
        """Validate initData query string with constant-time HMAC comparison."""
        if not init_data_raw:
            return False, None

        try:
            parsed_params = urllib.parse.parse_qsl(init_data_raw, keep_blank_values=True)
            params_dict: dict[str, str] = dict(parsed_params)
        except Exception:
            return False, None

        received_hash = params_dict.pop("hash", None)
        if not received_hash:
            return False, None

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(params_dict.items(), key=lambda item: item[0])
        )

        calculated_hash = hmac.new(
            key=self._secret_key,
            msg=data_check_string.encode("utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest()

        is_authentic = hmac.compare_digest(calculated_hash.lower(), received_hash.lower())
        if not is_authentic:
            return False, None

        payload: dict[str, Any] = {}
        for k, v in params_dict.items():
            if k in ("user", "receiver", "chat"):
                try:
                    payload[k] = json.loads(v)
                except json.JSONDecodeError:
                    payload[k] = v
            else:
                payload[k] = v

        return True, payload
