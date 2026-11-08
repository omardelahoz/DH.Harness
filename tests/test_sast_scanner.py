import pytest
from dh_harness.core.contracts import SecuritySeverity
from dh_harness.security.sast import SASTScanner

def test_sast_scanner_detects_python_eval_and_exec():
    scanner = SASTScanner()
    code = """
def run_dynamic(user_code):
    eval(user_code)
    exec(user_code)
"""
    findings = scanner.scan_python(code, "dynamic_runner.py")
    assert len(findings) >= 2
    rule_ids = [f.rule_id for f in findings]
    assert "PY_EVAL" in rule_ids
    assert "PY_EXEC" in rule_ids
    assert any(f.severity == SecuritySeverity.CRITICAL for f in findings)

def test_sast_scanner_detects_python_command_injection_shell_true():
    scanner = SASTScanner()
    code = """
import subprocess
def execute_cmd(user_input):
    subprocess.Popen(f"ping {user_input}", shell=True)
    subprocess.run("ls " + user_input, shell=True)
"""
    findings = scanner.scan_python(code, "cmd_runner.py")
    assert len(findings) >= 1
    assert any("SHELL_TRUE" in f.rule_id for f in findings)
    assert any(f.cwe_id == "CWE-78" for f in findings)

def test_sast_scanner_detects_python_insecure_deserialization():
    scanner = SASTScanner()
    code = """
import pickle
def load_data(raw):
    return pickle.loads(raw)
"""
    findings = scanner.scan_python(code, "deser.py")
    assert len(findings) == 1
    assert findings[0].rule_id == "PY_PICKLE_DESER"
    assert findings[0].cwe_id == "CWE-502"

def test_sast_scanner_detects_csharp_sqli_raw():
    scanner = SASTScanner()
    code = """
public class UserRepository {
    public async Task<User> GetUser(string name) {
        return await _context.Users.FromSqlRaw($"SELECT * FROM Users WHERE Name = '{name}'").FirstOrDefaultAsync();
    }
}
"""
    findings = scanner.scan_csharp(code, "UserRepository.cs")
    assert len(findings) >= 1
    assert any("CS_SQLI_RAW" in f.rule_id for f in findings)
    assert any(f.cwe_id == "CWE-89" for f in findings)

def test_sast_scanner_detects_csharp_disabled_ssl():
    scanner = SASTScanner()
    code = """
var handler = new HttpClientHandler {
    ServerCertificateCustomValidationCallback = (sender, cert, chain, sslPolicyErrors) => true
};
"""
    findings = scanner.scan_csharp(code, "ClientFactory.cs")
    assert len(findings) == 1
    assert findings[0].rule_id == "CS_DISABLE_SSL"
    assert findings[0].severity == SecuritySeverity.CRITICAL

def test_sast_scanner_detects_js_xss_and_eval():
    scanner = SASTScanner()
    code = """
function render(content) {
    document.getElementById("output").innerHTML = content;
    eval(content);
}
"""
    findings = scanner.scan_javascript(code, "render.js")
    assert len(findings) >= 2
    rule_ids = [f.rule_id for f in findings]
    assert "JS_INNER_HTML_XSS" in rule_ids
    assert "JS_EVAL" in rule_ids

def test_sast_scanner_passes_clean_code():
    scanner = SASTScanner()
    clean_py = """
def add(a: int, b: int) -> int:
    return a + b
"""
    res = scanner.scan_python(clean_py, "math_utils.py")
    assert len(res) == 0
