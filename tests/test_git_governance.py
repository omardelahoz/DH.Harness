import pytest
from dh_harness.core.contracts import GitProvider
from dh_harness.git.manager import (
    GitGovernanceManager,
    ProtectedBranchViolationError,
    detect_git_provider
)

def test_detect_git_provider():
    assert detect_git_provider("https://github.com/omardelahoz/DH.Harness.git") == GitProvider.GITHUB
    assert detect_git_provider("git@github.com:omardelahoz/DH.Harness.git") == GitProvider.GITHUB
    assert detect_git_provider("https://dev.azure.com/myorg/myproj/_git/myrepo") == GitProvider.AZURE_DEVOPS
    assert detect_git_provider("https://gitlab.com/group/repo.git") == GitProvider.GITLAB
    assert detect_git_provider("https://bitbucket.org/workspace/repo.git") == GitProvider.BITBUCKET
    assert detect_git_provider(None) == GitProvider.LOCAL
    assert detect_git_provider("") == GitProvider.LOCAL

def test_validate_branch_naming():
    mgr = GitGovernanceManager()

    # Valid branch naming
    assert mgr.validate_branch_name("feature/DH-001-setup-foundation") is True
    assert mgr.validate_branch_name("bugfix/DH-002-fix-null-pointer") is True
    assert mgr.validate_branch_name("refactor/DH-003-clean-architecture") is True
    assert mgr.validate_branch_name("hotfix/DH-004-critical-patch") is True

    # Invalid branch naming
    assert mgr.validate_branch_name("my-random-branch") is False
    assert mgr.validate_branch_name("feature-no-slash") is False

def test_protected_branch_violation():
    mgr = GitGovernanceManager()

    for protected in ["main", "master", "release", "production", "prod"]:
        with pytest.raises(ProtectedBranchViolationError) as exc_info:
            mgr.validate_branch_name(protected)
        assert "protected branch" in str(exc_info.value).lower()

def test_validate_commit_message():
    mgr = GitGovernanceManager()

    # Valid Conventional Commits
    assert mgr.validate_commit_message("feat(git): implement git governance manager") is True
    assert mgr.validate_commit_message("fix(core): correct task status transition") is True
    assert mgr.validate_commit_message("docs: update architecture adr") is True
    assert mgr.validate_commit_message("test(tdd): add false test cases") is True
    assert mgr.validate_commit_message("refactor: simplify dag traversal") is True

    # Invalid commit messages
    assert mgr.validate_commit_message("fixed a bug") is False
    assert mgr.validate_commit_message("WIP") is False
    assert mgr.validate_commit_message("update files") is False

def test_diagnose_current_repo():
    mgr = GitGovernanceManager()
    diag = mgr.diagnose_repo()

    assert diag.is_git is True
    assert diag.remote_provider == GitProvider.GITHUB
    assert bool(diag.active_branch)
    assert diag.active_branch.startswith("feature/") or diag.active_branch in {"main", "master"}
