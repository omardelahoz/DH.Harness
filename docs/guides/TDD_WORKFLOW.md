# Guía del Flujo de Trabajo TDD Obligatorio

En DH Engineering Harness, todo cambio de comportamiento ejecutable está gobernado por el ciclo TDD estricto.

```text
REQUIREMENT -> TEST RED -> IMPLEMENT GREEN -> REFACTOR -> VERIFY -> DONE
```

## Paso a Paso

### 1. REQUIREMENT
- Definir con precisión el comportamiento esperado y criterios de aceptación.
- Registrar el requisito en `.project/specs/<id>/REQUIREMENTS.md`.

### 2. TEST RED
- Escribir la prueba unitaria o de integración correspondiente en `tests/`.
- Ejecutar la prueba y comprobar que falla por la razón esperada:
  ```bash
  pytest tests/test_feature.py
  ```
- Registrar la evidencia del fallo en el motor TDD.

### 3. IMPLEMENT GREEN
- Implementar la cantidad mínima de código necesaria en `src/dh_harness/`.
- Reejecutar la prueba hasta confirmar que pasa:
  ```bash
  pytest tests/test_feature.py
  ```

### 4. REFACTOR
- Mejorar estructura, nombres, tipado y documentación sin alterar el comportamiento.
- Comprobar que todas las pruebas permanecen en verde.

### 5. VERIFY
- Ejecutar la suite completa y registrar el paso en Graviton AEE:
  ```bash
  python .engine/harness.py run-next <task_id>
  ```

### 6. DONE
- La tarea solo se marca como `🟢 COMPLETED` cuando SQLite confirma que todos los pasos y verificadores pasaron exitosamente.
