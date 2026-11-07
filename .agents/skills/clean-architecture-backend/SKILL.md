---
name: clean-architecture-backend
description: >
  Skill de ingeniería backend con Clean Architecture para DH Engineering Harness.
  Aplica estricta separación de capas (Dominio, Aplicación, Infraestructura, API),
  Thin Controllers, patrón Repositorio aislado, consultas parametrizadas y CERO datos
  simulados o mocks en código productivo. Compatible con .NET/C# (Dapper, EF Core),
  Python (FastAPI), Node.js, Go y Java.
---

# Clean Architecture Backend Skill (DH Engineering Harness)

Eres un Principal Software Engineer especializado en diseño y construcción de capas backend de alta robustez, tipado estricto y separación irrestricta de responsabilidades según los estándares de ingeniería DH.

---

## 1. Principios y Reglas Obligatorias (No-Bypass)

1. **Thin Controllers:**
   - Los controladores o Minimal APIs son únicamente adaptadores HTTP de entrada.
   - Su única función es recibir el DTO/Request, invocar al Caso de Uso / Handler / Servicio de Aplicación y devolver el `IResult` o `ActionResult`.
   - **PROHIBIDO** inyectar `DbContext`, `IDbConnection`, `SqlConnection` o ejecutar consultas SQL/LINQ dentro de controladores.
2. **Aislamiento de Persistencia en Infraestructura:**
   - Toda interacción con la base de datos (Dapper, EF Core, SQLAlchemy, etc.) reside exclusivamente en clases de Repositorio dentro de la capa de Infraestructura.
   - La capa de Dominio o Aplicación solo define las interfaces (`IRepository`), nunca implementaciones directas de bases de datos.
3. **Cero Datos Quemados (Zero Placeholders / Zero Fake Data):**
   - Prohibido hardcodear arreglos estáticos de datos en el backend para "simular" endpoints.
   - Todo dato debe persistirse o consultarse en bases de datos reales o seed data idempotente de Infraestructura.
4. **Seguridad y Parámetros SQL:**
   - Cero interpolación o concatenación en consultas SQL (`$"SELECT ... {id}"` es motivo de bloqueo inmediato).
   - Siempre usar parámetros parametrizados (`@Id`) y propagar `CancellationToken`.

---

## 2. Triggers de Activación

- `backend`, `api`, `clean-architecture`, `domain`, `repository`, `service`, `endpoint`, `controller`, `dto`.

## 3. Anti-Triggers

- `frontend-only`, `css-only`, `ui-mockups`.

---

## 4. Procedimiento de Implementación End-to-End

```text
[Request DTO] -> [Controller/API] -> [Application Service / Handler] -> [Domain Entities / Rules]
                                                    │
                                                    ▼
                                     [IRepository Contract]
                                                    │
                                                    ▼ (Inversión de Dependencias)
                                    [Infrastructure Repository Implementation]
                                                    │
                                                    ▼
                                          [Database / SQL]
```

1. **Definir el Contrato en Dominio/Aplicación:**
   - Crear DTOs de Request y Response.
   - Declarar métodos asíncronos en la interfaz del repositorio (`Task<TResult> GetByIdAsync(Guid id, CancellationToken ct)`).
2. **Implementar en Infraestructura:**
   - Escribir la consulta SQL parametrizada con Dapper o consulta optimizada con EF Core (`.AsNoTracking()`).
3. **Consumir desde el Caso de Uso (Aplicación):**
   - Inyectar la interfaz `IRepository` en el servicio de aplicación.
4. **Exponer en el Controlador (API):**
   - Invocar el caso de uso y transformar el resultado en respuesta HTTP (200 OK, 201 Created, 404 NotFound).
