from __future__ import annotations
import os
import re
from datetime import datetime
from typing import List, Optional

from dh_harness.core.contracts import ADRStatus, ArchitectureDecisionRecord

def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", cleaned).strip("-")

class ADRManager:
    """
    Architecture Decision Records (ADR) Manager (info.md § 19).
    Discovers, generates, and validates architectural decisions.
    """

    FILE_PATTERN = re.compile(r"^ADR-(\d+)-(.*?)\.md$", re.IGNORECASE)
    HEADER_PATTERN = re.compile(r"^#\s*ADR-(\d+):\s*(.*)$", re.MULTILINE)
    STATUS_PATTERN = re.compile(r"##\s*Estado\s*\n+([^\n#]+)", re.IGNORECASE)
    CONTEXT_PATTERN = re.compile(r"##\s*Contexto\s*\n+([\s\S]*?)(?=##\s*Decisión|$)", re.IGNORECASE)
    DECISION_PATTERN = re.compile(r"##\s*Decisión\s*\n+([\s\S]*?)(?=##\s*Consecuencias|$)", re.IGNORECASE)
    CONSEQUENCES_PATTERN = re.compile(r"##\s*Consecuencias\s*\n+([\s\S]*?)(?=$)", re.IGNORECASE)

    def __init__(self, docs_dir: str = "docs/decisions"):
        self.docs_dir = docs_dir

    def list_adrs(self) -> List[ArchitectureDecisionRecord]:
        """Lists and parses all ADR files present in the documentation directory."""
        if not os.path.exists(self.docs_dir):
            return []

        adrs: List[ArchitectureDecisionRecord] = []
        for filename in os.listdir(self.docs_dir):
            m = self.FILE_PATTERN.match(filename)
            if not m:
                continue

            num = int(m.group(1))
            full_path = os.path.join(self.docs_dir, filename)

            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                h_match = self.HEADER_PATTERN.search(content)
                title = h_match.group(2).strip() if h_match else m.group(2).replace("-", " ").title()

                st_match = self.STATUS_PATTERN.search(content)
                status_raw = st_match.group(1).strip() if st_match else "ACCEPTED"
                status = ADRStatus.ACCEPTED if "aprobado" in status_raw.lower() or "accepted" in status_raw.lower() else ADRStatus.PROPOSED

                ctx_match = self.CONTEXT_PATTERN.search(content)
                context = ctx_match.group(1).strip() if ctx_match else ""

                dec_match = self.DECISION_PATTERN.search(content)
                decision = dec_match.group(1).strip() if dec_match else ""

                cons_match = self.CONSEQUENCES_PATTERN.search(content)
                consequences = cons_match.group(1).strip() if cons_match else ""

                adrs.append(ArchitectureDecisionRecord(
                    number=num,
                    title=title,
                    status=status,
                    context=context,
                    decision=decision,
                    consequences=consequences,
                    path=full_path
                ))
            except Exception:
                continue

        adrs.sort(key=lambda a: a.number)
        return adrs

    def get_next_adr_number(self) -> int:
        """Determines the next sequential ADR number."""
        existing = self.list_adrs()
        if not existing:
            return 1
        return max(a.number for a in existing) + 1

    def create_adr(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        status: ADRStatus = ADRStatus.ACCEPTED
    ) -> ArchitectureDecisionRecord:
        """Creates a new ADR markdown document with standardized template."""
        os.makedirs(self.docs_dir, exist_ok=True)
        next_num = self.get_next_adr_number()
        slug = _slugify(title)
        filename = f"ADR-{next_num:03d}-{slug}.md"
        full_path = os.path.join(self.docs_dir, filename)

        status_text = "Aprobado" if status == ADRStatus.ACCEPTED else "Propuesto"
        content = f"""# ADR-{next_num:03d}: {title}

## Estado
{status_text}

## Contexto
{context.strip()}

## Decisión
{decision.strip()}

## Consecuencias
{consequences.strip()}
"""
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return ArchitectureDecisionRecord(
            number=next_num,
            title=title,
            status=status,
            context=context,
            decision=decision,
            consequences=consequences,
            path=full_path,
            date=datetime.now().isoformat()
        )

    def validate_adr_content(self, content: str) -> bool:
        """Validates that markdown document has all standard ADR sections."""
        has_header = bool(self.HEADER_PATTERN.search(content))
        has_status = bool(self.STATUS_PATTERN.search(content))
        has_context = bool(self.CONTEXT_PATTERN.search(content))
        has_decision = bool(self.DECISION_PATTERN.search(content))
        has_consequences = bool(self.CONSEQUENCES_PATTERN.search(content))

        return has_header and has_status and has_context and has_decision and has_consequences
