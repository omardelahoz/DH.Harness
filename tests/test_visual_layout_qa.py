import pytest
from dh_harness.core.contracts import VisualDefectType
from dh_harness.uiux.visual import VisualLayoutAuditor

def test_visual_auditor_detects_unresponsive_fixed_width():
    auditor = VisualLayoutAuditor()
    html_content = """
<div class="container" style="width: 1200px; max-width: none;">
    <p>This layout will cause horizontal overflow on mobile viewports.</p>
</div>
"""
    report = auditor.audit_layout_content(html_content, "broken_layout.html")
    assert report.passed is False
    assert len(report.defects) >= 1
    types = [d.defect_type for d in report.defects]
    assert VisualDefectType.UNRESPONSIVE_WIDTH in types or VisualDefectType.OVERFLOW in types

def test_visual_auditor_detects_touch_target_too_small():
    auditor = VisualLayoutAuditor()
    html_content = """
<button style="width: 20px; height: 20px; font-size: 10px;">
    X
</button>
"""
    report = auditor.audit_layout_content(html_content, "tiny_button.html")
    assert report.passed is False
    types = [d.defect_type for d in report.defects]
    assert VisualDefectType.TOUCH_TARGET_TOO_SMALL in types or VisualDefectType.FONT_TOO_SMALL in types

def test_visual_auditor_passes_clean_responsive_component():
    auditor = VisualLayoutAuditor()
    html_content = """
<div class="responsive-card" style="width: 100%; max-width: 600px; padding: 1rem;">
    <button style="min-width: 48px; min-height: 48px; font-size: 16px;">
        Click Me
    </button>
</div>
"""
    report = auditor.audit_layout_content(html_content, "clean_card.html")
    assert report.passed is True
    assert len(report.defects) == 0
    assert report.score == 100.0
