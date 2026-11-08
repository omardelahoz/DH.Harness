import pytest
from dh_harness.core.contracts import SecuritySeverity
from dh_harness.security.sca import SCAScanner

def test_sca_scanner_parses_requirements_and_detects_vulnerable_pkg(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("requests==2.19.0\nurllib3==1.24.1\npydantic==2.8.2\n")

    scanner = SCAScanner()
    result = scanner.scan_manifest(str(req_file))

    assert result.total_dependencies == 3
    assert result.passed is False
    assert len(result.vulnerabilities) >= 1

    vuln_pkgs = [v.package_name.lower() for v in result.vulnerabilities]
    assert "requests" in vuln_pkgs or "urllib3" in vuln_pkgs
    assert any(v.cve_id.startswith("CVE-") for v in result.vulnerabilities)
    assert any(v.fixed_version != "" for v in result.vulnerabilities)

def test_sca_scanner_parses_package_json_and_detects_vulnerabilities(tmp_path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text("""{
  "name": "my-app",
  "dependencies": {
    "lodash": "4.17.11",
    "axios": "0.19.0",
    "react": "18.2.0"
  }
}""")

    scanner = SCAScanner()
    result = scanner.scan_manifest(str(pkg_file))

    assert result.total_dependencies == 3
    assert result.passed is False
    vuln_pkgs = [v.package_name.lower() for v in result.vulnerabilities]
    assert "lodash" in vuln_pkgs or "axios" in vuln_pkgs

def test_sca_scanner_parses_csproj_and_detects_vulnerabilities(tmp_path):
    csproj_file = tmp_path / "Backend.csproj"
    csproj_file.write_text("""<Project Sdk="Microsoft.NET.Sdk.Web">
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="12.0.1" />
    <PackageReference Include="Dapper" Version="2.1.35" />
  </ItemGroup>
</Project>""")

    scanner = SCAScanner()
    result = scanner.scan_manifest(str(csproj_file))

    assert result.total_dependencies == 2
    assert result.passed is False
    vuln_pkgs = [v.package_name.lower() for v in result.vulnerabilities]
    assert "newtonsoft.json" in vuln_pkgs

def test_sca_scanner_passes_on_clean_dependencies(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("pydantic==2.8.2\ntyper==0.12.3\nrich==13.7.1\n")

    scanner = SCAScanner()
    result = scanner.scan_manifest(str(req_file))

    assert result.total_dependencies == 3
    assert result.passed is True
    assert len(result.vulnerabilities) == 0
