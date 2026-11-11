import os
import sys
import tempfile
import sqlite3
import pytest
from dh_harness.tdd.evidence import TDDEvidenceVault, InvalidRedEvidenceError, GENESIS_HASH

def test_record_valid_red_evidence():
    vault = TDDEvidenceVault(db_path=":memory:")
    record = vault.record_red_evidence(
        task_id="DH-100",
        test_file="tests/test_calc.py",
        stdout="",
        stderr="AssertionError: 15 != 20",
        exit_code=1
    )
    assert record.task_id == "DH-100"
    assert record.exit_code == 1
    assert len(record.sha256_hash) == 64
    assert vault.has_valid_red_evidence("DH-100") is True

def test_reject_passing_test_as_red_evidence():
    vault = TDDEvidenceVault(db_path=":memory:")
    with pytest.raises(InvalidRedEvidenceError) as exc_info:
        vault.record_red_evidence(
            task_id="DH-101",
            test_file="tests/test_calc.py",
            stdout="1 passed",
            stderr="",
            exit_code=0
        )
    assert "exit code 0" in str(exc_info.value).lower() or "cannot record red" in str(exc_info.value).lower()

def test_evidence_hashing_uniqueness():
    vault = TDDEvidenceVault(db_path=":memory:")
    r1 = vault.record_red_evidence("T1", "test_a.py", "", "Error 1", exit_code=1)
    r2 = vault.record_red_evidence("T2", "test_b.py", "", "Error 2", exit_code=1)
    assert r1.sha256_hash != r2.sha256_hash

def test_sqlite_persistence_across_instances():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_harness.db")

        vault1 = TDDEvidenceVault(db_path=db_path)
        vault1.record_red_evidence(
            task_id="DH-200",
            test_file="tests/test_feature.py",
            stdout="FAILED tests/test_feature.py::test_fn - AssertionError",
            stderr="",
            exit_code=1
        )
        assert vault1.has_valid_red_evidence("DH-200") is True
        vault1.close()

        # New instance pointing to same DB must load active records
        vault2 = TDDEvidenceVault(db_path=db_path)
        assert vault2.has_valid_red_evidence("DH-200") is True
        rec = vault2.get_active_red_evidence("DH-200")
        assert rec is not None
        assert rec.task_id == "DH-200"
        assert rec.exit_code == 1
        vault2.close()

def test_cryptographic_hash_chaining():
    vault = TDDEvidenceVault(db_path=":memory:")
    r1 = vault.record_red_evidence("T1", "test1.py", "", "AssertionError: 1", exit_code=1)
    assert r1.prev_hash == GENESIS_HASH

    r2 = vault.record_red_evidence("T2", "test2.py", "", "AssertionError: 2", exit_code=1)
    assert r2.prev_hash == r1.sha256_hash

    r3 = vault.record_red_evidence("T3", "test3.py", "", "AssertionError: 3", exit_code=1)
    assert r3.prev_hash == r2.sha256_hash

    valid, reason = vault.verify_evidence_chain()
    assert valid is True
    assert reason is None
    vault.close()

def test_tampered_chain_detection():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_harness.db")

        vault = TDDEvidenceVault(db_path=db_path)
        vault.record_red_evidence("T1", "test1.py", "", "AssertionError: 1", exit_code=1)
        vault.record_red_evidence("T2", "test2.py", "", "AssertionError: 2", exit_code=1)
        vault.close()

        # Directly tamper with SQLite data
        conn = sqlite3.connect(db_path)
        conn.execute("UPDATE tdd_evidence SET failure_log = 'Tampered log' WHERE task_id = 'T1'")
        conn.commit()
        conn.close()

        tampered_vault = TDDEvidenceVault(db_path=db_path)
        valid, reason = tampered_vault.verify_evidence_chain()
        assert valid is False
        assert "Tampered hash" in reason
        tampered_vault.close()

def test_reject_collection_error_in_strict_mode():
    vault = TDDEvidenceVault(db_path=":memory:")
    collection_error_log = "INTERNALERROR: pytest crashed\nERROR collecting test_broken.py: ModuleNotFoundError: No module named 'missing'"
    
    with pytest.raises(InvalidRedEvidenceError) as exc_info:
        vault.record_red_evidence(
            task_id="DH-300",
            test_file="test_broken.py",
            stdout=collection_error_log,
            stderr="",
            exit_code=2,
            strict_validation=True
        )
    assert "assertion failure" in str(exc_info.value).lower() or "collection" in str(exc_info.value).lower()
    vault.close()

def test_run_and_record_red_execution_success():
    vault = TDDEvidenceVault(db_path=":memory:")
    # Simulate a test runner command that fails with AssertionError
    cmd = [sys.executable, "-c", "import sys; print('FAILED test_foo.py - AssertionError: expected 4 got 5'); sys.exit(1)"]
    record = vault.run_and_record_red(task_id="DH-400", test_target="test_foo.py", runner_cmd=cmd)
    
    assert record.task_id == "DH-400"
    assert record.exit_code == 1
    assert "AssertionError" in record.failure_log
    assert vault.has_valid_red_evidence("DH-400") is True
    vault.close()

def test_run_and_record_red_rejects_passing_test():
    vault = TDDEvidenceVault(db_path=":memory:")
    cmd = [sys.executable, "-c", "import sys; print('1 passed in 0.01s'); sys.exit(0)"]
    with pytest.raises(InvalidRedEvidenceError) as exc:
        vault.run_and_record_red(task_id="DH-401", test_target="test_pass.py", runner_cmd=cmd)
    assert "code 0" in str(exc.value).lower()
    vault.close()

def test_run_and_record_red_rejects_collection_crash():
    vault = TDDEvidenceVault(db_path=":memory:")
    cmd = [sys.executable, "-c", "import sys; print('ERROR collecting test_crash.py: ModuleNotFoundError'); sys.exit(2)"]
    with pytest.raises(InvalidRedEvidenceError) as exc:
        vault.run_and_record_red(task_id="DH-402", test_target="test_crash.py", runner_cmd=cmd)
    assert "assertion failure" in str(exc.value).lower() or "collection" in str(exc.value).lower()
    vault.close()
