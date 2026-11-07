import pytest
from dh_harness.release.hardening import ReleaseHardeningEngine, ReleaseManager

def test_hardening_engine_validates_global_acceptance_criteria():
    engine = ReleaseHardeningEngine()
    demo_result = engine.run_acceptance_scenario_demo()

    assert demo_result.get("all_scenarios_passed") is True
    assert demo_result.get("scenario_count") == 8
    scenarios = demo_result.get("scenarios", {})
    assert scenarios.get("interaction_classification") == "PASS"
    assert scenarios.get("dag_orchestration") == "PASS"
    assert scenarios.get("tdd_guard") == "PASS"
    assert scenarios.get("false_test_detection") == "PASS"
    assert scenarios.get("agent_delegation") == "PASS"
    assert scenarios.get("memory_engine") == "PASS"
    assert scenarios.get("security_scanner") == "PASS"
    assert scenarios.get("git_dod") == "PASS"

def test_release_manager_builds_valid_manifest():
    manager = ReleaseManager()
    manifest = manager.build_release_manifest(version="1.0.0")

    assert manifest.version == "1.0.0"
    assert bool(manifest.git_commit)
    assert manifest.tests_count >= 130
    assert manifest.adrs_count >= 12
    assert "MIT" in manifest.spdx_compliance or "Apache" in manifest.spdx_compliance
