import pytest
from dh_harness.core.contracts import TaskState, HierarchicalTask
from dh_harness.tasks.manager import TaskManager
from dh_harness.continuity.engine import ContinuityEngine

def test_continuity_engine_recommends_next_task():
    mgr = TaskManager()
    t1 = HierarchicalTask(id="TASK-1", title="Init Project", state=TaskState.DONE, evidence=["Done"])
    t2 = HierarchicalTask(id="TASK-2", title="Setup DB", state=TaskState.BACKLOG, dependencies=["TASK-1"], priority=1)
    t3 = HierarchicalTask(id="TASK-3", title="Setup Auth", state=TaskState.BACKLOG, dependencies=["TASK-1"], priority=2)
    t4 = HierarchicalTask(id="TASK-4", title="UI Form", state=TaskState.BACKLOG, dependencies=["TASK-2"], priority=1)

    for t in [t1, t2, t3, t4]:
        mgr.register_task(t)

    engine = ContinuityEngine(task_manager=mgr)
    report = engine.generate_continuity_report()

    assert report.completed_count == 1
    assert "TASK-1" in report.completed_tasks
    assert set(report.parallel_candidates) == {"TASK-2", "TASK-3"}
    # TASK-2 has priority 1 (higher than priority 2)
    assert report.recommended_task == "TASK-2"
    assert "preconditions" in report.rationale.lower() or "priority" in report.rationale.lower()

def test_continuity_engine_prioritizes_active_in_progress():
    mgr = TaskManager()
    t1 = HierarchicalTask(id="TASK-A", title="In flight work", state=TaskState.IN_PROGRESS)
    t2 = HierarchicalTask(id="TASK-B", title="Pending work", state=TaskState.READY)
    mgr.register_task(t1)
    mgr.register_task(t2)

    engine = ContinuityEngine(task_manager=mgr)
    report = engine.generate_continuity_report()

    assert report.in_progress_count == 1
    assert report.recommended_task == "TASK-A"
    assert "progress" in report.rationale.lower()
