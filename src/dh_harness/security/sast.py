from __future__ import annotations
import ast
import os
import re
from typing import List, Optional

from dh_harness.core.contracts import SASTFinding, SASTScanResult, SecuritySeverity

class SASTScanner:
    """
    Static Application Security Testing (SAST) Engine (info.md Section 14).
    Scans Python (via AST & semantic patterns), C# (.NET), and JavaScript/TypeScript
    for vulnerabilities, insecure functions, and code-level defects.
    """

    def scan_python(self, code: str, file_path: str = "") -> List[SASTFinding]:
        findings: List[SASTFinding] = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # 1. Detect eval() and exec()
                if isinstance(node, ast.Call):
                    func_name = ""
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        func_name = node.func.attr

                    if func_name == "eval":
                        findings.append(SASTFinding(
                            rule_id="PY_EVAL",
                            file_path=file_path,
                            line_number=node.lineno,
                            severity=SecuritySeverity.CRITICAL,
                            cwe_id="CWE-95",
                            description="Use of dangerous function eval() executes arbitrary Python code.",
                            code_snippet="eval(...)",
                            remediation="Replace dynamic evaluation with safe parsers like ast.literal_eval or json.loads."
                        ))
                    elif func_name == "exec":
                        findings.append(SASTFinding(
                            rule_id="PY_EXEC",
                            file_path=file_path,
                            line_number=node.lineno,
                            severity=SecuritySeverity.CRITICAL,
                            cwe_id="CWE-95",
                            description="Use of dangerous function exec() allows arbitrary code execution.",
                            code_snippet="exec(...)",
                            remediation="Refactor to static methods or dispatch tables."
                        ))

                    # 2. Insecure deserialization (pickle.loads)
                    if isinstance(node.func, ast.Attribute) and node.func.attr == "loads":
                        if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                            findings.append(SASTFinding(
                                rule_id="PY_PICKLE_DESER",
                                file_path=file_path,
                                line_number=node.lineno,
                                severity=SecuritySeverity.CRITICAL,
                                cwe_id="CWE-502",
                                description="Insecure deserialization using pickle.loads() can lead to remote code execution.",
                                code_snippet="pickle.loads(...)",
                                remediation="Use safe serialization formats like JSON, MessagePack, or Protocol Buffers."
                            ))

                    # 3. Subprocess shell=True
                    if isinstance(node.func, ast.Attribute) and node.func.attr in ("Popen", "run", "call", "check_output"):
                        if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                            for kw in node.keywords:
                                if kw.arg == "shell":
                                    is_true = False
                                    if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                        is_true = True
                                    elif isinstance(kw.value, ast.NameConstant) and kw.value.value is True:
                                        is_true = True
                                    if is_true:
                                        findings.append(SASTFinding(
                                            rule_id="PY_SHELL_TRUE",
                                            file_path=file_path,
                                            line_number=node.lineno,
                                            severity=SecuritySeverity.HIGH,
                                            cwe_id="CWE-78",
                                            description="subprocess invoked with shell=True facilitates OS command injection.",
                                            code_snippet=f"subprocess.{node.func.attr}(..., shell=True)",
                                            remediation="Pass command arguments as a list with shell=False."
                                        ))
        except Exception:
            # Fallback regex scanning if AST parse fails (syntax error)
            pass

        # Regex fallback for patterns that might be in unparsed code
        lines = code.splitlines()
        for idx, line in enumerate(lines, start=1):
            if re.search(r"\bsubprocess\.[a-zA-Z0-9_]+\s*\(.*?\bshell\s*=\s*True\b", line) and not any(f.line_number == idx for f in findings):
                findings.append(SASTFinding(
                    rule_id="PY_SHELL_TRUE",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.HIGH,
                    cwe_id="CWE-78",
                    description="subprocess invoked with shell=True facilitates OS command injection.",
                    code_snippet=line.strip(),
                    remediation="Pass command arguments as a list with shell=False."
                ))

        return findings

    def scan_csharp(self, code: str, file_path: str = "") -> List[SASTFinding]:
        findings: List[SASTFinding] = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            # 1. SQL Injection via FromSqlRaw / ExecuteSqlRaw
            if re.search(r"(?:FromSqlRaw|ExecuteSqlRaw(?:Async)?)\s*\(\s*\$?\s*[\"'].*?\{.*?\}", line):
                findings.append(SASTFinding(
                    rule_id="CS_SQLI_RAW",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.CRITICAL,
                    cwe_id="CWE-89",
                    description="Interpolated string passed to FromSqlRaw allows SQL Injection.",
                    code_snippet=line.strip(),
                    remediation="Use FromSqlInterpolated or parameterized parameters (@param)."
                ))

            # 2. Disabled SSL certificate validation
            if re.search(r"ServerCertificateCustomValidationCallback\s*=\s*.*?(?:true|=>\s*true)", line, re.IGNORECASE):
                findings.append(SASTFinding(
                    rule_id="CS_DISABLE_SSL",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.CRITICAL,
                    cwe_id="CWE-295",
                    description="ServerCertificateCustomValidationCallback returns true, disabling SSL/TLS certificate verification.",
                    code_snippet=line.strip(),
                    remediation="Validate certificate chains properly against trusted roots."
                ))

            # 3. BinaryFormatter insecure deserialization
            if re.search(r"BinaryFormatter\b.*?Deserialize\s*\(", line):
                findings.append(SASTFinding(
                    rule_id="CS_INSECURE_DESER",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.HIGH,
                    cwe_id="CWE-502",
                    description="BinaryFormatter is obsolete and inherently insecure against remote code execution.",
                    code_snippet=line.strip(),
                    remediation="Migrate to System.Text.Json or protobuf-net."
                ))

        return findings

    def scan_javascript(self, code: str, file_path: str = "") -> List[SASTFinding]:
        findings: List[SASTFinding] = []
        lines = code.splitlines()

        for idx, line in enumerate(lines, start=1):
            # 1. innerHTML / dangerouslySetInnerHTML
            if re.search(r"\b(?:innerHTML|dangerouslySetInnerHTML)\s*=", line):
                findings.append(SASTFinding(
                    rule_id="JS_INNER_HTML_XSS",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.HIGH,
                    cwe_id="CWE-79",
                    description="Direct assignment to innerHTML introduces Cross-Site Scripting (XSS) risks.",
                    code_snippet=line.strip(),
                    remediation="Use textContent or sanitized DOM elements (DOMPurify)."
                ))

            # 2. eval()
            if re.search(r"\beval\s*\(", line):
                findings.append(SASTFinding(
                    rule_id="JS_EVAL",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.CRITICAL,
                    cwe_id="CWE-95",
                    description="eval() in JavaScript executes arbitrary code with local privileges.",
                    code_snippet=line.strip(),
                    remediation="Parse JSON with JSON.parse() or refactor to avoid dynamic evaluation."
                ))

            # 3. child_process.exec
            if re.search(r"\bchild_process\.exec\s*\(", line):
                findings.append(SASTFinding(
                    rule_id="JS_EXEC_INJECTION",
                    file_path=file_path,
                    line_number=idx,
                    severity=SecuritySeverity.HIGH,
                    cwe_id="CWE-78",
                    description="child_process.exec invokes shell interpreter and is vulnerable to command injection.",
                    code_snippet=line.strip(),
                    remediation="Use child_process.execFile() or spawn() without a shell."
                ))

        return findings

    def scan_file(self, file_path: str) -> List[SASTFinding]:
        if not os.path.isfile(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return []

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            return self.scan_python(content, file_path)
        elif ext in (".cs", ".fs"):
            return self.scan_csharp(content, file_path)
        elif ext in (".js", ".jsx", ".ts", ".tsx", ".mjs"):
            return self.scan_javascript(content, file_path)
        return []

    def scan_directory(self, dir_path: str) -> SASTScanResult:
        all_findings: List[SASTFinding] = []
        files_scanned = 0

        ignored_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".worktrees"}

        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in (".py", ".cs", ".js", ".ts", ".tsx", ".jsx"):
                    files_scanned += 1
                    full_p = os.path.join(root, file)
                    findings = self.scan_file(full_p)
                    all_findings.extend(findings)

        return SASTScanResult(
            findings=all_findings,
            total_files_scanned=files_scanned,
            passed=len(all_findings) == 0
        )
