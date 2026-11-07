from __future__ import annotations
import os
from typing import Dict, List, Optional, Callable, Any

from dh_harness.core.contracts import HookEventType, HookExecutionResult

class LifecycleHooksEngine:
    """
    Antigravity Lifecycle Hooks Engine (info.md § 18).
    Manages session lifecycle events and enforces pre/post-execution guards.
    """

    def __init__(self):
        self._hooks: Dict[HookEventType, List[Callable[[Dict[str, Any]], HookExecutionResult]]] = {
            event: [] for event in HookEventType
        }
        self._affected_files: List[str] = []

    def register_hook(
        self,
        event_type: HookEventType,
        callback: Callable[[Dict[str, Any]], HookExecutionResult]
    ) -> None:
        """Registers a lifecycle hook callback."""
        self._hooks[event_type].append(callback)

    def trigger_session_start(self, workspace: str, agent_id: str) -> HookExecutionResult:
        """Dispatches SessionStart event to registered listeners."""
        context = {"workspace": workspace, "agent_id": agent_id}
        last_res = None
        for cb in self._hooks[HookEventType.SESSION_START]:
            res = cb(context)
            if not res.allowed:
                return res
            last_res = res
        return last_res or HookExecutionResult(
            event_type=HookEventType.SESSION_START,
            allowed=True,
            context_data={"workspace": workspace, "agent_id": agent_id}
        )

    def trigger_pre_tool_use(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """
        Enforces pre-modification safety guards before executing tool (info.md § 18.1):
        - Verifies active task presence before allowing edits to production code (src/).
        """
        # Execute custom callbacks first
        ctx_payload = {"tool_name": tool_name, "tool_args": tool_args, **context}
        for cb in self._hooks[HookEventType.PRE_TOOL_USE]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        # Built-in Pre-Modification Guard:
        write_tools = {"write_file", "edit_file", "append_file"}
        if tool_name.lower() in write_tools:
            target_path = tool_args.get("path") or tool_args.get("Path") or ""
            target_norm = target_path.replace("\\", "/")

            # If modifying src/ but not tests/
            if "src/" in target_norm and not target_norm.startswith("tests/"):
                active_task = context.get("active_task_id")
                if not active_task:
                    return HookExecutionResult(
                        event_type=HookEventType.PRE_TOOL_USE,
                        allowed=False,
                        reason="Pre-modification blocked: Modifying production code in src/ requires an active task assigned."
                    )

        return HookExecutionResult(
            event_type=HookEventType.PRE_TOOL_USE,
            allowed=True,
            context_data={"tool_name": tool_name}
        )

    def trigger_post_tool_use(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        result: Any,
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """
        Records post-modification traces (info.md § 18.2):
        - Tracks affected files for auditing and regression targeting.
        """
        write_tools = {"write_file", "edit_file", "append_file"}
        if tool_name.lower() in write_tools:
            target_path = tool_args.get("path") or tool_args.get("Path") or ""
            if target_path and target_path not in self._affected_files:
                self._affected_files.append(target_path)

        ctx_payload = {"tool_name": tool_name, "tool_args": tool_args, "result": result, **context}
        for cb in self._hooks[HookEventType.POST_TOOL_USE]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.POST_TOOL_USE,
            allowed=True,
            context_data={"tool_name": tool_name, "affected_files": list(self._affected_files)}
        )

    def trigger_stop(self, context: Dict[str, Any]) -> HookExecutionResult:
        """Evaluates stop conditions and verifies clean session exit (info.md § 18.3)."""
        for cb in self._hooks[HookEventType.STOP]:
            res = cb(context)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.STOP,
            allowed=True,
            context_data=context
        )

    def get_affected_files(self) -> List[str]:
        """Returns the list of files touched during the session."""
        return list(self._affected_files)
