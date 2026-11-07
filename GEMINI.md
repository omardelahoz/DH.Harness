# GEMINI.md — Runtime & Context Guidance for Google Antigravity & Gemini

Este documento proporciona las directrices de contexto para la interacción entre modelos Gemini dentro del entorno **Google Antigravity** y **DH Engineering Harness**.

---

## 1. Integración con Google Antigravity

- DH Engineering Harness interactúa con el runtime de Google Antigravity a través del adaptador `AntigravitySDKAdapter` (`src/dh_harness/sdk/adapter.py`).
- El arnés consume las capacidades del SDK oficial `google.antigravity` respetando el principio de mínimo privilegio:
  - Agentes en modo solo-lectura no reciben herramientas de modificación de archivos ni ejecución de comandos destructivos.
  - Agentes de desarrollo operan bajo control de bóveda TDD y auditoría estática de arquitectura.

---

## 2. Modos de Operación y Respuesta

Al interactuar con solicitudes del usuario:
1. **Modo Conversacional (`CONVERSATIONAL`):** Responder con claridad conceptual, enlaces directos a código y explicaciones técnicas concisas. No iniciar ceremonias ni pipelines TDD para preguntas teóricas.
2. **Modo Investigación (`INVESTIGATION`):** Diagnosticar mediante lecturas específicas, rastreo de dependencias y análisis estático. Proponer soluciones antes de editar.
3. **Modo Corrección de Errores (`BUG_FIX`):** Exigir reproducción con prueba unitaria en RED antes de aplicar cualquier cambio en `src/`.
4. **Modo Desarrollo (`DEVELOPMENT` / `COMPLEX_ENGINEERING`):** Registrar tareas en el DAG, consultar dependencias (`dh-harness continue`), documentar ADRs cuando haya decisiones de diseño y verificar la Definition of Done antes de integrar PRs.

---

## 3. Acceso a Recursos Preempaquetados

- **Skills Disponibles:** En `.agents/skills/` se encuentran los 9 paquetes con directrices operativas completas.
- **Agentes Especializados:** En `.agents/agents/catalog.json` se definen roles, contratos de entrada/salida y permisos.
- **Memoria Persistente:** En `.project/` se almacena el estado continuo del proyecto, las especificaciones y las decisiones técnicas.
