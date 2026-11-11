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

def test_hooks_engine_enforces_tdd_guard_blocking_and_allowing():
    from dh_harness.tdd.evidence import TDDEvidenceVault
    from dh_harness.tdd.guard import CodeModificationGuard

    vault = TDDEvidenceVault(db_path=":memory:")
    guard = CodeModificationGuard(vault)
    engine = LifecycleHooksEngine(guard=guard)

    # 1. Blocked when active task has no RED evidence
    res_blocked = engine.trigger_pre_file_write(
        file_path="src/dh_harness/feature.py",
        proposed_content="def new_func(): pass",
        context={"active_task_id": "DH-020"}
    )
    assert res_blocked.allowed is False
    assert "TDD Guard Block" in res_blocked.reason

    # Also test trigger_pre_tool_use
    res_tool_blocked = engine.trigger_pre_tool_use(
        tool_name="edit_file",
        tool_args={"path": "src/dh_harness/feature.py"},
        context={"active_task_id": "DH-020"}
    )
    assert res_tool_blocked.allowed is False
    assert "TDD Guard" in res_tool_blocked.reason

    # 2. Record RED evidence
    vault.record_red_evidence("DH-020", "tests/test_feat.py", "", "AssertionError: failed", exit_code=1)

    # 3. Allowed now that RED evidence is recorded
    res_allowed = engine.trigger_pre_file_write(
        file_path="src/dh_harness/feature.py",
        proposed_content="def new_func(): pass",
        context={"active_task_id": "DH-020"}
    )
    assert res_allowed.allowed is True

    res_tool_allowed = engine.trigger_pre_tool_use(
        tool_name="edit_file",
        tool_args={"path": "src/dh_harness/feature.py"},
        context={"active_task_id": "DH-020"}
    )
    assert res_tool_allowed.allowed is True
    vault.close()
