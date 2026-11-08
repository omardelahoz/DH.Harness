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
        AgentDefinition(
            id="dotnet-lead-engineer",
            name=".NET & C# Lead Specialist",
            role=AgentRole.BACKEND_DEVELOPER,
            description="Specialist in .NET 8/9, C#, ASP.NET Core, EF Core, Dapper, CQRS, and Clean Architecture.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["dotnet-clean-architecture", "database-migrations", "tdd-test-automation"],
            evaluation_criteria=["Thin controllers", "Clean architecture layer compliance", "Parameterized Dapper/EF queries"]
        ),
        AgentDefinition(
            id="python-lead-engineer",
            name="Python & FastAPI Lead Specialist",
            role=AgentRole.BACKEND_DEVELOPER,
            description="Specialist in Python 3.12, FastAPI, Pydantic v2, SQLAlchemy async, and Clean Architecture.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["python-fastapi-clean-architecture", "clean-architecture-backend", "tdd-test-automation"],
            evaluation_criteria=["Async performance", "Strict Pydantic typing", "Clean layer boundaries"]
        ),
        AgentDefinition(
            id="react-frontend-lead",
            name="React & Next.js Lead Specialist",
            role=AgentRole.FRONTEND_DEVELOPER,
            description="Specialist in React 19, Next.js (App Router, Server Components), Tailwind, and accessible UI.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["react-nextjs-ui", "modern-frontend-ui"],
            evaluation_criteria=["Server/Client boundary correctness", "WCAG AA compliance", "Zero mock data in production"]
        ),
        AgentDefinition(
            id="angular-frontend-lead",
            name="Angular Enterprise Lead Specialist",
            role=AgentRole.FRONTEND_DEVELOPER,
            description="Specialist in Angular 18+, Standalone Components, Signals, RxJS, NgRx, and OnPush change detection.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["angular-enterprise-ui", "modern-frontend-ui"],
            evaluation_criteria=["Signals and reactive patterns", "OnPush performance", "Accessibility WCAG AA"]
        ),
        AgentDefinition(
            id="mobile-engineer",
            name="Mobile & Flutter Specialist",
            role=AgentRole.MOBILE_DEVELOPER,
            description="Specialist in mobile applications using Flutter, Dart, BLoC/Riverpod, and offline-first Clean Architecture.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            required_skills=["mobile-flutter-engineering", "modern-frontend-ui"],
            evaluation_criteria=["Clean Architecture mobile separation", "Offline-first resilience", "State management predictability"]
        ),
        AgentDefinition(
            id="devops-cloud-engineer",
            name="DevOps & Cloud Infrastructure Engineer",
            role=AgentRole.DEVOPS_ENGINEER,
            description="Specialist in CI/CD pipelines, Docker multi-stage builds, Kubernetes, Helm, and Terraform IaC.",
            allowed_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND, ToolPermission.GIT_OPERATIONS],
            required_skills=["devops-ci-cd-pipelines", "docker-kubernetes-iac", "git-governance"],
            evaluation_criteria=["Reproducible pipelines", "Non-root container security", "Immutable infrastructure"]
        ),
    ]
