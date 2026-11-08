# ADR-001: Adopción del Motor Determinista de TDD y Verificación de Pasos (AEE)

## Estado
Aprobado

## Contexto
Los agentes de inteligencia artificial tienden a asumir subjetivamente que su código funciona sin verificación objetiva o reportar como completadas tareas que contienen errores sintácticos o pruebas rotas.

## Decisión
Adoptar un **Motor Determinista de TDD y Verificación de Pasos** en Python (`src/dh_harness/tdd/`) respaldado por la base de datos de persistencia en SQLite (`.project/memory/harness.db`) y la bóveda criptográfica SHA-256 (`RedEvidenceVault`). Todo paso de ejecución y cambio en código de producción (`src/`) requiere evidencia previa de prueba en fallo (RED) y suite de pruebas pasando al 100%. Si cualquier verificación falla, la tarea pasa a estado `🔴 BLOCKED`.

## Consecuencias
- Cero tolerancia a reportes falsos de finalización.
- Auditoría exacta y reproducible de cada paso ejecutado.
- Dependencia local en SQLite sin servicios externos obligatorios.
