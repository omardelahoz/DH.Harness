# DH Engineering Harness - Agent Operating Manual (`.project/AGENT.md`)

Este documento es el manual operativo de ingeniería para cualquier agente que trabaje en este workspace. Define la gobernanza del proyecto, la estructura de memoria `.project/` y la interacción con el motor determinista de ejecución y pruebas **Graviton TDD (AEE)**.

---

## 1. Misión del Proyecto

DH Engineering Harness es una plataforma integral de ingeniería de software orientada a agentes para **Google Antigravity**. Proporciona gobernanza determinista, ciclo TDD estricto, orquestación de flujos de trabajo, memoria persistente multi-nivel y entrega controlada con Git/GitHub.

---

## 2. Jerarquía de Trabajo y Responsabilidades

```text
.engine/agent_engine.db  ->  Estado determinista de ejecución, pasos y verificadores en SQLite.
.engine/harness.py       ->  CLI ejecutable del motor AEE.
.engine/verifiers.py     ->  Biblioteca de pruebas y verificadores Python.
ENGINE_INSTRUCTIONS.md   ->  Protocolo de trabajo del motor de ejecución.
.project/                ->  Memoria persistente, reglas, especificaciones y trazabilidad.
src/dh_harness/          ->  Código fuente del Harness.
bin/cli.js               ->  Launcher ejecutable de Node.js (distribución npm).
pyproject.toml           ->  Empaquetado Python oficial con soporte del SDK de Antigravity.
tests/                   ->  Suites de pruebas TDD (unit, integration, contract).
docs/                    ->  Documentación de arquitectura, decisiones (ADRs) y guías.
```

---

## 3. Reglas de Operación Determinista (Graviton TDD)

1. **Zero-Trust:** Todo cambio de comportamiento ejecutable debe validarse mediante un paso registrado en `.engine/harness.py` con una expresión de prueba en `verifiers.py`.
2. **Ciclo TDD Obligatorio:** REQUIREMENT -> TEST RED -> IMPLEMENT GREEN -> REFACTOR -> VERIFY -> DONE.
3. **Cero Datos Simulados en Aplicación:** Prohibido el uso de mocks en código de producción. Los mocks son válidos exclusivamente en pruebas unitarias aisladas.
4. **Verificación SQLite:** Ninguna tarea se reporta al usuario como "completada" sin que `python .engine/harness.py status <task_id>` devuelva `🟢 COMPLETED`.

---

## 4. Comandos de Referencia

- Inicializar base de datos: `python .engine/harness.py init`
- Registrar tarea: `python .engine/harness.py start-task "<Título>" "<Descripción>"`
- Registrar paso: `python .engine/harness.py add-step <task_id> <orden> "<comando>" "<expresión_verificador>"`
- Ejecutar siguiente paso: `python .engine/harness.py run-next <task_id>`
- Consultar dashboard: `python .engine/harness.py status <task_id>`
