from __future__ import annotations
from typing import List
from dh_harness.core.contracts import SkillDefinition, SkillCategory, ToolPermission

def get_default_skills_catalog() -> List[SkillDefinition]:
    """
    Returns the canonical catalog of engineering skills compliant with info.md Section 5.
    """
    return [
        SkillDefinition(
            id="clean-architecture-backend",
            name="Clean Architecture Backend Engineering",
            category=SkillCategory.BACKEND,
            description="Domain, Application, Infrastructure, and API layer design with strict separation and strong typing.",
            triggers=["backend", "api", "clean-architecture", "domain", "repository", "service"],
            anti_triggers=["frontend-only", "css-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Thin controllers: no database access or business logic in controllers",
                "Repository pattern strictly isolated inside Infrastructure layer",
                "Zero fake or static mock data in production backend code"
            ]
        ),
        SkillDefinition(
            id="database-migrations-dapper-ef",
            name="Database Engineering & Migrations (Dapper & EF Core)",
            category=SkillCategory.DATABASE,
            description="Schema design, idempotent migrations, parameterized queries, and real seed data.",
            triggers=["database", "sql", "migration", "dapper", "ef-core", "postgres", "sqlite"],
            anti_triggers=["ui-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Zero SQL string interpolation: always use parameterized queries",
                "Idempotent migration scripts with transactional safety",
                "AsNoTracking on read queries and cancellation token propagation"
            ]
        ),
        SkillDefinition(
            id="modern-frontend-ui",
            name="Modern Responsive Web UI/UX",
            category=SkillCategory.FRONTEND,
            description="Accessible, responsive interface components consuming real backend endpoints.",
            triggers=["frontend", "ui", "react", "angular", "css", "tailwind", "responsive", "component"],
            anti_triggers=["backend-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Zero hardcoded data arrays in UI: consume real backend APIs",
                "WCAG accessibility standards with semantic HTML",
                "Responsive design handling desktop, tablet, and mobile views"
            ]
        ),
        SkillDefinition(
            id="system-architecture-c4",
            name="System Architecture & C4 Modeling",
            category=SkillCategory.ARCHITECTURE,
            description="System and software architecture design, C4 modeling, and ADR production.",
            triggers=["architecture", "c4", "adr", "system-design", "modeling"],
            anti_triggers=[],
            required_tools=[ToolPermission.READ_ONLY, ToolPermission.FILE_WRITE],
            guidelines=[
                "C4 context, container, and component diagram generation",
                "Systematic ADR documentation for all major technical decisions"
            ]
        ),
        SkillDefinition(
            id="appsec-threat-modeling",
            name="Application Security & Threat Modeling",
            category=SkillCategory.SECURITY,
            description="OWASP Top 10 auditing, STRIDE threat modeling, secret scanning, and secure defaults.",
            triggers=["security", "threat modeling", "owasp", "secret", "vulnerability", "auth"],
            anti_triggers=[],
            required_tools=[ToolPermission.READ_ONLY, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Fail-closed access controls and token validation",
                "Mandatory secret scanning prior to commits and merges"
            ]
        ),
        SkillDefinition(
            id="tdd-test-automation",
            name="Test Automation & Strict TDD Strategy",
            category=SkillCategory.TESTING,
            description="Testing pyramid, AST-based false test detection, and cryptographic RED evidence verification.",
            triggers=["tdd", "test", "testing", "pytest", "unit-test", "integration-test"],
            anti_triggers=[],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Zero cosmetic tests: every test must execute verifiable assertions",
                "Mandatory RED phase evidence before modifying production code in src/"
            ]
        )
    ]
