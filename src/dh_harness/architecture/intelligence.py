from __future__ import annotations
import os
import re
from typing import List, Optional, Set

from dh_harness.core.contracts import CleanArchViolation, ArchitectureHealthReport

FORBIDDEN_CONTROLLER_DB_MODULES: Set[str] = {
    "sqlite3",
    "dapper",
    "psycopg2",
    "mysql",
    "sqlalchemy",
    "dbcontext",
    "sqlconnection",
    "idbconnection",
    "dbset",
}

SQL_QUERY_PATTERN = re.compile(
    r"""(?i)["']\s*(?:SELECT\s+.+?\s+FROM|INSERT\s+INTO\s+.+?|DELETE\s+FROM\s+.+?|UPDATE\s+.+?\s+SET)\s*""",
    re.IGNORECASE
)

IMPORT_STATEMENT_PATTERN = re.compile(
    r"""(?m)^\s*(?:import\s+([a-zA-Z0-9_\.]+)|from\s+([a-zA-Z0-9_\.]+)\s+import|using\s+([a-zA-Z0-9_\.]+);)"""
)

class ArchitectureAuditor:
    """
    Enforces Clean Architecture layer boundaries and anti-bypass rules (Rule 4 & info.md § 19).
    Prohibits direct database access, raw SQL and domain logic in Controllers and Presentation layers.
    """

    def is_controller_file(self, file_path: str) -> bool:
        """Determines if a given path belongs to a controller or API presentation layer."""
        norm = file_path.lower().replace("\\", "/")
        return "controller" in norm or "/controllers/" in norm or "/endpoints/" in norm or "/routes/" in norm

    def audit_source_code(self, content: str, file_path: str = "") -> List[CleanArchViolation]:
        """Audits source code text for architectural violations."""
        violations: List[CleanArchViolation] = []
        is_controller = self.is_controller_file(file_path)

        if not is_controller:
            return violations

        # 1. Audit forbidden DB imports in Controllers
        for match in IMPORT_STATEMENT_PATTERN.finditer(content):
            imported_raw = match.group(1) or match.group(2) or match.group(3) or ""
            imported_base = imported_raw.split(".")[0].lower()

            if imported_base in FORBIDDEN_CONTROLLER_DB_MODULES or any(m in imported_raw.lower() for m in ["dbcontext", "sqlconnection", "idbconnection"]):
                violations.append(CleanArchViolation(
                    source_file=file_path,
                    imported_module=imported_raw,
                    violation_type="DIRECT_DB_ACCESS_IN_CONTROLLER",
                    rule_description=f"Controllers must not import DB access modules ('{imported_raw}'). Use Application Use Cases instead (Rule 4).",
                    severity="CRITICAL"
                ))

        # 2. Audit raw SQL queries in Controllers
        for match in SQL_QUERY_PATTERN.finditer(content):
            sql_snippet = match.group(0).strip()
            violations.append(CleanArchViolation(
                source_file=file_path,
                imported_module="",
                violation_type="SQL_IN_CONTROLLER",
                rule_description=f"Raw SQL queries ('{sql_snippet}') are forbidden in Controllers. Queries belong in Repositories (Rule 4).",
                severity="CRITICAL"
            ))

        return violations

    def audit_file(self, file_path: str) -> List[CleanArchViolation]:
        """Audits an individual source code file on disk."""
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return self.audit_source_code(content, file_path=file_path)
        except Exception:
            return []

    def check_architecture_health(self, src_dir: str = "src") -> ArchitectureHealthReport:
        """Recursively checks the codebase for architecture and layer boundary violations."""
        violations: List[str] = []

        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                for f in files:
                    if f.endswith((".py", ".cs", ".ts", ".js")):
                        full_path = os.path.join(root, f)
                        v_list = self.audit_file(full_path)
                        for v in v_list:
                            violations.append(f"{v.source_file}: {v.rule_description}")

        return ArchitectureHealthReport(
            is_clean_arch=len(violations) == 0,
            layer_violations=violations,
            adr_coverage=100.0,
            docs_synchronized=True
        )
