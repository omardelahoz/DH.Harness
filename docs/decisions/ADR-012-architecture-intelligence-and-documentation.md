# ADR-012: Inteligencia Arquitectónica, Gestión Automatizada de ADRs y Diagramas C4

## Estado
Aprobado

## Contexto
A medida que el harness de ingeniería evoluciona con múltiples agentes autónomos, la documentación técnica y las decisiones de diseño arquitectónico no pueden depender de procesos manuales propensos a desincronizarse del código fuente (info.md § 19 y Regla Global 4).
Es indispensable:
1. Centralizar y automatizar el registro, numeración, validación e indexación de decisiones técnicas de arquitectura mediante Registros de Decisión Arquitectónica (ADRs).
2. Auditar deterministamente las fronteras de Clean Architecture, prohibiendo expresamente el bypass de capas (ej. Controllers o vistas accediendo a base de datos o ejecutando consultas SQL directas en lugar de interactuar con Casos de Uso y Repositorios).
3. Generar dinámicamente modelos y diagramas de arquitectura basados en el modelo C4 (Contexto, Contenedor, Componente) en formato Mermaid nativo compatible con la interfaz del IDE y la documentación Markdown.

## Decisión
1. **Gestor de Registros de Decisión Arquitectónica (`ADRManager`):**
   - Implementado en `src/dh_harness/docs/engine.py`.
   - Indexa, analiza y secuencia automáticamente los documentos `ADR-xxx-*.md` en `docs/decisions/`.
   - Genera nuevas decisiones con numeración incremental automática, slug amigable y estructura estandarizada (Título, Estado, Contexto, Decisión y Consecuencias).
   - Valida la integridad estructural de cualquier documento ADR para garantizar uniformidad en el historial del proyecto.

2. **Auditor de Inteligencia Arquitectónica y Fronteras de Capas (`ArchitectureAuditor`):**
   - Implementado en `src/dh_harness/architecture/intelligence.py`.
   - Aplica de forma determinista la Regla Global 4 de Clean Architecture:
     - Detecta e intercepta importaciones directas de módulos de base de datos (`sqlite3`, `dapper`, `DbContext`, `SqlConnection`, `DbSet`) en la capa de controladores o APIs (`DIRECT_DB_ACCESS_IN_CONTROLLER`).
     - Detecta e intercepta cadenas o literales con consultas SQL en Controladores (`SQL_IN_CONTROLLER`).
     - Genera reportes de salud arquitectónica (`check_architecture_health`) consolidando violaciones de capas y cobertura documental.

3. **Generador de Modelos y Diagramas C4 en Mermaid (`C4DiagramGenerator`):**
   - Implementado en `src/dh_harness/docs/c4.py`.
   - Soporta la generación de:
     - Diagramas de Contexto de Sistema (Nivel 1): Relación entre usuarios, el sistema central y sistemas externos (GitHub, SQLite, SDK de Antigravity).
     - Diagramas de Contenedor (Nivel 2): Arquitectura desacoplada entre CLI Launcher de Node, Núcleo de Python y Base de Datos persistente.
   - Genera sintaxis Mermaid sanitizada (`flowchart TD`) y bloques Markdown listos para ser renderizados en el visualizador del IDE.

4. **Integración CLI y Distribución Node.js:**
   - Nuevos comandos integrados en Typer y el wrapper ejecutable `bin/cli.js`:
     - `dh-harness docs adr list`: Visualización tabular de todas las decisiones técnicas tomadas.
     - `dh-harness docs adr new "<title>"`: Creación estructurada de nuevos ADRs.
     - `dh-harness arch audit [src_dir]`: Auditoría determinista de Clean Architecture y límites de capas.

## Consecuencias
- Cero desincronización entre el código implementado y las decisiones de diseño documentadas.
- Imposibilidad de degradar la arquitectura limpia mediante atajos o anti-patrones en capas de presentación.
- Visualización gráfica estandarizada de la topología del sistema accesible para ingenieros y agentes.
