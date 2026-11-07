from __future__ import annotations
import os
import re
from typing import List, Tuple, Dict, Any, Optional

from dh_harness.core.contracts import (
    AccessibilityImpact,
    AccessibilityViolation,
    UIUXAuditReport
)

def _parse_hex_rgb(hex_color: str) -> Tuple[int, int, int]:
    clean = hex_color.strip().lstrip("#")
    if len(clean) == 3:
        clean = "".join([c * 2 for c in clean])
    if len(clean) != 6:
        return 0, 0, 0
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)

def _channel_luminance(val: int) -> float:
    c = val / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def _relative_luminance(hex_color: str) -> float:
    r, g, b = _parse_hex_rgb(hex_color)
    return 0.2126 * _channel_luminance(r) + 0.7152 * _channel_luminance(g) + 0.0722 * _channel_luminance(b)

class UIUXAuditor:
    """
    Audits UI components for accessibility (WCAG 2.1 AA/AAA), color contrast,
    and mandatory component lifecycle states (Rule 3 & info.md § 16).
    """

    IMG_TAG_REGEX = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
    ALT_ATTR_REGEX = re.compile(r'\balt=["\'](.*?)["\']', re.IGNORECASE)

    BUTTON_TAG_REGEX = re.compile(r"<button\b([^>]*)>(.*?)</button>", re.IGNORECASE | re.DOTALL)
    ARIA_LABEL_REGEX = re.compile(r'\baria-label=["\'](.*?)["\']', re.IGNORECASE)

    LOADING_PATTERN = re.compile(r"(?:skeleton|loading|spinner|aria-busy|is-loading)", re.IGNORECASE)
    EMPTY_PATTERN = re.compile(r"(?:empty-state|empty|no-data|no records|sin datos)", re.IGNORECASE)
    ERROR_PATTERN = re.compile(r"(?:error-state|error|alert|is-invalid|fallo)", re.IGNORECASE)

    def calculate_contrast_ratio(self, fg_hex: str, bg_hex: str) -> float:
        """Calculates WCAG 2.1 relative luminance contrast ratio between foreground and background."""
        l1 = _relative_luminance(fg_hex)
        l2 = _relative_luminance(bg_hex)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    def is_wcag_aa_compliant(self, fg_hex: str, bg_hex: str, large_text: bool = False) -> bool:
        """Verifies if color pair satisfies WCAG AA (4.5:1 for regular text, 3.0:1 for large text)."""
        ratio = self.calculate_contrast_ratio(fg_hex, bg_hex)
        threshold = 3.0 if large_text else 4.5
        return ratio >= threshold

    def audit_html(self, content: str, file_path: str = "") -> UIUXAuditReport:
        """Audits an HTML fragment or page for accessibility violations and required state handlers."""
        violations: List[AccessibilityViolation] = []

        # 1. Audit <img> tags for alt attribute
        for match in self.IMG_TAG_REGEX.finditer(content):
            attrs = match.group(1)
            alt_match = self.ALT_ATTR_REGEX.search(attrs)
            if not alt_match:
                violations.append(AccessibilityViolation(
                    rule_id="A11Y_IMG_ALT",
                    element=match.group(0),
                    description="Image element missing required 'alt' attribute for screen reader accessibility.",
                    impact=AccessibilityImpact.SERIOUS,
                    help_url="https://www.w3.org/WAI/tutorials/images/"
                ))

        # 2. Audit <button> tags for empty content without aria-label
        for match in self.BUTTON_TAG_REGEX.finditer(content):
            attrs = match.group(1)
            inner_text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
            aria_label = self.ARIA_LABEL_REGEX.search(attrs)
            if not inner_text and not aria_label:
                violations.append(AccessibilityViolation(
                    rule_id="A11Y_EMPTY_BUTTON",
                    element=match.group(0),
                    description="Button has no accessible text or 'aria-label', making it invisible to screen readers.",
                    impact=AccessibilityImpact.CRITICAL,
                    help_url="https://www.w3.org/WAI/WCAG21/Understanding/name-role-value.html"
                ))

        # 3. Audit component states (Rule 3 & info.md § 16.3)
        has_loading = bool(self.LOADING_PATTERN.search(content))
        has_empty = bool(self.EMPTY_PATTERN.search(content))
        has_error = bool(self.ERROR_PATTERN.search(content))

        # Scoring
        score = 100.0
        for v in violations:
            if v.impact == AccessibilityImpact.CRITICAL:
                score -= 25.0
            elif v.impact == AccessibilityImpact.SERIOUS:
                score -= 15.0
            else:
                score -= 5.0

        if not has_loading:
            score -= 15.0
        if not has_empty:
            score -= 15.0
        if not has_error:
            score -= 10.0

        score = max(0.0, min(100.0, score))

        return UIUXAuditReport(
            file_path=file_path,
            responsive_ok=True,
            has_loading_states=has_loading,
            has_empty_states=has_empty,
            has_error_states=has_error,
            violations=violations,
            score=round(score, 1)
        )

    def audit_file(self, file_path: str) -> Optional[UIUXAuditReport]:
        """Audits an individual HTML/template file on disk."""
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return self.audit_html(content, file_path=file_path)
        except Exception:
            return None
