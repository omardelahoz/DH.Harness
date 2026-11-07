# DH Engineering Harness - Architecture Overview

## 1. Visión y Propósito

**DH Engineering Harness** es una plataforma de ingeniería de software orientada a agentes para **Google Antigravity**, concebida para dotar a los modelos de IA de una capa determinista de gobernanza, control TDD estricto, gestión de memoria persistente, clasificación de solicitudes y orquestación de workflows.

---

## 2. Diagrama de Contenedores y Componentes (C4)

```mermaid
graph TD
    subgraph "Capas de Entrada & Distribución"
        Dev[Desarrollador / Agente] -->|npx dh-harness| NodeCLI[Node.js CLI Wrapper<br/>bin/cli.js]
        Dev -->|python -m dh_harness| PyCLI[Python CLI Interface<br/>src/dh_harness/cli/main.py]
        NodeCLI -->|Spawns / stdio forwarding| PyCLI
    end

    subgraph "DH Harness Core (src/dh_harness)"
        PyCLI --> Classifier[Interaction Classifier<br/>src/dh_harness/interaction/classifier.py]
        PyCLI --> TDDEngine[TDD Engine<br/>src/dh_harness/tdd/engine.py]
        PyCLI --> MemoryEng[Memory Engine<br/>src/dh_harness/memory/engine.py]
        PyCLI --> SDKAdapter[Antigravity SDK Adapter<br/>src/dh_harness/sdk/adapter.py]
    end

    subgraph "Graviton TDD Engine (.engine & .project)"
        TDDEngine --> HarnessPy[.engine/harness.py]
        HarnessPy --> Verifiers[.engine/verifiers.py]
        HarnessPy --> DB[(.engine/agent_engine.db)]
        MemoryEng --> MarkdownMemory[.project/<br/>rules/ | specs/ | tasks/ | decisions/]
    end

    subgraph "Runtime Externo"
        SDKAdapter --> GoogleAntigravitySDK[google.antigravity Runtime]
    end
```

---

## 3. Principios de Separación de Responsabilidades

1. **Google Antigravity:** Runtime de agentes, modelos de IA y herramientas nativas.
2. **DH Engineering Harness:** Gobernanza, clasificación, control TDD, orquestación y auditoría.
3. **Graviton AEE:** Motor de ejecución determinista local basado en SQLite y Zero-Trust.
4. **Memoria Persistente (`.project/`):** Contexto estructurado en Markdown para trazabilidad humana y de agentes.
