import pytest
from dh_harness.core.contracts import (
    HierarchicalTask,
    TaskState,
    AgentRole,
    WorkflowDefinition,
    WorkflowStage
)
from dh_harness.agents.registry import AgentRegistry
from dh_harness.workflows.catalog import get_default_workflow_catalog
from dh_harness.workflows.runner import WorkflowRunner, WorkflowStageExecutionError

def test_workflow_catalog_has_canonical_definitions():
    workflows = get_default_workflow_catalog()
    wf_ids = [w.id for w in workflows]

    assert "feature-development" in wf_ids
    assert "bug-fix" in wf_ids
    assert "security-audit" in wf_ids
    assert "api-development" in wf_ids

    feat_wf = next(w for w in workflows if w.id == "feature-development")
    stage_ids = [s.id for s in feat_wf.stages]
    assert "specification" in stage_ids
    assert "tdd_red" in stage_ids
    assert "implement_green" in stage_ids
    assert "independent_review" in stage_ids

def test_workflow_runner_executes_canonical_feature_dev():
    registry = AgentRegistry()
    registry.load_defaults()

    runner = WorkflowRunner(agent_registry=registry)
    task = HierarchicalTask(id="TASK-100", title="Build Authentication Service")

    result = runner.execute_workflow("feature-development", task)
    assert result.status == "SUCCESS"
    assert "specification" in result.completed_stages
    assert "tdd_red" in result.completed_stages
    assert "implement_green" in result.completed_stages
    assert "independent_review" in result.completed_stages
    assert len(result.evidence) >= 4

def test_workflow_runner_enforces_independent_review_stage():
    registry = AgentRegistry()
    registry.load_defaults()

    runner = WorkflowRunner(agent_registry=registry)
    task = HierarchicalTask(id="TASK-101", title="Payment Gateway Integration")

    result = runner.execute_workflow("feature-development", task)
    # Ensure evidence shows distinct agents for implementation and review
    impl_evidence = next(e for e in result.evidence if "implement_green" in e)
    review_evidence = next(e for e in result.evidence if "independent_review" in e)

    assert "developer-backend" in impl_evidence
    assert "independent-code-reviewer" in review_evidence

def test_workflow_runner_handles_missing_workflow():
    registry = AgentRegistry()
    registry.load_defaults()
    runner = WorkflowRunner(agent_registry=registry)
    task = HierarchicalTask(id="TASK-102", title="Unknown")

    with pytest.raises(ValueError) as exc_info:
        runner.execute_workflow("non-existent-workflow", task)
    assert "not found" in str(exc_info.value).lower()
