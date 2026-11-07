import pytest
from dh_harness.core.contracts import SecuritySeverity
from dh_harness.security.scanner import SecretScanner

def test_scanner_detects_github_tokens():
    scanner = SecretScanner()
    raw = 'export GITHUB_TOKEN="ghp_1234567890abcdef1234567890abcdef1234"'
    findings = scanner.scan_content(raw, file_path="config.sh")

    assert len(findings) == 1
    assert findings[0].secret_type == "GITHUB_TOKEN"
    assert findings[0].severity == SecuritySeverity.CRITICAL
    assert "ghp_1234" not in findings[0].snippet_redacted
    assert "[REDACTED_SECRET]" in findings[0].snippet_redacted

def test_scanner_detects_aws_keys():
    scanner = SecretScanner()
    raw = 'aws_access_key_id = AKIAIOSFODNN7EXAMPLE'
    findings = scanner.scan_content(raw, file_path="credentials")

    assert len(findings) == 1
    assert findings[0].secret_type == "AWS_ACCESS_KEY"
    assert findings[0].severity == SecuritySeverity.HIGH
    assert "[REDACTED_SECRET]" in findings[0].snippet_redacted

def test_scanner_detects_private_keys():
    scanner = SecretScanner()
    raw = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0Y123456789...
-----END RSA PRIVATE KEY-----"""
    findings = scanner.scan_content(raw, file_path="server.key")

    assert len(findings) == 1
    assert findings[0].secret_type == "PRIVATE_KEY"
    assert findings[0].severity == SecuritySeverity.CRITICAL

def test_scanner_detects_passwords_in_connection_strings():
    scanner = SecretScanner()
    raw = 'Server=myServerAddress;Database=myDataBase;Uid=myUsername;Password=P@ssw0rd12345!;'
    findings = scanner.scan_content(raw, file_path="appsettings.json")

    assert len(findings) == 1
    assert findings[0].secret_type == "PASSWORD_IN_CONNSTR"
    assert "P@ssw0rd" not in findings[0].snippet_redacted
    assert "[REDACTED_SECRET]" in findings[0].snippet_redacted

def test_scanner_scans_directory(tmp_path):
    scanner = SecretScanner()

    # Clean file
    (tmp_path / "clean.py").write_text("print('hello')", encoding="utf-8")
    # Dirty file
    (tmp_path / "secret.env").write_text("TOKEN=ghp_ABC1234567890abcdef1234567890abcdef", encoding="utf-8")

    findings = scanner.scan_directory(str(tmp_path))
    assert len(findings) == 1
    assert findings[0].file_path.endswith("secret.env")
