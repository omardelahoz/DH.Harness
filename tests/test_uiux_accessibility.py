import pytest
from dh_harness.core.contracts import AccessibilityImpact
from dh_harness.uiux.engine import UIUXAuditor

def test_auditor_detects_missing_image_alt():
    auditor = UIUXAuditor()
    html = """
    <div class="card">
        <img src="/assets/product.png">
        <h3>Product Title</h3>
    </div>
    """
    report = auditor.audit_html(html, file_path="Card.html")

    assert report.file_path == "Card.html"
    assert len(report.violations) >= 1
    v = [v for v in report.violations if v.rule_id == "A11Y_IMG_ALT"][0]
    assert v.impact == AccessibilityImpact.SERIOUS
    assert "alt" in v.description.lower()

def test_auditor_detects_empty_button_without_aria():
    auditor = UIUXAuditor()
    html = """
    <nav>
        <button class="icon-btn"><i class="fa fa-search"></i></button>
    </nav>
    """
    report = auditor.audit_html(html, file_path="Nav.html")

    v = [v for v in report.violations if v.rule_id == "A11Y_EMPTY_BUTTON"][0]
    assert v.impact == AccessibilityImpact.CRITICAL
    assert "aria-label" in v.description.lower() or "accessible text" in v.description.lower()

def test_auditor_detects_missing_component_states():
    auditor = UIUXAuditor()
    # A view without loading state or empty state
    html = """
    <div class="user-list">
        <ul>
            <li>User 1</li>
            <li>User 2</li>
        </ul>
    </div>
    """
    report = auditor.audit_html(html, file_path="UserList.html")

    assert report.has_loading_states is False
    assert report.has_empty_states is False
    assert report.score < 100.0

def test_auditor_calculates_wcag_contrast_ratio():
    auditor = UIUXAuditor()

    # Black on White: Max contrast (21:1)
    contrast_high = auditor.calculate_contrast_ratio("#000000", "#FFFFFF")
    assert contrast_high > 20.0
    assert auditor.is_wcag_aa_compliant("#000000", "#FFFFFF") is True

    # White on White: Min contrast (1:1)
    contrast_none = auditor.calculate_contrast_ratio("#FFFFFF", "#FFFFFF")
    assert round(contrast_none, 1) == 1.0
    assert auditor.is_wcag_aa_compliant("#FFFFFF", "#FFFFFF") is False

    # Low contrast gray on white: #AAAAAA on #FFFFFF (~2.3:1)
    contrast_low = auditor.calculate_contrast_ratio("#AAAAAA", "#FFFFFF")
    assert contrast_low < 4.5
    assert auditor.is_wcag_aa_compliant("#AAAAAA", "#FFFFFF") is False

def test_auditor_passes_compliant_component():
    auditor = UIUXAuditor()
    html = """
    <div class="user-dashboard">
        <img src="/avatar.png" alt="User avatar">
        <button aria-label="Close dialog">X</button>
        <div class="skeleton-loader" aria-busy="true">Loading...</div>
        <div class="empty-state">No users found.</div>
        <div class="error-state">Failed to load users.</div>
    </div>
    """
    report = auditor.audit_html(html, file_path="Dashboard.html")

    assert len(report.violations) == 0
    assert report.has_loading_states is True
    assert report.has_empty_states is True
    assert report.has_error_states is True
    assert report.score == 100.0
