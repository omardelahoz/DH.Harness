from __future__ import annotations
import os
from datetime import datetime
from typing import Dict, List, Optional, Set

from dh_harness.core.contracts import QualityControlStatus, QualityReport

class IndependentReviewRequiredError(Exception):
    """Raised when an author attempts to evaluate their own work (info.md § 15)."""
    pass

CRITICAL_CONTROLS: Set[str] = {
    "Compilation",
    "Unit Tests",
    "Security Scanning",
    "Dependency Audit",
    "Definition of Done",
    "Accessibility"
}

class QualityEngine:
    """
    Independent Quality Evaluation Engine (info.md § 15).
    Evaluates up to 15 controls across functional, architectural, security and visual domains.
    Enforces that critical FAILs block delivery and that review is strictly independent.
    """

    def evaluate_task(
        self,
        task_id: str,
        control_results: Dict[str, QualityControlStatus],
        author: str,
        evaluated_by: str
    ) -> QualityReport:
        """
        Evaluates the quality controls for a task.
        Enforces independent evaluation and zero tolerance for critical failures.
        """
        if not evaluated_by or author.strip().lower() == evaluated_by.strip().lower():
            raise IndependentReviewRequiredError(
                f"Evaluation for task '{task_id}' must be conducted by an independent reviewer, "
                f"not author '{author}'."
            )

        critical_failures: List[str] = []
        earned_points: float = 0.0
        applicable_count: int = 0

        for control, status in control_results.items():
            if status == QualityControlStatus.NOT_APPLICABLE:
                continue

            applicable_count += 1
            if status == QualityControlStatus.PASS:
                earned_points += 1.0
            elif status == QualityControlStatus.WARN:
                earned_points += 0.5
            elif status == QualityControlStatus.FAIL:
                if control in CRITICAL_CONTROLS:
                    critical_failures.append(control)

        score = round((earned_points / applicable_count * 100.0), 1) if applicable_count > 0 else 100.0
        passed = (len(critical_failures) == 0) and (score >= 70.0)

        return QualityReport(
            task_id=task_id,
            controls=control_results,
            passed=passed,
            critical_failures=critical_failures,
            score=score,
            evaluated_by=evaluated_by,
            timestamp=datetime.now().isoformat()
        )

    def can_deliver(self, report: QualityReport) -> bool:
        """
        Determines whether the deliverable is safe to merge/release.
        Returns False if any critical failure occurred, regardless of overall score.
        """
        return report.passed and (len(report.critical_failures) == 0)
