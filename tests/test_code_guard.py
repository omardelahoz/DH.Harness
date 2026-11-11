import pytest
from dh_harness.core.contracts import InteractionMode
from dh_harness.tdd.evidence import TDDEvidenceVault
from dh_harness.tdd.guard import CodeModificationGuard, TDDGuardViolationError

def test_guard_allows_editing_tests_freely():
    vault = TDDEvidenceVault()
    guard = CodeModificationGuard(vault)

    decision = guard.check_can_modify("tests/test_feature.py", mode=InteractionMode.DEVELOPMENT, task_id="DH-1")
    assert decision.allowed is True

def test_guard_allows_editing_documentation_freely():
    vault = TDDEvidenceVault()
    guard = CodeModificationGuard(vault)

    decision = guard.check_can_modify("README.md", mode=InteractionMode.DEVELOPMENT, task_id="DH-1")
    assert decision.allowed is True

def test_guard_blocks_src_modification_without_red_evidence():
    vault = TDDEvidenceVault()
    guard = CodeModificationGuard(vault)

    # Attempt to edit production code without prior RED test failure
    with pytest.raises(TDDGuardViolationError) as exc_info:
        guard.check_can_modify("src/dh_harness/core/calculator.py", mode=InteractionMode.DEVELOPMENT, task_id="DH-2")
    assert "red evidence" in str(exc_info.value).lower()

def test_guard_permits_src_modification_with_valid_red_evidence():
    vault = TDDEvidenceVault()
    vault.record_red_evidence("DH-3", "tests/test_foo.py", "", "AssertionError: 1 != 2", exit_code=1)
    guard = CodeModificationGuard(vault)

    decision = guard.check_can_modify("src/dh_harness/core/foo.py", mode=InteractionMode.DEVELOPMENT, task_id="DH-3")
    assert decision.allowed is True

def test_guard_blocks_src_in_investigation_mode():
    vault = TDDEvidenceVault(db_path=":memory:")
    guard = CodeModificationGuard(vault)

    with pytest.raises(TDDGuardViolationError) as exc_info:
        guard.check_can_modify("src/dh_harness/core/foo.py", mode=InteractionMode.INVESTIGATION, task_id="DH-4")
    assert "investigation" in str(exc_info.value).lower()

def test_guard_evaluate_modification_does_not_raise():
    vault = TDDEvidenceVault(db_path=":memory:")
    guard = CodeModificationGuard(vault)

    decision = guard.evaluate_modification("src/dh_harness/foo.py", mode=InteractionMode.DEVELOPMENT, task_id="DH-9")
    assert decision.allowed is False
    assert "No verified RED evidence" in decision.reason

def test_guard_protects_json_inside_src():
    vault = TDDEvidenceVault(db_path=":memory:")
    guard = CodeModificationGuard(vault)

    decision = guard.evaluate_modification("src/dh_harness/catalog.json", mode=InteractionMode.DEVELOPMENT, task_id="DH-10")
    assert decision.allowed is False
    assert "No verified RED evidence" in decision.reason
