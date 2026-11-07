# Specification: 002 - Master Orchestrator, DAG & Continuity Engine

## Objetivo
Implementar la Fase 1 del roadmap de `info.md`:
- Grafo de dependencias (DAG) con detección de ciclos y tareas paralelizables.
- Máquina de estados de tareas con 11 estados y guardas de transición.
- Motor de continuidad que responde a "¿Con qué continuamos hoy?" de manera determinista.
- Master Orchestrator y catálogo inicial de workflows componibles.

## Requisitos Verificados
- [x] DAG con orden topológico y detección de ciclos (`DependencyGraph`).
- [x] Gestión de tareas con validación de dependencias y evidencias para `DONE` (`TaskManager`).
- [x] Motor de continuidad con recomendación priorizada (`ContinuityEngine`).
- [x] Workflows canónicos (`BugFixWorkflow`, `FeatureDevelopmentWorkflow`, `InvestigationWorkflow`).
- [x] Comando interactivo CLI `dh-harness continue` y `npx dh-harness continue`.
