from __future__ import annotations
from typing import Dict, Any, List
from dh_harness.core.contracts import QualityGateResult, HierarchicalTask, TaskState

class QualityGateEngine:
    """
    Enforces quality standards, Definition of Done, and policy guards.
    Complies with Sections 11.6, 12 and 15 of info.md.
    """

    @staticmethod
    def validate_definition_of_done(task: HierarchicalTask) -> QualityGateResult:
        failures = []

        if not task.evidence:
            failures.append("Task lacks verified completion evidence in SQLite/AEE.")

        if task.state not in (TaskState.MERGED, TaskState.DONE):
            if not task.evidence:
                failures.append("Task is not merged or integrated.")

        passed = len(failures) == 0
        return QualityGateResult(
            gate_name="DefinitionOfDone",
            passed=passed,
            details={"task_id": task.id, "failures": failures},
            message="Definition of Done verified successfully" if passed else f"DoD Failed: {'; '.join(failures)}"
        )
