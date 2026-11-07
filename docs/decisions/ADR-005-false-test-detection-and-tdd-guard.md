# ADR-005: Detección Estática de Tests Falsos y Guarda de Modificación de Código

## Estado
Aprobado

## Contexto
En sistemas de desarrollo de software asistidos por IA, existe un riesgo recurrente de "falsos positivos de calidad" donde agentes crean pruebas cosméticas (tests vacíos con `pass`, aserciones triviales como `assert True`, `assert 1 == 1` o tests sin ningún `assert`), o modifican el código de producción sin haber demostrado previamente un fallo en una prueba (ciclo RED).

## Decisión
1. **Analizador AST (`FalseTestDetector`):** Implementar en `src/dh_harness/tdd/detector.py` un analizador sintáctico estático utilizando el módulo nativo `ast` de Python. Audita cada función `test_*` y clasifica defectos: `EMPTY_BODY`, `NO_ASSERTION`, `TRIVIAL_ASSERTION_CONSTANT`, `TRIVIAL_ASSERTION_TAUTOLOGY`.
2. **Bóveda de Evidencias Criptográficas (`TDDEvidenceVault`):** Implementar en `src/dh_harness/tdd/evidence.py` un almacén que calcula el digest SHA-256 de las fallas RED legítimas (`exit_code != 0`).
3. **Guarda de Modificación de Código (`CodeModificationGuard`):** Implementar en `src/dh_harness/tdd/guard.py` un control que intercepta y bloquea cualquier edición de archivos en `src/` a menos que exista una evidencia RED comprobada para la tarea activa.
4. **Compuerta de Calidad:** Integrar `TestQualityGate` y `SecretScanningGate` en las compuertas de gobernanza del Harness.

## Consecuencias
- Erradicación completa de pruebas cosméticas o falsas en el repositorio.
- Garantía estricta de que todo código en `src/` responde a un fallo previo demostrado.
- 100% determinismo y cero sobrecarga de librerías externas para el análisis AST.
