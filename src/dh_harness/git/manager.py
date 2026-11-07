from __future__ import annotations
import os
import re
import subprocess
from typing import Optional, List, Dict, Any

from dh_harness.core.contracts import (
    GitProvider,
    RepoDiagnostics,
    DoDVerificationResult,
    HierarchicalTask,
    TaskState
)

class ProtectedBranchViolationError(Exception):
    """Raised when an operation attempts to commit or author code directly on a protected branch."""
    pass

PROTECTED_BRANCHES = {"main", "master", "release", "production", "prod"}

BRANCH_NAME_REGEX = re.compile(
    r"^(feature|bugfix|refactor|hotfix)/[A-Za-z0-9_-]+$"
)

CONVENTIONAL_COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_\-\./]+\))?!?: .+"
)

def detect_git_provider(remote_url: Optional[str]) -> GitProvider:
    """Detects Git provider platform from remote URL."""
    if not remote_url:
        return GitProvider.LOCAL

    url_lower = remote_url.lower()
    if "github.com" in url_lower:
        return GitProvider.GITHUB
    if "dev.azure.com" in url_lower or "visualstudio.com" in url_lower:
        return GitProvider.AZURE_DEVOPS
    if "gitlab.com" in url_lower:
        return GitProvider.GITLAB
    if "bitbucket.org" in url_lower:
        return GitProvider.BITBUCKET

    return GitProvider.LOCAL

class GitGovernanceManager:
    """
    Enforces Git branch naming, Conventional Commits, protected branch guards,
    and Definition of Done (DoD) verification (info.md Section 11).
    """

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = repo_path or os.getcwd()

    def validate_branch_name(self, branch_name: str) -> bool:
        """Validates branch naming conventions and blocks protected branches."""
        cleaned = branch_name.strip()
        if cleaned.lower() in PROTECTED_BRANCHES:
            raise ProtectedBranchViolationError(
                f"Modifications cannot be made directly on protected branch '{cleaned}'. "
                f"You must create a dedicated feature or bugfix branch."
            )
        return bool(BRANCH_NAME_REGEX.match(cleaned))

    def validate_commit_message(self, message: str) -> bool:
        """Validates that commit messages comply with Conventional Commits specification."""
        first_line = message.strip().split("\n")[0].strip()
        return bool(CONVENTIONAL_COMMIT_REGEX.match(first_line))

    def diagnose_repo(self) -> RepoDiagnostics:
        """Runs Git diagnostic inspection on the active repository."""
        is_git = False
        active_branch = "unknown"
        remote_url = None
        is_clean = True
        modified_files: List[str] = []
        untracked_files: List[str] = []

        try:
            res = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            is_git = res.returncode == 0 and "true" in res.stdout.lower()
        except Exception:
            is_git = False

        if not is_git:
            return RepoDiagnostics(
                is_git=False,
                active_branch="",
                remote_provider=GitProvider.LOCAL,
                remote_url=None,
                is_clean=True,
                modified_files=[],
                untracked_files=[]
            )

        # Get active branch
        try:
            res = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if res.returncode == 0:
                active_branch = res.stdout.strip()
        except Exception:
            pass

        # Get remote URL
        try:
            res = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if res.returncode == 0 and res.stdout.strip():
                remote_url = res.stdout.strip()
        except Exception:
            pass

        # Get status porcelain
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if res.returncode == 0:
                lines = res.stdout.strip().splitlines()
                is_clean = len(lines) == 0
                for line in lines:
                    line_clean = line.strip()
                    if not line_clean:
                        continue
                    if line_clean.startswith("??"):
                        untracked_files.append(line_clean[3:].strip())
                    else:
                        parts = line_clean.split(None, 1)
                        if len(parts) > 1:
                            modified_files.append(parts[1])
        except Exception:
            pass

        provider = detect_git_provider(remote_url)
        return RepoDiagnostics(
            is_git=True,
            active_branch=active_branch,
            remote_provider=provider,
            remote_url=remote_url,
            is_clean=is_clean,
            modified_files=modified_files,
            untracked_files=untracked_files
        )

    def verify_definition_of_done(
        self,
        task: HierarchicalTask,
        require_pr: bool = True
    ) -> DoDVerificationResult:
        """
        Validates that all Definition of Done criteria are satisfied before marking a task as DONE (info.md § 11.6).
        """
        missing_criteria: List[str] = []
        evidence_collected: List[str] = list(task.evidence)

        # 1. Tests & Quality evidence
        has_test_evidence = any(
            ("test" in ev.lower() or "pytest" in ev.lower() or "pass" in ev.lower())
            for ev in task.evidence
        )
        if not has_test_evidence:
            missing_criteria.append("Automated test verification evidence missing")

        # 2. Independent Review evidence
        has_review_evidence = any(
            ("independent review" in ev.lower() or "review approved" in ev.lower())
            for ev in task.evidence
        )
        if not has_review_evidence:
            missing_criteria.append("Independent code review approval missing")

        # 3. Pull Request / Integration evidence (if required)
        if require_pr:
            has_pr = (
                task.pr_number is not None
                or any("pr #" in ev.lower() or "pull request" in ev.lower() for ev in task.evidence)
            )
            if not has_pr:
                missing_criteria.append("Pull Request integration evidence missing")

        satisfied = len(missing_criteria) == 0
        return DoDVerificationResult(
            task_id=task.id,
            satisfied=satisfied,
            missing_criteria=missing_criteria,
            evidence_collected=evidence_collected
        )
