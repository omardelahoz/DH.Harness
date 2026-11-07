import pytest
from dh_harness.security.licenses import LicenseAuditor, ALLOWED_SPDX_LICENSES

def test_license_auditor_allows_permissive_spdx():
    auditor = LicenseAuditor()

    for spdx in ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"]:
        finding = auditor.audit_dependency(package_name="test-pkg", version="1.0.0", license_spdx=spdx)
        assert finding.is_allowed is True
        assert finding.risk_level == "PERMITTED"

def test_license_auditor_blocks_restricted_licenses():
    auditor = LicenseAuditor()

    for spdx in ["GPL-3.0", "AGPL-3.0", "SSPL-1.0", "Commercial", "Proprietary"]:
        finding = auditor.audit_dependency(package_name="restricted-pkg", version="2.0.0", license_spdx=spdx)
        assert finding.is_allowed is False
        assert finding.risk_level in {"BLOCKED", "HIGH_RISK"}

def test_license_auditor_flags_critical_watchlist_versions():
    auditor = LicenseAuditor()

    # FluentAssertions v8.0 is commercial
    finding_fa8 = auditor.audit_dependency(package_name="FluentAssertions", version="8.0.1", license_spdx="Commercial")
    assert finding_fa8.is_allowed is False
    assert finding_fa8.risk_level == "BLOCKED"

    # FluentAssertions v7.0.5 is free Apache-2.0
    finding_fa7 = auditor.audit_dependency(package_name="FluentAssertions", version="7.0.5", license_spdx="Apache-2.0")
    assert finding_fa7.is_allowed is True

def test_license_auditor_scans_package_json(tmp_path):
    auditor = LicenseAuditor()
    pkg_json = tmp_path / "package.json"
    pkg_json.write_text("""{
      "dependencies": {
        "express": "^4.18.2",
        "some-gpl-tool": "^1.0.0"
      }
    }""", encoding="utf-8")

    # Mock lookup resolver for test
    findings = auditor.audit_package_manifest(
        str(pkg_json),
        license_resolver=lambda name, ver: "GPL-3.0" if "gpl" in name else "MIT"
    )

    assert len(findings) == 2
    gpl_finding = next(f for f in findings if "gpl" in f.package_name)
    assert gpl_finding.is_allowed is False
    assert gpl_finding.risk_level == "BLOCKED"
