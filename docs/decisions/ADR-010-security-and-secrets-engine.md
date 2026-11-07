# ADR-010: Motor de Seguridad, Escaneo de Secretos, Auditoría SPDX y Guarda Fail-Closed

## Estado
Aprobado

## Contexto
En arquitecturas autónomas de desarrollo de software asistido por IA, la delegación de permisos y ejecución de comandos debe estar estrictamente regulada bajo principios de **Zero-Trust** y **Fail-Closed** (info.md § 14, § 20 y Regla Global 6). 
Permitir que agentes de IA ejecuten comandos destructivos (eliminación masiva de tablas/directorios o force-push), comiteen credenciales/claves privadas sin enmascarar, o instalen librerías con licenciamiento comercial/restrictivo representa un riesgo crítico de seguridad, integridad operacional y cumplimiento legal.

## Decisión
1. **Escáner Exhaustivo de Secretos y Redacción Automática (`SecretScanner`):**
   - Implementado en `src/dh_harness/security/scanner.py`.
   - Detecta y neutraliza automáticamente tokens de GitHub (`ghp_`, `github_pat_`), llaves de acceso AWS (`AKIA...`), claves privadas PEM/SSH (`BEGIN PRIVATE KEY`), tokens de Slack y contraseñas en cadenas de conexión.
   - Enmascara cualquier secreto expuesto con `[REDACTED_SECRET]` tanto en reportes visuales como en logs persistidos.
   - Provee escaneo unitario por contenido, por archivo individual y recursivo por directorio (`scan_directory`), ignorando por defecto directorios de dependencias, artefactos y pruebas.

2. **Auditoría Determinista de Licencias SPDX (`LicenseAuditor`):**
   - Implementado en `src/dh_harness/security/licenses.py` siguiendo estrictamente la Regla Global 6.
   - Valida dependencias contra la lista blanca permitida: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `PostgreSQL` y `MS-PL`.
   - Intercepta y bloquea licencias de alto riesgo o comerciales: `Commercial`, `Proprietary`, `GPL`, `AGPL`, `SSPL`, `PolyForm`.
   - Incluye lista de vigilancia crítica (Critical Watchlist) para librerías con cambios históricos a licencias de pago (`FluentAssertions`, `MediatR`, `AutoMapper`, `MassTransit`, `EPPlus`, `Moq`).
   - Audita automáticamente manifiestos `package.json` y dependencias de proyecto.

3. **Guarda de Operaciones Destructivas Fail-Closed (`DestructiveOperationGuard`):**
   - Implementado en `src/dh_harness/security/guard.py`.
   - Filosofía Fail-Closed: Bloqueo inmediato ante cualquier coincidencia sin autorización explícita de supervisión humana (`DestructiveOperationBlockedError`).
   - Reglas activas:
     - SQL: `DROP DATABASE`, `DROP SCHEMA`, `DROP TABLE`, `TRUNCATE TABLE`, y `DELETE FROM` sin cláusula `WHERE`.
     - Git: `git push --force` (`-f`) y `git branch -D/-d` sobre ramas protegidas (`main`, `master`, `release`, `production`).
     - Sistema de archivos: comandos masivos como `rm -rf /` o `del C:\`.

4. **Integración CLI y Distribución Node.js:**
   - Nuevos comandos disponibles mediante `dh-harness security` y `node bin/cli.js security`:
     - `scan [path]`: Auditoría y detección de secretos en código o directorio.
     - `audit-licenses [manifest]`: Verificación de licencias de dependencias.
     - `check-cmd "<cmd>"`: Intercepción de comandos destructivos antes de su invocación.

## Consecuencias
- Cero exposición accidental de credenciales y tokens en repositorios y memoria.
- Cumplimiento irrestricto de licenciamiento 100% libre/código abierto sin sorpresas legales.
- Protección total contra borrado accidental de esquemas, tablas, ramas protegidas o sistemas de archivos.
