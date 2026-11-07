# Specification: 011 - Advanced Engineering, Hardening & Final Release

## Objetivo
Implementar la Fase 10 del roadmap de `info.md`:
- Motor integral de salud del proyecto (`ProjectHealthEngine`, info.md § 20).
- Suite de endurecimiento e integración end-to-end (`ReleaseHardeningEngine`, info.md § 20, 21).
- Comandos CLI integrados: `node bin/cli.js health` y `node bin/cli.js release manifest`.
- Empaquetado formal de distribución v1.0.0 (npm wrapper y módulo Python).

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts` (`DimensionHealth`, `ProjectHealthReport`, `ReleaseManifest`, `HardeningScenarioResult`, `HardeningSuiteReport`).
- [x] Motor de salud (`ProjectHealthEngine`) con diagnósticos multidimensionales: Git, DoD, tests, licencias, memoria, DAG y arquitectura.
- [x] Puntuación de salud global normalizada (0.0% a 100.0%) con recomendaciones accionables.
- [x] Suite de endurecimiento (`ReleaseHardeningEngine`) validando:
  - Ciclo de vida TDD (falla previa RED antes de GREEN con `CodeModificationGuard`).
  - Detección de pruebas falsas mediante `FalseTestDetector`.
  - Aislamiento y contratos de agentes (prohibición de auto-revisión de PR con `SelfReviewViolationError`).
  - Escaneo AST de secretos y bloqueo de credenciales con `SecretScanner`.
  - Validación de licencias según la lista blanca SPDX (`MIT`, `Apache-2.0`, etc.).
- [x] Comandos CLI `health` y `release manifest` operativos en Typer y wrapper binario Node `bin/cli.js`.
- [x] Decisión de arquitectura formal documentada en `docs/decisions/ADR-013-advanced-engineering-hardening-and-release.md`.
- [x] Suite completa de pruebas automatizadas en `tests/` ejecutándose con 100% de éxito.
