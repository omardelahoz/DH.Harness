from __future__ import annotations
import os
import sys
import sqlite3
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from pydantic import BaseModel

GENESIS_HASH = "0" * 64

class InvalidRedEvidenceError(Exception):
    """Raised when attempting to record invalid RED phase evidence (e.g. exit code 0 or collection/import crashes)."""
    pass

class EvidenceRecord(BaseModel):
    task_id: str
    test_file: str
    failure_log: str
    exit_code: int
    sha256_hash: str
    timestamp: str
    prev_hash: str = GENESIS_HASH
    git_tree_hash: str = "NO_GIT"
    status: str = "ACTIVE"

class TDDEvidenceVault:
    """
    Cryptographic evidence vault with SQLite persistence and hash chaining
    for recording, validating, and verifying TDD RED failure states.
    Complies with Section 7.5 of info.md and deterministic TDD governance.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = self._resolve_db_path(db_path)
        self._records: Dict[str, EvidenceRecord] = {}
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()
        self._load_active_records()

    def _resolve_db_path(self, db_path: Optional[str]) -> str:
        if db_path is not None:
            return db_path
        env_path = os.environ.get("DH_HARNESS_TDD_DB")
        if env_path:
            return env_path
        
        # Default persistence path
        candidate_dir = os.path.join(".project", "memory")
        if os.path.exists(candidate_dir):
            return os.path.join(candidate_dir, "harness.db")
        return ":memory:"

    def _get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            if self.db_path != ":memory:":
                os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self):
        """Closes the underlying database connection."""
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def __del__(self):
        self.close()

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tdd_evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    test_file TEXT NOT NULL,
                    exit_code INTEGER NOT NULL,
                    failure_log TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    git_tree_hash TEXT NOT NULL,
                    sha256_hash TEXT NOT NULL UNIQUE,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ACTIVE'
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tdd_evidence_task ON tdd_evidence(task_id);")
            conn.commit()

    def _load_active_records(self):
        """Loads latest ACTIVE records into in-memory cache for high-frequency queries."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT task_id, test_file, exit_code, failure_log, prev_hash,
                       git_tree_hash, sha256_hash, timestamp, status
                FROM tdd_evidence
                WHERE status = 'ACTIVE'
                ORDER BY id ASC
            """)
            for row in cur.fetchall():
                rec = EvidenceRecord(
                    task_id=row["task_id"],
                    test_file=row["test_file"],
                    exit_code=row["exit_code"],
                    failure_log=row["failure_log"],
                    prev_hash=row["prev_hash"],
                    git_tree_hash=row["git_tree_hash"],
                    sha256_hash=row["sha256_hash"],
                    timestamp=row["timestamp"],
                    status=row["status"]
                )
                self._records[rec.task_id] = rec

    def _get_latest_hash(self) -> str:
        """Returns the SHA-256 hash of the most recent evidence record for chaining."""
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT sha256_hash FROM tdd_evidence ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                return row["sha256_hash"]
        return GENESIS_HASH

    def _get_git_tree_hash(self) -> str:
        """Resolves current git commit or tree hash."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
        return "NO_GIT"

    def _validate_legitimate_failure(self, combined_log: str, exit_code: int):
        """
        Validates that a test run produced a legitimate test assertion failure
        rather than passing (exit_code 0) or an environmental crash (collection/syntax error).
        """
        if exit_code == 0:
            raise InvalidRedEvidenceError(
                "Cannot record RED evidence: Test exited with exit code 0 (passing test). "
                "A legitimate RED state requires a failing test assertion."
            )

        log_upper = combined_log.upper()
        # Markers of legitimate assertion or expectation failures
        assertion_markers = [
            "ASSERTIONERROR",
            "ASSERT ",
            "FAILED ",
            "FAIL:",
            "FAILS:",
            "FAILED (",
            "DID NOT RAISE",
            "EXPECTED EXCEPTION",
            "FAILURE:"
        ]
        has_assertion = any(marker in log_upper for marker in assertion_markers)

        # Fatal collection/environment crash markers
        crash_markers = [
            "ERROR COLLECTING ",
            "PYTEST: ERROR:",
            "USAGEERROR:",
            "INTERNALERROR:",
        ]
        has_fatal_crash = any(marker in log_upper for marker in crash_markers)

        # If there's a fatal crash or absence of actual test assertion failure, reject in strict validation
        if has_fatal_crash or not has_assertion:
            raise InvalidRedEvidenceError(
                "Cannot record RED evidence: Test runner exited with non-zero code but did not report a "
                "legitimate test assertion failure (requires AssertionError, FAILED, or test expectation failure)."
            )

    def record_red_evidence(
        self,
        task_id: str,
        test_file: str,
        stdout: str,
        stderr: str,
        exit_code: int,
        strict_validation: bool = False
    ) -> EvidenceRecord:
        """
        Records failure evidence from a RED test execution with cryptographic chaining and SQLite persistence.
        Raises InvalidRedEvidenceError if exit_code == 0 or if strict_validation fails.
        """
        combined_log = (stderr + "\n" + stdout).strip()

        if strict_validation:
            self._validate_legitimate_failure(combined_log, exit_code)
        elif exit_code == 0:
            raise InvalidRedEvidenceError(
                f"Cannot record RED evidence for task '{task_id}': Test exited with code 0 (passing test). "
                f"A legitimate RED state requires a failing test."
            )

        ts = datetime.now().isoformat()
        prev_hash = self._get_latest_hash()
        git_tree = self._get_git_tree_hash()

        # Compute deterministic content digest
        normalized_log = combined_log.replace("\r\n", "\n").strip()
        log_digest = hashlib.sha256(normalized_log.encode("utf-8")).hexdigest()
        
        # Block hash calculation with chaining
        block_raw = f"{prev_hash}:{task_id}:{test_file}:{exit_code}:{log_digest}:{git_tree}"
        digest = hashlib.sha256(block_raw.encode("utf-8")).hexdigest()

        record = EvidenceRecord(
            task_id=task_id,
            test_file=test_file,
            failure_log=combined_log,
            exit_code=exit_code,
            sha256_hash=digest,
            timestamp=ts,
            prev_hash=prev_hash,
            git_tree_hash=git_tree,
            status="ACTIVE"
        )

        with self._get_connection() as conn:
            # Supersede any previous active record for this task_id
            conn.execute(
                "UPDATE tdd_evidence SET status = 'SUPERSEDED' WHERE task_id = ? AND status = 'ACTIVE'",
                (task_id,)
            )
            conn.execute("""
                INSERT INTO tdd_evidence (
                    task_id, test_file, exit_code, failure_log, prev_hash,
                    git_tree_hash, sha256_hash, timestamp, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.task_id, record.test_file, record.exit_code, record.failure_log,
                record.prev_hash, record.git_tree_hash, record.sha256_hash,
                record.timestamp, record.status
            ))
            conn.commit()

        self._records[task_id] = record
        return record

    def run_and_record_red(
        self,
        task_id: str,
        test_target: str,
        runner_cmd: Optional[List[str]] = None,
        cwd: Optional[str] = None
    ) -> EvidenceRecord:
        """
        Executes test runner, validates legitimate RED failure, and records chained evidence.
        """
        if runner_cmd is None:
            runner_cmd = [sys.executable, "-m", "pytest", test_target]

        try:
            res = subprocess.run(
                runner_cmd,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60
            )
            stdout = res.stdout or ""
            stderr = res.stderr or ""
            exit_code = res.returncode
        except Exception as e:
            raise InvalidRedEvidenceError(f"Failed to execute test runner: {e}")

        # Validate that the test failed legitimately
        combined_log = (stderr + "\n" + stdout).strip()
        self._validate_legitimate_failure(combined_log, exit_code)

        return self.record_red_evidence(
            task_id=task_id,
            test_file=test_target,
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            strict_validation=True
        )

    def verify_evidence_chain(self) -> Tuple[bool, Optional[str]]:
        """
        Audits cryptographic integrity of the entire evidence chain in SQLite.
        Returns (True, None) if completely valid, or (False, reason) if tampered.
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, task_id, test_file, exit_code, failure_log, prev_hash,
                       git_tree_hash, sha256_hash
                FROM tdd_evidence
                ORDER BY id ASC
            """)
            rows = cur.fetchall()

        expected_prev = GENESIS_HASH
        for row in rows:
            if row["prev_hash"] != expected_prev:
                return False, f"Broken chain link at id {row['id']}: expected prev_hash {expected_prev}, got {row['prev_hash']}"

            normalized_log = row["failure_log"].replace("\r\n", "\n").strip()
            log_digest = hashlib.sha256(normalized_log.encode("utf-8")).hexdigest()
            block_raw = f"{row['prev_hash']}:{row['task_id']}:{row['test_file']}:{row['exit_code']}:{log_digest}:{row['git_tree_hash']}"
            expected_hash = hashlib.sha256(block_raw.encode("utf-8")).hexdigest()

            if expected_hash != row["sha256_hash"]:
                return False, f"Tampered hash at id {row['id']}: expected {expected_hash}, stored {row['sha256_hash']}"

            expected_prev = row["sha256_hash"]

        return True, None

    def get_active_red_evidence(self, task_id: str) -> Optional[EvidenceRecord]:
        """Retrieves active RED evidence for task."""
        if task_id in self._records:
            return self._records[task_id]
        
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT task_id, test_file, exit_code, failure_log, prev_hash,
                       git_tree_hash, sha256_hash, timestamp, status
                FROM tdd_evidence
                WHERE task_id = ? AND status = 'ACTIVE'
                ORDER BY id DESC LIMIT 1
            """, (task_id,))
            row = cur.fetchone()
            if row:
                rec = EvidenceRecord(
                    task_id=row["task_id"],
                    test_file=row["test_file"],
                    exit_code=row["exit_code"],
                    failure_log=row["failure_log"],
                    prev_hash=row["prev_hash"],
                    git_tree_hash=row["git_tree_hash"],
                    sha256_hash=row["sha256_hash"],
                    timestamp=row["timestamp"],
                    status=row["status"]
                )
                self._records[task_id] = rec
                return rec
        return None

    def has_valid_red_evidence(self, task_id: str) -> bool:
        """Returns True if there is a verified RED failure on record for task."""
        record = self.get_active_red_evidence(task_id)
        return record is not None and record.exit_code != 0

    def clear_evidence(self, task_id: str):
        """Clears evidence once GREEN is verified."""
        if task_id in self._records:
            del self._records[task_id]

        with self._get_connection() as conn:
            conn.execute(
                "UPDATE tdd_evidence SET status = 'CLEARED' WHERE task_id = ? AND status = 'ACTIVE'",
                (task_id,)
            )
            conn.commit()

