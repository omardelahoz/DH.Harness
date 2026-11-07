# ADR-006: Ecosistema de Agentes Especializados, Contratos de Delegación y Regla de Revisión Independiente

## Estado
Aprobado

## Contexto
En sistemas multi-agente complejos, permitir que un único agente monolítico asuma todos los roles (diseño, codificación, auditoría, pruebas y aprobación) genera conflictos de interés, deriva técnica y relajación de estándares. Se requiere un catálogo formal de agentes especializados con roles específicos, permisos de herramientas basados en el Principio de Menor Privilegio (Least Privilege), contratos explícitos de delegación de tareas y un control estricto que prohíba a cualquier agente revisar y aprobar su propio código (Regla de Revisión Independiente, info.md § 4.9 y § 23.2).

## Decisión
1. **Contratos Core Actualizados:**
   - Enriquecer `dh_harness.core.contracts` con los enums `AgentRole` (Orchestrator, Solution Architect, Backend Developer, Frontend Developer, Database Engineer, Code Reviewer, Security Engineer, QA Engineer, Technical Writer) y `ToolPermission` (Read Only, File Write, Run Command, Terminal Sandbox, Git Operations, MCP Tools).
   - Definir los modelos de datos tipados `AgentDefinition`, `AgentTaskContract` y `AgentExecutionResult`.
2. **Catálogo Canónico y Registro Extensible:**
   - Implementar `src/dh_harness/agents/catalog.py` con las definiciones canónicas de agentes especializados (descripción, roles, herramientas permitidas, habilidades requeridas y criterios de evaluación).
   - Implementar `src/dh_harness/agents/registry.py` (`AgentRegistry`) para indexar, buscar por rol/herramienta y consultar agentes.
3. **Motor de Delegación y Guarda de Revisión Independiente:**
   - Implementar `src/dh_harness/agents/delegation.py` (`DelegationEngine`).
   - Bloquear terminantemente el auto-review (`SelfReviewViolationError`) si un agente intenta revisar su propio trabajo asignado.
   - Restringir la capacidad de revisión exclusivamente a roles autorizados (`CODE_REVIEWER`, `QA_ENGINEER`, `SECURITY_ENGINEER`), rechazando roles no autorizados con `UnauthorizedReviewerError`.
   - Registrar la evidencia del review independiente directamente en el historial de la tarea.
4. **Spawning de Agentes con SDK Antigravity (`google.antigravity`):**
   - Actualizar `src/dh_harness/sdk/adapter.py` para mapear los permisos de `AgentDefinition` a `BuiltinTools` de Antigravity (`VIEW_FILE`, `FIND_FILE`, `LIST_DIR`, `SEARCH_DIR`, `CREATE_FILE`, `EDIT_FILE`, `RUN_COMMAND`) configurados dentro de `CapabilitiesConfig` y `LocalAgentConfig`.
5. **Comandos CLI:**
   - Incorporar el grupo de comandos `agents` en la CLI (`dh-harness agents list`, `dh-harness agents show <id>`) ejecutable vía Node (`node bin/cli.js agents list` / `npx dh-harness agents list`).

## Consecuencias
- Cero tolerancia a sesgos de autoría y auto-aprobación en el flujo de desarrollo.
- Principio de menor privilegio aplicado a nivel de herramientas por rol de agente.
- Transparencia total en la asignación, delegación y revisión dentro del ciclo TDD.
