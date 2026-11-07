# ADR-001: Adopción del Motor Determinista de TDD y Verificación de Pasos (AEE)

## Estado
Aprobado

## Contexto
Los agentes de inteligencia artificial tienden a asumir subjetivamente que su código funciona sin verificación objetiva o reportar como completadas tareas que contienen errores sintácticos o pruebas rotas.

## Decisión
Adoptar un **Motor Determinista de TDD y Verificación de Pasos (AEE)** mediante un motor determinista en Python (`.engine/harness.py`) respaldado por SQLite (`.engine/agent_engine.db`). Todo paso de ejecución debe vincularse a una expresión de verificación ejecutable en `verifiers.py`. Si cualquier paso falla, la tarea pasa a estado `🔴 BLOCKED`.

## Consecuencias
- Cero tolerancia a reportes falsos de finalización.
- Auditoría exacta y reproducible de cada paso ejecutado.
- Dependencia local en SQLite sin servicios externos obligatorios.
