import pytest
from dh_harness.core.contracts import TDDPhase
from dh_harness.tdd.complexity import ComplexityAnalyzer
from dh_harness.tdd.engine import TDDEngine, TDDCycleViolationError

def test_complexity_analyzer_calculates_simple_function():
    code = """
def simple_add(a, b):
    return a + b
"""
    analyzer = ComplexityAnalyzer()
    report = analyzer.analyze_python_code(code, "simple.py")
    assert report.passed is True
    assert len(report.violations) == 0

def test_complexity_analyzer_detects_nested_cyclomatic_complexity():
    # Construct a function with McCabe score > 10
    code = """
def complex_decision(x, y, z):
    if x > 1:
        if y > 2:
            if z > 3:
                return 1
            else:
                return 2
        elif y < 0:
            for i in range(10):
                if i % 2 == 0:
                    return 3
    elif x < -1:
        while z > 0:
            if y == 5:
                return 4
            z -= 1
    return 0
"""
    analyzer = ComplexityAnalyzer(max_complexity=5)
    report = analyzer.analyze_python_code(code, "complex.py")
    assert report.passed is False
    assert len(report.violations) == 1
    assert report.violations[0].function_name == "complex_decision"
    assert report.violations[0].complexity_score > 5

def test_tdd_engine_enforces_refactor_when_complexity_is_high():
    engine = TDDEngine(initial_phase=TDDPhase.IMPLEMENT_GREEN)
    engine.record_test_failure("AssertionError in test")
    engine.record_test_success()

    # If complexity violation is recorded
    engine.record_complexity_violation("complex.py", "bloated_func", 15)

    # Attempting to jump directly to VERIFY without REFACTOR must be blocked
    with pytest.raises(TDDCycleViolationError) as exc_info:
        engine.transition_to(TDDPhase.VERIFY)
    assert "refactor" in str(exc_info.value).lower()

    # Moving to REFACTOR, resolving it, then VERIFY succeeds
    engine.transition_to(TDDPhase.REFACTOR)
    engine.resolve_complexity_violations()
    engine.transition_to(TDDPhase.VERIFY)
    assert engine.current_phase == TDDPhase.VERIFY
