# AGENTS.md — Protocolo Operativo para Agentes en DH Engineering Harness

Este documento es la especificación operativa para cualquier agente o modelo de lenguaje (LLM) que ejecute tareas de ingeniería dentro de un repositorio gobernado por **DH Engineering Harness**.

---

## 1. Reglas Cardinales de Operación

1. **Gobernanza Determinista de Tareas:**
   - Ninguna tarea se reporta como "terminada" o "lista" sin verificación objetiva determinista (`check` y pruebas unitarias pasando al 100%).
2. **Ciclo TDD Obligatorio para Cambios de Código:**
   - Para cualquier modificación en `src/` (modos `BUG_FIX`, `DEVELOPMENT`, `COMPLEX_ENGINEERING`):
     - **Paso 1 (RED):** Escribir o ajustar la prueba unitaria que reproduce el bug o define la nueva funcionalidad y verificar que falle.
     - **Paso 2 (GREEN):** Implementar la solución quirúrgica en la capa adecuada hasta que la prueba pase.
     - **Paso 3 (REFACTOR):** Limpiar código manteniendo las pruebas en verde.
   - La bóveda criptográfica (`RedEvidenceVault`) y el guardia (`CodeModificationGuard`) bloquearán cualquier intento de editar archivos en `src/` sin evidencia previa de falla en RED.
3. **Auditoría Estricta de Clean Architecture:**
   - **Prohibido:** Importar librerías de persistencia (`DbContext`, `SqlConnection`, `dapper`, `sqlite3`, etc.) o embeber consultas SQL dentro de controladores o APIs.
   - **Prohibido:** Poner lógica de negocio en controladores o en repositorios.
   - **Prohibido:** Hardcodear datos falsos o estáticos en controladores o componentes de frontend.
4. **Revisión Independiente (Anti-Self-Review):**
   - El agente que desarrolla una tarea no puede ser el mismo que aprueba el código o el PR. La revisión debe delegarse a un agente revisor (`code-reviewer` o `qa-engineer`).
5. **Auditoría de Secretos y Licencias:**
   - Queda terminantemente prohibido incluir tokens, credenciales o claves privadas.
   - Solo se permiten paquetes con licencias de la lista blanca SPDX (`MIT`, `Apache-2.0`, `BSD`, `ISC`).

---

## 2. Comandos CLI Esenciales para Agentes

| Comando | Propósito |
| :--- | :--- |
| `dh-harness status` | Muestra el estado del workspace, salud de motores y memoria activa. |
| `dh-harness continue` | Diagnostica el DAG de dependencias y recomienda la siguiente tarea prioritaria. |
| `dh-harness health` | Evalúa los 6 pilares de salud del proyecto (umbral mínimo para release: 100%). |
| `dh-harness classify "<prompt>"` | Determina el modo de interacción y si se exige TDD estricto. |
| `dh-harness check` | Ejecuta la suite de quality gates y pruebas unitarias. |
| `dh-harness skills list` | Consulta los 18 skills de ingeniería integrados en el arnés. |
| `dh-harness agents list` | Consulta el catálogo de agentes especializados y sus permisos. |
| `dh-harness tdd audit-tests` | Audita que no existan pruebas falsas o cosméticas con el detector AST. |
| `dh-harness git check-dod <id>` | Valida que la tarea cumpla con todos los criterios de Definition of Done. |
| `dh-harness arch audit [src]` | Audita deterministamente las fronteras de Clean Architecture. |
| `dh-harness sec scan [path]` | Escanea el código en busca de secretos o credenciales expuestas. |

---

## 3. Catálogo de Skills Incorporados (`.agents/skills/`)

- `clean-architecture-backend`: Thin controllers, aislamiento de repositorios, consultas parametrizadas.
- `database-migrations`: Migraciones idempotentes, modelos normalizados y seed data real.
- `modern-frontend-ui`: UI/UX responsiva, WCAG 2.1 AA y consumo de endpoints backend reales.
- `system-architecture-c4`: Modelado C4 Contexto/Contenedor y gestión de ADRs.
- `appsec-threat-modeling`: Escaneo AST de secretos, OWASP Top 10 y licencias SPDX permisivas.
- `tdd-test-automation`: Ciclo determinista RED-GREEN y detector de tests falsos.
- `git-governance`: Políticas de ramas, Conventional Commits y verificación de DoD.
- `quality-engineering`: Quality gates y control de revisión independiente.
- `orchestrator-continuity`: Clasificación en 5 modos y resolución topológica del DAG.
