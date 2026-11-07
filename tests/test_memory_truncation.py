import pytest
from dh_harness.core.contracts import SessionCheckpoint, MemoryLevel
from dh_harness.memory.levels import MultiLevelMemory
from dh_harness.memory.truncation import ContextTruncationGuard

def test_truncation_guard_detects_overflow_threshold():
    guard = ContextTruncationGuard(max_tokens=1000)

    short_history = [{"role": "user", "content": "hello world"}]
    assert guard.should_compact(short_history) is False

    long_text = "This is a long engineering log entry with detailed output. " * 300
    long_history = [{"role": "user", "content": long_text}]
    assert guard.should_compact(long_history) is True

def test_truncation_guard_generates_compact_digest(tmp_path):
    guard = ContextTruncationGuard(max_tokens=4000)
    mem = MultiLevelMemory(storage_dir=str(tmp_path))

    mem.store(
        level=MemoryLevel.PROJECT,
        key="tech_stack",
        content="Python 3.12, Clean Architecture, Deterministic TDD"
    )

    checkpoint = SessionCheckpoint(
        session_id="sess_trunc_001",
        active_task_id="DH-005",
        active_branch="feature/DH-005-memory-and-session-recovery",
        recent_actions=[
            "Implemented MultiLevelMemory with secret redaction",
            "Implemented CheckpointManager with SHA-256 integrity"
        ],
        pending_steps=[
            "Implement ContextTruncationGuard",
            "Add CLI memory commands"
        ],
        created_at="2026-11-07T10:45:00",
        checksum="dummy_checksum"
    )

    recent_events = [
        "pytest run passed with 3 items",
        "AST syntax verification passed"
    ]

    digest = guard.generate_compact_digest(
        checkpoint=checkpoint,
        memory=mem,
        recent_events=recent_events
    )

    assert "# Compact Session Context Digest" in digest
    assert "**Active Task:** DH-005" in digest
    assert "**Branch:** feature/DH-005-memory-and-session-recovery" in digest
    assert "Implemented MultiLevelMemory" in digest
    assert "Implement ContextTruncationGuard" in digest
    assert guard.estimate_tokens(digest) < 1000  # Stays compact
