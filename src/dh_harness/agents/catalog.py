from __future__ import annotations
from typing import List
from dh_harness.core.contracts import AgentDefinition, AgentRole, ToolPermission

def get_default_catalog() -> List[AgentDefinition]:
    """
    Returns the canonical catalog of specialized engineering agents.
    Complies with Section 4 of info.md.
    """
    return [
        AgentDefinition(
            id="chief-orchestrator",
            name="Chief Orchestrator",
            role=AgentRole.ORCHESTRATOR,
            description="Central coordinator for request classification, task routing, workflow dispatch, and progress tracking.",
            allowed_tools=[ToolPermission.READ_ONLY, ToolPermission.MCP_TOOLS],
            required_skills=["orchestration", "workflow-planning"],
            evaluation_criteria=["Accurate classification", "Zero unauthorized writes", "Context preservation"]
        ),
        AgentDefinition(
            id="solution-architect",
            name="Solution Architect",
            role=AgentRole.SOLUTION_ARCHITECT,
            description="System and software architecture design, C4 modeling, ADR production, and technology stack evaluation.",
            allowed_tools=[ToolPermission.READ_ONLY, ToolPermission.FILE_WRITE],
            required_skills=["system-architecture", "c4-modeling", "adr"],
            evaluation_criteria=["Clean Architecture compliance", "Modularity", "Scalability", "Clear ADR justification"]
        ),
        AgentDefinition(
            id="developer-backend",
            name="Senior Backend Engineer",
            role=AgentRole.BACKEND_DEVELOPER,
            description="Production backend engineer for APIs, domain models, services, migrations, and strict TDD implementation.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND, ToolPermission.TERMINAL_SANDBOX],
            required_skills=["clean-architecture", "solid", "dapper", "ef-core", "asyncio", "python", "dotnet"],
            evaluation_criteria=["Mandatory TDD", "Zero fake data", "Clean architecture layer separation"]
        ),
        AgentDefinition(
            id="developer-frontend",
            name="Senior Frontend Engineer",
            role=AgentRole.FRONTEND_DEVELOPER,
            description="Specialist in modern web UIs, responsive layout, state management, design systems, and real backend integration.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["react", "angular", "typescript", "tailwind", "accessibility", "responsive-design"],
            evaluation_criteria=["Zero mock data in production", "Accessibility WCAG", "Responsive UI", "Zero layout overflow"]
        ),
        AgentDefinition(
            id="database-engineer",
            name="Senior DBA & Data Engineer",
            role=AgentRole.DATABASE_ENGINEER,
            description="Database schema design, query optimization, indexing, idempotent migrations, and real seed data.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["sql", "postgresql", "sql-server", "sqlite", "query-optimization", "data-modeling"],
            evaluation_criteria=["Referential integrity", "Idempotent migrations", "Optimized queries", "Zero SQL injection"]
        ),
        AgentDefinition(
            id="independent-code-reviewer",
            name="Independent Code Reviewer",
            role=AgentRole.CODE_REVIEWER,
            description="Strict peer code reviewer evaluating architecture, security, SOLID principles, and clean code. Cannot modify implementation.",
            allowed_tools=[ToolPermission.READ_ONLY],
            required_skills=["code-review", "clean-code", "solid", "dry", "kiss"],
            evaluation_criteria=["Objective review", "Detection of technical debt", "Independent verification"]
        ),
        AgentDefinition(
            id="security-engineer",
            name="Cybersecurity & AppSec Engineer",
            role=AgentRole.SECURITY_ENGINEER,
            description="Threat modeling, OWASP Top 10 auditing, secret scanning, dependency vulnerability audit, and secure defaults.",
            allowed_tools=[ToolPermission.READ_ONLY, ToolPermission.RUN_COMMAND],
            required_skills=["owasp", "threat-modeling", "secret-scanning", "dependency-audit"],
            evaluation_criteria=["Zero leaked secrets", "Least privilege compliance", "Fail-closed security"]
        ),
        AgentDefinition(
            id="qa-engineer",
            name="Test Architect & QA Engineer",
            role=AgentRole.QA_ENGINEER,
            description="Test automation strategy, integration and E2E test suites, quality gates, and false test detection.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["testing-pyramid", "pytest", "playwright", "tdd-enforcement", "quality-gates"],
            evaluation_criteria=["Zero false tests", "Meaningful coverage", "Deterministic assertions"]
        ),
    ]
