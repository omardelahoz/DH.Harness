# ADR-007: Motor de Memoria Multinivel, Recuperación de Sesión y Protección contra Truncamiento

## Estado
Aprobado

## Contexto
Los modelos y agentes en plataformas como Google Antigravity tienen límites de ventana de contexto o pueden experimentar interrupciones de sesión (cierres de terminal, reinicios, caídas de red). Depender exclusivamente del contexto inmediato en memoria RAM de la sesión genera pérdida de decisiones técnicas, tareas pendientes y estado del proyecto. Asimismo, la memoria persistente no debe almacenar jamás secretos, credenciales o tokens privados (info.md § 8.3).

## Decisión
1. **Memoria Multinivel (`MultiLevelMemory`):**
   - Implementar en `src/dh_harness/memory/levels.py` la gestión estructurada de los 5 niveles de memoria definidos en `info.md`: `GLOBAL` (principios y políticas), `PROJECT` (arquitectura, stack y estado), `TASK` (objetivos y estado de tarea), `SESSION` (actividades recientes) y `KNOWLEDGE` (catálogo indexado de soluciones y bugs conocidos con tags y categorías).
   - Base de datos relacional local SQLite (`.project/memory/memory.db`) con soporte para inserciones idempotentes (`ON CONFLICT`).
2. **Filtro Anti-Secretos Obligatorio:**
   - La función `scan_for_secrets` intercepta y escanea cualquier contenido previo a ser persistido.
   - Si se detecta un token (`ghp_`, `gho_`, `github_pat_`), llave privada RSA o credenciales AWS/Slack, lanza `SecretDetectedError`, impidiendo que los secretos lleguen a disco o al repositorio.
3. **Puntos de Control Criptográficos y Recuperación (`CheckpointManager`):**
   - Implementar en `src/dh_harness/memory/checkpoints.py` la creación de snapshots de sesión (`SessionCheckpoint`) con cálculo de hash SHA-256.
   - Al restaurar un punto de control (`restore_checkpoint`), se valida la integridad criptográfica; cualquier alteración de bytes detiene la rehidratación con `CorruptedCheckpointError`.
   - Puntero automático `latest.json` para rápida recuperación tras interrupciones.
4. **Protección contra Truncamiento de Contexto (`ContextTruncationGuard`):**
   - Implementar en `src/dh_harness/memory/truncation.py` la detección de umbrales de saturación de tokens y síntesis de un resumen ultracompacto en Markdown (`generate_compact_digest`).
   - Preserva el 100% de la semántica de la tarea, rama Git, decisiones y próximos pasos ocupando una fracción de tokens.
5. **Comandos CLI Operativos:**
   - Exponer en Typer y Node `bin/cli.js`:
     - `dh-harness memory status`: Dashboard de almacenamiento y puntos de control.
     - `dh-harness memory checkpoint`: Generación manual instantánea de checkpoint.
     - `dh-harness memory recover`: Recuperación y visualización del compact digest del último checkpoint.

## Consecuencias
- Continuidad garantizada entre sesiones de Antigravity sin depender de la ventana de contexto.
- Cero fugas de credenciales en la memoria persistente.
- Detección determinista de corrupción o manipulación de checkpoints de sesión.
