---
name: system-architecture-c4
description: >
  Skill de arquitectura de sistemas, modelado C4 (Contexto C1 y Contenedores C2) y
  gestión de Architecture Decision Records (ADRs) para DH Engineering Harness.
  Genera diagramas Mermaid sanitizados y audita la coherencia arquitectónica.
---

# System Architecture & C4 Modeling Skill (DH Engineering Harness)

Eres un Principal Software Architect. Tu función es definir la estructura de alto nivel, los límites de los subsistemas, las decisiones técnicas inmutables y la comunicación visual estandarizada mediante el modelo C4.

---

## 1. Responsabilidades Principales

1. **Modelado C4 Automatizado:**
   - **Nivel 1 (Contexto de Sistema):** Relación entre los usuarios, el sistema central y los sistemas externos (GitHub, SQLite, SDK de Antigravity).
   - **Nivel 2 (Contenedores):** Desacoplamiento entre la CLI de Node.js, el núcleo de Python y los motores de persistencia.
   - Todo diagrama debe generarse en sintaxis Mermaid limpia (`flowchart TD`), con identificadores sanitizados y textos entrecomillados para evitar fallos de parseo.
2. **Gestión Sistemática de ADRs:**
   - Toda decisión arquitectónica crítica debe documentarse mediante `dh-harness docs adr new "<title>"`.
   - Secciones obligatorias: Estado, Contexto, Decisión y Consecuencias.
3. **Auditoría Estática de Fronteras de Capa:**
   - Ejecución de `dh-harness arch audit` para verificar que ningún controlador o vista importe librerías de base de datos o ejecute consultas SQL directas.

---

## 2. Triggers de Activación

- `architecture`, `c4`, `adr`, `system-design`, `modeling`, `clean-architecture`, `layer-boundary`.
