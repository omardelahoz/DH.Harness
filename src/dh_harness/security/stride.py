from __future__ import annotations
from typing import Dict, Any, List

from dh_harness.core.contracts import (
    STRIDECategory,
    ThreatFinding,
    ThreatModelReport,
    SecuritySeverity
)

class STRIDETaskThreatModeler:
    """
    Microsoft STRIDE Threat Modeling Engine (info.md Section 14).
    Maps software components and architecture interfaces to STRIDE threat categories:
    - Spoofing
    - Tampering
    - Repudiation
    - Information Disclosure
    - Denial of Service
    - Elevation of Privilege
    """

    def model_threats(self, target_name: str, component: Dict[str, Any]) -> ThreatModelReport:
        threats: List[ThreatFinding] = []

        # 1. Spoofing
        if not component.get("has_auth", True):
            threats.append(ThreatFinding(
                id="STRIDE-S01",
                category=STRIDECategory.SPOOFING,
                component=target_name,
                risk_level=SecuritySeverity.CRITICAL,
                threat_description="Authentication is not enforced; an attacker can impersonate legitimate users or clients.",
                mitigation_strategy="Implement mutual TLS (mTLS), JWT token validation, or OAuth 2.0 / OpenID Connect."
            ))

        # 2. Tampering
        if not component.get("input_validation", True):
            threats.append(ThreatFinding(
                id="STRIDE-T01",
                category=STRIDECategory.TAMPERING,
                component=target_name,
                risk_level=SecuritySeverity.HIGH,
                threat_description="Input payloads are not validated schema-wise; vulnerable to parameter manipulation or SQLi.",
                mitigation_strategy="Enforce strict Pydantic/FluentValidation models and parameterized queries."
            ))

        # 3. Repudiation
        if not component.get("writes_audit_logs", True):
            threats.append(ThreatFinding(
                id="STRIDE-R01",
                category=STRIDECategory.REPUDIATION,
                component=target_name,
                risk_level=SecuritySeverity.MEDIUM,
                threat_description="Critical operations lack tamper-evident audit logs; transactions cannot be conclusively attributed.",
                mitigation_strategy="Write structured non-repudiation audit trails with timestamps and user identifiers."
            ))

        # 4. Information Disclosure
        if component.get("stores_secrets", False) or not component.get("encryption", True):
            threats.append(ThreatFinding(
                id="STRIDE-I01",
                category=STRIDECategory.INFORMATION_DISCLOSURE,
                component=target_name,
                risk_level=SecuritySeverity.HIGH,
                threat_description="Sensitive tokens, passwords or confidential customer data may be exposed at rest or in transit.",
                mitigation_strategy="Use Azure Key Vault / AWS Secrets Manager and enforce TLS 1.3 encryption."
            ))

        # 5. Denial of Service
        if not component.get("has_rate_limiting", True):
            threats.append(ThreatFinding(
                id="STRIDE-D01",
                category=STRIDECategory.DENIAL_OF_SERVICE,
                component=target_name,
                risk_level=SecuritySeverity.HIGH,
                threat_description="Endpoint lacks rate limiting, pagination, or query timeouts; vulnerable to resource exhaustion.",
                mitigation_strategy="Implement token-bucket rate limiters and mandatory result pagination."
            ))

        # 6. Elevation of Privilege
        if not component.get("has_rbac", True):
            threats.append(ThreatFinding(
                id="STRIDE-E01",
                category=STRIDECategory.ELEVATION_OF_PRIVILEGE,
                component=target_name,
                risk_level=SecuritySeverity.HIGH,
                threat_description="Authorization lacks fine-grained Role-Based Access Control (RBAC); vertical privilege escalation possible.",
                mitigation_strategy="Enforce least privilege principle and claims-based authorization filters."
            ))

        # Calculate Risk Score: 100 - (CRITICAL * 25, HIGH * 15, MEDIUM * 5)
        penalty = 0.0
        for t in threats:
            if t.risk_level == SecuritySeverity.CRITICAL:
                penalty += 25.0
            elif t.risk_level == SecuritySeverity.HIGH:
                penalty += 15.0
            elif t.risk_level == SecuritySeverity.MEDIUM:
                penalty += 5.0
            else:
                penalty += 2.0

        risk_score = max(0.0, 100.0 - penalty)

        return ThreatModelReport(
            target=target_name,
            threats=threats,
            risk_score=risk_score
        )
