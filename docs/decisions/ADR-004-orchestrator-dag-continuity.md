# ADR-004: Master Orchestrator, Grafo de Dependencias (DAG) y Motor de Continuidad

## Estado
Aprobado

## Contexto
En proyectos extensos asistidos por agentes, el contexto conversacional se fragmenta con el paso de las sesiones. Sin una estructura formal de dependencias y memoria persistente, los agentes no pueden determinar de manera confiable qué tareas están terminadas, cuáles pueden ejecutarse simultáneamente en paralelo y cuál es el paso inmediato que debe priorizarse.

## Decisión
1. **Grafo Acíclico Dirigido (DAG):** Implementar `DependencyGraph` en `src/dh_harness/tasks/dag.py` para modelar dependencias entre tareas, ordenar la ejecución mediante algoritmo topológico (Kahn) y detectar ciclos de forma determinista (`CircularDependencyError`).
2. **Motor de Continuidad de Proyecto:** Implementar `ContinuityEngine` en `src/dh_harness/continuity/engine.py` para responder a la pregunta *"¿Con qué continuamos hoy?"* (`dh-harness continue` / `npx dh-harness continue`). El motor analiza tareas activas, completadas y candidatas listas, priorizando el cierre del trabajo en curso antes de iniciar nuevas tareas.
3. **Master Orchestrator:** Implementar `MasterOrchestrator` para conectar el clasificador de interacciones con workflows componibles ejecutables (`BugFixWorkflow`, `FeatureDevelopmentWorkflow`, `InvestigationWorkflow`).

## Consecuencias
- Cero ambigüedad al reanudar sesiones tras interrupciones.
- Detección automática de tareas independientes ejecutables en paralelo.
- Respeto riguroso de las precondiciones antes de iniciar cualquier desarrollo.
