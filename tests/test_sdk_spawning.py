import pytest
from dh_harness.core.contracts import AgentDefinition, AgentRole, ToolPermission
from dh_harness.sdk.adapter import AntigravitySDKAdapter

def test_sdk_adapter_maps_least_privilege_for_readonly_agent():
    adapter = AntigravitySDKAdapter()
    if not adapter.is_available():
        pytest.skip("google.antigravity SDK not installed")

    import google.antigravity as ag

    readonly_agent = AgentDefinition(
        id="independent-reviewer",
        name="Independent Reviewer",
        role=AgentRole.CODE_REVIEWER,
        allowed_tools=[ToolPermission.READ_ONLY],
        system_prompt_template="Strict code review instructions."
    )

    tools = adapter.get_enabled_builtin_tools(readonly_agent)
    assert ag.BuiltinTools.VIEW_FILE in tools
    assert ag.BuiltinTools.FIND_FILE in tools
    assert ag.BuiltinTools.LIST_DIR in tools
    assert ag.BuiltinTools.CREATE_FILE not in tools
    assert ag.BuiltinTools.EDIT_FILE not in tools
    assert ag.BuiltinTools.RUN_COMMAND not in tools

def test_sdk_adapter_maps_developer_privileges():
    adapter = AntigravitySDKAdapter()
    if not adapter.is_available():
        pytest.skip("google.antigravity SDK not installed")

    import google.antigravity as ag

    dev_agent = AgentDefinition(
        id="backend-dev",
        name="Backend Dev",
        role=AgentRole.BACKEND_DEVELOPER,
        allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
        system_prompt_template="Write production code."
    )

    tools = adapter.get_enabled_builtin_tools(dev_agent)
    assert ag.BuiltinTools.CREATE_FILE in tools
    assert ag.BuiltinTools.EDIT_FILE in tools
    assert ag.BuiltinTools.RUN_COMMAND in tools

def test_spawn_agent_for_definition_creates_agent_instance():
    adapter = AntigravitySDKAdapter()
    if not adapter.is_available():
        pytest.skip("google.antigravity SDK not installed")

    import google.antigravity as ag

    agent_def = AgentDefinition(
        id="independent-reviewer",
        name="Independent Reviewer",
        role=AgentRole.CODE_REVIEWER,
        allowed_tools=[ToolPermission.READ_ONLY],
        system_prompt_template="Review without modifying code."
    )

    agent_instance = adapter.spawn_agent_for_definition(agent_def)
    assert isinstance(agent_instance, ag.Agent)

def test_sdk_adapter_unavailable_raises_runtime_error(monkeypatch):
    adapter = AntigravitySDKAdapter()
    monkeypatch.setattr(adapter, "_sdk", None)

    agent_def = AgentDefinition(
        id="test-agent",
        name="Test Agent",
        role=AgentRole.ORCHESTRATOR,
        allowed_tools=[ToolPermission.READ_ONLY]
    )

    with pytest.raises(RuntimeError) as exc_info:
        adapter.spawn_agent_for_definition(agent_def)
    assert "sdk is not available" in str(exc_info.value).lower()
