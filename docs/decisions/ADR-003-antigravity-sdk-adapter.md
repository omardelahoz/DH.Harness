# ADR-003: Aislamiento del SDK de Antigravity mediante Adapter Pattern

## Estado
Aprobado

## Contexto
El SDK de Google Antigravity (`google-antigravity`) evoluciona rápidamente y depende de binarios de plataforma para el runtime del agente. El Harness debe evitar acoplarse directamente a interfaces internas o detalles de implementación no documentados.

## Decisión
Encapsular toda interacción con `google.antigravity` detrás de `AntigravitySDKAdapter` (`src/dh_harness/sdk/adapter.py`). El adaptador expone una interfaz limpia para verificar disponibilidad, inspeccionar metadatos de versión, crear configuraciones seguras (read-only por defecto) y gestionar el ciclo de arrendamiento del agente.

## Consecuencias
- Alta resiliencia ante actualizaciones del SDK.
- Facilidad para escribir pruebas unitarias sin requerir el runtime binario activo.
- Configuración segura por defecto (Least Privilege).
