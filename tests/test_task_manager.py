import pytest
from dh_harness.core.contracts import TaskState, HierarchicalTask
from dh_harness.tasks.manager import TaskManager, TaskStateTransitionError

def test_task_manager_register_and_get():
    mgr = TaskManager()
    task = HierarchicalTask(
        id="DH-001",
        title="Setup Auth",
        state=TaskState.BACKLOG
    )
    mgr.register_task(task)
    retrieved = mgr.get_task("DH-001")
    assert retrieved is not None
    assert retrieved.id == "DH-001"
    assert retrieved.state == TaskState.BACKLOG

def test_task_manager_valid_transitions():
    mgr = TaskManager()
    task = HierarchicalTask(id="DH-002", title="API Endpoint")
    mgr.register_task(task)

    mgr.transition_state("DH-002", TaskState.READY)
    assert mgr.get_task("DH-002").state == TaskState.READY

    mgr.transition_state("DH-002", TaskState.IN_PROGRESS)
    assert mgr.get_task("DH-002").state == TaskState.IN_PROGRESS

    mgr.transition_state("DH-002", TaskState.IN_REVIEW)
    assert mgr.get_task("DH-002").state == TaskState.IN_REVIEW

    mgr.transition_state("DH-002", TaskState.READY_FOR_PR)
    assert mgr.get_task("DH-002").state == TaskState.READY_FOR_PR

    mgr.transition_state("DH-002", TaskState.PR_OPEN)
    assert mgr.get_task("DH-002").state == TaskState.PR_OPEN

    mgr.transition_state("DH-002", TaskState.MERGED)
    assert mgr.get_task("DH-002").state == TaskState.MERGED

    mgr.transition_state("DH-002", TaskState.DONE, evidence="All gates passed and PR merged")
    assert mgr.get_task("DH-002").state == TaskState.DONE

def test_task_manager_blocks_done_without_evidence():
    mgr = TaskManager()
    task = HierarchicalTask(id="DH-003", title="Payment Gateway")
    mgr.register_task(task)
    mgr.transition_state("DH-003", TaskState.READY)
    mgr.transition_state("DH-003", TaskState.IN_PROGRESS)
    mgr.transition_state("DH-003", TaskState.IN_REVIEW)
    mgr.transition_state("DH-003", TaskState.READY_FOR_PR)
    mgr.transition_state("DH-003", TaskState.PR_OPEN)
    mgr.transition_state("DH-003", TaskState.MERGED)

    # Attempting to transition to DONE without evidence must raise error
    with pytest.raises(TaskStateTransitionError) as exc_info:
        mgr.transition_state("DH-003", TaskState.DONE, evidence="")
    assert "evidence" in str(exc_info.value).lower()

def test_task_manager_blocks_in_progress_with_unmet_dependencies():
    mgr = TaskManager()
    parent = HierarchicalTask(id="DH-10", title="DB Migration", state=TaskState.BACKLOG)
    child = HierarchicalTask(id="DH-11", title="User Service", state=TaskState.BACKLOG, dependencies=["DH-10"])

    mgr.register_task(parent)
    mgr.register_task(child)

    mgr.transition_state("DH-11", TaskState.READY)
    # Child cannot start IN_PROGRESS while parent is not DONE/MERGED
    with pytest.raises(TaskStateTransitionError) as exc_info:
        mgr.transition_state("DH-11", TaskState.IN_PROGRESS)
    assert "dependencies" in str(exc_info.value).lower()
