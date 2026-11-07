from __future__ import annotations
from typing import Dict, List, Optional
from dh_harness.core.contracts import TaskState, HierarchicalTask

class TaskStateTransitionError(Exception):
    """Raised when an illegal or unfulfilled task transition is attempted."""
    pass

class TaskManager:
    """
    Manages task lifecycle, state machine transitions, and dependency validation.
    Complies with Section 9 of info.md.
    """

    ALLOWED_TRANSITIONS: Dict[TaskState, List[TaskState]] = {
        TaskState.BACKLOG: [TaskState.READY, TaskState.CANCELLED],
        TaskState.READY: [TaskState.IN_PROGRESS, TaskState.BACKLOG, TaskState.CANCELLED],
        TaskState.IN_PROGRESS: [TaskState.BLOCKED, TaskState.IN_REVIEW, TaskState.CANCELLED],
        TaskState.BLOCKED: [TaskState.IN_PROGRESS, TaskState.CANCELLED],
        TaskState.IN_REVIEW: [TaskState.CHANGES_REQUESTED, TaskState.READY_FOR_PR, TaskState.CANCELLED],
        TaskState.CHANGES_REQUESTED: [TaskState.IN_PROGRESS, TaskState.CANCELLED],
        TaskState.READY_FOR_PR: [TaskState.PR_OPEN, TaskState.IN_PROGRESS, TaskState.CANCELLED],
        TaskState.PR_OPEN: [TaskState.MERGED, TaskState.CHANGES_REQUESTED, TaskState.CANCELLED],
        TaskState.MERGED: [TaskState.DONE],
        TaskState.DONE: [],
        TaskState.CANCELLED: [TaskState.BACKLOG],
    }

    def __init__(self):
        self._tasks: Dict[str, HierarchicalTask] = {}
        self._history: List[Dict[str, str]] = []

    def register_task(self, task: HierarchicalTask):
        """Registers a hierarchical task into management."""
        self._tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[HierarchicalTask]:
        """Retrieves a task by ID."""
        return self._tasks.get(task_id)

    def list_tasks(self, state: Optional[TaskState] = None) -> List[HierarchicalTask]:
        """Lists tasks optionally filtered by state."""
        if state is None:
            return list(self._tasks.values())
        return [t for t in self._tasks.values() if t.state == state]

    def transition_state(
        self,
        task_id: str,
        new_state: TaskState,
        reason: str = "",
        evidence: Optional[str] = None
    ):
        """
        Validates preconditions and executes state transition for a task.
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskStateTransitionError(f"Task with ID '{task_id}' does not exist.")

        allowed = self.ALLOWED_TRANSITIONS.get(task.state, [])
        if new_state not in allowed:
            raise TaskStateTransitionError(
                f"Illegal state transition from {task.state.value} to {new_state.value} for task {task_id}. "
                f"Allowed transitions: {[s.value for s in allowed]}"
            )

        # Precondition check: IN_PROGRESS requires all dependencies to be DONE or MERGED
        if new_state == TaskState.IN_PROGRESS:
            unmet_deps = []
            for dep_id in task.dependencies:
                dep_task = self.get_task(dep_id)
                if not dep_task or dep_task.state not in (TaskState.DONE, TaskState.MERGED):
                    unmet_deps.append(dep_id)
            if unmet_deps:
                raise TaskStateTransitionError(
                    f"Cannot start task {task_id} in IN_PROGRESS. Unmet dependencies: {unmet_deps}"
                )

        # Precondition check: DONE requires explicit evidence
        if new_state == TaskState.DONE:
            if not evidence or not evidence.strip():
                raise TaskStateTransitionError(
                    f"Cannot mark task {task_id} as DONE without verifiable completion evidence."
                )
            task.evidence.append(evidence)

        old_state = task.state
        task.state = new_state
        self._history.append({
            "task_id": task_id,
            "from_state": old_state.value,
            "to_state": new_state.value,
            "reason": reason
        })
