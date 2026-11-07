import pytest
from dh_harness.core.contracts import HierarchicalTask, TaskState
from dh_harness.git.manager import GitGovernanceManager

def test_dod_fails_without_test_evidence():
    mgr = GitGovernanceManager()
    task = HierarchicalTask(
        id="TASK-200",
        title="Add user entity",
        evidence=["Manual verification in terminal"]
    )

    result = mgr.verify_definition_of_done(task, require_pr=True)
    assert result.satisfied is False
    assert any("test" in m.lower() for m in result.missing_criteria)

def test_dod_fails_without_independent_review():
    mgr = GitGovernanceManager()
    task = HierarchicalTask(
        id="TASK-201",
        title="Add payment module",
        evidence=["pytest passed 10 unit tests", "PR #10 merged"]
    )

    result = mgr.verify_definition_of_done(task, require_pr=True)
    assert result.satisfied is False
    assert any("review" in m.lower() for m in result.missing_criteria)

def test_dod_fails_without_pr_integration():
    mgr = GitGovernanceManager()
    task = HierarchicalTask(
        id="TASK-202",
        title="Refactor database gateway",
        evidence=[
            "pytest passed 5 unit tests",
            "Independent review approved by 'independent-code-reviewer'"
        ]
    )

    result = mgr.verify_definition_of_done(task, require_pr=True)
    assert result.satisfied is False
    assert any("pull request" in m.lower() for m in result.missing_criteria)

def test_dod_passes_with_all_evidence():
    mgr = GitGovernanceManager()
    task = HierarchicalTask(
        id="TASK-203",
        title="Implement secure tokens",
        pr_number=12,
        evidence=[
            "pytest passed 15 unit tests",
            "Independent review approved by 'security-engineer'",
            "PR #12 merged into main"
        ]
    )

    result = mgr.verify_definition_of_done(task, require_pr=True)
    assert result.satisfied is True
    assert len(result.missing_criteria) == 0

def test_dod_supports_local_workflow_without_pr():
    mgr = GitGovernanceManager()
    task = HierarchicalTask(
        id="TASK-204",
        title="Internal config update",
        evidence=[
            "pytest passed 3 tests",
            "Independent review approved by 'qa-engineer'"
        ]
    )

    result = mgr.verify_definition_of_done(task, require_pr=False)
    assert result.satisfied is True
