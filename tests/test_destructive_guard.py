import pytest
from dh_harness.security.guard import (
    DestructiveOperationGuard,
    DestructiveOperationBlockedError
)

def test_guard_blocks_destructive_sql():
    guard = DestructiveOperationGuard()

    destructive_queries = [
        "DROP DATABASE ProductionDB;",
        "drop table users cascade;",
        "TRUNCATE TABLE audit_logs;",
        "DELETE FROM users;"
    ]

    for sql in destructive_queries:
        result = guard.check_command(sql)
        assert result.is_destructive is True

        with pytest.raises(DestructiveOperationBlockedError):
            guard.guard(sql, authorized=False)

def test_guard_allows_safe_sql():
    guard = DestructiveOperationGuard()

    safe_queries = [
        "SELECT id, username FROM users WHERE is_active = 1;",
        "DELETE FROM sessions WHERE expired_at < NOW();",
        "UPDATE accounts SET balance = balance + 100 WHERE id = 1;"
    ]

    for sql in safe_queries:
        result = guard.check_command(sql)
        assert result.is_destructive is False
        # Should not raise
        guard.guard(sql, authorized=False)

def test_guard_blocks_destructive_git():
    guard = DestructiveOperationGuard()

    assert guard.check_command("git push --force origin main").is_destructive is True
    assert guard.check_command("git push -f origin master").is_destructive is True
    assert guard.check_command("git branch -D main").is_destructive is True

    # Safe git commands
    assert guard.check_command("git push -u origin feature/my-branch").is_destructive is False
    assert guard.check_command("git status").is_destructive is False

def test_guard_blocks_destructive_filesystem():
    guard = DestructiveOperationGuard()

    assert guard.check_command("rm -rf /").is_destructive is True
    assert guard.check_command("del /f /s /q C:\\").is_destructive is True

def test_guard_permits_when_authorized():
    guard = DestructiveOperationGuard()
    cmd = "DROP TABLE test_temp_table;"

    # Should not raise when authorized=True
    guard.guard(cmd, authorized=True)
    res = guard.check_command(cmd)
    assert res.is_destructive is True
