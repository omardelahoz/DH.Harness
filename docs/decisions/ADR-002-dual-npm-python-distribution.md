# ADR-002: Distribución Dual con Wrapper CLI de Node.js (npm/npx)

## Estado
Aprobado

## Contexto
El usuario requiere que el proyecto pueda ser instalado mediante `npm` o ejecutado al vuelo con herramientas como `npx dh-harness`, permitiendo una adopción ágil en entornos donde los desarrolladores trabajan habitualmente con el ecosistema JavaScript/Node.js, mientras que el núcleo técnico del SDK de Antigravity reside en Python.

## Decisión
Implementar una arquitectura de empaquetado dual:
1. Paquete Node.js (`package.json`) con entrypoint `bin/cli.js`.
2. El script `bin/cli.js` detecta el entorno Python local (`.venv` o sistema), valida las dependencias y despacha los comandos al CLI del Harness con redirección completa de terminal interactiva (`stdio: 'inherit'`).
3. Empaquetado Python complementario vía `pyproject.toml` (PEP 621) para uso directo en pipelines de Python.

## Consecuencias
- Instalación fluida: `npm install -g dh-harness` o ejecución al vuelo `npx dh-harness`.
- Mantenimiento centralizado de la lógica de negocio en Python.
