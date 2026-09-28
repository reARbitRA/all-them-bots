from __future__ import annotations

from src.core.hub_router import HUB_ROUTER, MEGA_HUBS
from src.core.omni_catalog import OMNI_CATALOG


def test_catalogue_total_and_source_router_hub_counts() -> None:
    assert len(OMNI_CATALOG) == 445
    hub_summary = HUB_ROUTER.get_hub_summary()
    assert len(hub_summary) == 15 == len(MEGA_HUBS)
    assert sum(hub["bot_count"] for hub in hub_summary.values()) == len(OMNI_CATALOG)


def test_current_exact_per_hub_counts_are_documented_runtime_truth() -> None:
    hub_counts = {hub_key: hub["bot_count"] for hub_key, hub in HUB_ROUTER.get_hub_summary().items()}
    assert hub_counts == {
        "hub_01_commerce": 8,
        "hub_02_vip_paywalls": 5,
        "hub_03_ai_studio": 93,
        "hub_04_coding_katas": 0,
        "hub_05_b2b_compliance": 6,
        "hub_06_fintech_crypto": 2,
        "hub_07_education_learning": 12,
        "hub_08_growth_leadgen": 2,
        "hub_09_health_fitness": 3,
        "hub_10_real_estate_rental": 2,
        "hub_11_productivity_search": 4,
        "hub_12_media_optimization": 1,
        "hub_13_rubika_baleh_local": 50,
        "hub_14_gamification_leagues": 2,
        "hub_15_agency_factory": 255,
    }
