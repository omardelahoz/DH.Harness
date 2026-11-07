import os
import subprocess
import pytest
from dh_harness.git.worktrees import GitWorktreeManager
from dh_harness.git.manager import ProtectedBranchViolationError

@pytest.fixture
def temp_git_repo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    # Initialize real git repo
    subprocess.run(["git", "init"], cwd=str(repo_dir), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test Runner"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(repo_dir), check=True)

    # Initial commit
    init_file = repo_dir / "README.md"
    init_file.write_text("# Test Repo", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=str(repo_dir), check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "chore: initial commit"], cwd=str(repo_dir), check=True, capture_output=True)

    return str(repo_dir)

def test_worktree_manager_lists_main_worktree(temp_git_repo):
    wt_mgr = GitWorktreeManager(repo_path=temp_git_repo)
    worktrees = wt_mgr.list_worktrees()
    assert len(worktrees) >= 1
    assert os.path.samefile(worktrees[0]["path"], temp_git_repo)

def test_worktree_lifecycle(temp_git_repo):
    wt_mgr = GitWorktreeManager(repo_path=temp_git_repo)
    branch = "feature/DH-099-test-parallel"

    wt_path = wt_mgr.create_worktree(branch_name=branch)
    assert os.path.exists(wt_path)

    # Check worktree is listed
    worktrees = wt_mgr.list_worktrees()
    assert any(os.path.samefile(w["path"], wt_path) for w in worktrees)

    # Remove worktree
    wt_mgr.remove_worktree(wt_path, force=True)
    assert not os.path.exists(wt_path)

def test_worktree_blocks_protected_branch(temp_git_repo):
    wt_mgr = GitWorktreeManager(repo_path=temp_git_repo)

    with pytest.raises(ProtectedBranchViolationError):
        wt_mgr.create_worktree(branch_name="main")
