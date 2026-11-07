from __future__ import annotations
import re
from typing import Optional, List, Tuple
from dh_harness.core.contracts import DestructiveOpCheckResult

class DestructiveOperationBlockedError(Exception):
    """Raised when an agent attempts to execute an unauthorized destructive operation (info.md § 14.5)."""
    pass

DESTRUCTIVE_RULES: List[Tuple[str, re.Pattern, str]] = [
    # Destructive SQL
    (
        "SQL_DROP_DATABASE",
        re.compile(r"(?i)\bDROP\s+(?:DATABASE|SCHEMA)\b"),
        "Dropping a database or schema is a permanent, high-impact operation."
    ),
    (
        "SQL_DROP_TABLE",
        re.compile(r"(?i)\bDROP\s+TABLE\b"),
        "Dropping a database table causes irreversible data loss."
    ),
    (
        "SQL_TRUNCATE_TABLE",
        re.compile(r"(?i)\bTRUNCATE\s+TABLE\b"),
        "Truncating a table deletes all rows without row-level triggers."
    ),
    (
        "SQL_DELETE_WITHOUT_WHERE",
        re.compile(r"(?i)^\s*DELETE\s+FROM\s+[a-zA-Z0-9_\.]+\s*;?\s*$"),
        "DELETE statement without a WHERE clause causes total table wipeout."
    ),

    # Destructive Git operations
    (
        "GIT_FORCE_PUSH",
        re.compile(r"\bgit\s+push\s+.*(?:--force|-f)\b"),
        "Force pushing rewrites remote history and can overwrite peer commits."
    ),
    (
        "GIT_DELETE_PROTECTED_BRANCH",
        re.compile(r"\bgit\s+branch\s+(?:-D|-d)\s+(?:main|master|release|production|prod)\b"),
        "Deleting a protected branch causes repository disruption."
    ),

    # Destructive filesystem operations
    (
        "FS_MASS_DELETE",
        re.compile(r"(?:rm\s+-rf\s+(?:/|/\*|~\*?)|del\s+.*[a-zA-Z]:\\)"),
        "Mass filesystem deletion targeting root directories is strictly prohibited."
    ),
]

class DestructiveOperationGuard:
    """
    Fail-Closed guard intercepting and blocking dangerous SQL, Git, and filesystem commands
    unless explicitly authorized by a human supervisor (info.md § 14.5).
    """

    def check_command(self, command: str) -> DestructiveOpCheckResult:
        """Analyzes a command string to determine if it constitutes a destructive action."""
        cleaned = command.strip()

        for op_type, pattern, reason in DESTRUCTIVE_RULES:
            if pattern.search(cleaned):
                return DestructiveOpCheckResult(
                    command=cleaned,
                    is_destructive=True,
                    operation_type=op_type,
                    reason=reason
                )

        return DestructiveOpCheckResult(
            command=cleaned,
            is_destructive=False,
            operation_type=None,
            reason=""
        )

    def guard(self, command: str, authorized: bool = False) -> None:
        """
        Validates command safety. Raises DestructiveOperationBlockedError
        if destructive and not explicitly authorized.
        """
        result = self.check_command(command)
        if result.is_destructive and not authorized:
            raise DestructiveOperationBlockedError(
                f"Destructive operation blocked [{result.operation_type}]: {result.reason} "
                f"Command: '{command}'. Explicit human authorization is required."
            )
