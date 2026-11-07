# Referencia de Comandos CLI

El CLI de DH Engineering Harness puede ejecutarse tanto vía Node (`npx dh-harness` / `node bin/cli.js`) como directamente mediante Python (`python -m dh_harness.cli.main` o el comando `dh-harness`).

---

## Comandos Principales

### `status`
Muestra el panel de salud del proyecto, el estado del SDK de Antigravity, el resumen de tareas en SQLite de Graviton AEE y la memoria `.project/`.
```bash
npx dh-harness status
```

### `classify <prompt>`
Analiza un texto o solicitud y determina el modo de interacción canónico (`CONVERSATIONAL`, `INVESTIGATION`, `BUG_FIX`, `DEVELOPMENT`, `COMPLEX_ENGINEERING`), indicando si requiere TDD obligatorio y el workflow sugerido.
```bash
npx dh-harness classify "Corrige el error en el procesamiento de pagos"
```

### `check`
Ejecuta las puertas de calidad (quality gates) del proyecto, ejecutando la suite completa de pruebas unitarias y de integración.
```bash
npx dh-harness check
```

---

## Comandos Graviton AEE (`.engine/harness.py`)

- `python .engine/harness.py init`: Inicializa la base de datos SQLite `agent_engine.db`.
- `python .engine/harness.py start-task <title> <desc>`: Registra una nueva tarea.
- `python .engine/harness.py add-step <task_id> <orden> <comando> <expresión>`: Registra un paso con verificador determinista.
- `python .engine/harness.py update-step <task_id> <orden> <comando> <expresión>`: Actualiza un paso y resetea su estado.
- `python .engine/harness.py run-next <task_id>`: Ejecuta el siguiente paso pendiente y evalúa el verificador.
- `python .engine/harness.py status <task_id>`: Muestra el estado detallado de pasos y verificaciones.
