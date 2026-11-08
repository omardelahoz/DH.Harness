# Referencia de Comandos CLI

El CLI de DH Engineering Harness puede ejecutarse tanto vía Node (`npx dh-harness` / `node bin/cli.js`) como directamente mediante Python (`python -m dh_harness.cli.main` o el comando `dh-harness`).

---

## Comandos Principales

### `status`
Muestra el panel de salud del proyecto, el estado del SDK de Antigravity, el resumen de tareas en SQLite y la memoria `.project/`.
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

### `health`
Evalúa los 6 pilares de salud del proyecto (Seguridad, TDD, Arquitectura, Git, Calidad y UI/UX). Umbral mínimo para producción: 100%.
```bash
npx dh-harness health
```

---

## Comandos de Módulos Especializados (`dh-harness`)

- `dh-harness tdd audit-tests`: Audita que no existan pruebas falsas o cosméticas con el detector AST.
- `dh-harness sec scan [path]`: Escanea el código en busca de secretos o credenciales expuestas.
- `dh-harness arch audit [src]`: Audita deterministamente las fronteras de Clean Architecture.
- `dh-harness git check-dod <id>`: Valida que la tarea cumpla con todos los criterios de Definition of Done.
- `dh-harness skills list`: Consulta los 18 skills de ingeniería integrados en el arnés.
- `dh-harness agents list`: Consulta el catálogo de 14 agentes especializados y sus permisos.
