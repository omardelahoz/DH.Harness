import pytest
from dh_harness.core.contracts import QualityControlStatus, QualityReport
from dh_harness.quality.engine import QualityEngine, IndependentReviewRequiredError

def test_quality_engine_evaluates_all_pass():
    engine = QualityEngine()
    controls = {
        "Compilation": QualityControlStatus.PASS,
        "Unit Tests": QualityControlStatus.PASS,
        "Static Analysis": QualityControlStatus.PASS,
        "Security Scanning": QualityControlStatus.PASS,
        "Dependency Audit": QualityControlStatus.PASS,
        "Accessibility": QualityControlStatus.PASS,
    }
    report = engine.evaluate_task(
        task_id="DH-008",
        control_results=controls,
        author="backend-developer",
        evaluated_by="qa-engineer"
    )

    assert report.task_id == "DH-008"
    assert report.passed is True
    assert report.score == 100.0
    assert len(report.critical_failures) == 0
    assert engine.can_deliver(report) is True

def test_quality_engine_blocks_critical_fail_despite_high_score():
    engine = QualityEngine()
    controls = {
        "Compilation": QualityControlStatus.PASS,
        "Unit Tests": QualityControlStatus.PASS,
        "Static Analysis": QualityControlStatus.PASS,
        "Formatting": QualityControlStatus.PASS,
        "Lint": QualityControlStatus.PASS,
        "Security Scanning": QualityControlStatus.FAIL,  # Critical control failed!
        "Dependency Audit": QualityControlStatus.PASS,
        "Performance": QualityControlStatus.PASS,
    }
    report = engine.evaluate_task(
        task_id="DH-008",
        control_results=controls,
        author="backend-developer",
        evaluated_by="security-engineer"
    )

    # Even if 7 of 8 pass, a critical failure MUST block delivery (info.md § 15)
    assert report.passed is False
    assert "Security Scanning" in report.critical_failures
    assert engine.can_deliver(report) is False

def test_quality_engine_enforces_independent_evaluation():
    engine = QualityEngine()
    controls = {
        "Compilation": QualityControlStatus.PASS,
        "Unit Tests": QualityControlStatus.PASS,
    }

    # Author cannot evaluate their own work (Zero-Trust rule)
    with pytest.raises(IndependentReviewRequiredError):
        engine.evaluate_task(
            task_id="DH-008",
            control_results=controls,
            author="backend-developer",
            evaluated_by="backend-developer"
        )

def test_quality_engine_calculates_score_with_warn_and_na():
    engine = QualityEngine()
    controls = {
        "Compilation": QualityControlStatus.PASS,
        "Unit Tests": QualityControlStatus.PASS,
        "Performance": QualityControlStatus.WARN,        # Warning penalizes partially
        "Mutation Testing": QualityControlStatus.NOT_APPLICABLE, # N/A does not penalize
    }
    report = engine.evaluate_task(
        task_id="DH-008",
        control_results=controls,
        author="backend-developer",
        evaluated_by="qa-engineer"
    )

    assert report.passed is True
    assert 70.0 <= report.score < 100.0
    assert len(report.critical_failures) == 0
    assert engine.can_deliver(report) is True
