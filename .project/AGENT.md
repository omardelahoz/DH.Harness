# DH Engineering Harness - Agent Operating Manual (`.project/AGENT.md`)

Este documento es el manual operativo de ingeniería para cualquier agente que trabaje en este workspace. Define la gobernanza del proyecto, la estructura de memoria `.project/` y la interacción con el motor determinista de ejecución y pruebas de **DH Engineering Harness**.

---

## 1. Misión del Proyecto

DH Engineering Harness es una plataforma integral de ingeniería de software orientada a agentes para **Google Antigravity**. Proporciona gobernanza determinista, ciclo TDD estricto, orquestación de flujos de trabajo, memoria persistente multi-nivel y entrega controlada con Git/GitHub.

---

## 2. Jerarquía de Trabajo y Responsabilidades

```text
.project/memory/harness.db ->  Estado determinista de verificación y tareas en SQLite.
.project/                  ->  Memoria persistente, reglas, especificaciones y trazabilidad.
.agents/skills/            ->  Catálogo modular de 18 skills de ingeniería.
.agents/agents/            ->  Catálogo de 14 roles especializados de agentes.
AGENTS.md                  ->  Protocolo de gobernanza y directrices operativas.
src/dh_harness/            ->  Código fuente del Harness.
bin/cli.js                 ->  Launcher ejecutable de Node.js (distribución npm).
pyproject.toml             ->  Empaquetado Python oficial con soporte del SDK de Antigravity.
tests/                     ->  Suites de pruebas TDD (unit, integration, contract).
docs/                      ->  Documentación de arquitectura, decisiones (ADRs) y guías.
```

---

## 3. Reglas de Operación Determinista (DH Engineering Harness)

1. **Zero-Trust:** Todo cambio de comportamiento ejecutable debe validarse mediante pruebas unitarias en RED antes de tocar `src/` (bóveda criptográfica SHA-256).
2. **Ciclo TDD Obligatorio:** REQUIREMENT -> TEST RED -> IMPLEMENT GREEN -> REFACTOR -> VERIFY -> DONE.
3. **Cero Datos Simulados en Aplicación:** Prohibido el uso de mocks en código de producción. Los mocks son válidos exclusivamente en pruebas unitarias aisladas.
4. **Verificación Determinista:** Ninguna tarea se reporta al usuario como "completada" sin que la suite de pruebas pase al 100% y `dh-harness health` reporte estado EXCELLENT.

---

## 4. Comandos de Referencia

- Comprobar salud del proyecto: `dh-harness health`
- Ejecutar suite de pruebas: `dh-harness check` (o `pytest tests/`)
- Auditar pruebas falsas: `dh-harness tdd audit-tests`
- Escaneo de secretos: `dh-harness sec scan`
- Verificar Definition of Done: `dh-harness git check-dod <id>`
- Diagnóstico de continuidad: `dh-harness continue`
