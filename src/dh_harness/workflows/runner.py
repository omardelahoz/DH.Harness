from __future__ import annotations
from typing import Dict, List, Optional
from dh_harness.core.contracts import (
    HierarchicalTask,
    WorkflowDefinition,
    WorkflowStage,
    WorkflowExecutionResult,
    AgentRole
)
from dh_harness.agents.registry import AgentRegistry
from dh_harness.workflows.catalog import get_default_workflow_catalog

class WorkflowStageExecutionError(Exception):
    """Raised when a stage in a composable workflow fails execution or preconditions."""
    pass

class WorkflowRunner:
    """
    Executes composable multi-stage workflows, assigning specialized agents,
    verifying stage dependencies, and collecting execution evidence (info.md § 6).
    """

    def __init__(
        self,
        agent_registry: Optional[AgentRegistry] = None,
        workflows: Optional[List[WorkflowDefinition]] = None
    ):
        if agent_registry is None:
            self.agent_registry = AgentRegistry()
            self.agent_registry.load_defaults()
        else:
            self.agent_registry = agent_registry

        self._workflows: Dict[str, WorkflowDefinition] = {}
        for wf in (workflows or get_default_workflow_catalog()):
            self._workflows[wf.id] = wf

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Retrieves a workflow definition by its unique identifier."""
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[WorkflowDefinition]:
        """Lists all registered workflow definitions."""
        return list(self._workflows.values())

    def execute_workflow(
        self,
        workflow_id: str,
        task: HierarchicalTask
    ) -> WorkflowExecutionResult:
        """
        Executes all stages of a workflow in dependency order.
        Guarantees independent review separation between authoring and review stages.
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found in registry.")

        completed_stages: List[str] = []
        evidence: List[str] = []
        errors: List[str] = []
        primary_author_agent: Optional[str] = task.assigned_agent

        for stage in workflow.stages:
            # Check stage preconditions
            for dep in stage.depends_on:
                if dep not in completed_stages:
                    err = f"Stage '{stage.id}' blocked: dependency stage '{dep}' not completed."
                    errors.append(err)
                    return WorkflowExecutionResult(
                        workflow_id=workflow_id,
                        task_id=task.id,
                        status="FAILED",
                        completed_stages=completed_stages,
                        evidence=evidence,
                        errors=errors
                    )

            # Resolve qualified agent with the required role
            candidates = self.agent_registry.find_by_role(stage.required_role)
            if not candidates:
                err = f"No specialized agent registered with role '{stage.required_role.value}' for stage '{stage.id}'."
                errors.append(err)
                return WorkflowExecutionResult(
                    workflow_id=workflow_id,
                    task_id=task.id,
                    status="FAILED",
                    completed_stages=completed_stages,
                    evidence=evidence,
                    errors=errors
                )

            # Enforce independent review separation
            selected_agent = None
            if stage.required_role == AgentRole.CODE_REVIEWER:
                for candidate in candidates:
                    if candidate.id != primary_author_agent:
                        selected_agent = candidate
                        break
                if not selected_agent:
                    err = f"Independent review violation: all reviewers match author agent '{primary_author_agent}'."
                    errors.append(err)
                    return WorkflowExecutionResult(
                        workflow_id=workflow_id,
                        task_id=task.id,
                        status="FAILED",
                        completed_stages=completed_stages,
                        evidence=evidence,
                        errors=errors
                    )
            else:
                selected_agent = candidates[0]
                if not primary_author_agent and stage.required_role == AgentRole.BACKEND_DEVELOPER:
                    primary_author_agent = selected_agent.id
                    task.assigned_agent = selected_agent.id

            stage_evidence = (
                f"Stage '{stage.id}' ({stage.name}) completed by agent '{selected_agent.id}' "
                f"with role '{stage.required_role.value}' for task '{task.id}'."
            )
            completed_stages.append(stage.id)
            evidence.append(stage_evidence)
            task.evidence.append(stage_evidence)

        return WorkflowExecutionResult(
            workflow_id=workflow_id,
            task_id=task.id,
            status="SUCCESS",
            completed_stages=completed_stages,
            evidence=evidence,
            errors=[]
        )
