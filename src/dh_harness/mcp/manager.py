from __future__ import annotations
import json
import os
import shutil
import subprocess
import time
from typing import Dict, List, Optional, Tuple, Any

from dh_harness.core.contracts import (
    MCPServerInfo,
    MCPServerState,
    MCPToolSchema
)

class MCPManager:
    """
    Dynamic Model Context Protocol (MCP) Manager (info.md Section 7).
    Discovers, validates, and manages external MCP tools and servers
    configured in .agents/mcp_config.json.
    """

    BUILTIN_TOOL_REGISTRY: Dict[str, List[MCPToolSchema]] = {
        "git": [
            MCPToolSchema(
                name="git_status",
                description="Get the status of the git working tree",
                server_name="git",
                input_schema={
                    "type": "object",
                    "properties": {
                        "options": {"type": "array", "items": {"type": "string"}}
                    }
                }
            ),
            MCPToolSchema(
                name="git_diff",
                description="Show changes between commits, commit and working tree, etc",
                server_name="git",
                input_schema={
                    "type": "object",
                    "properties": {
                        "staged": {"type": "boolean"},
                        "path": {"type": "string"}
                    }
                }
            ),
            MCPToolSchema(
                name="git_commit",
                description="Record changes to the repository",
                server_name="git",
                input_schema={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            )
        ],
        "sqlite": [
            MCPToolSchema(
                name="sqlite_query",
                description="Execute read-only SQL query against SQLite database",
                server_name="sqlite",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            )
        ]
    }

    def __init__(self, config_path: Optional[str] = None):
        self.workspace_root = os.getcwd()
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = os.path.join(self.workspace_root, ".agents", "mcp_config.json")
        self._servers: Dict[str, MCPServerInfo] = {}
        self.discover_servers()

    def discover_servers(self) -> Dict[str, MCPServerInfo]:
        """Discovers and parses configured MCP servers from .agents/mcp_config.json."""
        self._servers.clear()
        if not os.path.isfile(self.config_path):
            return self._servers

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            servers_dict = data.get("mcpServers", {})
            for name, cfg in servers_dict.items():
                tools = self.BUILTIN_TOOL_REGISTRY.get(name, [])
                self._servers[name] = MCPServerInfo(
                    name=name,
                    command=cfg.get("command", ""),
                    args=cfg.get("args", []),
                    description=cfg.get("description", ""),
                    state=MCPServerState.STOPPED,
                    tool_count=len(tools)
                )
        except Exception:
            pass

        return dict(self._servers)

    def ping_server(self, server_name: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """Pings the server command to check availability and measure latency."""
        if server_name not in self._servers:
            return False, None, f"Server '{server_name}' not configured in mcp_config.json"

        info = self._servers[server_name]
        cmd = info.command
        if not cmd:
            return False, None, f"Server '{server_name}' has no command configured"

        # Check executable existence in PATH
        executable = shutil.which(cmd)
        if not executable:
            return False, None, f"Executable '{cmd}' not found on system PATH"

        start_time = time.perf_counter()
        try:
            # Ping using --version or harmless invocation
            res = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            if res.returncode == 0:
                info.state = MCPServerState.RUNNING
                info.latency_ms = round(elapsed_ms, 2)
                return True, info.latency_ms, None
            else:
                info.state = MCPServerState.ERROR
                return False, None, f"Command exited with code {res.returncode}"
        except Exception as e:
            info.state = MCPServerState.UNRESPONSIVE
            return False, None, str(e)

    def list_tools(self, server_name: Optional[str] = None) -> List[MCPToolSchema]:
        """Lists available tools exposed by servers."""
        tools: List[MCPToolSchema] = []
        if server_name:
            return list(self.BUILTIN_TOOL_REGISTRY.get(server_name, []))

        for s_tools in self.BUILTIN_TOOL_REGISTRY.values():
            tools.extend(s_tools)
        return tools

    def validate_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validates tool invocation payload against its JSON schema."""
        target_tool = None
        for s_tools in self.BUILTIN_TOOL_REGISTRY.values():
            for t in s_tools:
                if t.name == tool_name:
                    target_tool = t
                    break
            if target_tool:
                break

        if not target_tool:
            return False, f"Unknown tool '{tool_name}'"

        schema = target_tool.input_schema
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in arguments:
                return False, f"Missing required parameter '{field}' for tool '{tool_name}'"

        # Validate types if specified
        props = schema.get("properties", {})
        for key, val in arguments.items():
            if key in props:
                expected_type = props[key].get("type")
                if expected_type == "string" and not isinstance(val, str):
                    return False, f"Parameter '{key}' must be a string"
                elif expected_type == "boolean" and not isinstance(val, bool):
                    return False, f"Parameter '{key}' must be a boolean"
                elif expected_type == "array" and not isinstance(val, list):
                    return False, f"Parameter '{key}' must be an array"
                elif expected_type == "object" and not isinstance(val, dict):
                    return False, f"Parameter '{key}' must be an object"

        return True, None
