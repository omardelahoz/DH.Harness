# ADR-013: Ingeniería Avanzada, Hardening End-to-End, Diagnóstico de Salud y Manifiesto de Release v1.0.0

## Estado
Aprobado

## Contexto
Con la finalización de las fases fundamentales y de soporte (Fases 0 a 9) de DH.Harness para Google Antigravity, se requiere una fase de culminación, endurecimiento y cierre que consolide todos los motores del sistema en un flujo unificado y verifique la robustez de extremo a extremo antes de la liberación final (info.md § 20, 21 y Regla Global).
Específicamente se necesita:
1. Un motor de salud integral del proyecto (`ProjectHealthEngine`) que audite deterministamente Git, DoD, tests, licencias, memoria, DAG y arquitectura, produciendo un puntaje ponderado global (0 a 100%) y recomendando acciones de remediación.
2. Un harness de pruebas de endurecimiento e2e (`ReleaseHardeningEngine`) que simule el ciclo de vida completo de un requerimiento (flujo TDD RED-GREEN, validación de delegación de agentes con prevención de auto-revisión, escaneo de secretos y validación de licencias SPDX permisivas).
3. La generación automatizada del manifiesto de release (`release manifest`) y empaquetado de producción v1.0.0 tanto para el paquete npm (`bin/cli.js`) como para el módulo Python (`pyproject.toml`).

## Decisión
1. **Motor de Diagnóstico de Salud Integral (`ProjectHealthEngine`):**
   - Implementado en `src/dh_harness/health/engine.py`.
   - Evalúa múltiples dimensiones deterministas: Git y DoD (`GitGovernanceManager`), estado de la suite de pruebas TDD, auditoría de licencias SPDX (`LicenseAuditor`), consistencia de memoria persistente (`MemoryEngine`), estado del grafo de tareas (`DependencyGraph`) e integridad de Clean Architecture (`ArchitectureAuditor`).
   - Calcula un puntaje de salud normalizado (0.0% a 100.0%) y genera diagnósticos detallados por dimensión.

2. **Harness de Endurecimiento e Integración End-to-End (`ReleaseHardeningEngine`):**
   - Implementado en `src/dh_harness/release/hardening.py`.
   - Ejecuta escenarios de validación cruzada:
     - Ciclo TDD determinista: Validación de RED antes de GREEN mediante `CodeModificationGuard`.
     - Detección de pruebas falsas o tautológicas mediante `FalseTestDetector`.
     - Gobernanza de agentes: Aislamiento de roles e intercepción de auto-revisión en pull requests mediante `SelfReviewViolationError`.
     - Auditoría de seguridad: Detección y bloqueo de tokens/secretos mediante `SecretScanner`.
     - Validación de licencias: Verificación determinista de dependencias contra la lista blanca SPDX (`MIT`, `Apache-2.0`, etc.).

3. **Generación del Manifiesto de Release y Comandos CLI:**
   - Comandos expuestos en Typer y el wrapper de Node.js (`bin/cli.js`):
     - `dh-harness health`: Diagnóstico visual del estado de salud del proyecto.
     - `dh-harness release manifest`: Manifiesto formal de release v1.0.0 con metadatos del paquete, hashes de integridad, módulos activos y resumen de cumplimiento.
   - Distribución dual validada y lista para despliegue en entornos de ingeniería de Google Antigravity.

## Consecuencias
- Certificación formal de preparación para producción con cero falsos positivos y trazabilidad completa.
- Verificación exhaustiva de todas las garantías de seguridad, licencias, arquitectura y calidad del sistema.
- Disponibilidad inmediata de la herramienta como CLI binario universal Node/Python.
