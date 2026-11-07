from __future__ import annotations
import re
from typing import Dict, Any, List
from dh_harness.core.contracts import QualityGateResult, HierarchicalTask, TaskState
from dh_harness.tdd.detector import FalseTestDetector

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

class SecretScanningGate:
    """
    Scans source code and configuration for leaked credentials, private keys, or API tokens.
    Complies with Section 14 of info.md (Security & Secrets Engine).
    """

    PATTERNS = [
        (r"gh[pousr]_[A-Za-z0-9_]{36,255}", "GitHub Token"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
        (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private Key"),
        (r"(?:api_key|apikey|secret|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "High Entropy Secret/Password"),
    ]

    def scan_text(self, content: str) -> QualityGateResult:
        detected = []
        for pattern, label in self.PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                detected.append(label)

        passed = len(detected) == 0
        return QualityGateResult(
            gate_name="SecretScanning",
            passed=passed,
            details={"detected_secrets": detected},
            message="No secrets detected." if passed else f"Secret Scanning Alert: Found {', '.join(detected)}."
        )

class TestQualityGate:
    """
    Audits test suites to eliminate false or cosmetic tests.
    Complies with Section 7.4 of info.md.
    """
    __test__ = False

    def __init__(self):
        self.detector = FalseTestDetector()

    def audit_test_file(self, file_path: str) -> QualityGateResult:
        defects = self.detector.inspect_file(file_path)
        passed = len(defects) == 0
        descriptions = [f"{d.defect_type.value}: {d.description}" for d in defects]
        return QualityGateResult(
            gate_name="TestQuality",
            passed=passed,
            details={"defects": [d.model_dump() for d in defects]},
            message="All tests passed semantic quality checks." if passed else f"Test Quality Failed: {'; '.join(descriptions)}"
        )

    def audit_directory(self, dir_path: str) -> QualityGateResult:
        dir_defects = self.detector.inspect_directory(dir_path)
        total_defects = sum(len(d) for d in dir_defects.values())
        passed = total_defects == 0
        return QualityGateResult(
            gate_name="TestQualitySuite",
            passed=passed,
            details={"files_with_defects": list(dir_defects.keys())},
            message="Test suite is free of cosmetic or false tests." if passed else f"Found {total_defects} test defect(s) in suite."
        )
