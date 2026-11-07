import pytest
from dh_harness.governance.gates import SecretScanningGate, TestQualityGate

def test_secret_scanner_detects_github_token():
    scanner = SecretScanningGate()
    dirty_content = "TOKEN = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'"
    result = scanner.scan_text(dirty_content)
    assert result.passed is False
    assert "github" in result.message.lower() or "token" in result.message.lower()

def test_secret_scanner_detects_private_key():
    scanner = SecretScanningGate()
    dirty_content = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA..."
    result = scanner.scan_text(dirty_content)
    assert result.passed is False
    assert "private key" in result.message.lower()

def test_secret_scanner_passes_clean_content():
    scanner = SecretScanningGate()
    clean_content = "def calculate_sum(a, b):\n    return a + b\n"
    result = scanner.scan_text(clean_content)
    assert result.passed is True

def test_test_quality_gate_detects_defects(tmp_path):
    bad_test = tmp_path / "test_bad.py"
    bad_test.write_text("def test_nothing():\n    pass\n")

    gate = TestQualityGate()
    result = gate.audit_test_file(str(bad_test))
    assert result.passed is False
    assert "empty" in result.message.lower()
