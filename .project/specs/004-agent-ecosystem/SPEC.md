# Specification: 004 - Agent Ecosystem, Specialized Roles & Delegation Engine

## Objetivo
Implementar la Fase 3 del roadmap de `info.md`:
- Catálogo y Registro formal de agentes especializados (`AgentRole`, `ToolPermission`, `AgentDefinition`, `AgentRegistry`).
- Motor de delegación de tareas con contratos explícitos (`DelegationEngine`, `AgentTaskContract`).
- Regla de revisión independiente estricta (`SelfReviewViolationError`, `UnauthorizedReviewerError`).
- Spawning de agentes en el SDK oficial `google.antigravity` con menor privilegio (`CapabilitiesConfig`, `LocalAgentConfig`, `BuiltinTools`).
- Exposición CLI del ecosistema de agentes: `node bin/cli.js agents list` y `node bin/cli.js agents show <id>`.

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts`.
- [x] Catálogo con 8 roles especializados canónicos (Orchestrator, Architect, Backend Dev, Frontend Dev, DBA, Code Reviewer, Security Engineer, QA Engineer).
- [x] Registro con búsqueda por ID, rol, herramientas permitidas y prevención de duplicados.
- [x] Motor de delegación que bloquea auto-revisiones de agentes (`SelfReviewViolationError`).
- [x] Motor de delegación que restringe reviews a roles autorizados (`UnauthorizedReviewerError`).
- [x] Mapeo de menor privilegio hacia `google.antigravity.BuiltinTools` e instanciación de `google.antigravity.Agent`.
- [x] Comando CLI operativo: `dh-harness agents list` y `dh-harness agents show <id>`.
