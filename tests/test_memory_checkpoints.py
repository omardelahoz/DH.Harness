import pytest
from dh_harness.core.contracts import SessionCheckpoint
from dh_harness.memory.checkpoints import CheckpointManager, CorruptedCheckpointError

def test_create_and_restore_checkpoint(tmp_path):
    mgr = CheckpointManager(storage_dir=str(tmp_path))

    chk = mgr.create_checkpoint(
        session_id="sess_001",
        active_task_id="DH-005",
        active_branch="feature/DH-005-memory-and-session-recovery",
        recent_actions=["Created tests/test_memory_levels.py", "Implemented MultiLevelMemory"],
        pending_steps=["Implement CheckpointManager", "Implement TruncationDigest"]
    )

    assert chk.session_id == "sess_001"
    assert chk.active_task_id == "DH-005"
    assert len(chk.checksum) == 64  # SHA-256

    latest = mgr.get_latest_checkpoint()
    assert latest is not None
    assert latest.session_id == "sess_001"
    assert latest.active_branch == "feature/DH-005-memory-and-session-recovery"

def test_restore_checkpoint_detects_tampering(tmp_path):
    mgr = CheckpointManager(storage_dir=str(tmp_path))

    chk = mgr.create_checkpoint(
        session_id="sess_secure",
        active_task_id="DH-001",
        active_branch="main",
        recent_actions=["Bootstrap"],
        pending_steps=[]
    )

    # Tamper with the saved checkpoint file
    chk_file = tmp_path / "checkpoints" / f"{chk.session_id}.json"
    content = chk_file.read_text(encoding="utf-8")
    tampered_content = content.replace("DH-001", "DH-HACKED")
    chk_file.write_text(tampered_content, encoding="utf-8")

    with pytest.raises(CorruptedCheckpointError) as exc_info:
        mgr.restore_checkpoint("sess_secure")
    assert "checksum mismatch" in str(exc_info.value).lower()

def test_checkpoint_history_order(tmp_path):
    mgr = CheckpointManager(storage_dir=str(tmp_path))

    mgr.create_checkpoint("s1", "T-1", "main", ["a1"], [])
    mgr.create_checkpoint("s2", "T-2", "main", ["a2"], [])

    history = mgr.list_checkpoints()
    assert len(history) == 2
    # Latest first
    assert history[0].session_id == "s2"
    assert history[1].session_id == "s1"
