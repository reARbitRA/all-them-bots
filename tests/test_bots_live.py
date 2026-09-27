"""
Fable-Omega End-to-End Bot Fleet Integration Tests
Verifies that all 5 bots, FSM state machines, database transactions, and monetization work without errors.
"""

import pytest
import asyncio
from src.core.dispatcher import DISPATCHER
from src.core.database import DB
from src.core.monetization import PaymentManager


@pytest.mark.asyncio
async def test_bot_01_commerce_flow():
    """Test full e-commerce flow: /start -> catalog -> add to cart -> checkout -> receipt -> approved."""
    user_id = 1001

    # 1. /start
    res1 = await DISPATCHER.dispatch_update("commerce", {
        "message": {"from": {"id": user_id, "first_name": "TestBuyer"}, "text": "/start"}
    })
    assert "سلام" in res1["text"]

    # 2. Add product to cart
    res2 = await DISPATCHER.dispatch_update("commerce", {
        "callback_query": {"from": {"id": user_id}, "data": "buy_prod_01"}
    })
    assert "اضافه شد" in res2["text"]

    # 3. Checkout
    res3 = await DISPATCHER.dispatch_update("commerce", {
        "callback_query": {"from": {"id": user_id}, "data": "checkout_cart"}
    })
    assert "نام و نام‌خانوادگی" in res3["text"]

    # 4. Submit Shipping Info
    res4 = await DISPATCHER.dispatch_update("commerce", {
        "message": {"from": {"id": user_id}, "text": "Ali Rezaei, 09121111111, Tehran"}
    })
    assert "فاکتور" in res4["text"]

    # 5. Upload receipt photo
    res5 = await DISPATCHER.dispatch_update("commerce", {
        "message": {"from": {"id": user_id}, "photo": [{"file_id": "test_photo"}]}
    })
    assert "تایید شد" in res5["text"]


@pytest.mark.asyncio
async def test_bot_02_vip_paywall_flow():
    """Test VIP Paywall subscription flow with Telegram Stars."""
    user_id = 1002

    # 1. /start
    res1 = await DISPATCHER.dispatch_update("vip_paywall", {
        "message": {"from": {"id": user_id, "first_name": "VipUser"}, "text": "/start"}
    })
    assert "VIP" in res1["text"]

    # 2. Select 1-Month Plan with Stars
    res2 = await DISPATCHER.dispatch_update("vip_paywall", {
        "callback_query": {"from": {"id": user_id}, "data": "pay_vip_stars_plan_1m"}
    })
    assert "موفقیت" in res2["text"]
    assert "t.me/+VIP" in res2["text"]

    # 3. Check status
    res3 = await DISPATCHER.dispatch_update("vip_paywall", {
        "message": {"from": {"id": user_id}, "text": "👤 وضعیت اشتراک من"}
    })
    assert "فعال" in res3["text"]


@pytest.mark.asyncio
async def test_bot_03_ai_gateway_flow():
    """Test AI Gateway credit deduction and task execution."""
    user_id = 1003

    # 1. /start
    res1 = await DISPATCHER.dispatch_update("ai_gateway", {
        "message": {"from": {"id": user_id, "first_name": "AiUser"}, "text": "/start"}
    })
    assert "هوش مصنوعی" in res1["text"]

    # 2. Select copywriting tool
    res2 = await DISPATCHER.dispatch_update("ai_gateway", {
        "callback_query": {"from": {"id": user_id}, "data": "tool_copywriting"}
    })
    assert "موضوع" in res2["text"]

    # 3. Submit Prompt
    res3 = await DISPATCHER.dispatch_update("ai_gateway", {
        "message": {"from": {"id": user_id}, "text": "سایت فروشگاهی لباس"}
    })
    assert "باقی‌مانده اعتبار" in res3["text"]


@pytest.mark.asyncio
async def test_bot_04_kata_runner_flow():
    """Test Code Kata Python sandbox execution."""
    user_id = 1004

    # 1. /start
    res1 = await DISPATCHER.dispatch_update("kata_runner", {
        "message": {"from": {"id": user_id, "first_name": "DevUser"}, "text": "/start"}
    })
    assert "کاتا" in res1["text"]

    # 2. Solve Two Sum
    res2 = await DISPATCHER.dispatch_update("kata_runner", {
        "callback_query": {"from": {"id": user_id}, "data": "solve_kata_01"}
    })
    assert "مسئله" in res2["text"]

    # 3. Submit correct code
    solution_code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    res3 = await DISPATCHER.dispatch_update("kata_runner", {
        "message": {"from": {"id": user_id}, "text": solution_code}
    })
    assert "تبریک" in res3["text"]
    assert "XP" in res3["text"]


@pytest.mark.asyncio
async def test_bot_05_license_reminder_flow():
    """Test B2B Expiry reminder creation."""
    user_id = 1005

    # 1. /start
    res1 = await DISPATCHER.dispatch_update("license_reminder", {
        "message": {"from": {"id": user_id, "first_name": "BizUser"}, "text": "/start"}
    })
    assert "انقضا" in res1["text"]

    # 2. Add Reminder
    res2 = await DISPATCHER.dispatch_update("license_reminder", {
        "message": {"from": {"id": user_id}, "text": "➕ ثبت یادآور انقضا جدید"}
    })
    assert "عنوان" in res2["text"]

    # 3. Enter Title
    res3 = await DISPATCHER.dispatch_update("license_reminder", {
        "message": {"from": {"id": user_id}, "text": "تمدید سرور آلمان"}
    })
    assert "چند روز دیگر" in res3["text"]

    # 4. Enter Days
    res4 = await DISPATCHER.dispatch_update("license_reminder", {
        "message": {"from": {"id": user_id}, "text": "30"}
    })
    assert "فعال شد" in res4["text"]
