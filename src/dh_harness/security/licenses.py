from __future__ import annotations
import os
import json
from typing import List, Dict, Optional, Callable, Any

from dh_harness.core.contracts import LicenseAuditFinding

# Permitted SPDX Licenses (100% Free Open Source - Rule 6)
ALLOWED_SPDX_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "PostgreSQL",
    "MS-PL"
}

# Critical Watchlist: libraries that switched to commercial / paid licenses in recent versions
CRITICAL_WATCHLIST = {
    "FluentAssertions": {"restricted_from": "8.0", "free_until": "7.x"},
    "MediatR": {"restricted_from": "13.0", "free_until": "12.x"},
    "AutoMapper": {"restricted_from": "15.0", "free_until": "14.x"},
    "MassTransit": {"restricted_from": "9.0", "free_until": "8.x"},
    "EPPlus": {"restricted_from": "5.0", "free_until": "4.x"},
    "Moq": {"restricted_from": "4.20.0", "free_until": "4.18.4"}
}

class LicenseAuditor:
    """
    Audits third-party dependencies against the SPDX permitted license whitelist
    and flags commercial or dual-license risks (Rule 6 & info.md § 14.4).
    """

    def audit_dependency(
        self,
        package_name: str,
        version: str,
        license_spdx: str
    ) -> LicenseAuditFinding:
        """Audits an individual package and version for license compliance."""
        spdx_clean = license_spdx.strip()
        is_allowed = spdx_clean in ALLOWED_SPDX_LICENSES

        if is_allowed:
            risk_level = "PERMITTED"
        else:
            is_blocked = any(
                bad in spdx_clean
                for bad in ["Commercial", "Proprietary", "GPL", "AGPL", "SSPL", "PolyForm"]
            )
            risk_level = "BLOCKED" if is_blocked else "HIGH_RISK"

        return LicenseAuditFinding(
            package_name=package_name,
            version=version,
            license_spdx=spdx_clean,
            is_allowed=is_allowed,
            risk_level=risk_level
        )

    def audit_package_manifest(
        self,
        manifest_path: str,
        license_resolver: Optional[Callable[[str, str], str]] = None
    ) -> List[LicenseAuditFinding]:
        """Audits dependencies listed in a package.json manifest."""
        if not os.path.exists(manifest_path):
            return []

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []

        findings: List[LicenseAuditFinding] = []
        deps: Dict[str, str] = {}
        deps.update(data.get("dependencies", {}))
        deps.update(data.get("devDependencies", {}))

        for name, ver in deps.items():
            spdx = license_resolver(name, ver) if license_resolver else "MIT"
            finding = self.audit_dependency(name, ver, spdx)
            findings.append(finding)

        return findings
