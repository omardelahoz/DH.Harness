# Requirements: 001 - DH Engineering Harness Core

- **REQ-001:** El sistema debe proveer modelos de datos fuertemente tipados (`pydantic`) para representar los modos de interacción (`CONVERSATIONAL`, `INVESTIGATION`, `BUG_FIX`, `DEVELOPMENT`, `COMPLEX_ENGINEERING`) y las fases de TDD.
- **REQ-002:** El adaptador del SDK debe encapsular `google.antigravity`, permitiendo instanciar agentes con configuración segura y manejo de excepciones cuando el runtime nativo no esté presente.
- **REQ-003:** El clasificador de interacciones debe determinar el modo de operación basado en el texto de la solicitud, asociando el nivel de rigor apropiado.
- **REQ-004:** El motor TDD debe validar las transiciones de fases y bloquear la implementación de cambios de código si no existe una prueba en fallo (RED).
- **REQ-005:** El paquete debe proveer un CLI ejecutable en Node.js (`bin/cli.js`) para ser distribuido e instalado con npm, reenviando comandos al motor Python.
- **REQ-006:** Toda la ejecución de inicialización y verificación debe ser trazable mediante el motor SQLite de Graviton AEE (`.engine/harness.py`).
