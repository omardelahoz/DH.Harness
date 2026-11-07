# Specification: 005 - Memory Engine, Session Recovery & Checkpoints

## Objetivo
Implementar la Fase 4 del roadmap de `info.md`:
- Persistencia de memoria estructurada multinivel (`GLOBAL`, `PROJECT`, `TASK`, `SESSION`, `KNOWLEDGE`).
- Prevención estricta de fuga de secretos en memoria (`SecretDetectedError`).
- Puntos de control criptográficos con checksums SHA-256 (`CheckpointManager`, `CorruptedCheckpointError`).
- Detección de umbrales y sintetizador de compact digest para evitar truncamiento de contexto (`ContextTruncationGuard`).
- Interfaz CLI (`dh-harness memory status`, `checkpoint`, `recover`).

## Requisitos Verificados
- [x] Contratos tipados: `MemoryLevel`, `SessionCheckpoint`, `KnowledgeItem` en `dh_harness.core.contracts`.
- [x] Motor multinivel con almacenamiento SQLite y búsqueda de conocimiento en `src/dh_harness/memory/levels.py`.
- [x] Filtro anti-secretos (`scan_for_secrets`) para tokens de GitHub, llaves privadas RSA y credenciales.
- [x] Manejo de checkpoints con verificación de checksums SHA-256 en `src/dh_harness/memory/checkpoints.py`.
- [x] Detección de corrupción y alteración de checkpoints (`CorruptedCheckpointError`).
- [x] Síntesis de compact digest para protección de contexto en `src/dh_harness/memory/truncation.py`.
- [x] Comandos CLI operativos en Node: `node bin/cli.js memory status`, `checkpoint`, `recover`.
