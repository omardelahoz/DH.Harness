import pytest
from dh_harness.core.contracts import (
    InteractionMode,
    TDDPhase,
    TaskState,
    TaskDefinition,
    TaskStep,
    QualityGateResult,
    HierarchicalTask,
    ContinuityReport,
)

def test_interaction_modes():
    modes = [
        InteractionMode.CONVERSATIONAL,
        InteractionMode.INVESTIGATION,
        InteractionMode.BUG_FIX,
        InteractionMode.DEVELOPMENT,
        InteractionMode.COMPLEX_ENGINEERING,
    ]
    assert len(modes) == 5
    assert InteractionMode.CONVERSATIONAL.value == "CONVERSATIONAL"

def test_tdd_phases_sequence():
    phases = [
        TDDPhase.REQUIREMENT,
        TDDPhase.TEST_RED,
        TDDPhase.IMPLEMENT_GREEN,
        TDDPhase.REFACTOR,
        TDDPhase.VERIFY,
        TDDPhase.DONE,
    ]
    assert len(phases) == 6
    assert TDDPhase.TEST_RED.value == "TEST_RED"

def test_task_states_full_lifecycle():
    states = [
        TaskState.BACKLOG,
        TaskState.READY,
        TaskState.IN_PROGRESS,
        TaskState.BLOCKED,
        TaskState.IN_REVIEW,
        TaskState.CHANGES_REQUESTED,
        TaskState.READY_FOR_PR,
        TaskState.PR_OPEN,
        TaskState.MERGED,
        TaskState.DONE,
        TaskState.CANCELLED,
    ]
    assert len(states) == 11
    assert TaskState.DONE.value == "DONE"

def test_hierarchical_task():
    task = HierarchicalTask(
        id="DH-101",
        title="Implement Auth Flow",
        description="OAuth2/OIDC integration",
        state=TaskState.BACKLOG,
        dependencies=["DH-100"]
    )
    assert task.id == "DH-101"
    assert task.state == TaskState.BACKLOG
    assert "DH-100" in task.dependencies

def test_continuity_report():
    report = ContinuityReport(
        completed_count=3,
        in_progress_count=1,
        pending_count=4,
        blocked_count=0,
        parallel_candidates=["DH-102", "DH-103"],
        recommended_task="DH-102",
        rationale="All preconditions met and high priority."
    )
    assert report.recommended_task == "DH-102"
    assert len(report.parallel_candidates) == 2
