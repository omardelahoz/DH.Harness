import pytest
from dh_harness.core.contracts import HierarchicalTask, AgentRole
from dh_harness.agents.registry import AgentRegistry
from dh_harness.workflows.runner import WorkflowRunner

def test_extended_workflow_runner_lists_all_workflows():
    runner = WorkflowRunner()
    workflows = runner.list_workflows()

    assert len(workflows) >= 7
    wf_ids = [w.id for w in workflows]
    assert "mobile-feature-development" in wf_ids
    assert "devops-pipeline-release" in wf_ids
    assert "architecture-refactoring" in wf_ids

def test_mobile_feature_workflow_execution():
    registry = AgentRegistry()
    registry.load_defaults()

    runner = WorkflowRunner(agent_registry=registry)
    task = HierarchicalTask(id="MOB-1", title="User Profile Mobile Screen")

    result = runner.execute_workflow("mobile-feature-development", task)

    assert result.status == "SUCCESS"
    assert "mobile_spec" in result.completed_stages
    assert "bloc_state_tdd" in result.completed_stages
    assert "flutter_implementation" in result.completed_stages
    assert "independent_review" in result.completed_stages
    assert len(result.evidence) == 4

def test_devops_workflow_execution():
    registry = AgentRegistry()
    registry.load_defaults()

    runner = WorkflowRunner(agent_registry=registry)
    task = HierarchicalTask(id="OPS-1", title="Setup Non-root Dockerfile and CI/CD")

    result = runner.execute_workflow("devops-pipeline-release", task)

    assert result.status == "SUCCESS"
    assert "iac_container_audit" in result.completed_stages
    assert "pipeline_definition" in result.completed_stages
    assert "quality_gate_audit" in result.completed_stages
    assert "release_review" in result.completed_stages
    assert len(result.evidence) == 4
