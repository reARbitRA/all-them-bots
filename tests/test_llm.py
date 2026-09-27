from __future__ import annotations

import json

import httpx
import pytest

from autofreelance.clients.llm import FastLLMClient
from autofreelance.config import Settings
from autofreelance.models import FreelanceJob


@pytest.mark.asyncio
async def test_classifier_accepts_strict_persian_structured_decision():
    response_body = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "automatable": True,
                            "confidence": 0.96,
                            "rationale": "اسکریپت مشخص و قابل آزمون است.",
                            "risks": ["نیاز به کلید API معتبر"],
                            "proposal_fa": "سلام، این اسکریپت پایتون را با مدیریت خطا و راهنمای اجرای کامل پیاده‌سازی می‌کنم. خروجی قابل آزمون و سورس مرتب تحویل می‌شود.",
                            "estimated_days": 2,
                        },
                        ensure_ascii=False,
                    )
                }
            }
        ]
    }

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200, json=response_body)

    settings = Settings(llm_api_url="https://llm.test/v1/chat/completions", llm_api_key="test-key")
    client = FastLLMClient(settings, httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    result = await client.classify(
        FreelanceJob("test", "1", "https://example.test/jobs/1", "Python", "یک اسکریپت پایتون")
    )
    assert result.automatable is True
    assert result.confidence == 0.96
    await client.close()
