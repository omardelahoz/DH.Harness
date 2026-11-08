import pytest
from dh_harness.core.contracts import STRIDECategory, SecuritySeverity
from dh_harness.security.stride import STRIDETaskThreatModeler

def test_stride_modeler_generates_all_six_categories():
    modeler = STRIDETaskThreatModeler()
    component = {
        "name": "Payment Gateway API",
        "has_auth": False,
        "stores_secrets": True,
        "has_rate_limiting": False,
        "writes_audit_logs": False,
        "input_validation": False,
        "has_rbac": False
    }

    report = modeler.model_threats("Payment Gateway API", component)

    assert report.target == "Payment Gateway API"
    assert len(report.threats) >= 6

    categories = {t.category for t in report.threats}
    assert STRIDECategory.SPOOFING in categories
    assert STRIDECategory.TAMPERING in categories
    assert STRIDECategory.REPUDIATION in categories
    assert STRIDECategory.INFORMATION_DISCLOSURE in categories
    assert STRIDECategory.DENIAL_OF_SERVICE in categories
    assert STRIDECategory.ELEVATION_OF_PRIVILEGE in categories

    for threat in report.threats:
        assert threat.mitigation_strategy != ""
        assert threat.threat_description != ""

def test_stride_modeler_calculates_high_risk_score_for_defenseless_service():
    modeler = STRIDETaskThreatModeler()
    component = {
        "name": "Public Insecure Endpoint",
        "has_auth": False,
        "has_rate_limiting": False
    }
    report = modeler.model_threats("Public Insecure Endpoint", component)
    assert report.risk_score < 70.0

def test_stride_modeler_gives_high_score_to_secure_component():
    modeler = STRIDETaskThreatModeler()
    secure_comp = {
        "name": "Hardened Auth Service",
        "has_auth": True,
        "stores_secrets": False,
        "has_rate_limiting": True,
        "writes_audit_logs": True,
        "input_validation": True,
        "has_rbac": True
    }
    report = modeler.model_threats("Hardened Auth Service", secure_comp)
    assert report.risk_score >= 90.0
