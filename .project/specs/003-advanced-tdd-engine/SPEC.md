# Specification: 003 - Mandatory TDD Advanced Engine & False Test Detector

## Objetivo
Implementar la Fase 2 del roadmap de `info.md`:
- Detección de tests falsos mediante análisis estático AST (`FalseTestDetector`).
- Bóveda criptográfica de evidencias de fallo RED con SHA-256 (`TDDEvidenceVault`).
- Guarda de modificación de código en tiempo de ejecución (`CodeModificationGuard`).
- Compuertas de calidad de secretos (`SecretScanningGate`) y calidad de tests (`TestQualityGate`).

## Requisitos Verificados
- [x] Detecta funciones de test vacías (`EMPTY_BODY`).
- [x] Detecta funciones de test sin aserciones (`NO_ASSERTION`).
- [x] Detecta aserciones constantes y tautológicas (`assert True`, `assert 1 == 1`).
- [x] Permite aserciones válidas y capturas de excepciones con `pytest.raises`.
- [x] Bloquea modificaciones en `src/` si no existe evidencia RED previa registrada.
- [x] Escanea y detecta tokens de GitHub, llaves privadas y credenciales expuestas.
- [x] Comando CLI operativo: `dh-harness tdd audit-tests` y `node bin/cli.js tdd audit-tests`.
