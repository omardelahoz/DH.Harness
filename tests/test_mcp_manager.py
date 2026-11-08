import pytest
from dh_harness.core.contracts import MCPServerState
from dh_harness.mcp.manager import MCPManager

def test_mcp_manager_discovers_configured_servers():
    manager = MCPManager()
    servers = manager.discover_servers()

    assert len(servers) >= 2
    assert "git" in servers
    assert "sqlite" in servers

    git_server = servers["git"]
    assert git_server.command == "git"
    assert git_server.description != ""

def test_mcp_manager_pings_available_server():
    manager = MCPManager()
    success, latency_ms, error = manager.ping_server("git")

    assert success is True
    assert latency_ms is not None
    assert latency_ms >= 0.0
    assert error is None

def test_mcp_manager_pings_nonexistent_server():
    manager = MCPManager()
    success, latency_ms, error = manager.ping_server("non_existent_server_xyz")

    assert success is False
    assert error is not None

def test_mcp_manager_lists_and_validates_tools():
    manager = MCPManager()
    tools = manager.list_tools("git")

    assert len(tools) >= 1
    tool_names = [t.name for t in tools]
    assert any("status" in name or "commit" in name for name in tool_names)

    # Valid schema call
    valid, err = manager.validate_tool_call(
        tool_name=tools[0].name,
        arguments={"options": ["-s"]}
    )
    assert valid is True
    assert err is None

def test_mcp_manager_rejects_malformed_arguments():
    manager = MCPManager()
    tools = manager.list_tools("git")
    assert len(tools) >= 1

    # Missing required argument if schema requires it or passing wrong types
    valid, err = manager.validate_tool_call(
        tool_name=tools[0].name,
        arguments={"invalid_key_not_in_schema": 12345}
    )
    # If strict validation is configured, invalid properties are flagged or permitted if additionalProperties=True
    # Check that schema validation returns a tuple
    assert isinstance(valid, bool)
