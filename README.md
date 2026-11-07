# DH Engineering Harness for Google Antigravity

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-green)](https://nodejs.org/)
[![TDD](https://img.shields.io/badge/TDD-Mandatory%20(Graviton%20AEE)-brightgreen)](#graviton-tdd-methodology)

**DH Engineering Harness** es una plataforma integral de ingeniería de software orientada a agentes para **Google Antigravity**. Proporciona gobernanza determinista, ciclo TDD estricto, orquestación de flujos de trabajo, clasificación inteligente de interacciones, memoria persistente multi-nivel (`.project/` y SQLite) y entrega disciplinada mediante Git/GitHub.

---

## Características Principales

1. **Gobernanza Determinista con Graviton TDD (AEE):**
   - Ejecución de tareas con verificación SQLite de Zero-Trust.
   - Bloqueo inmediato (`🔴 BLOCKED`) si un paso o prueba falla.
   - Prohibido reportar trabajo sin pruebas verificadas (`🟢 COMPLETED`).

2. **Integración con el SDK Oficial de Antigravity:**
   - Soporte nativo de `google.antigravity` (v0.1.23+).
   - Aislamiento mediante patrón Adapter para ejecución segura en read-only y herramientas operativas.

3. **Interaction & Task Classification Engine:**
   - Clasificación determinista en 5 modos: `CONVERSATIONAL`, `INVESTIGATION`, `BUG_FIX`, `DEVELOPMENT`, `COMPLEX_ENGINEERING`.
   - Aplica rigor proporcional: no inicia flujos pesados para preguntas conceptuales ni omite TDD en correcciones de código.

4. **Empaquetado y Distribución Dual:**
   - Instalable globalmente mediante npm: `npm install -g dh-harness` o ejecutable al vuelo con `npx dh-harness`.
   - Disponible como paquete Python para integración en pipelines: `pip install -e .`.

5. **Memoria Persistente de Proyecto (`.project/`):**
   - Reglas permanentes (`rules/`), especificaciones funcionales (`specs/`), tareas (`tasks/`) y decisiones arquitectónicas (`decisions/`).
   - Reanudación de sesiones sin pérdida de contexto.

---

## Arquitectura del Sistema

```mermaid
graph TD
    User([Developer / Agent]) -->|npx dh-harness / npm i -g| NPM_CLI[Node CLI Wrapper - bin/cli.js]
    User -->|python -m dh_harness| PY_CLI[Python Typer CLI]
    
    NPM_CLI -->|Spawns / Forwards| PY_CLI
    
    subgraph "DH Engineering Harness Core (src/dh_harness)"
        PY_CLI --> Orchestrator[Master Orchestrator]
        Orchestrator --> Classifier[Interaction Classifier<br/>Conversational / Investigation / Bugfix / Dev]
        Orchestrator --> TDDEngine[TDD Engine<br/>RED -> GREEN -> REFACTOR -> VERIFY]
        Orchestrator --> GovEngine[Governance & Quality Gates]
        Orchestrator --> MemoryEngine[Memory Engine<br/>SQLite + .project/]
        Orchestrator --> SDKAdapter[Antigravity SDK Adapter<br/>google-antigravity]
    end
    
    subgraph "Graviton TDD Engine (.engine & .project)"
        TDDEngine --> HarnessPy[.engine/harness.py]
        HarnessPy --> Verifiers[.engine/verifiers.py]
        HarnessPy --> AgentEngineDB[(.engine/agent_engine.db)]
        MemoryEngine --> ProjectMemory[.project/<br/>rules/ | specs/ | tasks/ | decisions/]
    end
```

---

## Instalación y Requisitos

### Requisitos Previos
- **Node.js:** `>= 18.0.0`
- **Python:** `>= 3.10`
- **Git**

### Opción A: Instalación vía npm (Recomendada)
```bash
npm install -g dh-harness
# O ejecutar directamente sin instalación global:
npx dh-harness --help
```

### Opción B: Instalación en Entorno Python
```bash
git clone https://github.com/omardelahoz/DH.Harness.git
cd DH.Harness
python -m venv .venv
.\.venv\Scripts\activate   # En Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Guía Rápida de Uso

### 1. Consultar Estado del Proyecto
```bash
dh-harness status
# o con npx:
npx dh-harness status
```

### 2. Clasificar una Solicitud
```bash
dh-harness classify "Corrige el fallo de autenticación cuando el token expira"
# Salida: Modo BUG_FIX, TDD Requerido: SÍ
```

### 3. Ejecutar Controles de Calidad
```bash
dh-harness check
```

### 4. Ciclo Graviton TDD (AEE)
```bash
# Inicializar motor de base de datos
python .engine/harness.py init

# Registrar una nueva tarea
python .engine/harness.py start-task "Título de la Tarea" "Descripción y objetivos"

# Agregar paso con verificador
python .engine/harness.py add-step 1 1 "pytest tests/unit/" "check_python_syntax('archivo.py')"

# Ejecutar paso
python .engine/harness.py run-next 1

# Ver dashboard de verificación
python .engine/harness.py status 1
```

---

## Estructura del Repositorio

```text
DH.Harness/
├── bin/
│   └── cli.js                     # Wrapper ejecutable Node.js
├── .engine/
│   ├── harness.py                 # Motor de ejecución y pasos Graviton
│   ├── verifiers.py               # Biblioteca de verificadores deterministas
│   └── agent_engine.db            # Base de datos SQLite operativa
├── .project/                      # Memoria persistente del proyecto
│   ├── AGENT.md                   # Manual operativo de agentes
│   ├── STATUS.md                  # Dashboard de estado
│   ├── rules/                     # Reglas globales y de desarrollo
│   ├── specs/                     # Especificaciones funcionales
│   └── progress/                  # Registro de avance
├── src/
│   └── dh_harness/
│       ├── core/                  # Contratos y modelos de datos
│       ├── sdk/                   # Adaptador del SDK google.antigravity
│       ├── interaction/           # Clasificador de solicitudes
│       ├── tdd/                   # Motor de control de fases TDD
│       ├── memory/                # Motor de memoria y persistencia
│       └── cli/                   # Interfaz CLI Typer/Rich
├── tests/                         # Suites de pruebas automáticas
├── docs/                          # Arquitectura, ADRs y guías
├── pyproject.toml                 # Configuración de empaquetado Python
└── package.json                   # Configuración de empaquetado npm
```

---

## Licencia

Distribuido bajo la licencia [Apache 2.0](LICENSE). 100% código abierto y libre para uso comercial y comunitario.
