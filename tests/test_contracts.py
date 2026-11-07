import pytest
from dh_harness.core.contracts import (
    InteractionMode,
    TDDPhase,
    TaskState,
    AgentRole,
    ToolPermission,
    AgentDefinition,
    AgentTaskContract,
    AgentExecutionResult,
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

def test_agent_roles_and_permissions():
    roles = [
        AgentRole.ORCHESTRATOR,
        AgentRole.SOLUTION_ARCHITECT,
        AgentRole.BACKEND_DEVELOPER,
        AgentRole.FRONTEND_DEVELOPER,
        AgentRole.DATABASE_ENGINEER,
        AgentRole.SECURITY_ENGINEER,
        AgentRole.CODE_REVIEWER,
        AgentRole.QA_ENGINEER,
        AgentRole.TECHNICAL_WRITER,
    ]
    assert len(roles) == 9

    permissions = [
        ToolPermission.READ_ONLY,
        ToolPermission.FILE_WRITE,
        ToolPermission.RUN_COMMAND,
        ToolPermission.TERMINAL_SANDBOX,
        ToolPermission.GIT_OPERATIONS,
        ToolPermission.MCP_TOOLS,
    ]
    assert len(permissions) == 6

def test_agent_definition():
    agent = AgentDefinition(
        id="backend-expert",
        name="Backend Specialist",
        role=AgentRole.BACKEND_DEVELOPER,
        description="Senior backend engineer specializing in Clean Architecture and TDD",
        allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
        required_skills=["csharp", "python", "sql"],
        evaluation_criteria=["TDD pass", "Clean code", "Zero fake data"]
    )
    assert agent.id == "backend-expert"
    assert ToolPermission.FILE_WRITE in agent.allowed_tools

def test_agent_task_contract_and_result():
    contract = AgentTaskContract(
        task_id="TASK-42",
        agent_id="backend-expert",
        objective="Implement repository query",
        input_artifacts=["specs/001/SPEC.md"],
        expected_outputs=["src/repository.py", "tests/test_repository.py"]
    )
    assert contract.task_id == "TASK-42"
    assert len(contract.expected_outputs) == 2

    result = AgentExecutionResult(
        task_id="TASK-42",
        agent_id="backend-expert",
        status="COMPLETED",
        changes_made=["src/repository.py"],
        tests_run=["tests/test_repository.py"],
        evidence=["Exit code 0, 5 tests passed"],
        output_artifacts=["src/repository.py"]
    )
    assert result.status == "COMPLETED"
    assert len(result.changes_made) == 1
