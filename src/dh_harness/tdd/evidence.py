from __future__ import annotations
import hashlib
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class InvalidRedEvidenceError(Exception):
    """Raised when attempting to record invalid RED phase evidence (e.g. exit code 0)."""
    pass

class EvidenceRecord(BaseModel):
    task_id: str
    test_file: str
    failure_log: str
    exit_code: int
    sha256_hash: str
    timestamp: str

class TDDEvidenceVault:
    """
    Cryptographic evidence vault for recording and validating TDD RED failure states.
    Complies with Section 7.5 of info.md:
    Persists task ID, failure reason, exit code, timestamp, and SHA-256 hash.
    """

    def __init__(self):
        self._records: Dict[str, EvidenceRecord] = {}

    def record_red_evidence(
        self,
        task_id: str,
        test_file: str,
        stdout: str,
        stderr: str,
        exit_code: int
    ) -> EvidenceRecord:
        """
        Records failure evidence from a RED test execution.
        Raises InvalidRedEvidenceError if exit_code == 0.
        """
        if exit_code == 0:
            raise InvalidRedEvidenceError(
                f"Cannot record RED evidence for task '{task_id}': Test exited with code 0 (passing test). "
                f"A legitimate RED state requires a failing test."
            )

        combined_log = (stderr + "\n" + stdout).strip()
        ts = datetime.now().isoformat()
        
        # Calculate SHA-256 digest
        hasher = hashlib.sha256()
        hasher.update(f"{task_id}:{test_file}:{exit_code}:{combined_log}:{ts}".encode("utf-8"))
        digest = hasher.hexdigest()

        record = EvidenceRecord(
            task_id=task_id,
            test_file=test_file,
            failure_log=combined_log,
            exit_code=exit_code,
            sha256_hash=digest,
            timestamp=ts
        )

        self._records[task_id] = record
        return record

    def get_active_red_evidence(self, task_id: str) -> Optional[EvidenceRecord]:
        """Retrieves active RED evidence for task."""
        return self._records.get(task_id)

    def has_valid_red_evidence(self, task_id: str) -> bool:
        """Returns True if there is a verified RED failure on record for task."""
        record = self._records.get(task_id)
        return record is not None and record.exit_code != 0

    def clear_evidence(self, task_id: str):
        """Clears evidence once GREEN is verified."""
        if task_id in self._records:
            del self._records[task_id]
