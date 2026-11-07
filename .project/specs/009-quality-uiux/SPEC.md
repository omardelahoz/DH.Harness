# Specification: 009 - Quality Engine, UI/UX Engineering & Lifecycle Hooks

## Objetivo
Implementar la Fase 8 del roadmap de `info.md`:
- Motor de calidad independiente multi-control con estados `PASS`, `WARN`, `FAIL`, `NOT_APPLICABLE` (`QualityEngine`, `QualityReport`, info.md § 15).
- Bloqueo determinista ante cualquier control crítico en `FAIL` independientemente del score global.
- Auditoría UI/UX, accesibilidad WCAG 2.1 AA (contraste, `alt`, `aria-label`) y estados de ciclo de vida de componentes (`UIUXAuditor`, info.md § 16 y Regla 3).
- Motor de Lifecycle Hooks para intercepción de herramientas y registro de archivos modificados (`LifecycleHooksEngine`, info.md § 18).
- Comandos CLI integrados: `node bin/cli.js quality check <task_id>` y `node bin/cli.js uiux audit [path]`.

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts` (`QualityControlStatus`, `QualityReport`, `AccessibilityViolation`, `UIUXAuditReport`, `HookEventType`, `HookExecutionResult`).
- [x] Control crítico `FAIL` bloquea inmediatamente la entrega (`can_deliver = False`).
- [x] Revisión independiente obligatoria (rechazo de auto-evaluación con `IndependentReviewRequiredError`).
- [x] Cálculo determinista de luminancia y contraste WCAG 2.1 AA/AAA (`calculate_contrast_ratio`, `is_wcag_aa_compliant`).
- [x] Detección de imágenes sin `alt` y botones vacíos sin texto ni `aria-label`.
- [x] Validación de presencia de estados obligatorios: loading/skeleton, empty state y error state.
- [x] Intercepción `PreToolUse` bloqueando modificaciones a `src/` sin tarea activa asignada.
- [x] Registro `PostToolUse` de archivos modificados en la sesión.
- [x] Comandos CLI operativos en Typer y binario distribuible `bin/cli.js`.
