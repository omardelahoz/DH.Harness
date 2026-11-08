import pytest
from dh_harness.core.contracts import HookEventType, HookExecutionResult
from dh_harness.hooks.engine import LifecycleHooksEngine

def test_hooks_engine_pre_file_write_blocks_src_without_task():
    engine = LifecycleHooksEngine()

    res = engine.trigger_pre_file_write(
        file_path="src/dh_harness/critical.py",
        proposed_content="print('change')",
        context={"active_task_id": None}
    )

    assert res.allowed is False
    assert "active task" in res.reason.lower()

def test_hooks_engine_pre_file_write_allows_with_active_task():
    engine = LifecycleHooksEngine()

    res = engine.trigger_pre_file_write(
        file_path="src/dh_harness/critical.py",
        proposed_content="print('change')",
        context={"active_task_id": "DH-015"}
    )

    assert res.allowed is True

def test_hooks_engine_pre_file_write_detects_secrets():
    engine = LifecycleHooksEngine()

    res = engine.trigger_pre_file_write(
        file_path="src/config.py",
        proposed_content='AWS_KEY = "AKIAIOSFODNN7EXAMPLE"',
        context={"active_task_id": "DH-015"}
    )

    assert res.allowed is False
    assert "secret" in res.reason.lower()

def test_hooks_engine_post_file_write_records_file_and_emits_log():
    engine = LifecycleHooksEngine()

    res = engine.trigger_post_file_write(
        file_path="src/dh_harness/security/sast.py",
        context={"active_task_id": "DH-015"}
    )

    assert res.allowed is True
    assert "src/dh_harness/security/sast.py" in engine.get_affected_files()
    assert len(engine.get_execution_log()) >= 1

def test_hooks_engine_pre_git_push_enforces_clean_gates():
    engine = LifecycleHooksEngine()

    # Blocked if blockers exist
    res_blocked = engine.trigger_pre_git_push(
        branch="feature/DH-015-test",
        remote="origin",
        context={"has_blockers": True, "blockers": ["Test failure in test_sast"]}
    )
    assert res_blocked.allowed is False

    # Allowed if clean
    res_clean = engine.trigger_pre_git_push(
        branch="feature/DH-015-test",
        remote="origin",
        context={"has_blockers": False, "blockers": []}
    )
    assert res_clean.allowed is True

def test_hooks_engine_on_task_blocked_logs_diagnostic():
    engine = LifecycleHooksEngine()

    res = engine.trigger_on_task_blocked(
        task_id="DH-015",
        reason="Unit tests failing on line 42",
        context={"agent": "python-lead-engineer"}
    )

    assert res.allowed is True
    assert res.context_data.get("task_id") == "DH-015"
    log = engine.get_execution_log()
    assert any(entry["event"] == HookEventType.ON_TASK_BLOCKED.value for entry in log)
