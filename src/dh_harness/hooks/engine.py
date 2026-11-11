from __future__ import annotations
import os
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any

from dh_harness.core.contracts import HookEventType, HookExecutionResult, InteractionMode
from dh_harness.security.scanner import SecretScanner
from dh_harness.tdd.guard import CodeModificationGuard

class LifecycleHooksEngine:
    """
    Antigravity Lifecycle Hooks Engine (info.md § 18).
    Manages session lifecycle events and enforces pre/post-execution guards.
    """

    def __init__(self, guard: Optional[CodeModificationGuard] = None):
        self._hooks: Dict[HookEventType, List[Callable[[Dict[str, Any]], HookExecutionResult]]] = {
            event: [] for event in HookEventType
        }
        self._affected_files: List[str] = []
        self._execution_log: List[Dict[str, Any]] = []
        self._secret_scanner = SecretScanner()
        self._guard = guard

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
        self._log_event(HookEventType.SESSION_START, context)
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
        ctx_payload = {"tool_name": tool_name, "tool_args": tool_args, **context}
        self._log_event(HookEventType.PRE_TOOL_USE, ctx_payload)

        # Execute custom callbacks first
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

                if self._guard is not None or context.get("enforce_tdd_guard"):
                    guard_instance = self._guard or CodeModificationGuard()
                    mode = context.get("mode", InteractionMode.DEVELOPMENT)
                    decision = guard_instance.evaluate_modification(target_path, mode=mode, task_id=active_task)
                    if not decision.allowed:
                        return HookExecutionResult(
                            event_type=HookEventType.PRE_TOOL_USE,
                            allowed=False,
                            reason=f"Pre-modification blocked by TDD Guard: {decision.reason}"
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
        self._log_event(HookEventType.POST_TOOL_USE, ctx_payload)

        for cb in self._hooks[HookEventType.POST_TOOL_USE]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.POST_TOOL_USE,
            allowed=True,
            context_data={"tool_name": tool_name, "affected_files": list(self._affected_files)}
        )

    def trigger_pre_file_write(
        self,
        file_path: str,
        proposed_content: str,
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """
        Granular pre-write hook:
        - Validates active task presence when touching production files (src/).
        - Scans proposed content for hardcoded secrets, preventing credential leaks.
        """
        ctx_payload = {"file_path": file_path, "context": context}
        self._log_event(HookEventType.PRE_FILE_WRITE, ctx_payload)

        target_norm = file_path.replace("\\", "/")
        if "src/" in target_norm and not target_norm.startswith("tests/"):
            active_task = context.get("active_task_id")
            if not active_task:
                return HookExecutionResult(
                    event_type=HookEventType.PRE_FILE_WRITE,
                    allowed=False,
                    reason="Pre-file-write blocked: Modifying production code in src/ requires an active task assigned."
                )

            if self._guard is not None or context.get("enforce_tdd_guard"):
                guard_instance = self._guard or CodeModificationGuard()
                mode = context.get("mode", InteractionMode.DEVELOPMENT)
                decision = guard_instance.evaluate_modification(file_path, mode=mode, task_id=active_task)
                if not decision.allowed:
                    return HookExecutionResult(
                        event_type=HookEventType.PRE_FILE_WRITE,
                        allowed=False,
                        reason=f"Pre-file-write blocked by TDD Guard: {decision.reason}"
                    )

        # Secret scanning on proposed content
        if proposed_content:
            secret_findings = self._secret_scanner.scan_content(proposed_content, file_path)
            if secret_findings:
                sec = secret_findings[0]
                return HookExecutionResult(
                    event_type=HookEventType.PRE_FILE_WRITE,
                    allowed=False,
                    reason=f"Pre-file-write blocked: Hardcoded secret detected ({sec.secret_type}) at line {sec.line_number}."
                )

        for cb in self._hooks[HookEventType.PRE_FILE_WRITE]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.PRE_FILE_WRITE,
            allowed=True,
            context_data={"file_path": file_path}
        )

    def trigger_post_file_write(
        self,
        file_path: str,
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """Granular post-write hook: records file modification in traceability and audit history."""
        if file_path and file_path not in self._affected_files:
            self._affected_files.append(file_path)

        ctx_payload = {"file_path": file_path, **context}
        self._log_event(HookEventType.POST_FILE_WRITE, ctx_payload)

        for cb in self._hooks[HookEventType.POST_FILE_WRITE]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.POST_FILE_WRITE,
            allowed=True,
            context_data={"file_path": file_path, "affected_files": list(self._affected_files)}
        )

    def trigger_pre_git_push(
        self,
        branch: str,
        remote: str,
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """Granular pre-push hook: ensures zero active blockers and verified DoD before pushing remote."""
        ctx_payload = {"branch": branch, "remote": remote, **context}
        self._log_event(HookEventType.PRE_GIT_PUSH, ctx_payload)

        if context.get("has_blockers", False):
            blockers = context.get("blockers", [])
            return HookExecutionResult(
                event_type=HookEventType.PRE_GIT_PUSH,
                allowed=False,
                reason=f"Pre-git-push blocked: Active quality gate blockers detected ({', '.join(blockers)})."
            )

        for cb in self._hooks[HookEventType.PRE_GIT_PUSH]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.PRE_GIT_PUSH,
            allowed=True,
            context_data={"branch": branch, "remote": remote}
        )

    def trigger_on_task_blocked(
        self,
        task_id: str,
        reason: str,
        context: Dict[str, Any]
    ) -> HookExecutionResult:
        """Granular task-blocked hook: logs diagnostic traces and triggers continuity recalculation."""
        ctx_payload = {"task_id": task_id, "reason": reason, **context}
        self._log_event(HookEventType.ON_TASK_BLOCKED, ctx_payload)

        for cb in self._hooks[HookEventType.ON_TASK_BLOCKED]:
            res = cb(ctx_payload)
            if not res.allowed:
                return res

        return HookExecutionResult(
            event_type=HookEventType.ON_TASK_BLOCKED,
            allowed=True,
            context_data=ctx_payload
        )

    def trigger_stop(self, context: Dict[str, Any]) -> HookExecutionResult:
        """Evaluates stop conditions and verifies clean session exit (info.md § 18.3)."""
        self._log_event(HookEventType.STOP, context)
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

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Returns the audit log of all hook events executed during the session."""
        return list(self._execution_log)

    def _log_event(self, event_type: HookEventType, payload: Dict[str, Any]) -> None:
        self._execution_log.append({
            "event": event_type.value,
            "timestamp": datetime.now().isoformat(),
            "payload": payload
        })
