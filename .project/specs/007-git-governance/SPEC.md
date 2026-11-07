# Specification: 007 - Git & Repository Governance & Delivery

## Objetivo
Implementar la Fase 6 del roadmap de `info.md`:
- Diagnóstico automático de repositorio Git y proveedor (`GitProvider`, `RepoDiagnostics`).
- Guarda de ramas protegidas (`ProtectedBranchViolationError`) y validación de nomenclatura.
- Validador de Conventional Commits (`validate_commit_message`).
- Verificador formal de Definition of Done (`verify_definition_of_done`, `DoDVerificationResult`).
- Aislamiento seguro con Git Worktrees (`GitWorktreeManager`).
- Interfaz CLI: `node bin/cli.js git status`, `validate-branch`, `validate-commit`, `check-dod`.

## Requisitos Verificados
- [x] Contratos core tipados en `dh_harness.core.contracts`.
- [x] Detección de proveedores: GitHub, Azure DevOps, GitLab, Bitbucket y Local.
- [x] Bloqueo de commits en ramas protegidas (`main`, `master`, `release`, `production`).
- [x] Validación de nomenclatura de ramas (`feature/`, `bugfix/`, `refactor/`, `hotfix/`).
- [x] Validación de Conventional Commits.
- [x] Verificación de DoD rechazando tareas sin tests, sin revisión o sin PR.
- [x] Creación, listado y remoción de `git worktree` aislados.
- [x] Comandos CLI operativos en Typer y binario de Node `bin/cli.js`.
