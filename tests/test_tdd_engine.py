import pytest
from dh_harness.core.contracts import TDDPhase
from dh_harness.tdd.engine import TDDEngine, TDDCycleViolationError

def test_tdd_engine_normal_cycle():
    engine = TDDEngine()
    assert engine.current_phase == TDDPhase.REQUIREMENT

    # Move to RED
    engine.transition_to(TDDPhase.TEST_RED)
    assert engine.current_phase == TDDPhase.TEST_RED
    engine.record_test_failure("AssertionError: expected True but got False")

    # Move to GREEN
    engine.transition_to(TDDPhase.IMPLEMENT_GREEN)
    assert engine.current_phase == TDDPhase.IMPLEMENT_GREEN
    engine.record_test_success()

    # Move to REFACTOR
    engine.transition_to(TDDPhase.REFACTOR)
    assert engine.current_phase == TDDPhase.REFACTOR

    # Move to VERIFY
    engine.transition_to(TDDPhase.VERIFY)
    assert engine.current_phase == TDDPhase.VERIFY

    # Complete
    engine.transition_to(TDDPhase.DONE)
    assert engine.current_phase == TDDPhase.DONE

def test_tdd_engine_blocks_green_without_red_evidence():
    engine = TDDEngine()
    engine.transition_to(TDDPhase.TEST_RED)

    # Attempting to move to IMPLEMENT_GREEN without recorded RED failure evidence must fail
    with pytest.raises(TDDCycleViolationError) as exc_info:
        engine.transition_to(TDDPhase.IMPLEMENT_GREEN)
    assert "RED" in str(exc_info.value)

def test_tdd_engine_blocks_skip_phases():
    engine = TDDEngine()
    with pytest.raises(TDDCycleViolationError):
        # Cannot jump from REQUIREMENT straight to DONE
        engine.transition_to(TDDPhase.DONE)
