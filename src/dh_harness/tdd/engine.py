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
        self.complexity_violations: List[Dict[str, Any]] = []

    def record_test_failure(self, error_message: str):
        """Records evidence of failing test (RED state)."""
        self.red_evidence = error_message
        self.history.append({"phase": "TEST_RED", "evidence": error_message})

    def record_test_success(self):
        """Records evidence that test has passed (GREEN state)."""
        self.green_evidence = "Tests passed successfully (exit code 0)"
        self.history.append({"phase": "IMPLEMENT_GREEN", "evidence": self.green_evidence})

    def record_complexity_violation(self, file_path: str, function_name: str, score: int):
        """Records cyclomatic complexity violation requiring REFACTOR phase."""
        self.complexity_violations.append({
            "file": file_path,
            "function": function_name,
            "score": score
        })
        self.history.append({"complexity_violation": f"{file_path}:{function_name} score={score}"})

    def resolve_complexity_violations(self):
        """Marks complexity violations as resolved after clean refactoring."""
        self.complexity_violations.clear()
        self.history.append({"complexity_status": "CLEAN_REFACTORED"})

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

        # Enforce REFACTOR if complexity violations exist before VERIFY
        if next_phase == TDDPhase.VERIFY:
            if self.complexity_violations:
                raise TDDCycleViolationError(
                    f"Cannot transition to VERIFY with active cyclomatic complexity violations "
                    f"({len(self.complexity_violations)} function(s) exceeding threshold). "
                    f"Perform REFACTOR phase first."
                )

        self.current_phase = next_phase
        self.history.append({"transition_to": next_phase.value})
