import pytest
from dh_harness.health.engine import ProjectHealthEngine

def test_health_engine_evaluates_clean_workspace():
    engine = ProjectHealthEngine()
    health = engine.evaluate_project_health(workspace=".")

    assert health.overall_score >= 95.0
    assert health.security_score == 100.0
    assert health.architecture_health == 100.0
    assert health.git_governance_score >= 90.0
    assert len(health.active_blockers) == 0
    assert health.is_production_ready is True

def test_health_engine_detects_blockers_on_dirty_workspace(monkeypatch):
    engine = ProjectHealthEngine()

    # Simulate presence of a secret finding and layer violation
    monkeypatch.setattr(
        engine,
        "_check_security",
        lambda ws: (50.0, ["Exposed token in config.env"])
    )
    monkeypatch.setattr(
        engine,
        "_check_architecture",
        lambda ws: (70.0, ["Direct DB access in UserController"])
    )

    health = engine.evaluate_project_health(workspace=".")

    assert health.is_production_ready is False
    assert len(health.active_blockers) >= 2
    assert "Exposed token in config.env" in health.active_blockers
    assert health.overall_score < 90.0

def test_health_engine_subscore_breakdown():
    engine = ProjectHealthEngine()
    health = engine.evaluate_project_health(workspace=".")

    assert 0.0 <= health.tdd_compliance <= 100.0
    assert 0.0 <= health.security_score <= 100.0
    assert 0.0 <= health.architecture_health <= 100.0
    assert 0.0 <= health.git_governance_score <= 100.0
    assert 0.0 <= health.uiux_score <= 100.0

def test_health_engine_tdd_detects_missing_tests(tmp_path):
    # Workspace with src/ but no tests/
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text("def run(): pass")

    engine = ProjectHealthEngine()
    score, blockers = engine._check_tdd(str(tmp_path))

    assert score < 100.0
    assert any("No 'tests/' directory found" in b for b in blockers)

def test_health_engine_tdd_detects_false_test_defects(tmp_path):
    # Workspace with tests containing a cosmetic/false test
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text("def run(): pass")

    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_fake.py").write_text("def test_dummy(): assert True")

    engine = ProjectHealthEngine()
    score, blockers = engine._check_tdd(str(tmp_path))

    assert score < 100.0
    assert any("False test defect" in b for b in blockers)
