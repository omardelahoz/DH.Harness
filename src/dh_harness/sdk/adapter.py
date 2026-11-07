from __future__ import annotations
import sys
from typing import Optional, Dict, Any, List
from dh_harness.core.contracts import AgentDefinition, ToolPermission

class AntigravitySDKAdapter:
    """
    Adapter around the official google.antigravity Python SDK.
    Isolates external SDK dependencies and manages agent lease lifecycle.
    """

    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self._sdk = None
        self._load_sdk()

    def _load_sdk(self):
        try:
            import google.antigravity as ag
            self._sdk = ag
        except ImportError:
            self._sdk = None

    def is_available(self) -> bool:
        return self._sdk is not None

    def get_runtime_info(self) -> Dict[str, Any]:
        if not self.is_available():
            return {
                "available": False,
                "package": "google.antigravity",
                "version": None,
                "error": "Package not installed in current environment"
            }
        
        # Package is available
        version = getattr(self._sdk, "__version__", "0.1.23")
        return {
            "available": True,
            "package": "google.antigravity",
            "version": version,
            "has_agent": hasattr(self._sdk, "Agent"),
            "has_local_config": hasattr(self._sdk, "LocalAgentConfig")
        }

    def create_local_agent_config(
        self,
        system_instructions: str,
        enable_write_tools: bool = False
    ) -> Any:
        if not self.is_available():
            raise RuntimeError("google.antigravity SDK is not available.")

        capabilities = None
        if enable_write_tools and hasattr(self._sdk, "CapabilitiesConfig"):
            capabilities = self._sdk.CapabilitiesConfig()

        if hasattr(self._sdk, "LocalAgentConfig"):
            if capabilities:
                return self._sdk.LocalAgentConfig(
                    system_instructions=system_instructions,
                    capabilities=capabilities
                )
            return self._sdk.LocalAgentConfig(
                system_instructions=system_instructions
            )
        return None

    def spawn_agent(self, config: Any) -> Any:
        if not self.is_available():
            raise RuntimeError("google.antigravity SDK is not available.")
        return self._sdk.Agent(config)

    def get_enabled_builtin_tools(self, agent_def: AgentDefinition) -> List[Any]:
        """
        Calculates the exact set of SDK BuiltinTools permitted for the given agent
        adhering strictly to the Principle of Least Privilege.
        """
        if not self.is_available():
            return []

        ag = self._sdk
        tools: List[Any] = []

        if ToolPermission.READ_ONLY in agent_def.allowed_tools:
            tools.extend([
                ag.BuiltinTools.VIEW_FILE,
                ag.BuiltinTools.FIND_FILE,
                ag.BuiltinTools.LIST_DIR,
                ag.BuiltinTools.SEARCH_DIR,
                ag.BuiltinTools.READ_URL_CONTENT,
            ])

        if ToolPermission.FILE_WRITE in agent_def.allowed_tools:
            tools.extend([
                ag.BuiltinTools.CREATE_FILE,
                ag.BuiltinTools.EDIT_FILE,
            ])

        if ToolPermission.RUN_COMMAND in agent_def.allowed_tools or ToolPermission.TERMINAL_SANDBOX in agent_def.allowed_tools:
            tools.append(ag.BuiltinTools.RUN_COMMAND)

        if ToolPermission.MCP_TOOLS in agent_def.allowed_tools:
            tools.append(ag.BuiltinTools.ASK_QUESTION)

        # Return unique tools preserving insertion order
        return list(dict.fromkeys(tools))

    def spawn_agent_for_definition(self, agent_def: AgentDefinition) -> Any:
        """
        Spawns an official google.antigravity Agent instance configured specifically
        for the given AgentDefinition with least privilege capabilities.
        """
        if not self.is_available():
            raise RuntimeError("google.antigravity SDK is not available.")

        enabled_tools = self.get_enabled_builtin_tools(agent_def)
        capabilities = None
        if hasattr(self._sdk, "CapabilitiesConfig"):
            capabilities = self._sdk.CapabilitiesConfig(
                enabled_tools=enabled_tools,
                enable_subagents=False
            )

        instructions = (
            agent_def.system_prompt_template
            or f"You are {agent_def.name} ({agent_def.role.value}). {agent_def.description}"
        )

        config = self._sdk.LocalAgentConfig(
            system_instructions=instructions,
            capabilities=capabilities
        )
        return self.spawn_agent(config)
