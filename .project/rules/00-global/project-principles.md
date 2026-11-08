# Global Project Principles (`.project/rules/00-global/project-principles.md`)

1. **Evidencia sobre Suposiciones:** No declarar capacidades o implementaciones sin pruebas automatizadas verificables.
2. **Determinismo:** El progreso y estado de tareas se gestiona mediante la persistencia en SQLite (`.project/memory/harness.db`) y la suite de pruebas unitarias.
3. **Mínimo Proceso Necesario, Máximo Rigor:** Adaptar el esfuerzo al impacto. Preguntas conceptuales no crean tareas; cambios de código exigen TDD obligatorio.
4. **Seguridad por Diseño (Fail-Closed):** Nunca registrar secretos ni datos sensibles en commits, logs o memoria.
5. **Clean Architecture:** Mantener separación estricta entre Adaptadores (SDK/CLI/FS), Dominio/Core (Modelos y contratos), Aplicación (Orquestador, Clasificador, TDD) e Infraestructura.
