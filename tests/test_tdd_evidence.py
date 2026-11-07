import pytest
from dh_harness.tdd.evidence import TDDEvidenceVault, InvalidRedEvidenceError

def test_record_valid_red_evidence():
    vault = TDDEvidenceVault()
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
    vault = TDDEvidenceVault()
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
    vault = TDDEvidenceVault()
    r1 = vault.record_red_evidence("T1", "test_a.py", "", "Error 1", exit_code=1)
    r2 = vault.record_red_evidence("T2", "test_b.py", "", "Error 2", exit_code=1)
    assert r1.sha256_hash != r2.sha256_hash
