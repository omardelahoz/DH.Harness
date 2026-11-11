from __future__ import annotations
import os
from typing import Optional
from pydantic import BaseModel
from dh_harness.core.contracts import InteractionMode
from dh_harness.tdd.evidence import TDDEvidenceVault

class TDDGuardViolationError(Exception):
    """Raised when an unauthorized or unverified code modification is blocked."""
    pass

class GuardDecision(BaseModel):
    allowed: bool
    reason: str

class CodeModificationGuard:
    """
    Guards codebase modifications by strictly enforcing TDD RED evidence preconditions.
    Complies with Section 7.1, 7.3 and 18.1 of info.md.
    """

    def __init__(self, evidence_vault: Optional[TDDEvidenceVault] = None):
        self.evidence_vault = evidence_vault or TDDEvidenceVault()

    def evaluate_modification(
        self,
        file_path: str,
        mode: InteractionMode = InteractionMode.DEVELOPMENT,
        task_id: Optional[str] = None
    ) -> GuardDecision:
        """
        Evaluates whether a file modification is permitted without raising exceptions.
        Returns a GuardDecision(allowed=bool, reason=str).
        """
        normalized_path = file_path.replace("\\", "/").lstrip("./")

        # 1. Test code files can always be written/modified to establish the RED state
        if normalized_path.startswith("tests/") or "/test_" in normalized_path or normalized_path.startswith("test_"):
            return GuardDecision(allowed=True, reason="Test code modification to author expectations or assertions.")

        # 2. Files outside src/ that are documentation or configuration are allowed
        is_src_file = normalized_path.startswith("src/") or "/src/" in normalized_path
        if not is_src_file and normalized_path.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".toml")):
            return GuardDecision(allowed=True, reason="Documentation or configuration file outside production code.")

        # 3. Investigation and Conversational modes prohibit production code modification
        if mode in (InteractionMode.CONVERSATIONAL, InteractionMode.INVESTIGATION):
            return GuardDecision(
                allowed=False,
                reason=(
                    f"Modifications to production code '{file_path}' are blocked in {mode.value} mode. "
                    f"Transition to BUG_FIX or DEVELOPMENT workflow first."
                )
            )

        # 4. For production code, require task_id and verified RED evidence
        if not task_id:
            return GuardDecision(
                allowed=False,
                reason=f"Cannot modify production code '{file_path}' without an active Task ID."
            )

        if not self.evidence_vault.has_valid_red_evidence(task_id):
            return GuardDecision(
                allowed=False,
                reason=(
                    f"TDD Guard Block: Cannot modify production file '{file_path}' for task '{task_id}'. "
                    f"No verified RED evidence found on record. Write a failing test and record RED evidence first "
                    f"(run 'dh-harness tdd red {task_id} <test_file>')."
                )
            )

        return GuardDecision(
            allowed=True,
            reason=f"Verified active RED test evidence exists for task '{task_id}'. Modification permitted."
        )

    def check_can_modify(
        self,
        file_path: str,
        mode: InteractionMode = InteractionMode.DEVELOPMENT,
        task_id: Optional[str] = None
    ) -> GuardDecision:
        """
        Validates modification permission. Raises TDDGuardViolationError if blocked.
        """
        decision = self.evaluate_modification(file_path=file_path, mode=mode, task_id=task_id)
        if not decision.allowed:
            raise TDDGuardViolationError(decision.reason)
        return decision
