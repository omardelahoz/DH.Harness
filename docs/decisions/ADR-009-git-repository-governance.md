# ADR-009: Gobernanza de Git, Políticas de Ramas y Definition of Done (DoD)

## Estado
Aprobado

## Contexto
En entornos asistidos por agentes de software, permitir que agentes o desarrolladores realicen commits directamente sobre ramas productivas (`main`, `master`), omitan convenciones de nombres o marquen tareas como completadas sin pruebas verificadas o revisiones independientes introduce regresiones y deuda técnica silenciosa (info.md § 11 y § 22).

## Decisión
1. **Diagnóstico Determinista del Repositorio (`RepoDiagnostics`):**
   - Implementar `src/dh_harness/git/manager.py` para identificar el proveedor remoto (`GitProvider.GITHUB`, `AZURE_DEVOPS`, `GITLAB`, `BITBUCKET`, `LOCAL`), la rama activa y el estado del árbol de trabajo.
2. **Guarda de Ramas Protegidas y Nomenclatura:**
   - La función `validate_branch_name` prohíbe de forma terminante cualquier intento de autoría directa sobre ramas protegidas (`main`, `master`, `release`, `production`), lanzando `ProtectedBranchViolationError`.
   - Exige la convención de ramas: `(feature|bugfix|refactor|hotfix)/[nombre]`.
3. **Validación de Conventional Commits:**
   - La función `validate_commit_message` valida sintácticamente que los mensajes sigan el estándar Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, etc.).
4. **Comprobación Formal de Definition of Done (DoD):**
   - `verify_definition_of_done` exige 3 pilares indispensables para dar una tarea por finalizada:
     1. Evidencia de pruebas automatizadas aprobadas.
     2. Evidencia de revisión de código independiente aprobada.
     3. Evidencia de Pull Request integrado (o flujo alternativo de commit validado en repositorios locales sin remoto).
5. **Gestor de Git Worktrees (`GitWorktreeManager`):**
   - Implementar `src/dh_harness/git/worktrees.py` para crear, listar y eliminar entornos de trabajo aislados (`.worktrees/`), permitiendo la concurrencia de agentes sin colisión sobre el árbol de trabajo principal.
6. **Comandos CLI e Integración Node:**
   - Nuevos comandos en Typer y Node `bin/cli.js`:
     - `dh-harness git status`: Diagnóstico del repositorio y proveedor.
     - `dh-harness git validate-branch <name>`: Auditoría de ramas.
     - `dh-harness git validate-commit "<msg>"`: Validación de commits.
     - `dh-harness git check-dod <task_id>`: Verificación formal de DoD.

## Consecuencias
- 100% de protección contra commits directos en ramas principales.
- Trazabilidad y consistencia garantizadas en ramas, commits y entregas.
- Ninguna tarea puede cerrarse como DONE sin pruebas, review y PR verificados.
