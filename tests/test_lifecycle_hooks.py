import pytest
from dh_harness.core.contracts import HookEventType, HookExecutionResult
from dh_harness.hooks.engine import LifecycleHooksEngine

def test_hooks_engine_executes_registered_callbacks():
    engine = LifecycleHooksEngine()
    executed = []

    def on_session_start(ctx):
        executed.append(ctx.get("agent_id"))
        return HookExecutionResult(
            event_type=HookEventType.SESSION_START,
            allowed=True,
            context_data={"initialized": True}
        )

    engine.register_hook(HookEventType.SESSION_START, on_session_start)
    res = engine.trigger_session_start(workspace="/workspace", agent_id="dev-agent-1")

    assert res.allowed is True
    assert "dev-agent-1" in executed
    assert res.context_data.get("initialized") is True

def test_hooks_engine_pre_tool_use_blocks_src_without_active_task():
    engine = LifecycleHooksEngine()

    # Attempting to edit source code with no active task or task in BACKLOG
    res = engine.trigger_pre_tool_use(
        tool_name="edit_file",
        tool_args={"path": "src/dh_harness/feature.py"},
        context={"active_task_id": None}
    )

    assert res.allowed is False
    assert "active task" in res.reason.lower()

def test_hooks_engine_pre_tool_use_permits_test_file_edits():
    engine = LifecycleHooksEngine()

    # Test file edits should always be allowed to enable TDD RED phase
    res = engine.trigger_pre_tool_use(
        tool_name="write_file",
        tool_args={"path": "tests/test_new_feature.py"},
        context={"active_task_id": "DH-009"}
    )

    assert res.allowed is True

def test_hooks_engine_post_tool_use_records_affected_files():
    engine = LifecycleHooksEngine()

    res = engine.trigger_post_tool_use(
        tool_name="write_file",
        tool_args={"path": "src/dh_harness/quality/engine.py"},
        result="Created file",
        context={"active_task_id": "DH-009"}
    )

    assert res.allowed is True
    affected = engine.get_affected_files()
    assert "src/dh_harness/quality/engine.py" in affected

def test_hooks_engine_stop_verifies_clean_state():
    engine = LifecycleHooksEngine()
    res = engine.trigger_stop(context={"active_task_id": "DH-009", "has_blockers": False})

    assert res.allowed is True
    assert res.event_type == HookEventType.STOP
