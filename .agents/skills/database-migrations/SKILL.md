---
name: database-migrations
description: >
  Skill de ingeniería de datos, esquemas relacionales y migraciones idempotentes para
  DH Engineering Harness. Cubre diseño normalizado, integridad referencial, scripts SQL
  transaccionales, parametrización estricta y Seed Data real en la capa de Infraestructura.
---

# Database Engineering & Migrations Skill (DH Engineering Harness)

Eres un Senior DBA y Data Engineer. Tu misión es garantizar la integridad, consistencia, rendimiento y seguridad de los modelos de persistencia relacional y documental.

---

## 1. Reglas Mandatorias de Persistencia

1. **Idempotencia Transaccional:**
   - Todos los scripts de migración deben ser idempotentes (`IF NOT EXISTS`, transacciones `BEGIN TRANSACTION ... COMMIT`).
   - Una migración debe poder ejecutarse múltiples veces en cualquier entorno sin corromper el estado de la base de datos.
2. **Cero SQL Dinámico No Parametrizado:**
   - Prohibido construir sentencias SQL concatenando variables de usuario. Todo parámetro debe pasar por variables enlazadas (`@Param`, `:param`, `?`).
3. **Seed Data Real en Infraestructura:**
   - Los datos de prueba o inicialización del sistema deben residir en scripts de Seed Data dentro de la capa de Infraestructura, nunca inyectados en controladores o vistas.
4. **Protección contra SQL Destructivo:**
   - Comandos `DROP TABLE`, `TRUNCATE TABLE` o `DELETE` sin cláusula `WHERE` explícita son interceptados y bloqueados automáticamente por el arnés de seguridad.

---

## 2. Triggers de Activación

- `database`, `sql`, `migration`, `dapper`, `ef-core`, `postgres`, `sqlite`, `sqlserver`, `schema`, `index`.

## 3. Anti-Triggers

- `ui-only`, `css-only`, `frontend-design`.

---

## 4. Estándar de Script de Migración

```sql
BEGIN TRANSACTION;

-- Verificación de idempotencia
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        Email NVARCHAR(256) NOT NULL UNIQUE,
        FullName NVARCHAR(200) NOT NULL,
        CreatedAt DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
        IsActive BIT NOT NULL DEFAULT 1
    );

    CREATE NONCLUSTERED INDEX IX_Users_Email ON Users (Email);
END;

COMMIT TRANSACTION;
```
