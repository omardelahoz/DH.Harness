from __future__ import annotations
from typing import Optional, List, Dict
from dh_harness.core.contracts import TDDPhase

class TDDCycleViolationError(Exception):
    """Raised when a TDD phase transition violates methodology rules."""
    pass

class TDDEngine:
    """
    State machine and enforcement engine for strict Test-Driven Development (TDD).
    Sequence: REQUIREMENT -> TEST_RED -> IMPLEMENT_GREEN -> REFACTOR -> VERIFY -> DONE
    """

    VALID_TRANSITIONS: Dict[TDDPhase, List[TDDPhase]] = {
        TDDPhase.REQUIREMENT: [TDDPhase.TEST_RED],
        TDDPhase.TEST_RED: [TDDPhase.IMPLEMENT_GREEN],
        TDDPhase.IMPLEMENT_GREEN: [TDDPhase.REFACTOR, TDDPhase.VERIFY],
        TDDPhase.REFACTOR: [TDDPhase.VERIFY, TDDPhase.IMPLEMENT_GREEN],
        TDDPhase.VERIFY: [TDDPhase.DONE, TDDPhase.TEST_RED, TDDPhase.REFACTOR],
        TDDPhase.DONE: [TDDPhase.REQUIREMENT],
    }

    def __init__(self, initial_phase: TDDPhase = TDDPhase.REQUIREMENT):
        self.current_phase = initial_phase
        self.red_evidence: Optional[str] = None
        self.green_evidence: Optional[str] = None
        self.history: List[Dict[str, str]] = []

    def record_test_failure(self, error_message: str):
        """Records evidence of failing test (RED state)."""
        self.red_evidence = error_message
        self.history.append({"phase": "TEST_RED", "evidence": error_message})

    def record_test_success(self):
        """Records evidence that test has passed (GREEN state)."""
        self.green_evidence = "Tests passed successfully (exit code 0)"
        self.history.append({"phase": "IMPLEMENT_GREEN", "evidence": self.green_evidence})

    def transition_to(self, next_phase: TDDPhase):
        """Validates and applies phase transition."""
        allowed = self.VALID_TRANSITIONS.get(self.current_phase, [])
        if next_phase not in allowed:
            raise TDDCycleViolationError(
                f"Illegal TDD transition from {self.current_phase.value} to {next_phase.value}. "
                f"Allowed transitions: {[p.value for p in allowed]}"
            )

        # Enforce RED evidence before moving to IMPLEMENT_GREEN
        if next_phase == TDDPhase.IMPLEMENT_GREEN:
            if not self.red_evidence:
                raise TDDCycleViolationError(
                    "Cannot transition to IMPLEMENT_GREEN without recorded RED test failure evidence. "
                    "Write a failing test first."
                )

        self.current_phase = next_phase
        self.history.append({"transition_to": next_phase.value})
