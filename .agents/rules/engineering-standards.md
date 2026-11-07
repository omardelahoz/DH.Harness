# DH Engineering Standards & Strict Architectural Governance

Toda contribución, edición de código o diseño dentro de DH Engineering Harness debe cumplir obligatoriamente con los siguientes estándares de ingeniería:

---

## 1. Clean Architecture & Prohibición de Bypass de Capas
1. **Thin Controllers:**
   - Queda terminantemente prohibido inyectar `DbContext`, `IDbConnection`, `SqlConnection` o escribir consultas SQL (Dapper) o LINQ (EF Core) dentro de Controllers o Minimal APIs.
   - Toda interacción con la base de datos reside exclusivamente en repositorios en la capa de Infraestructura.
2. **Cero Lógica de Negocio en Capas de Entrada o Persistencia:**
   - La lógica de negocio y las validaciones residen en Dominio y Aplicación.
3. **Cero Datos Quemados (No Fake / No Mock Data en Producción):**
   - Prohibido hardcodear arreglos estáticos de datos para simular respuestas en el frontend o backend. Los datos de prueba deben residir como Seed Data en la capa de Infraestructura.
4. **Mocks Permitidos Exclusivamente en Pruebas Unitarias:**
   - En las suites de tests unitarios se recomienda el aislamiento de capas mockeando interfaces.

---

## 2. Desarrollo Guiado por Pruebas (TDD) Determinista
1. **Evidencia Previa en Fase RED:**
   - Ningún archivo en `src/` puede modificarse sin haber registrado previamente la prueba fallida en `RedEvidenceVault`.
2. **Cero Pruebas Falsas:**
   - Pruebas vacías, con `assert True` o sin aserciones verificables son automáticamente bloqueadas por el arnés de calidad.

---

## 3. Seguridad & Licenciamiento Abierto (SPDX Whitelist)
1. **Licencias Permitidas:** Únicamente licencias 100% permisivas (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `PostgreSQL`, `MS-PL`).
2. **Cero Secretos:** Escaneo obligatorio de tokens, credenciales y claves privadas.
3. **Bloqueo de SQL Destructivo:** Comandos `DROP TABLE`, `TRUNCATE` o `DELETE` sin `WHERE` son bloqueados de forma inmediata.

---

## 4. Gobernanza Git & Entrega
1. **Ramas:** Todo cambio se desarrolla en ramas `feature/*`. La rama `main` es inmutable y protegida.
2. **Conventional Commits:** Todo commit debe cumplir con la sintaxis convencional.
3. **Definition of Done (DoD):** Toda tarea requiere evidencia de tests, auditoría de calidad y revisión independiente.
