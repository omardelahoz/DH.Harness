from __future__ import annotations
from typing import Optional, List
from dh_harness.core.contracts import TaskState, ContinuityReport, HierarchicalTask
from dh_harness.tasks.manager import TaskManager
from dh_harness.tasks.dag import DependencyGraph

class ContinuityEngine:
    """
    Project Continuity & Work Planning Engine.
    Implements Section 10 of info.md: answers "¿Con qué continuamos hoy?",
    resolves DAG dependencies, identifies parallel tasks, and recommends optimal next steps.
    """

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def generate_continuity_report(self) -> ContinuityReport:
        all_tasks = self.task_manager.list_tasks()

        completed: List[str] = []
        in_progress: List[str] = []
        blocked: List[str] = []
        pending: List[str] = []

        dag = DependencyGraph()
        for t in all_tasks:
            dag.add_node(t.id, t.dependencies)
            if t.state in (TaskState.DONE, TaskState.MERGED):
                completed.append(t.id)
            elif t.state in (TaskState.IN_PROGRESS, TaskState.IN_REVIEW, TaskState.READY_FOR_PR, TaskState.PR_OPEN):
                in_progress.append(t.id)
            elif t.state == TaskState.BLOCKED:
                blocked.append(t.id)
            elif t.state in (TaskState.BACKLOG, TaskState.READY):
                pending.append(t.id)

        # Calculate parallel executable candidates
        ready_from_dag = dag.get_ready_tasks(completed_nodes=completed)
        parallel_candidates = [
            t_id for t_id in ready_from_dag
            if self.task_manager.get_task(t_id) and self.task_manager.get_task(t_id).state in (TaskState.BACKLOG, TaskState.READY)
        ]

        # Recommendation logic (RECOMMENDED mode)
        recommended_task: Optional[str] = None
        rationale: str = ""

        if in_progress:
            recommended_task = in_progress[0]
            rationale = (
                f"Task '{recommended_task}' is already IN_PROGRESS. "
                f"Engineering policy recommends closing active work before starting new tasks."
            )
        elif parallel_candidates:
            # Sort by priority ascending (1 = highest priority)
            candidate_objs = [self.task_manager.get_task(t_id) for t_id in parallel_candidates if self.task_manager.get_task(t_id)]
            candidate_objs.sort(key=lambda x: (x.priority, x.id))
            top_task = candidate_objs[0]
            recommended_task = top_task.id
            rationale = (
                f"Task '{recommended_task}' has all preconditions and dependencies satisfied with priority {top_task.priority}. "
                f"Can be executed immediately or in parallel with {len(parallel_candidates) - 1} other task(s)."
            )
        elif blocked:
            rationale = f"All pending tasks are blocked or awaiting dependencies. Review blocked tasks: {blocked}"
        else:
            rationale = "All registered project tasks are completed! Definition of Done satisfied."

        return ContinuityReport(
            completed_count=len(completed),
            in_progress_count=len(in_progress),
            pending_count=len(pending),
            blocked_count=len(blocked),
            completed_tasks=sorted(completed),
            in_progress_tasks=sorted(in_progress),
            pending_tasks=sorted(pending),
            blocked_tasks=sorted(blocked),
            parallel_candidates=sorted(parallel_candidates),
            recommended_task=recommended_task,
            rationale=rationale
        )
