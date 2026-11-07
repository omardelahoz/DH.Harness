# Specification: 010 - Architecture Intelligence & Documentation Engine

## Objetivo
Implementar la Fase 9 del roadmap de `info.md`:
- Gestor y validador incremental de registros de decisiones arquitectónicas (`ADRManager`, info.md § 19).
- Auditor estático de fronteras de Clean Architecture y anti-bypass de capas (`ArchitectureAuditor`, Regla Global 4).
- Generador de diagramas y modelos C4 en Mermaid (`C4DiagramGenerator`, Nivel 1 Contexto y Nivel 2 Contenedor).
- Comandos CLI integrados: `node bin/cli.js docs adr list`, `docs adr new`, y `node bin/cli.js arch audit [src]`.

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts` (`ADRStatus`, `ArchitectureDecisionRecord`, `CleanArchViolation`, `C4DiagramType`, `C4DiagramDefinition`, `ArchitectureHealthReport`).
- [x] Descubrimiento, listado y numeración incremental automática de ADRs en `docs/decisions/`.
- [x] Creación de ADRs estructurados con títulos amigables y slugs normalizados.
- [x] Validación obligatoria de secciones estándar (Título, Estado, Contexto, Decisión, Consecuencias).
- [x] Detección de importaciones prohibidas de bases de datos en capas de presentación / controladores (`DIRECT_DB_ACCESS_IN_CONTROLLER`).
- [x] Detección de consultas SQL embebidas en controladores (`SQL_IN_CONTROLLER`).
- [x] Generación de diagramas Mermaid C4 sintácticamente válidos (`flowchart TD`) para Contexto y Contenedores.
- [x] Comandos CLI operativos en Typer y binario distribuible `bin/cli.js`.
