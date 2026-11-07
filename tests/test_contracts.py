import pytest
from dh_harness.core.contracts import (
    InteractionMode,
    TDDPhase,
    TaskDefinition,
    TaskStep,
    QualityGateResult,
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

def test_task_definition_validation():
    task = TaskDefinition(
        title="Test Task",
        description="A sample test task",
        mode=InteractionMode.DEVELOPMENT,
    )
    assert task.title == "Test Task"
    assert task.status == "PENDING"
    assert len(task.steps) == 0
