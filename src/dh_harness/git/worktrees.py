from __future__ import annotations
import os
import re
import subprocess
from typing import Optional, List, Dict, Any

from dh_harness.git.manager import GitGovernanceManager, ProtectedBranchViolationError

class GitWorktreeManager:
    """
    Manages isolated Git worktrees for safe parallel execution and multi-agent coordination
    without workspace collision (info.md § 11.7 and § 22).
    """

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = repo_path or os.getcwd()
        self.governance = GitGovernanceManager(self.repo_path)
        self.worktrees_dir = os.path.join(self.repo_path, ".worktrees")

    def create_worktree(self, branch_name: str, target_path: Optional[str] = None) -> str:
        """
        Creates a new worktree on a dedicated feature/bugfix branch.
        Rejects protected branches to ensure workspace safety.
        """
        # Validates naming and raises ProtectedBranchViolationError if branch is protected
        self.governance.validate_branch_name(branch_name)

        if target_path is None:
            safe_dirname = re.sub(r"[^A-Za-z0-9_-]", "_", branch_name)
            target_path = os.path.join(self.worktrees_dir, safe_dirname)

        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

        # Attempt creating worktree with a new branch; fallback to existing branch
        cmd_new_branch = ["git", "worktree", "add", "-b", branch_name, target_path]
        res = subprocess.run(cmd_new_branch, cwd=self.repo_path, capture_output=True, text=True)

        if res.returncode != 0:
            # If branch already exists, add without -b
            cmd_existing = ["git", "worktree", "add", target_path, branch_name]
            res_existing = subprocess.run(cmd_existing, cwd=self.repo_path, capture_output=True, text=True)
            if res_existing.returncode != 0:
                raise RuntimeError(
                    f"Failed to create worktree for branch '{branch_name}': {res_existing.stderr or res.stderr}"
                )

        return os.path.abspath(target_path)

    def list_worktrees(self) -> List[Dict[str, str]]:
        """Lists all active Git worktrees registered in the repository."""
        res = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            return []

        worktrees: List[Dict[str, str]] = []
        current: Dict[str, str] = {}

        for line in res.stdout.splitlines():
            line = line.strip()
            if not line:
                if current:
                    worktrees.append(current)
                    current = {}
                continue

            parts = line.split(None, 1)
            key = parts[0]
            val = parts[1] if len(parts) > 1 else ""

            if key == "worktree":
                current["path"] = os.path.abspath(val)
            elif key == "HEAD":
                current["head"] = val
            elif key == "branch":
                current["branch"] = val

        if current:
            worktrees.append(current)

        return worktrees

    def remove_worktree(self, target_path: str, force: bool = False):
        """Safely removes an existing worktree."""
        abs_path = os.path.abspath(target_path)
        cmd = ["git", "worktree", "remove"]
        if force:
            cmd.append("--force")
        cmd.append(abs_path)

        res = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to remove worktree at '{abs_path}': {res.stderr}")

    def prune_worktrees(self):
        """Prunes stale worktree administrative records."""
        subprocess.run(["git", "worktree", "prune"], cwd=self.repo_path, capture_output=True, text=True)
