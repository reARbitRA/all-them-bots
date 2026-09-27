"""Conservative structured-output classifier using an OpenAI-compatible API."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import httpx

from ..config import Settings
from ..exceptions import LLMResponseError
from ..models import EligibilityDecision, FreelanceJob
from ..text import has_persian_text, normalize_text

logger = logging.getLogger(__name__)

_DECISION_SCHEMA: dict[str, Any] = {
    "name": "freelance_automation_decision",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["automatable", "confidence", "rationale", "risks", "proposal_fa", "estimated_days"],
        "properties": {
            "automatable": {"type": "boolean"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "rationale": {"type": "string", "maxLength": 800},
            "risks": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
            "proposal_fa": {"type": ["string", "null"], "maxLength": 900},
            "estimated_days": {"type": ["integer", "null"], "minimum": 1, "maximum": 90},
        },
    },
}

_SYSTEM_PROMPT = """You are the conservative pre-qualification component of a freelance delivery service.
Assess whether the ENTIRE requested job can be delivered ethically and reliably as a software artifact without human-only work. Only mark automatable=true for bounded programming work such as a Python script, an API integration, a permitted scraper, bot, data transformation, or testable web service.
Return automatable=false for ambiguous scope, physical work, academic cheating, unlawful surveillance, credential abuse, CAPTCHA/access-control evasion, account manipulation, or anything needing a human to make an unverified claim.
If true, provide a natural short Persian proposal of two to four sentences. It must be specific to the task, modest, should not pretend work is already complete, and must not mention AI. If false, proposal_fa must be null. Return only JSON matching the supplied schema."""


class FastLLMClient:
    """Calls a configured OpenAI-compatible chat-completions endpoint asynchronously."""

    def __init__(self, settings: Settings, http_client: httpx.AsyncClient | None = None) -> None:
        settings.require_classifier()
        self.settings = settings
        self._client = http_client or httpx.AsyncClient(timeout=settings.llm_timeout_seconds)
        self._owns_client = http_client is None

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def classify(self, job: FreelanceJob) -> EligibilityDecision:
        payload = {
            "model": self.settings.llm_model,
            "temperature": 0.2,
            "response_format": {"type": "json_schema", "json_schema": _DECISION_SCHEMA},
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "title": job.title,
                            "description": job.description,
                            "budget_text": job.budget_text,
                            "platform": job.platform,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
        }
        response = await self._post_with_retry(payload)
        data = self._extract_json(response)
        decision = self._validate_decision(data)
        logger.info(
            "job_classified",
            extra={
                "job_key": job.key,
                "automatable": decision.automatable,
                "confidence": decision.confidence,
            },
        )
        return decision

    async def _post_with_retry(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.settings.secret_value(self.settings.llm_api_key)}",
            "Content-Type": "application/json",
        }
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = await self._client.post(self.settings.llm_api_url, headers=headers, json=payload)
                if response.status_code == 400 and "response_format" in response.text and attempt == 0:
                    # Some compatible providers do not implement JSON Schema. Request JSON mode, then
                    # validate exactly the same schema locally before allowing any bid.
                    payload = {**payload, "response_format": {"type": "json_object"}}
                    continue
                if response.status_code in {408, 409, 429, 500, 502, 503, 504}:
                    await asyncio.sleep(2**attempt)
                    continue
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                if attempt < 2:
                    await asyncio.sleep(2**attempt)
        raise LLMResponseError("LLM request failed after bounded retries") from last_error

    @staticmethod
    def _extract_json(response: dict[str, Any]) -> dict[str, Any]:
        try:
            content = response["choices"][0]["message"]["content"]
            if isinstance(content, list):
                content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
            if not isinstance(content, str):
                raise TypeError("message content is not text")
            cleaned = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                raise TypeError("decision is not an object")
            return parsed
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMResponseError("LLM did not return a JSON decision") from exc

    @staticmethod
    def _validate_decision(data: dict[str, Any]) -> EligibilityDecision:
        required = {"automatable", "confidence", "rationale", "risks", "proposal_fa", "estimated_days"}
        if set(data) != required:
            raise LLMResponseError("LLM decision keys do not match the strict contract")
        automatable = data["automatable"]
        confidence = data["confidence"]
        rationale = data["rationale"]
        risks = data["risks"]
        proposal = data["proposal_fa"]
        days = data["estimated_days"]
        if type(automatable) is not bool or type(confidence) not in {int, float}:
            raise LLMResponseError("Invalid decision primitives")
        if not 0 <= float(confidence) <= 1 or not isinstance(rationale, str):
            raise LLMResponseError("Invalid confidence or rationale")
        if not isinstance(risks, list) or not all(isinstance(item, str) for item in risks):
            raise LLMResponseError("Invalid risks")
        if proposal is not None and not isinstance(proposal, str):
            raise LLMResponseError("Invalid Persian proposal")
        if days is not None and (type(days) is not int or not 1 <= days <= 90):
            raise LLMResponseError("Invalid estimate")
        proposal = normalize_text(proposal or "", max_length=900) or None
        if automatable and (proposal is None or len(proposal) < 20 or not has_persian_text(proposal)):
            raise LLMResponseError("Automatable work requires a usable short Persian proposal")
        if not automatable:
            proposal = None
        return EligibilityDecision(
            automatable=automatable,
            confidence=float(confidence),
            rationale=normalize_text(rationale, max_length=800),
            risks=tuple(normalize_text(item, max_length=300) for item in risks),
            proposal_fa=proposal,
            estimated_days=days,
        )
