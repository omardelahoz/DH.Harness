import pytest
from dh_harness.core.contracts import HierarchicalTask, TaskState
from dh_harness.agents.registry import AgentRegistry
from dh_harness.agents.delegation import DelegationEngine, SelfReviewViolationError, UnauthorizedReviewerError

def test_delegation_engine_creates_contract():
    registry = AgentRegistry()
    registry.load_defaults()
    engine = DelegationEngine(registry)

    task = HierarchicalTask(id="TASK-1", title="Build User Entity")
    contract = engine.assign_task(task, "developer-backend")

    assert contract.task_id == "TASK-1"
    assert contract.agent_id == "developer-backend"
    assert task.assigned_agent == "developer-backend"

def test_delegation_engine_blocks_self_review():
    registry = AgentRegistry()
    registry.load_defaults()
    engine = DelegationEngine(registry)

    task = HierarchicalTask(id="TASK-2", title="Build Payment Gateway", assigned_agent="developer-backend", state=TaskState.IN_REVIEW)

    # developer-backend cannot review their own work
    with pytest.raises(SelfReviewViolationError) as exc_info:
        engine.submit_review(task, reviewer_agent_id="developer-backend", approved=True, feedback="Looks good to me!")
    assert "cannot review or approve their own" in str(exc_info.value).lower()

def test_delegation_engine_permits_independent_reviewer():
    registry = AgentRegistry()
    registry.load_defaults()
    engine = DelegationEngine(registry)

    task = HierarchicalTask(id="TASK-3", title="Build Auth", assigned_agent="developer-backend", state=TaskState.IN_REVIEW)

    # independent-code-reviewer is a distinct agent with CODE_REVIEWER role
    review_record = engine.submit_review(task, reviewer_agent_id="independent-code-reviewer", approved=True, feedback="Clean architecture followed.")
    assert review_record["approved"] is True
    assert review_record["reviewer"] == "independent-code-reviewer"
    assert "Independent review approved by 'independent-code-reviewer'" in task.evidence[0]

def test_delegation_engine_blocks_unauthorized_role_as_reviewer():
    registry = AgentRegistry()
    registry.load_defaults()
    engine = DelegationEngine(registry)

    task = HierarchicalTask(id="TASK-4", title="Build Service", assigned_agent="developer-backend", state=TaskState.IN_REVIEW)

    # frontend developer cannot act as official code reviewer
    with pytest.raises(UnauthorizedReviewerError):
        engine.submit_review(task, reviewer_agent_id="developer-frontend", approved=True, feedback="LGTM")
