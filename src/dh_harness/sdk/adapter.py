from __future__ import annotations
import sys
from typing import Optional, Dict, Any

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
