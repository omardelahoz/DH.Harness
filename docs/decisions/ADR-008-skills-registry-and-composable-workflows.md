# ADR-008: Registro Dinámico de Skills y Motor de Workflows Componibles

## Estado
Aprobado

## Contexto
En sistemas asistidos por agentes para desarrollo de software, la ejecución no estructurada de tareas complejas genera omisión de pasos críticos (como pruebas RED, diseño arquitectónico o revisiones de seguridad). Asimismo, cada especialidad técnica requiere procedimientos, herramientas permitidas y directrices específicas que no deben acoplarse rígidamente al agente central ni confundirse con simples prompts (info.md § 5 y § 6).

## Decisión
1. **Contratos Core de Habilidades y Flujos:**
   - Enriquecer `dh_harness.core.contracts` con los enums `SkillCategory` (Core, Backend, Frontend, Database, UI/UX, Testing, Security, DevOps, Architecture) y los modelos de datos tipados `SkillDefinition`, `WorkflowStage`, `WorkflowDefinition` y `WorkflowExecutionResult`.
2. **Registro Dinámico de Skills (`SkillsRegistry`):**
   - Implementar `src/dh_harness/skills/catalog.py` con 6 habilidades canónicas de ingeniería: Clean Architecture, Database Migrations (Dapper & EF Core), Modern Responsive UI/UX, System Architecture (C4), AppSec Threat Modeling y Test Automation & Strict TDD.
   - Implementar `src/dh_harness/skills/registry.py` con búsqueda por categoría, permisos de herramientas y resolución automática de intenciones por coincidencia de palabras clave (`triggers`) y exclusión de anti-patrones (`anti_triggers`).
3. **Motor y Ejecutor de Workflows Componibles (`WorkflowRunner`):**
   - Implementar `src/dh_harness/workflows/catalog.py` con los workflows estándar: `feature-development`, `bug-fix`, `security-audit`, y `api-development`.
   - Implementar `src/dh_harness/workflows/runner.py` garantizando la ejecución de etapas en orden topológico según sus dependencias (`depends_on`).
   - Asignar dinámicamente agentes especializados desde el `AgentRegistry` según el rol requerido por cada etapa.
   - Forzar la separación de responsabilidades e independencia de revisión: la etapa de revisión de código (`AgentRole.CODE_REVIEWER`) no puede ser asignada al mismo agente que desarrolló la implementación previa.
4. **Comandos CLI e Integración Node:**
   - Exponer en Typer y en el binario de Node `bin/cli.js`:
     - `dh-harness skills list`: Catálogo de habilidades registradas.
     - `dh-harness skills show <id>`: Detalle de directrices, herramientas y triggers.
     - `dh-harness skills match <prompt>`: Emparejamiento dinámico de skills según el requerimiento del usuario.
     - `dh-harness workflows list`: Listado de workflows componibles disponibles.
     - `dh-harness workflows describe <id>`: Desglose de etapas, dependencias y roles.

## Consecuencias
- Flujos de trabajo estructurados, reproducibles y trazables con evidencia verificable por etapa.
- Activación proporcional de procedimientos técnicos especializados según el dominio del problema.
- Garantía inviolable de revisión de código independiente en todos los workflows.
