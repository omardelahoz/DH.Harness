"""Headless visual and responsive layout QA auditor for UI components."""
import os
import re
from typing import Dict, List, Any, Optional

from dh_harness.core.contracts import (
    VisualDefectType,
    VisualDefectFinding,
    VisualLayoutReport,
)

DEFAULT_VIEWPORTS = ["mobile (375px)", "tablet (768px)", "desktop (1440px)"]


class VisualLayoutAuditor:
    """Audits HTML/CSS templates for responsive layout breaks, touch targets, and typography defects."""

    # RegEx patterns for layout analysis
    FIXED_WIDTH_PATTERN = re.compile(
        r'<([a-zA-Z0-9\-]+)[^>]*\bstyle=["\'][^"\']*\bwidth:\s*([0-9]+)px[^"\']*["\']',
        re.IGNORECASE
    )
    MAX_WIDTH_NONE_PATTERN = re.compile(
        r'\bmax-width:\s*none\b',
        re.IGNORECASE
    )
    TOUCH_TARGET_PATTERN = re.compile(
        r'<(button|a|input)[^>]*\bstyle=["\']([^"\']*)["\']',
        re.IGNORECASE
    )
    DIMENSION_PX_PATTERN = re.compile(
        r'\b(width|height):\s*([0-9]+)px\b',
        re.IGNORECASE
    )
    FONT_SIZE_PX_PATTERN = re.compile(
        r'\bfont-size:\s*([0-9]+)px\b',
        re.IGNORECASE
    )
    NEGATIVE_MARGIN_PATTERN = re.compile(
        r'\bmargin-(?:top|left|right|bottom):\s*-([3-9][0-9]|[1-9][0-9]{2,})px\b',
        re.IGNORECASE
    )

    def audit_layout_content(
        self,
        content: str,
        file_path: str = "snippet.html",
        viewports: Optional[List[str]] = None
    ) -> VisualLayoutReport:
        """Audits HTML and inline styles for layout defects across viewports."""
        viewports_tested = viewports or DEFAULT_VIEWPORTS
        defects: List[VisualDefectFinding] = []

        lines = content.splitlines()

        # 1. Audit for unresponsive fixed width (> 600px without responsive constraint)
        for line_num, line in enumerate(lines, start=1):
            for match in self.FIXED_WIDTH_PATTERN.finditer(line):
                tag_name = match.group(1)
                width_val = int(match.group(2))
                full_tag = match.group(0)

                if width_val > 600:
                    # Check if max-width is explicitly none or missing responsive fallback
                    if self.MAX_WIDTH_NONE_PATTERN.search(full_tag) or "max-width" not in full_tag:
                        defects.append(
                            VisualDefectFinding(
                                defect_type=VisualDefectType.UNRESPONSIVE_WIDTH,
                                selector=f"<{tag_name}>",
                                viewport="mobile (375px)",
                                description=f"Fixed width of {width_val}px exceeds mobile screen width (375px) causing horizontal scroll.",
                                line_number=line_num,
                                remediation="Replace fixed pixel width with relative units (e.g. width: 100%) and max-width."
                            )
                        )

        # 2. Audit interactive elements for touch target sizing (< 44px) and font sizing
        for line_num, line in enumerate(lines, start=1):
            for match in self.TOUCH_TARGET_PATTERN.finditer(line):
                tag_name = match.group(1)
                style_str = match.group(2)

                # Check width / height for small touch target
                dim_matches = self.DIMENSION_PX_PATTERN.findall(style_str)
                is_small_target = False
                for prop, val_str in dim_matches:
                    val = int(val_str)
                    if val < 44 and "min-width" not in style_str and "min-height" not in style_str:
                        is_small_target = True
                        break

                if is_small_target:
                    defects.append(
                        VisualDefectFinding(
                            defect_type=VisualDefectType.TOUCH_TARGET_TOO_SMALL,
                            selector=f"<{tag_name}>",
                            viewport="mobile (375px)",
                            description=f"Interactive <{tag_name}> element has dimensions smaller than WCAG minimum 44x44px touch target.",
                            line_number=line_num,
                            remediation="Ensure interactive touch targets are at least 44px by 44px with min-width and min-height."
                        )
                    )

                # Check font size
                font_matches = self.FONT_SIZE_PX_PATTERN.findall(style_str)
                for f_val_str in font_matches:
                    f_val = int(f_val_str)
                    if f_val < 12:
                        defects.append(
                            VisualDefectFinding(
                                defect_type=VisualDefectType.FONT_TOO_SMALL,
                                selector=f"<{tag_name}>",
                                viewport="all",
                                description=f"Font size of {f_val}px is below readable threshold (12px minimum).",
                                line_number=line_num,
                                remediation="Increase font size to at least 12px (or 0.75rem)."
                            )
                        )

            # 3. Check for severe negative margins causing overlap
            for match in self.NEGATIVE_MARGIN_PATTERN.finditer(line):
                defects.append(
                    VisualDefectFinding(
                        defect_type=VisualDefectType.ELEMENT_OVERLAP,
                        selector="element-with-negative-margin",
                        viewport="all",
                        description=f"Severe negative margin detected ({match.group(0)}) which may cause visual overlap on smaller viewports.",
                        line_number=line_num,
                        remediation="Avoid large negative margins for positioning; use CSS Flexbox or Grid instead."
                    )
                )

        score = max(0.0, 100.0 - (len(defects) * 25.0))
        passed = len(defects) == 0

        return VisualLayoutReport(
            target=file_path,
            defects=defects,
            viewports_tested=viewports_tested,
            passed=passed,
            score=round(score, 1)
        )

    def audit_layout_file(self, file_path: str) -> Optional[VisualLayoutReport]:
        """Audits a single layout or template file on disk."""
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return self.audit_layout_content(content, file_path=file_path)
        except Exception:
            return None

    def audit_directory(self, dir_path: str) -> List[VisualLayoutReport]:
        """Audits all HTML/template files in a directory."""
        reports: List[VisualLayoutReport] = []
        if not os.path.exists(dir_path):
            return reports

        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".html", ".htm", ".vue", ".jsx", ".tsx")):
                    full_path = os.path.join(root, file)
                    report = self.audit_layout_file(full_path)
                    if report:
                        reports.append(report)
        return reports
