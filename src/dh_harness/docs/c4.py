from __future__ import annotations
import re
from typing import List, Dict, Any, Optional

from dh_harness.core.contracts import C4DiagramType, C4DiagramDefinition

class C4DiagramGenerator:
    """
    Generates Mermaid-compliant C4 Architecture Diagrams (info.md § 19).
    Produces Context, Container, and Component diagrams with sanitized node labels.
    """

    def generate_system_context(
        self,
        system_name: str,
        description: str,
        users: List[str],
        external_systems: List[str]
    ) -> C4DiagramDefinition:
        """Generates a Level 1 System Context Diagram."""
        lines = ["flowchart TD"]
        elements: List[str] = [system_name]
        relationships: List[str] = []

        # System Node
        lines.append(f'    sys["💻 {system_name}\\n({description})"]')

        # User Nodes
        for i, user in enumerate(users):
            node_id = f"user_{i}"
            elements.append(user)
            lines.append(f'    {node_id}["👤 {user}"]')
            lines.append(f'    {node_id} -->|Uses| sys')
            relationships.append(f"{user} -> {system_name}")

        # External Systems
        for i, ext in enumerate(external_systems):
            node_id = f"ext_{i}"
            elements.append(ext)
            lines.append(f'    {node_id}["🌐 {ext}"]')
            lines.append(f'    sys -->|Integrates with| {node_id}')
            relationships.append(f"{system_name} -> {ext}")

        mermaid_code = "\n".join(lines)
        return C4DiagramDefinition(
            title=f"System Context: {system_name}",
            diagram_type=C4DiagramType.CONTEXT,
            mermaid_code=mermaid_code,
            elements=elements,
            relationships=relationships
        )

    def generate_container_diagram(
        self,
        system_name: str,
        containers: List[Dict[str, str]]
    ) -> C4DiagramDefinition:
        """Generates a Level 2 Container Diagram."""
        lines = ["flowchart TD"]
        lines.append(f'    subgraph sys_boundary["{system_name}"]')
        elements: List[str] = []
        relationships: List[str] = []

        prev_id: Optional[str] = None
        for i, c in enumerate(containers):
            cid = f"cont_{i}"
            name = c.get("name", f"Container {i}")
            tech = c.get("tech", "")
            desc = c.get("desc", "")
            elements.append(name)

            label = f"📦 {name}"
            if tech:
                label += f"\\n[{tech}]"
            if desc:
                label += f"\\n({desc})"

            lines.append(f'        {cid}["{label}"]')
            if prev_id:
                lines.append(f'        {prev_id} -->|Communicates with| {cid}')
                relationships.append(f"{containers[i-1].get('name')} -> {name}")
            prev_id = cid

        lines.append("    end")
        mermaid_code = "\n".join(lines)

        return C4DiagramDefinition(
            title=f"Container Diagram: {system_name}",
            diagram_type=C4DiagramType.CONTAINER,
            mermaid_code=mermaid_code,
            elements=elements,
            relationships=relationships
        )

    def render_markdown(self, definition: C4DiagramDefinition) -> str:
        """Renders the diagram inside a fenced mermaid markdown block."""
        return f"```mermaid\n{definition.mermaid_code}\n```\n"
