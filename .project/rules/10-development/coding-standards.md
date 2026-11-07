# Coding Standards (`.project/rules/10-development/coding-standards.md`)

1. **SOLID, KISS, DRY, YAGNI:** Código simple, tipado estricto y sin sobreingeniería especulativa.
2. **Python:** Python 3.10+, tipado estático con `typing` / `pydantic`, nombres PEP8, asincronía adecuada con `asyncio`.
3. **Node.js CLI:** ES Modules / CommonJS compatible, sin dependencias pesadas innecesarias en el launcher `bin/cli.js`.
4. **Manejo de Errores:** Errores explícitos con mensajes contextuales claros. Cero excepciones silenciosas (`except: pass`).
5. **Licencias:** Solo dependencias con licencia permisiva (MIT, Apache-2.0, BSD). Prohibido introducir software con copyleft restrictivo o modelos comerciales de cobro.
