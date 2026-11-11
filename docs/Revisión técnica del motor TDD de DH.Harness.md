# Revisión técnica del motor TDD de DH.Harness

*Análisis del código en `src/dh_harness/tdd/`, `hooks.json`, la CLI, el orquestador y el motor de salud. Basado en lectura directa del código clonado desde github.com/omardelahoz/DH.Harness. No se pudieron ejecutar los tests por conflictos de dependencias en el entorno de análisis.*

## Hallazgo principal: el guard TDD no está conectado a nada

El README afirma que `CodeModificationGuard` bloquea cualquier edición en `src/` si no existe evidencia RED previa. En el código, el guard solo se instancia en `release/hardening.py` (el autotest de release) y en los tests. No lo invoca ninguna otra parte:

- **La CLI.** `tdd --help` anuncia "audit-tests, guard, evidence", pero solo existen los comandos `audit-tests` y `complexity`. No hay comando para registrar evidencia RED ni para consultar el guard.
- **El orquestador.** `master.py` solo lee `classification.tdd_required` y devuelve un mensaje. No invoca el guard ni la bóveda.
- **Los hooks.** `hooks.json` ejecuta `status`, `sec scan src/`, `quality audit` y `continue`. Ninguno pasa por el guard.

Hoy el guard es una clase bien escrita y bien testeada, pero nada impide que un agente edite `src/`. El enforcement sigue siendo cooperativo, aunque se presente como mecánico.

## Problemas dentro del motor TDD

1. **La bóveda vive solo en memoria.** `TDDEvidenceVault` guarda todo en un `dict`, sin SQLite ni disco. Cada ejecución de la CLI empieza vacía y la evidencia no sobrevive entre comandos. El README habla de persistencia, pero no hay `sqlite` en `tdd/`.
2. **El hash no protege nada.** Se calcula sobre `task_id:test_file:exit_code:log:timestamp`, con la hora incluida. No se puede recalcular para verificar, no hay clave ni cadena de hashes, y se guarda junto al log. Es un checksum decorativo, no evidencia criptográfica.
3. **Se confía en lo que el agente declara.** `record_red_evidence` recibe `stdout`, `stderr` y `exit_code` como parámetros. La bóveda no ejecuta el test, así que basta con pasar `exit_code=1` y cualquier texto. Tampoco distingue un fallo de assertion de un `ImportError` o un error de colección, que no son un RED legítimo.
4. **`TDDEngine` y la bóveda son dos sistemas separados.** El engine guarda `red_evidence` como un string sin validar y no usa la bóveda. Hay dos mecanismos de evidencia RED que no se comunican.
5. **El guard permite escribir archivos por extensión.** Todo `.json`, `.yaml`, `.toml` y `.md` queda permitido siempre, y los tests también. Solo se protege código bajo `src/`, por convención de nombres.
6. **El detector de tests falsos es sólido pero limitado.** Detecta cuerpo vacío, ausencia de asserts, `assert True` y `1 == 1`. No detecta `assert x == x`, `assert result is not None`, `assert len(x) >= 0`, tests que mockean la función bajo prueba ni tests que no importan código de producción. Además, un `SyntaxError` devuelve lista vacía (un archivo roto pasa como limpio) y solo analiza Python.
7. **Detalle menor.** `engine.py` usa `Any` sin importarlo. No falla por el `from __future__ import annotations`, pero es un bug latente.

## Sobre el health score de 100%

El score se calcula restando penalizaciones fijas. La parte de TDD solo cuenta tareas `BLOCKED` en SQLite, no evidencia RED ni cobertura. Seguridad y arquitectura dependen de escáneres sencillos. Un proyecto vacío o sin `src/` puntúa 100. El número mide que el harness no detecta problemas con sus propias reglas, no que el proyecto esté sano.

## Lo que sí está bien

- Código limpio, tipado y legible.
- La máquina de estados de `TDDEngine` es correcta.
- El gate de complejidad ciclomática (REFACTOR antes de VERIFY) es una buena idea poco común.
- El detector AST es correcto en lo que cubre.
- La arquitectura está bien separada, así que es fácil de corregir.

## Plan de mejora, por prioridad

1. **Conectar el guard de verdad.** Crear `dh-harness tdd guard <file>` y `tdd red <task> <test>`, y engancharlos a un hook bloqueante PRE-WRITE o a un pre-commit. Sin esto, el resto es teoría.
2. **Que la bóveda ejecute el test.** Recibir el comando, correrlo con `subprocess`, capturar el resultado y rechazar errores de colección o `ImportError`.
3. **Persistir en SQLite** con una cadena de hashes (cada registro incluye el hash del anterior y el hash del árbol de git actual).
4. **Unificar** `TDDEngine` y `TDDEvidenceVault`.
5. **Ampliar el detector** con tautologías de variables, asserts débiles, tests que no importan código de producción y un fallo explícito ante `SyntaxError`.
6. **Corregir el README** para que describa lo que existe hoy, o marcar lo pendiente como roadmap.

## Cómo empezar a colaborar

El paso 1 es el mejor punto de entrada: es acotado, tiene mucho impacto y hace que el proyecto cumpla lo que promete. Una propuesta razonable es un primer PR que incluya los pasos 1 a 3 (comandos de CLI, bóveda que ejecuta y persiste, y sus tests).
