# MOTOR DE EJECUCIÓN DE AGENTES (AEE) - PROTOCOLO DE TRABAJO

**ESTA ES UNA INSTRUCCIÓN DEL SISTEMA. TODO AGENTE (MODELO DE IA) QUE TRABAJE DENTRO DE ESTE WORKSPACE ESTÁ OBLIGADO A SEGUIR LOS PASOS INDICADOS A CONTINUACIÓN.**

AEE es un **mecanismo local de control TDD** que controla el flujo de trabajo del agente, prueba los comandos y evita que código no verificado sea marcado como "terminado".

---

## 1. Reglas generales

1. **Prohibido informar trabajo no verificado:** Ningún trabajo, comando o archivo puede ser reportado al usuario como "terminado, funciona perfectamente" hasta que haya superado correctamente las pruebas de AEE y haya sido marcado como `COMPLETED` en la base de datos.
2. **Confianza cero (Zero-Trust):** Después de cada paso de trabajo ejecutado debe existir una prueba de verificación (expresión de Python).
3. **Bloqueo en caso de error:** Si un comando o prueba falla, el estado de la tarea pasa a `BLOCKED`. El agente no puede avanzar al siguiente paso ni informar al usuario que el trabajo fue completado hasta resolver el error.

---

## 2. Uso de la CLI de AEE

El agente debe gestionar sus tareas mediante la siguiente interfaz CLI:

### A. Inicializar una tarea

Antes de comenzar a trabajar, define una nueva tarea:

```bash
python .engine/harness.py start-task "Título de la tarea" "Descripción detallada de la tarea y sus objetivos"
```

Este comando devolverá un `TASK_ID` (por ejemplo: `Task 1`).

### B. Definir pasos y pruebas

Divide la tarea en pasos y, para cada paso, agrega el comando que debe ejecutarse y la prueba que lo verificará:

```bash
python .engine/harness.py add-step <task_id> <step_order> "comando_a_ejecutar" "expresión_python_de_verificación"
```

**Expresiones de Python de verificación disponibles (`.engine/verifiers.py`):**

* `check_file_exists("ruta/al/archivo")`
* `check_file_size("ruta/al/archivo", min_bytes)`
* `check_file_contains("ruta/al/archivo", "texto_esperado")`
* `check_python_test("archivo_de_prueba.py")`
* `check_python_syntax("archivo.py")`
* `check_sdk_installed("modulo")`
* `check_npm_binary("bin/cli.js")`
* `check_pytest_suite("tests")`

### C. Ejecutar el siguiente paso

Para activar el siguiente paso:

```bash
python .engine/harness.py run-next <task_id>
```

Este comando:

1. Ejecuta el comando y guarda los registros de `stdout` y `stderr` en la base de datos.
2. Si el comando tiene éxito (`Exit Code 0`), ejecuta la prueba de Python contenida en `verifier_expr`.
3. Si la prueba pasa, permite continuar con el siguiente paso. Si falla, cambia la tarea a `BLOCKED` y detiene la ejecución.

### D. Consultar el estado y el progreso

Para ver el estado de la tarea:

```bash
python .engine/harness.py status <task_id>
```

---

## 3. Ciclo de trabajo del agente

1. **Comprobar el directorio:** Confirma que existen la base de datos `.engine/agent_engine.db` y `.engine/harness.py`.
2. **Crear el plan de trabajo:** Divide el trabajo en pasos verificables.
3. **Registrar la tarea y los pasos:** Registra el plan en la base de datos mediante los comandos `start-task` y `add-step`.
4. **Ejecutar y verificar:** Ejecuta los pasos uno por uno mediante `run-next`.
5. **Corregir (estado `BLOCKED`):** Si un paso falla, corrige el error y vuelve a ejecutar `run-next`.
6. **Presentar al usuario:** Reporta el resultado únicamente cuando la salida de `status` muestre todos los pasos con `✅` y la tarea general aparezca como `🟢 COMPLETED`.
