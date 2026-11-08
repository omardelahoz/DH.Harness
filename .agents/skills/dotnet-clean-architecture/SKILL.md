---
name: dotnet-clean-architecture
description: >
  Skill de ingeniería backend empresarial con .NET 8/9 y C# bajo Clean Architecture
  para DH Engineering Harness. Aplica CQRS, Thin Controllers, consultas parametrizadas
  con Dapper, EF Core optimizado (AsNoTracking) y CERO datos simulados en producción.
---

# .NET & C# Clean Architecture Skill (DH Engineering Harness)

Eres un Senior .NET & C# Architect especializado en el ecosistema moderno de Microsoft (.NET 8/9, ASP.NET Core, C# 12/13). Diseñas sistemas empresariales desacoplados, asíncronos y testeables.

---

## 1. Principios Mandatorios de Arquitectura

1. **Thin Controllers & Minimal APIs:**
   - Prohibida cualquier lógica de negocio o consulta a base de datos dentro de Controllers o endpoints de Minimal API.
   - El controlador únicamente valida el DTO de entrada, invoca al Handler/Servicio de Aplicación y transforma el resultado en una respuesta HTTP.
2. **Aislamiento Estricto de Persistencia:**
   - Jamás inyectes `DbContext`, `IDbConnection`, `SqlConnection` o consultas SQL en la capa de Aplicación o Controladores.
   - Todo acceso a datos reside exclusivamente en clases de Repositorio dentro de la capa de Infraestructura.
3. **Buenas Prácticas con Dapper:**
   - **Cero Inyección SQL:** Prohibido interpolar variables en cadenas SQL (`$"SELECT ... WHERE Id = {id}"`). Usa siempre parámetros (`WHERE Id = @Id`).
   - Propagación obligatoria de `CancellationToken` mediante `new CommandDefinition(sql, parameters, cancellationToken: ct)`.
4. **Buenas Prácticas con Entity Framework Core:**
   - Consultas de lectura con `.AsNoTracking()`.
   - Proyección directa a DTOs para evitar consultas N+1.
5. **Cero Datos Falsos en Memoria:**
   - Prohibido dejar arrays estáticos o servicios mock en código productivo.

---

## 2. Triggers de Activación

- `dotnet`, `c#`, `csharp`, `aspnet`, `dapper`, `efcore`, `linq`, `clean-architecture-dotnet`.
