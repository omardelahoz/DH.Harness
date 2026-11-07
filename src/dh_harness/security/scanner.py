from __future__ import annotations
import os
import re
from typing import List, Optional, Tuple, Dict, Any

from dh_harness.core.contracts import SecretFinding, SecuritySeverity

SECRET_RULE_DEFINITIONS: List[Tuple[str, re.Pattern, SecuritySeverity]] = [
    (
        "GITHUB_TOKEN",
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}|github_pat_[A-Za-z0-9_]{40,}"),
        SecuritySeverity.CRITICAL
    ),
    (
        "AWS_ACCESS_KEY",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        SecuritySeverity.HIGH
    ),
    (
        "PRIVATE_KEY",
        re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH)? ?PRIVATE KEY-----"),
        SecuritySeverity.CRITICAL
    ),
    (
        "SLACK_TOKEN",
        re.compile(r"xox[baprs]-[0-9a-zA-Z-]{10,}"),
        SecuritySeverity.HIGH
    ),
    (
        "PASSWORD_IN_CONNSTR",
        re.compile(r"(?i)\b(?:password|pwd)\s*=\s*([^;'\"]+)", re.IGNORECASE),
        SecuritySeverity.HIGH
    ),
]

DEFAULT_IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".worktrees", "tests", ".engine"
}

class SecretScanner:
    """
    Exhaustive scanner detecting leaked credentials, tokens, private keys,
    and hardcoded database passwords in source code and configurations (info.md § 14.2).
    """

    def scan_content(self, content: str, file_path: str = "") -> List[SecretFinding]:
        """Scans arbitrary text content for secrets and returns redacted findings."""
        findings: List[SecretFinding] = []
        lines = content.splitlines()

        for idx, line in enumerate(lines, 1):
            for secret_type, pattern, severity in SECRET_RULE_DEFINITIONS:
                match = pattern.search(line)
                if match:
                    if secret_type == "PASSWORD_IN_CONNSTR":
                        raw_val = match.group(1)
                        redacted_line = line.replace(raw_val, "[REDACTED_SECRET]")
                    else:
                        raw_val = match.group(0)
                        redacted_line = line.replace(raw_val, "[REDACTED_SECRET]")

                    findings.append(SecretFinding(
                        file_path=file_path,
                        line_number=idx,
                        secret_type=secret_type,
                        snippet_redacted=redacted_line.strip(),
                        severity=severity
                    ))

        return findings

    def scan_file(self, file_path: str) -> List[SecretFinding]:
        """Scans a single file for secrets."""
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return self.scan_content(content, file_path=file_path)
        except Exception:
            return []

    def scan_directory(
        self,
        dir_path: str,
        exclude_dirs: Optional[set] = None
    ) -> List[SecretFinding]:
        """Recursively scans a directory for exposed secrets, skipping standard ignored directories."""
        ignored = exclude_dirs or DEFAULT_IGNORED_DIRS
        findings: List[SecretFinding] = []

        for root, dirs, files in os.walk(dir_path):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in ignored]

            for file in files:
                full_path = os.path.join(root, file)
                file_findings = self.scan_file(full_path)
                findings.extend(file_findings)

        return findings
