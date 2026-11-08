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
        ),
        SkillDefinition(
            id="git-governance",
            name="Git Repository Governance & DoD",
            category=SkillCategory.ENGINEERING_CORE,
            description="Conventional commits, protected branch enforcement, Definition of Done audits, and isolated worktrees.",
            triggers=["git", "branch", "commit", "dod", "worktree", "pr"],
            anti_triggers=[],
            required_tools=[ToolPermission.READ_ONLY, ToolPermission.GIT_OPERATIONS],
            guidelines=[
                "Zero direct commits to protected main branch",
                "Strict Conventional Commits format validation",
                "Full evidence verification before completing Definition of Done"
            ]
        ),
        SkillDefinition(
            id="quality-engineering",
            name="Quality Gates & Independent Review",
            category=SkillCategory.TESTING,
            description="Multidimensional quality scoring, independent review enforcement, and test coverage gates.",
            triggers=["quality", "qa", "gate", "review", "score"],
            anti_triggers=[],
            required_tools=[ToolPermission.READ_ONLY, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Independent peer review mandatory (anti-self-review)",
                "Zero failing unit tests tolerated in quality gates"
            ]
        ),
        SkillDefinition(
            id="orchestrator-continuity",
            name="Master Orchestration & Project Continuity",
            category=SkillCategory.ENGINEERING_CORE,
            description="Interaction classification into 5 modes, DAG dependency resolution, and continuity recommendations.",
            triggers=["orchestrator", "continuity", "classify", "next", "continue", "dag"],
            anti_triggers=[],
            required_tools=[ToolPermission.READ_ONLY, ToolPermission.MCP_TOOLS],
            guidelines=[
                "Proportional rigor based on interaction mode",
                "Topological task ordering with cycle detection"
            ]
        ),
        SkillDefinition(
            id="dotnet-clean-architecture",
            name=".NET & C# Clean Architecture Engineering",
            category=SkillCategory.BACKEND,
            description="Enterprise .NET 8/9, ASP.NET Core, EF Core, Dapper, CQRS, and strict layer boundary enforcement.",
            triggers=["dotnet", "c#", "csharp", "aspnet", "dapper", "efcore", "linq"],
            anti_triggers=["frontend-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Thin controllers with CQRS command/query handlers",
                "Dapper parameterized queries with cancellation token propagation",
                "AsNoTracking on EF Core read projections",
                "Zero database access from Presentation or Application layers"
            ]
        ),
        SkillDefinition(
            id="python-fastapi-clean-architecture",
            name="Python & FastAPI Clean Architecture",
            category=SkillCategory.BACKEND,
            description="High-performance async APIs with FastAPI, Pydantic v2 schemas, SQLAlchemy async sessions, and dependency injection.",
            triggers=["python", "fastapi", "pydantic", "sqlalchemy", "asyncio", "uvicorn"],
            anti_triggers=["frontend-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Strict Pydantic v2 schema validation for inputs and responses",
                "Asynchronous database sessions managed via context managers",
                "Layer separation: Routers -> Application Services -> Domain Models -> Repositories"
            ]
        ),
        SkillDefinition(
            id="angular-enterprise-ui",
            name="Angular Enterprise UI Architecture",
            category=SkillCategory.FRONTEND,
            description="Modern Angular 18+ architecture with Standalone Components, Signals, RxJS state management, and OnPush change detection.",
            triggers=["angular", "rxjs", "signals", "ngrx", "typescript-ui"],
            anti_triggers=["backend-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Standalone components with OnPush change detection strategy",
                "Reactive state management utilizing modern Signals",
                "WCAG 2.1 AA accessible templates and semantic HTML"
            ]
        ),
        SkillDefinition(
            id="react-nextjs-ui",
            name="React 19 & Next.js App Router Engineering",
            category=SkillCategory.FRONTEND,
            description="Scalable React interfaces using Next.js App Router, Server Components, client boundaries, and Tailwind styling.",
            triggers=["react", "nextjs", "next.js", "jsx", "tsx", "tailwind"],
            anti_triggers=["backend-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Clear separation between Server Components and Client Components ('use client')",
                "Complete component states: loading skeleton, empty state, error boundary, and data view",
                "Consume real backend APIs with typed fetch / TanStack Query"
            ]
        ),
        SkillDefinition(
            id="mobile-flutter-engineering",
            name="Mobile Multiplatform Engineering with Flutter",
            category=SkillCategory.MOBILE,
            description="Cross-platform mobile apps using Flutter & Dart, BLoC/Riverpod state management, and offline-first Clean Architecture.",
            triggers=["flutter", "dart", "mobile", "android", "ios", "bloc"],
            anti_triggers=["web-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Clean Architecture layer separation (Domain, Data, Presentation)",
                "Immutable state models with BLoC / Cubit",
                "Offline-first resilience with local key-value and SQLite caching"
            ]
        ),
        SkillDefinition(
            id="postgresql-database-specialist",
            name="PostgreSQL Advanced Data Engineering",
            category=SkillCategory.DATABASE,
            description="PostgreSQL schema optimization, GIN/BRIN indexing, JSONB queries, table partitioning, and execution plan auditing.",
            triggers=["postgres", "postgresql", "psql", "jsonb", "gin-index"],
            anti_triggers=["ui-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Transactional and idempotent schema migration scripts",
                "EXPLAIN ANALYZE validation for query execution cost optimization",
                "Zero string concatenation in SQL queries"
            ]
        ),
        SkillDefinition(
            id="sqlserver-database-specialist",
            name="SQL Server & T-SQL Engineering",
            category=SkillCategory.DATABASE,
            description="SQL Server enterprise engineering, T-SQL transactional scripting, columnstore indexes, and deadlock prevention.",
            triggers=["sqlserver", "sql-server", "tsql", "t-sql", "ssms"],
            anti_triggers=["ui-only"],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Explicit transaction handling and appropriate isolation levels (READ COMMITTED SNAPSHOT)",
                "Clustered and non-clustered index tuning with covering index strategy",
                "Parameterized queries compatible with Dapper and Entity Framework Core"
            ]
        ),
        SkillDefinition(
            id="devops-ci-cd-pipelines",
            name="CI/CD Pipelines & Continuous Delivery",
            category=SkillCategory.DEVOPS,
            description="Automated continuous integration and delivery pipelines (GitHub Actions, Azure DevOps) with integrated quality gates.",
            triggers=["cicd", "ci-cd", "github-actions", "pipeline", "azure-pipelines", "devops"],
            anti_triggers=[],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND, ToolPermission.GIT_OPERATIONS],
            guidelines=[
                "Fail-fast quality gates running unit tests, AST false test detection, and secret scanning",
                "Hermetic and reproducible build environments with dependency caching",
                "Least-privilege service account credentials in CI runners"
            ]
        ),
        SkillDefinition(
            id="docker-kubernetes-iac",
            name="Containers, Kubernetes & Infrastructure as Code",
            category=SkillCategory.CLOUD,
            description="Multi-stage production Dockerfiles, non-root containers, Kubernetes manifests, Helm charts, and Terraform IaC.",
            triggers=["docker", "kubernetes", "k8s", "helm", "terraform", "iac", "container"],
            anti_triggers=[],
            required_tools=[ToolPermission.FILE_WRITE, ToolPermission.RUN_COMMAND],
            guidelines=[
                "Multi-stage builds producing minimal distroless or alpine non-root images",
                "Health probes (liveness, readiness, startup) on all Kubernetes deployments",
                "Declarative and idempotent infrastructure configurations with Terraform"
            ]
        )
    ]
