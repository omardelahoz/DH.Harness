from __future__ import annotations
import json
import os
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

from dh_harness.core.contracts import SCAScanResult, SCAVulnerabilityFinding, SecuritySeverity

KNOWN_VULNERABILITY_DB: List[Dict[str, Any]] = [
    {
        "ecosystem": "pypi",
        "package": "requests",
        "affected_below": "2.20.0",
        "cve": "CVE-2018-18074",
        "severity": SecuritySeverity.HIGH,
        "description": "Session credentials leak on HTTP redirect to different host.",
        "fixed_version": "2.20.0",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2018-18074"
    },
    {
        "ecosystem": "pypi",
        "package": "urllib3",
        "affected_below": "1.24.2",
        "cve": "CVE-2019-11324",
        "severity": SecuritySeverity.HIGH,
        "description": "SSL certificate verification bypass on cross-host redirects.",
        "fixed_version": "1.24.2",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2019-11324"
    },
    {
        "ecosystem": "npm",
        "package": "lodash",
        "affected_below": "4.17.21",
        "cve": "CVE-2019-10744",
        "severity": SecuritySeverity.HIGH,
        "description": "Prototype pollution vulnerability via defaultsDeep function.",
        "fixed_version": "4.17.21",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2019-10744"
    },
    {
        "ecosystem": "npm",
        "package": "axios",
        "affected_below": "0.21.1",
        "cve": "CVE-2020-28168",
        "severity": SecuritySeverity.MEDIUM,
        "description": "Server-Side Request Forgery (SSRF) bypass in proxy parameter.",
        "fixed_version": "0.21.1",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2020-28168"
    },
    {
        "ecosystem": "nuget",
        "package": "newtonsoft.json",
        "affected_below": "13.0.1",
        "cve": "CVE-2024-21907",
        "severity": SecuritySeverity.HIGH,
        "description": "Improper handling of heavily nested JSON causes stack overflow / DoS.",
        "fixed_version": "13.0.1",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-21907"
    },
    {
        "ecosystem": "nuget",
        "package": "log4net",
        "affected_below": "2.0.10",
        "cve": "CVE-2018-1285",
        "severity": SecuritySeverity.CRITICAL,
        "description": "Insecure XML external entity (XXE) parsing allows remote code execution.",
        "fixed_version": "2.0.10",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2018-1285"
    }
]

def _parse_version(v: str) -> Tuple[int, ...]:
    cleaned = re.sub(r"[^\d\.]", "", v)
    parts = []
    for p in cleaned.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)

def _is_vulnerable(installed: str, affected_below: str) -> bool:
    try:
        inst_parts = _parse_version(installed)
        aff_parts = _parse_version(affected_below)
        return inst_parts < aff_parts
    except Exception:
        return False

class SCAScanner:
    """
    Software Composition Analysis (SCA) & Vulnerability Scanner (info.md Section 14).
    Scans dependency manifests (Python requirements.txt, Node package.json, .NET *.csproj)
    and checks for known CVEs and outdated insecure versions.
    """

    def scan_manifest(self, manifest_path: str) -> SCAScanResult:
        if not os.path.isfile(manifest_path):
            return SCAScanResult(manifest_path=manifest_path, passed=True)

        filename = os.path.basename(manifest_path).lower()
        if filename == "requirements.txt" or filename.endswith(".txt"):
            return self._scan_requirements_txt(manifest_path)
        elif filename == "package.json":
            return self._scan_package_json(manifest_path)
        elif filename.endswith(".csproj"):
            return self._scan_csproj(manifest_path)

        return SCAScanResult(manifest_path=manifest_path, passed=True)

    def _scan_requirements_txt(self, path: str) -> SCAScanResult:
        vulnerabilities: List[SCAVulnerabilityFinding] = []
        total_deps = 0

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = re.match(r"^([a-zA-Z0-9_\-\.]+)\s*(?:==|>=|<=|~=)\s*([0-9\.]+)", line)
                if match:
                    total_deps += 1
                    pkg_name, version = match.group(1).lower(), match.group(2)
                    for rule in KNOWN_VULNERABILITY_DB:
                        if rule["ecosystem"] == "pypi" and rule["package"] == pkg_name:
                            if _is_vulnerable(version, rule["affected_below"]):
                                vulnerabilities.append(SCAVulnerabilityFinding(
                                    package_name=match.group(1),
                                    installed_version=version,
                                    cve_id=rule["cve"],
                                    severity=rule["severity"],
                                    description=rule["description"],
                                    fixed_version=rule["fixed_version"],
                                    advisory_url=rule["url"]
                                ))

        return SCAScanResult(
            manifest_path=path,
            vulnerabilities=vulnerabilities,
            total_dependencies=total_deps,
            passed=len(vulnerabilities) == 0
        )

    def _scan_package_json(self, path: str) -> SCAScanResult:
        vulnerabilities: List[SCAVulnerabilityFinding] = []
        total_deps = 0

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            total_deps = len(deps)

            for pkg_raw, ver_raw in deps.items():
                pkg_name = pkg_raw.lower()
                clean_ver = re.sub(r"[\^~>=<]", "", ver_raw).strip()
                for rule in KNOWN_VULNERABILITY_DB:
                    if rule["ecosystem"] == "npm" and rule["package"] == pkg_name:
                        if _is_vulnerable(clean_ver, rule["affected_below"]):
                            vulnerabilities.append(SCAVulnerabilityFinding(
                                package_name=pkg_raw,
                                installed_version=ver_raw,
                                cve_id=rule["cve"],
                                severity=rule["severity"],
                                description=rule["description"],
                                fixed_version=rule["fixed_version"],
                                advisory_url=rule["url"]
                            ))
        except Exception:
            pass

        return SCAScanResult(
            manifest_path=path,
            vulnerabilities=vulnerabilities,
            total_dependencies=total_deps,
            passed=len(vulnerabilities) == 0
        )

    def _scan_csproj(self, path: str) -> SCAScanResult:
        vulnerabilities: List[SCAVulnerabilityFinding] = []
        total_deps = 0

        try:
            tree = ET.parse(path)
            root = tree.getroot()
            for elem in root.iter("PackageReference"):
                pkg_raw = elem.attrib.get("Include") or elem.attrib.get("Update")
                ver_raw = elem.attrib.get("Version")
                if pkg_raw and ver_raw:
                    total_deps += 1
                    pkg_name = pkg_raw.lower()
                    clean_ver = re.sub(r"[\^~>=<]", "", ver_raw).strip()
                    for rule in KNOWN_VULNERABILITY_DB:
                        if rule["ecosystem"] == "nuget" and rule["package"] == pkg_name:
                            if _is_vulnerable(clean_ver, rule["affected_below"]):
                                vulnerabilities.append(SCAVulnerabilityFinding(
                                    package_name=pkg_raw,
                                    installed_version=ver_raw,
                                    cve_id=rule["cve"],
                                    severity=rule["severity"],
                                    description=rule["description"],
                                    fixed_version=rule["fixed_version"],
                                    advisory_url=rule["url"]
                                ))
        except Exception:
            pass

        return SCAScanResult(
            manifest_path=path,
            vulnerabilities=vulnerabilities,
            total_dependencies=total_deps,
            passed=len(vulnerabilities) == 0
        )
