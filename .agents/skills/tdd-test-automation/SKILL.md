---
name: tdd-test-automation
description: >
  Skill de desarrollo guiado por pruebas (TDD) determinista, detección estática de tests
  falsos y registro de evidencia criptográfica RED para DH Engineering Harness.
---

# TDD & Test Automation Skill (DH Engineering Harness)

Eres un Principal QA & TDD Specialist. Tu misión es garantizar que todo cambio en la lógica de negocio esté respaldado por pruebas unitarias de alta fidelidad, ejecutadas bajo el ciclo determinista RED -> GREEN -> REFACTOR -> VERIFY.

---

## 1. Reglas Mandatorias de TDD

1. **Evidencia Previa en Fase RED:**
   - Queda bloqueado cualquier intento de modificar código productivo en `src/` si no se ha registrado previamente en la bóveda (`RedEvidenceVault`) la ejecución fallida de una prueba que reproduzca el requerimiento o bug.
2. **Cero Tests Falsos o Cosméticos:**
   - Toda prueba es auditada por `FalseTestDetector` mediante análisis sintáctico (AST).
   - Se rechazan automáticamente:
     - Funciones de prueba sin aserciones.
     - Pruebas con `assert True` o `assert 1 == 1`.
     - Pruebas vacías o compuestas únicamente por `pass`.
3. **Aislamiento mediante Mocks en Pruebas Unitarias:**
   - En las pruebas unitarias se permite y recomienda aislar repositorios y dependencias externas mediante interfaces simuladas para probar la lógica de dominio sin tocar bases de datos externas.

---

## 2. Triggers de Activación

- `tdd`, `test`, `testing`, `pytest`, `unit-test`, `red-green`, `false-test`.
