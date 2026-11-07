# Specification: 008 - Security & Secrets Engine

## Objetivo
Implementar la Fase 7 del roadmap de `info.md`:
- Escáner exhaustivo de credenciales, llaves API, tokens y claves privadas (`SecretScanner`, `SecretFinding`).
- Redacción obligatoria con `[REDACTED_SECRET]` en terminal, reportes y memoria persistente.
- Auditor de licenciamiento de dependencias contra lista blanca SPDX (`LicenseAuditor`, `LicenseAuditFinding`, Regla Global 6).
- Lista de vigilancia crítica de dependencias (Critical Watchlist) para paquetes con cambio a modelos de pago.
- Guarda Fail-Closed para interceptar comandos destructivos de SQL, Git y sistema de archivos (`DestructiveOperationGuard`, `DestructiveOperationBlockedError`).
- Comandos CLI integrados: `node bin/cli.js security scan`, `audit-licenses`, `check-cmd`.

## Requisitos Verificados
- [x] Contratos de seguridad tipados en `dh_harness.core.contracts` (`SecretFinding`, `LicenseAuditFinding`, `DestructiveOpCheckResult`, `SecuritySeverity`).
- [x] Detección de GitHub tokens, AWS keys, Slack tokens, claves privadas RSA/EC/SSH y contraseñas en connection strings.
- [x] Enmascaramiento inmediato de secretos con `[REDACTED_SECRET]`.
- [x] Validación determinista de licencias SPDX: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `PostgreSQL`, `MS-PL`.
- [x] Intercepción y bloqueo de licencias restrictivas o comerciales (`Commercial`, `GPL`, `AGPL`, `SSPL`, `PolyForm`).
- [x] Detección de versiones restringidas en Critical Watchlist (`FluentAssertions`, `MediatR`, `AutoMapper`, `MassTransit`, `EPPlus`, `Moq`).
- [x] Bloqueo inmediato de `DROP DATABASE`, `DROP TABLE`, `TRUNCATE TABLE`, `DELETE FROM` sin `WHERE`.
- [x] Bloqueo inmediato de `git push --force` y `git branch -D` sobre ramas protegidas.
- [x] Bloqueo de comandos destructivos masivos de filesystem (`rm -rf /`, `del C:\`).
- [x] Comandos CLI operativos en Typer y binario distribuible `bin/cli.js`.
