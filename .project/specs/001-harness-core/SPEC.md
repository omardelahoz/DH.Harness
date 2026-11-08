# Specification: 001 - DH Engineering Harness Core Foundation

## Objetivo
Establecer los cimientos del DH Engineering Harness para Antigravity con:
- Integración del SDK oficial de Antigravity mediante Adapter Pattern.
- Motor de clasificación de solicitudes (Interaction Classifier).
- Motor de control TDD (RED/GREEN/REFACTOR/VERIFY).
- Empaquetado dual: CLI de Node para `npm i -g dh-harness` y paquete Python `dh_harness`.
- Soporte de ejecución determinista y calidad verificada con DH Engineering Harness.

## Alcance
- `src/dh_harness/core/contracts.py`: Modelos Pydantic para clasificaciones, fases TDD y tareas.
- `src/dh_harness/sdk/adapter.py`: Adaptador desacoplado para el SDK `google.antigravity`.
- `src/dh_harness/interaction/classifier.py`: Clasificador de 5 modos de interacción.
- `src/dh_harness/tdd/engine.py`: Motor de control y enforcement TDD.
- `src/dh_harness/cli/main.py`: CLI de Python con comandos principales.
- `package.json` + `bin/cli.js`: Wrapper de Node para distribución e invocación vía npm/npx.
- `pyproject.toml`: Configuración de empaquetado Python.
- Suite de pruebas unitarias exhaustivas con pytest.

## Criterios de Aceptación
- [ ] Entorno virtual creado con `google-antigravity` y dependencias instaladas.
- [ ] Suite de pruebas pasando al 100% en pytest.
- [ ] Wrapper Node `bin/cli.js` responde correctamente a `node bin/cli.js --help` y `status`.
- [ ] Pasos AEE registrados en SQLite y ejecutados con estado `🟢 COMPLETED`.
