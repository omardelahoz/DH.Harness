# ADR-011: Quality Engine, Ingeniería UI/UX y Gobernanza de Lifecycle Hooks

## Estado
Aprobado

## Contexto
En sistemas autónomos de ingeniería de software basados en agentes de IA, asegurar la calidad del producto no se limita a pasar pruebas unitarias funcionales (info.md § 15, § 16 y § 18).
Es imperativo contar con:
1. Una evaluación de calidad multi-control verdaderamente independiente (Quality Engine) donde el autor no pueda aprobar su propio trabajo y donde un fallo crítico en seguridad, compilación o DoD bloquee de forma irreversible la entrega.
2. Una validación de la experiencia de usuario y accesibilidad (UI/UX Engineering) que verifique la ausencia de elementos inaccesibles (sin `alt`, botones vacíos sin `aria-label`, contrastes insuficientes) y la presencia obligatoria de estados de interfaz (loading/skeletons, empty states, error boundaries) según la Regla Global 3.
3. Un motor de intercepción de ciclo de vida (Lifecycle Hooks Engine) que supervise las acciones del agente antes (`PreToolUse`) y después (`PostToolUse`) de modificar código fuente.

## Decisión
1. **Quality Engine con Verificación Independiente (`QualityEngine`):**
   - Implementado en `src/dh_harness/quality/engine.py`.
   - Evalúa hasta 15 controles divididos en críticos (`Compilation`, `Unit Tests`, `Security Scanning`, `Dependency Audit`, `Definition of Done`, `Accessibility`) y estándar (`Static Analysis`, `Formatting`, `Lint`, `Performance`, etc.).
   - Aplica la regla estricta: un resultado `FAIL` en cualquier control crítico bloquea inmediatamente la entrega (`can_deliver = False`), sin que un puntaje general alto compense la deficiencia.
   - Lanza `IndependentReviewRequiredError` si se intenta auto-evaluar un entregable.

2. **Auditoría UI/UX y Cumplimiento WCAG 2.1 (`UIUXAuditor`):**
   - Implementado en `src/dh_harness/uiux/engine.py`.
   - Inspección estática de plantillas y componentes HTML/JSX/Vue.
   - Detecta y sanciona:
     - Imágenes sin atributo `alt` (`A11Y_IMG_ALT`, impacto SERIOUS).
     - Botones vacíos sin texto legible ni `aria-label` (`A11Y_EMPTY_BUTTON`, impacto CRITICAL).
     - Ausencia de estados de interfaz obligatorios (loading/skeleton, empty state, error state).
   - Cálculo de luminancia relativa y ratio de contraste de color bajo la especificación WCAG 2.1 AA (mínimo 4.5:1 para texto normal, 3:1 para texto grande).

3. **Motor de Lifecycle Hooks (`LifecycleHooksEngine`):**
   - Implementado en `src/dh_harness/hooks/engine.py`.
   - Soporta eventos: `SessionStart`, `PreInvocation`, `PreToolUse`, `PostToolUse`, `PostInvocation`, `Stop`.
   - Interceptor `PreToolUse`: Bloquea modificaciones sobre código fuente de producción (`src/`) si no existe una tarea activa asignada.
   - Interceptor `PostToolUse`: Registra de forma transparente los archivos modificados para auditoría y trazabilidad.

4. **Integración CLI y Distribución Node.js:**
   - Nuevos comandos Typer y Node `bin/cli.js`:
     - `dh-harness quality check <task_id>`: Auditoría completa de calidad con evaluador independiente.
     - `dh-harness uiux audit [path]`: Auditoría de componentes web y accesibilidad.

## Consecuencias
- 100% de cumplimiento del principio de revisión independiente en la entrega de artefactos.
- Detección temprana y bloqueo de interfaces inaccesibles o con pantallas rotas/incompletas.
- Trazabilidad y supervisión determinista de las herramientas ejecutadas por cada agente en el workspace.
