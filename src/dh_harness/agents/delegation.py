from __future__ import annotations
from typing import Dict, Any, Optional
from dh_harness.core.contracts import (
    HierarchicalTask,
    AgentTaskContract,
    AgentRole,
    TaskState,
)
from dh_harness.agents.registry import AgentRegistry

class SelfReviewViolationError(Exception):
    """Raised when an agent attempts to review their own authored work."""
    pass

class UnauthorizedReviewerError(Exception):
    """Raised when an agent without a legitimate reviewer role attempts to review work."""
    pass

AUTHORIZED_REVIEWER_ROLES = {
    AgentRole.CODE_REVIEWER,
    AgentRole.QA_ENGINEER,
    AgentRole.SECURITY_ENGINEER,
}

class DelegationEngine:
    """
    Orchestrates task assignment to specialized agents and enforces
    independent review boundaries (info.md § 4.9 & § 23.2).
    """

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def assign_task(
        self,
        task: HierarchicalTask,
        agent_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentTaskContract:
        agent = self.registry.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' is not registered in the agent registry.")

        task.assigned_agent = agent_id

        return AgentTaskContract(
            task_id=task.id,
            agent_id=agent_id,
            objective=task.title,
            context=context or {},
            input_artifacts=[],
            expected_outputs=[],
        )

    def submit_review(
        self,
        task: HierarchicalTask,
        reviewer_agent_id: str,
        approved: bool,
        feedback: str,
    ) -> Dict[str, Any]:
        """
        Submits an independent review for a task.
        Guarantees that an agent cannot review or approve their own work,
        and that the reviewer holds an authorized review role.
        """
        if task.assigned_agent and task.assigned_agent == reviewer_agent_id:
            raise SelfReviewViolationError(
                f"Agent '{reviewer_agent_id}' cannot review or approve their own work on task '{task.id}'."
            )

        reviewer = self.registry.get_agent(reviewer_agent_id)
        if not reviewer:
            raise UnauthorizedReviewerError(
                f"Reviewer '{reviewer_agent_id}' is not registered in the agent registry."
            )

        if reviewer.role not in AUTHORIZED_REVIEWER_ROLES:
            raise UnauthorizedReviewerError(
                f"Agent '{reviewer_agent_id}' with role '{reviewer.role.value}' is not authorized to perform reviews. "
                f"Authorized roles are: {[r.value for r in AUTHORIZED_REVIEWER_ROLES]}."
            )

        review_status = "approved" if approved else "rejected"
        evidence_entry = f"Independent review {review_status} by '{reviewer_agent_id}': {feedback}"
        task.evidence.append(evidence_entry)

        if not approved:
            task.state = TaskState.CHANGES_REQUESTED

        return {
            "reviewer": reviewer_agent_id,
            "approved": approved,
            "feedback": feedback,
        }
