# Specification: 006 - Skills Registry & Composable Workflow Engine

## Objetivo
Implementar la Fase 5 del roadmap de `info.md`:
- Catálogo y Registro formal de habilidades de ingeniería (`SkillCategory`, `SkillDefinition`, `SkillsRegistry`).
- Emparejamiento dinámico de habilidades por intenciones (`match_skills_for_task`) respetando triggers y anti-triggers.
- Catálogo de workflows estándar (`feature-development`, `bug-fix`, `security-audit`, `api-development`).
- Motor de ejecución componible con verificación de dependencias entre etapas y recolección de evidencias (`WorkflowRunner`).
- Cumplimiento de la regla de revisión independiente en etapas de auditoría y revisión de código.
- Exposición CLI: `node bin/cli.js skills list`, `node bin/cli.js workflows list`, `workflows describe <id>`.

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts`.
- [x] Catálogo con 6 habilidades canónicas (Backend, Database, Frontend, Architecture, Security, Testing).
- [x] Registro con búsqueda por categoría, herramientas y emparejamiento por triggers.
- [x] Workflows estándar con etapas ordenadas por dependencias (`depends_on`).
- [x] Runner de workflows que valida dependencias de etapas y asigna agentes por rol.
- [x] Separación de agentes entre implementación y revisión independiente.
- [x] Comandos CLI operativos en Typer y binario de Node `bin/cli.js`.
