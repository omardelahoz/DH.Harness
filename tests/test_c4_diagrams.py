import pytest
from dh_harness.core.contracts import C4DiagramType
from dh_harness.docs.c4 import C4DiagramGenerator

def test_c4_generator_creates_context_diagram():
    generator = C4DiagramGenerator()
    diag = generator.generate_system_context(
        system_name="DH Engineering Harness",
        description="Autonomous Agentic Software Engineering Harness for Google Antigravity",
        users=["Software Engineer", "AI Agent"],
        external_systems=["GitHub", "Google Antigravity SDK", "SQLite Engine"]
    )

    assert diag.diagram_type == C4DiagramType.CONTEXT
    assert "DH Engineering Harness" in diag.mermaid_code
    assert "GitHub" in diag.mermaid_code
    assert len(diag.elements) >= 4

def test_c4_generator_creates_container_diagram():
    generator = C4DiagramGenerator()
    containers = [
        {"name": "CLI Launcher", "tech": "Node.js (bin/cli.js)", "desc": "Entry point for developers and CI/CD"},
        {"name": "Core Harness", "tech": "Python / Typer", "desc": "Domain logic, TDD engine & orchestration"},
        {"name": "Persistent Storage", "tech": "SQLite (agent_engine.db)", "desc": "Deterministic state and audit logs"}
    ]
    diag = generator.generate_container_diagram(
        system_name="DH Engineering Harness",
        containers=containers
    )

    assert diag.diagram_type == C4DiagramType.CONTAINER
    assert "CLI Launcher" in diag.mermaid_code
    assert "SQLite" in diag.mermaid_code
    assert len(diag.elements) == 3

def test_c4_generator_renders_valid_mermaid_markdown():
    generator = C4DiagramGenerator()
    diag = generator.generate_system_context(
        system_name="Test System",
        description="Sample system",
        users=["User"],
        external_systems=["ExtAPI"]
    )
    rendered = generator.render_markdown(diag)

    assert rendered.startswith("```mermaid")
    assert rendered.endswith("```\n")
    assert "flowchart" in rendered or "graph" in rendered
