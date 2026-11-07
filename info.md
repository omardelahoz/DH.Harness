# DH Engineering Harness for Antigravity
## Especificación Maestra de Producto, Arquitectura y Requerimientos

**Versión:** 1.0  
**Estado:** Propuesta arquitectónica consolidada  
**Tipo:** Especificación funcional y técnica  
**Plataforma objetivo:** Google Antigravity  
**Proyecto:** DH Engineering Harness  
**Enfoque:** Agentic Software Engineering, TDD, Governance, Workflow Orchestration y Continuous Engineering

---

# 1. Visión del producto

## 1.1. Propósito

DH Engineering Harness es una plataforma de ingeniería de software asistida por agentes, diseñada para operar sobre Google Antigravity y proporcionar una capa integral de organización, planificación, ejecución, control, persistencia, calidad y entrega de proyectos de software.

No debe ser una simple colección de prompts, instrucciones Markdown, agentes o skills.

Debe funcionar como un verdadero sistema de ingeniería de software, capaz de:

- Comprender solicitudes de los usuarios.
- Identificar la naturaleza de cada interacción.
- Investigar problemas técnicos.
- Diseñar arquitecturas.
- Planificar proyectos y funcionalidades.
- Organizar historias, tareas y subtareas.
- Desarrollar software utilizando TDD obligatorio cuando corresponda.
- Coordinar agentes especializados.
- Ejecutar workflows controlados.
- Administrar memoria y contexto persistente.
- Gestionar repositorios Git.
- Crear ramas, commits y Pull Requests.
- Ejecutar pruebas y controles de calidad.
- Proteger credenciales y recursos.
- Documentar decisiones y cambios.
- Recuperar el trabajo después de interrupciones.
- Recomendar qué hacer a continuación.
- Evaluar objetivamente el resultado de cada actividad.

El objetivo es que el usuario pueda trabajar con el harness mediante lenguaje natural, sin tener que administrar manualmente cada agente, procedimiento, herramienta o control de calidad.

## 1.2. Filosofía principal

**Mínimo proceso necesario, máximo rigor cuando se modifica software.**

El harness no debe convertir cualquier pregunta en un proyecto formal.

Debe diferenciar entre conversar, investigar, corregir, desarrollar y ejecutar proyectos complejos.

El rigor aumenta según el impacto y el riesgo de la operación.

Principios rectores:

1. Calidad antes que velocidad aparente.
2. TDD como metodología obligatoria para cambios de comportamiento que puedan probarse.
3. Evidencia antes que afirmaciones.
4. Arquitectura mantenible antes que complejidad innecesaria.
5. Seguridad desde el diseño.
6. Memoria persistente y trazabilidad.
7. Responsabilidades claramente delimitadas.
8. Automatización con supervisión y autorización.
9. Reutilización sin acoplamiento innecesario.
10. Adaptación a las tecnologías y necesidades de cada proyecto.
11. Recuperación confiable del trabajo.
12. Entregas completas y verificables.

## 1.3. Separación de responsabilidades

La solución debe diferenciar tres elementos:

**Google Antigravity**
- Runtime de agentes.
- Modelos de inteligencia artificial.
- Herramientas de ejecución.
- Integración con el entorno de desarrollo.
- Capacidades nativas disponibles en la plataforma.

**DH Engineering Harness**
- Gobernanza.
- Orquestación.
- Clasificación de solicitudes.
- Planificación.
- Gestión de tareas.
- TDD.
- Memoria.
- Workflows.
- Seguridad.
- Persistencia.
- Auditoría.
- Calidad.
- Git y entrega.

**Ecosistema de ingeniería**
- Agentes especializados.
- Skills.
- Workflows.
- Hooks.
- MCP.
- Herramientas externas.
- Integraciones con repositorios, bases de datos, plataformas cloud y sistemas de CI/CD.

El harness no debe depender innecesariamente de APIs internas o no documentadas de Antigravity.

---

# 2. Interaction & Task Classification Engine

## 2.1. Propósito

Es el componente encargado de comprender qué quiere hacer el usuario y determinar qué proceso debe ejecutar.

Debe evitar que una pregunta sencilla desencadene una planificación, un workflow y una batería de pruebas innecesarias.

La clasificación debe realizarse antes de activar agentes especializados o procesos formales.

## 2.2. Modos de operación

### CONVERSATIONAL

Para:
- Preguntas técnicas.
- Explicaciones de código.
- Consultas de arquitectura.
- Recomendaciones.
- Comparaciones tecnológicas.
- Aclaraciones.
- Consultas sobre mejores prácticas.

Comportamiento:
- Responder directamente.
- Consultar especialistas cuando aporten valor.
- Utilizar documentación y contexto cuando sea necesario.
- No crear tareas formales automáticamente.
- No modificar archivos sin autorización.

No requiere TDD.

### INVESTIGATION

Para:
- Diagnóstico de errores.
- Troubleshooting.
- Análisis de rendimiento.
- Investigación de vulnerabilidades.
- Análisis de arquitectura.
- Revisión de dependencias.
- Análisis de código heredado.
- Investigación de alternativas tecnológicas.

Comportamiento:
- Definir el objetivo de investigación.
- Recopilar evidencia.
- Inspeccionar código y configuración.
- Consultar documentación oficial.
- Separar hechos, hipótesis y recomendaciones.
- Presentar causa raíz cuando sea posible.
- No modificar archivos sin autorización explícita.

No requiere TDD si no hay cambios de comportamiento.

### BUG_FIX

Para solicitudes explícitas de corrección de defectos.

Proceso:
1. Reproducir el problema.
2. Identificar la causa raíz.
3. Definir el comportamiento esperado.
4. Crear prueba de regresión.
5. Verificar RED.
6. Implementar la corrección mínima.
7. Verificar GREEN.
8. Refactorizar si corresponde.
9. Ejecutar pruebas de regresión.
10. Revisar independientemente.
11. Documentar evidencia.
12. Entregar según la política del repositorio.

TDD obligatorio cuando el defecto admite una prueba automatizada.

### DEVELOPMENT

Para:
- Nuevas funcionalidades.
- Mejoras.
- Refactorizaciones.
- Desarrollo de API.
- Desarrollo frontend.
- Integraciones.
- Cambios en bases de datos.

Comportamiento:
- Definir alcance.
- Identificar criterios de aceptación.
- Planificar proporcionalmente.
- Aplicar TDD.
- Coordinar agentes.
- Ejecutar quality gates.
- Documentar cambios.

### COMPLEX_ENGINEERING

Para:
- Nuevos productos.
- Nuevas plataformas.
- Arquitecturas complejas.
- Sistemas distribuidos.
- Transformaciones tecnológicas.
- Migraciones importantes.
- Cambios que afectan múltiples módulos o sistemas.

Comportamiento:
- Discovery.
- Análisis de requisitos.
- Diseño arquitectónico.
- ADR.
- Planificación detallada.
- Descomposición en épicas e historias.
- Análisis de dependencias.
- Ejecución coordinada.
- Validación integral.
- Seguridad, rendimiento y documentación.
- Preparación de release.

## 2.3. Investigación y aprendizaje técnico

El harness debe incorporar una capacidad transversal de Learning & Research.

Debe poder:

- Consultar documentación oficial.
- Analizar repositorios.
- Comparar librerías y frameworks.
- Verificar compatibilidad de versiones.
- Investigar vulnerabilidades.
- Comparar patrones arquitectónicos.
- Evaluar benchmarks.
- Analizar tendencias técnicas.
- Identificar herramientas mantenidas.
- Recomendar alternativas.

No debe inventar APIs, características, versiones ni capacidades.

Cuando una decisión dependa de información vigente, debe verificar fuentes confiables y registrar las referencias utilizadas.

## 2.4. Transiciones entre modos

Se deben permitir transiciones dinámicas:

- CONVERSATIONAL → INVESTIGATION.
- INVESTIGATION → BUG_FIX.
- INVESTIGATION → DEVELOPMENT.
- BUG_FIX → DEVELOPMENT.
- DEVELOPMENT → COMPLEX_ENGINEERING.

El contexto debe conservarse.

La autorización para investigar no implica autorización para modificar código.

Cuando exista ambigüedad sobre una operación que pueda modificar archivos, datos o infraestructura, debe solicitar una aclaración concreta.

---

# 3. Orchestrator

## 3.1. Responsabilidad

Es el coordinador central de las operaciones.

Debe:

- Recibir solicitudes.
- Consultar el clasificador.
- Recuperar el contexto.
- Seleccionar el workflow.
- Identificar agentes necesarios.
- Determinar dependencias.
- Coordinar ejecuciones.
- Administrar tiempos y recursos.
- Recopilar resultados.
- Validar entregables.
- Actualizar tareas.
- Generar checkpoints.
- Comunicar resultados.

No debe asumir que todos los agentes tienen las mismas capacidades o permisos.

## 3.2. Ejecución

El orchestrator debe soportar:

- Ejecución secuencial.
- Ejecución paralela.
- Ejecución condicionada.
- Delegación.
- Reintentos controlados.
- Cancelación.
- Recuperación.
- Checkpoints.
- Timeout.
- Idempotencia.
- Circuit breakers.

Las operaciones críticas deben estar protegidas por Governance Engine.

---

# 4. Agent Ecosystem

## 4.1. Diseño de agentes especializados

No se debe construir un único agente omnisciente.

Se debe disponer de un catálogo extensible de especialistas con responsabilidades delimitadas.

Cada agente debe tener:

- Identificador.
- Nombre.
- Descripción.
- Especialidad.
- Capacidades.
- Skills asociadas.
- Herramientas permitidas.
- Permisos.
- Restricciones.
- Modelo o perfil de ejecución.
- Contrato de entrada.
- Contrato de salida.
- Criterios de evaluación.

## 4.2. Agentes de dirección y arquitectura

- Chief Orchestrator.
- Business Analyst.
- Product Manager.
- Solution Architect.
- Software Architect.
- Domain Architect.
- API Architect.
- Cloud Architect.
- DevOps Architect.
- Technical Writer.
- Architecture Reviewer.

## 4.3. Agentes backend

Debe existir cobertura especializada para:

- .NET y C#.
- ASP.NET Core.
- Entity Framework Core.
- Dapper.
- Go.
- Python.
- FastAPI.
- Django.
- Java.
- Spring Boot.
- Node.js.
- NestJS.
- PHP.
- Laravel.
- Ruby.
- Rust.
- Integración de APIs.
- Microservicios.
- Sistemas distribuidos.
- Event-driven architecture.

## 4.4. Agentes frontend

Debe existir cobertura para:

- HTML.
- CSS.
- JavaScript.
- TypeScript.
- Angular.
- React.
- Next.js.
- Vue.
- Nuxt.
- Svelte.
- SvelteKit.
- Astro.
- SolidJS.
- Qwik.
- Lit.
- Web Components.
- Tailwind CSS.
- Bootstrap.
- Material UI.
- State Management.
- Formularios.
- SSR y SSG.
- SEO.
- Responsive Design.
- Accesibilidad.
- Arquitectura frontend.
- Design Systems.

## 4.5. Agentes de bases de datos

Relacionales:
- SQL Server.
- PostgreSQL.
- MySQL.
- Oracle.
- MariaDB.
- SQLite.
- CockroachDB.
- Cloud SQL.

No relacionales:
- MongoDB.
- Redis.
- Cassandra.
- DynamoDB.
- Firestore.
- Elasticsearch.
- OpenSearch.
- Neo4j.
- Couchbase.
- InfluxDB.
- ClickHouse.

Especialistas transversales:
- Database Architect.
- Data Modeler.
- Query Optimization.
- Database Performance.
- Database Security.
- Migration Engineer.
- Backup & Recovery.
- Database Governance.

## 4.6. Agentes UI/UX

- UX Researcher.
- Product Designer.
- UI Designer.
- Interaction Designer.
- Design System Architect.
- Accessibility Specialist.
- UX Writer.
- Visual QA Designer.
- Frontend Design Engineer.

El objetivo es producir interfaces profesionales, no solamente funcionales.

Deben evaluar:
- Jerarquía visual.
- Tipografía.
- Espaciado.
- Contraste.
- Consistencia.
- Navegación.
- Estados.
- Responsividad.
- Accesibilidad.
- Usabilidad.
- Fidelidad al diseño.

## 4.7. Agentes de calidad y seguridad

- Test Architect.
- TDD Enforcer.
- Unit Test Engineer.
- Integration Test Engineer.
- E2E Test Engineer.
- Performance Engineer.
- Independent Code Reviewer.
- Security Engineer.
- OWASP Specialist.
- Dependency Auditor.
- Accessibility Auditor.
- Reliability Engineer.
- SRE.
- Release Manager.

## 4.8. Otros especialistas

- Flutter.
- React Native.
- Kotlin.
- Swift.
- Electron.
- Tauri.
- .NET MAUI.
- AWS.
- Azure.
- Google Cloud.
- Oracle Cloud Infrastructure.
- Docker.
- Kubernetes.
- Terraform.
- OpenTofu.
- Ansible.
- Helm.
- CI/CD.
- Data Engineering.
- ETL/ELT.
- Airflow.
- Spark.
- dbt.
- AI Engineering.
- LLM.
- RAG.
- Embeddings.
- Agent Development.
- MCP Development.
- Machine Learning.
- PyTorch.
- TensorFlow.
- Scikit-learn.
- Playwright.
- Cypress.
- Selenium.
- Appium.
- OpenAPI.
- ADR.
- C4.
- Mermaid.
- Git.
- Legacy Modernization.

El catálogo debe ser ampliable sin modificar el núcleo.

## 4.9. Contrato de ejecución

Cada agente debe entregar:

- Task ID.
- Agent ID.
- Objective.
- Context.
- Input artifacts.
- Changes.
- Decisions.
- Tests.
- Evidence.
- Blockers.
- Output artifacts.
- Status.

Un agente no puede modificar su propia evaluación ni declarar aprobada una revisión independiente de su propio trabajo.

---

# 5. Skills Registry

## 5.1. Propósito

Las skills representan conocimiento especializado y procedimientos reutilizables.

Deben activarse según la tarea y la especialidad necesaria.

## 5.2. Estructura

Cada skill debe incluir cuando corresponda:

- SKILL.md.
- References.
- Scripts.
- Templates.
- Examples.
- Validation rules.
- Official documentation references.

## 5.3. Contenido obligatorio

Cada skill debe definir:

- Propósito.
- Cuándo activarse.
- Cuándo no activarse.
- Nivel de especialización.
- Procedimiento.
- Reglas obligatorias.
- Herramientas.
- Validaciones.
- Criterios de aceptación.
- Ejemplos.

## 5.4. Categorías

- Engineering Core.
- Backend.
- Frontend.
- Database.
- UI/UX.
- Testing.
- Security.
- DevOps.
- Cloud.
- AI.
- Documentation.
- Delivery.
- Git.
- Architecture.

Las reglas transversales de seguridad y TDD no pueden depender de que una skill opcional sea activada.

---

# 6. Workflow Engine

## 6.1. Responsabilidad

Los workflows deben ser procesos ejecutables, persistentes, reanudables y auditables.

No deben ser simples documentos con instrucciones.

Deben definir:

- Objetivo.
- Trigger.
- Precondiciones.
- Etapas.
- Agentes.
- Skills.
- Herramientas.
- Dependencias.
- Estados.
- Validaciones.
- Condiciones de salida.
- Manejo de errores.
- Recuperación.
- Evidencias.

## 6.2. Workflows iniciales

- New Project.
- Feature Development.
- Bug Fixing.
- Code Refactoring.
- UI/UX Development.
- Database Engineering.
- Security Audit.
- Production Release.
- Legacy Modernization.
- API Development.
- Microservices Development.
- Event-Driven Development.
- Cloud Provisioning.
- CI/CD Implementation.
- Database Migration.
- Performance Optimization.
- Accessibility Audit.
- Dependency Upgrade.
- Documentation.
- Technical Debt Reduction.
- Incident Investigation.
- Disaster Recovery.
- Architecture Review.
- AI/RAG Development.
- MCP Server Development.
- Agent Development.
- Test Automation.
- Pull Request Preparation.

Los workflows deben ser componibles.

Ejemplo: una API .NET con PostgreSQL y frontend Angular debe coordinar arquitectura, backend, database, frontend, pruebas, seguridad y documentación según las necesidades reales.

---

# 7. TDD Engine

## 7.1. Regla fundamental

El desarrollo de cambios de comportamiento debe seguir TDD cuando sea posible automatizar su validación.

Ciclo obligatorio:

REQUIREMENT → TEST RED → IMPLEMENT GREEN → REFACTOR → VERIFY → DONE.

## 7.2. Fases

### REQUIREMENT

- Identificar el comportamiento esperado.
- Definir criterios de aceptación.
- Identificar escenarios normales y excepcionales.
- Identificar riesgos.

### TEST RED

- Crear una prueba que represente el requisito.
- Ejecutarla.
- Comprobar que falla por la razón correcta.

### IMPLEMENT GREEN

- Implementar el mínimo código necesario.
- Ejecutar la prueba.
- Confirmar que pasa.

### REFACTOR

- Mejorar estructura.
- Eliminar duplicación injustificada.
- Mantener comportamiento.
- Preservar pruebas.

### VERIFY

- Ejecutar pruebas relevantes.
- Ejecutar pruebas de regresión.
- Ejecutar validaciones de calidad.
- Registrar evidencias.

### DONE

Solo se alcanza cuando se satisfacen los criterios de aceptación y las políticas de entrega.

## 7.3. Excepciones

No requieren TDD formal:

- Preguntas conceptuales.
- Investigación.
- Diseño conceptual.
- Documentación sin cambios ejecutables.
- Configuraciones sin comportamiento testeable.
- Tareas sin comportamiento verificable mediante pruebas automatizadas.

En estos casos se debe utilizar la validación apropiada.

En código heredado sin cobertura, primero se deben crear pruebas de caracterización cuando corresponda.

## 7.4. Detección de pruebas falsas

El sistema debe detectar:

- Tests vacíos.
- Assertions triviales.
- Tests que no validan el requisito.
- Mocks que reproducen la implementación.
- Pruebas que nunca se ejecutan.
- Pruebas que siempre pasan.
- Casos importantes omitidos.

## 7.5. Evidencias

Persistir:
- Task ID.
- Requirement ID.
- Test ID.
- Resultado RED.
- Razón del fallo.
- Implementación.
- Resultado GREEN.
- Refactor.
- Verificación.
- Comandos ejecutados.
- Timestamps.
- Agente responsable.
- Hash de commit.

## 7.6. Quality Gates

- Tests obligatorios.
- Build.
- Lint.
- Format.
- Análisis estático.
- Seguridad.
- Cobertura.
- Validaciones específicas del stack.

La cobertura debe ser configurable por proyecto y módulo. Se puede proponer un 80% inicial, pero no debe optimizarse artificialmente ni utilizarse como sustituto de la calidad de las pruebas.

Se debe considerar cobertura de ramas y mutation testing cuando aporte valor.

---

# 8. Memory Engine

## 8.1. Propósito

Proporcionar memoria persistente para que el harness no dependa exclusivamente de la ventana de contexto de una sesión.

Debe permitir continuar proyectos después de días, semanas o interrupciones.

## 8.2. Niveles de memoria

### Global

- Principios de ingeniería.
- Políticas generales.
- Preferencias técnicas configurables.
- Tecnologías soportadas.
- Reglas de gobernanza.

### Proyecto

- Arquitectura.
- Stack.
- Estructura.
- Dependencias.
- Convenciones.
- ADR.
- Reglas específicas.
- Estado general.
- Deuda técnica.

### Tarea

- Objetivo.
- Criterios de aceptación.
- Cambios.
- Pruebas.
- Decisiones.
- Bloqueos.
- Estado.
- Evidencias.

### Sesión

- Conversación reciente.
- Acciones.
- Actividades.
- Contexto inmediato.
- Checkpoint.

### Conocimiento

- Soluciones reutilizables.
- Patrones.
- Errores conocidos.
- Lecciones aprendidas.
- Referencias técnicas.

## 8.3. Requisitos

- Persistencia.
- Búsqueda.
- Actualización.
- Trazabilidad.
- Versionado.
- Detección de información obsoleta.
- Recuperación.
- Separación por proyecto.
- Control de acceso.

La memoria no debe reemplazar el repositorio, los tests ni los artefactos verificables como fuente de verdad.

Nunca debe almacenar credenciales, tokens o secretos.

## 8.4. Implementación inicial

Propuesta:
- SQLite.
- JSON/YAML.
- Markdown.
- Índice semántico opcional.

La solución debe permitir evolucionar hacia almacenamiento más avanzado sin modificar los contratos de los módulos consumidores.

---

# 9. Task Management Engine

## 9.1. Propósito

Administrar el trabajo del proyecto de forma persistente y estructurada.

Debe permitir conocer en todo momento:

- Qué falta.
- Qué está en ejecución.
- Qué está bloqueado.
- Qué se terminó.
- Qué necesita revisión.
- Qué depende de otras tareas.
- Qué se puede ejecutar en paralelo.
- Qué falta para completar un hito.

## 9.2. Jerarquía

Project → Epic → Feature/User Story → Task/Subtask → Tests/Evidence.

## 9.3. Entidades

Cada tarea debe tener:

- ID único.
- Título.
- Descripción.
- Objetivo.
- Criterios de aceptación.
- Prioridad.
- Complejidad.
- Estado.
- Dependencias.
- Responsable.
- Agente asignado.
- Fechas.
- Archivos afectados.
- Pruebas.
- Evidencias.
- Rama.
- Commit.
- Pull Request.
- Historial.

## 9.4. Estados

- BACKLOG.
- READY.
- IN_PROGRESS.
- BLOCKED.
- IN_REVIEW.
- CHANGES_REQUESTED.
- READY_FOR_PR.
- PR_OPEN.
- MERGED.
- DONE.
- CANCELLED.

No se puede marcar una historia como terminada solamente porque un agente diga que terminó.

## 9.5. Reglas de transición

Ejemplos:

- BACKLOG → READY.
- READY → IN_PROGRESS.
- IN_PROGRESS → BLOCKED.
- IN_PROGRESS → IN_REVIEW.
- IN_REVIEW → CHANGES_REQUESTED.
- IN_REVIEW → READY_FOR_PR.
- READY_FOR_PR → PR_OPEN.
- PR_OPEN → MERGED.
- MERGED → DONE.

Cada transición debe cumplir precondiciones.

La cancelación requiere justificación.

El cierre debe incluir evidencia y conservar el historial.

---

# 10. Project Continuity & Work Planning Engine

## 10.1. Propósito

Permitir que el usuario retome cualquier proyecto sin reconstruir manualmente el contexto.

Debe responder preguntas como:

- ¿Con qué continuamos hoy?
- ¿Qué tenemos pendiente?
- ¿Qué terminamos?
- ¿Qué quedó a medias?
- ¿Qué podemos hacer en paralelo?
- ¿Cuál es la siguiente tarea?
- ¿Qué nos está bloqueando?
- ¿Cuánto falta para terminar?
- ¿Qué debemos priorizar?

## 10.2. Proceso de recuperación

Ante una solicitud de continuidad, el harness debe:

1. Consultar el estado de las tareas.
2. Revisar historias abiertas y terminadas.
3. Consultar el roadmap.
4. Revisar dependencias.
5. Consultar el historial de ejecución.
6. Revisar commits y ramas.
7. Consultar PR abiertos y su estado.
8. Revisar pruebas y quality gates.
9. Detectar bloqueos.
10. Identificar tareas ejecutables.
11. Determinar actividades paralelizables.
12. Recomendar la mejor continuación.

No debe confiar exclusivamente en la memoria conversacional.

Debe contrastar el estado con el repositorio y los registros verificables.

## 10.3. Experiencia de usuario

Ejemplo conceptual:

**Usuario:** ¿Con qué continuamos hoy?

**Harness:**

Estado del proyecto:
- 12 historias terminadas.
- 3 en progreso.
- 8 pendientes.
- 1 bloqueada.

Último avance:
- Clasificador de tareas completado.
- Pruebas satisfactorias.
- PR integrado.
- Integración con Workflow Engine pendiente.

Opciones:

1. Continuar con la siguiente tarea recomendada.
2. Ejecutar tareas independientes en paralelo.
3. Revisar backlog y prioridades.
4. Revisar entregas terminadas.
5. Revisar bloqueos.
6. Revisar roadmap.
7. Definir una nueva prioridad.

Las cantidades son ilustrativas; en ejecución deben provenir de los datos reales.

## 10.4. Dependency Graph Engine

Debe construir un grafo de dependencias (DAG).

Cada tarea debe poder definir:

- Dependencias obligatorias.
- Dependencias opcionales.
- Recursos requeridos.
- Archivos compartidos.
- Restricciones de ejecución.
- Condiciones de salida.

Debe identificar:

- Tareas secuenciales.
- Tareas independientes.
- Tareas paralelizables.
- Tareas bloqueadas.
- Dependencias circulares.

No debe ejecutar tareas dependientes antes de cumplir sus precondiciones.

## 10.5. Modos de planificación

### SEQUENTIAL

Presentar la siguiente tarea obligatoria.

### PARALLEL

Presentar tareas independientes que pueden ejecutarse simultáneamente.

### FLEXIBLE

Presentar diferentes opciones y permitir al usuario escoger.

### RECOMMENDED

Recomendar la combinación óptima considerando prioridad, dependencias, riesgo, esfuerzo y recursos.

RECOMMENDED será el modo predeterminado.

## 10.6. Recomendaciones

Cada recomendación debe explicar:

- Qué se propone.
- Por qué.
- Qué dependencias cumple.
- Qué resultado producirá.
- Qué riesgos existen.
- Si puede ejecutarse en paralelo.
- Qué agentes se necesitan.

El usuario puede cambiar prioridades sin perder el historial ni la trazabilidad.

## 10.7. Checkpoint & Recovery

Guardar checkpoints al:

- Completar una tarea.
- Interrumpir una sesión.
- Cerrar un workflow.
- Encontrar un bloqueo.
- Cambiar de objetivo.
- Alcanzar un hito.
- Recuperar una ejecución fallida.

El checkpoint debe incluir:
- Estado.
- Último avance.
- Pendientes.
- Archivos modificados.
- Pruebas.
- Resultados.
- Decisiones.
- Bloqueos.
- Próxima actividad recomendada.

Al reanudar, debe reconciliar el checkpoint con el repositorio y las evidencias actuales.

---

# 11. Git & Repository Governance

## 11.1. Propósito

Administrar el ciclo de vida de los cambios de software y garantizar que las entregas cumplan las reglas del proyecto.

## 11.2. Descubrimiento inicial

Al iniciar un proyecto, debe identificar:

- Si existe Git.
- Si existe un repositorio.
- Si hay cambios locales.
- Si existe remoto.
- Qué proveedor se utiliza.
- Cuál es la rama principal.
- Qué estrategia de ramas está configurada.
- Qué políticas de Pull Request existen.

Si la información no está disponible, preguntar al usuario.

Proveedores soportados conceptualmente:

- GitHub.
- Azure DevOps.
- GitLab.
- Bitbucket.
- Otros proveedores compatibles.
- Repositorio local sin remoto.

No asumir GitHub por defecto.

## 11.3. Configuración inicial

Preguntar cuando corresponda:

- ¿El proyecto ya tiene repositorio?
- ¿Dónde está alojado?
- ¿Cuál es su URL?
- ¿Cuál es la rama principal?
- ¿Qué estrategia de ramas utiliza?
- ¿Se requieren aprobaciones?
- ¿Quién puede integrar cambios?
- ¿Qué convenciones de commits utiliza el equipo?

El harness debe detectar configuración existente antes de proponer modificaciones.

## 11.4. Política de ramas

Cada historia debe trabajar en una rama independiente, salvo excepciones aprobadas.

Ejemplos:

- feature/DH-123-user-authentication.
- bugfix/DH-124-invalid-token.
- refactor/DH-125-payment-module.
- hotfix/DH-126-production-error.

La convención debe ser configurable.

No modificar directamente ramas protegidas.

## 11.5. Flujo de entrega

1. Validar tarea y criterios.
2. Confirmar repositorio y estado local.
3. Crear rama.
4. Implementar mediante TDD.
5. Ejecutar pruebas.
6. Ejecutar quality gates.
7. Ejecutar revisión independiente.
8. Crear commits.
9. Crear Pull Request.
10. Incorporar descripción y evidencias.
11. Esperar aprobaciones cuando corresponda.
12. Verificar integración.
13. Actualizar tareas.
14. Actualizar memoria y documentación.
15. Marcar DONE cuando se cumpla la política de entrega.

## 11.6. Definition of Done

Una historia no debe marcarse DONE mientras falten controles obligatorios.

Cuando existe un remoto:

- Cambios implementados.
- Criterios de aceptación satisfechos.
- TDD verificado cuando corresponde.
- Quality gates aprobados.
- Revisión independiente aprobada.
- PR integrado.
- Documentación actualizada.
- Evidencias persistidas.
- Estado reconciliado.

Si no hay remoto, debe existir un flujo local alternativo basado en commits y validaciones. El sistema debe registrar que no hubo PR y no fingir una integración.

Los proyectos pueden configurar excepciones, pero nunca desactivar silenciosamente las políticas globales.

## 11.7. Git Worktrees

Para trabajo paralelo:

- Crear worktree por tarea o agente cuando corresponda.
- Evitar modificaciones simultáneas sobre los mismos archivos.
- Definir contratos de integración.
- Detectar conflictos.
- Ejecutar pruebas integrales después de integrar.
- Eliminar worktrees solamente después de verificar que no contienen trabajo pendiente.

---

# 12. DH Engineering Standards

## 12.1. Política maestra

Debe existir un conjunto de reglas globales llamado DH Engineering Standards.

Estas reglas se aplican a todos los agentes y proyectos.

Los proyectos pueden añadir reglas particulares, pero no desactivar restricciones globales de seguridad, auditoría, integridad o TDD.

## 12.2. Principios obligatorios

### SOLID

- Single Responsibility Principle.
- Open/Closed Principle.
- Liskov Substitution Principle.
- Interface Segregation Principle.
- Dependency Inversion Principle.

### KISS

Preferir soluciones simples y comprensibles.

### DRY

Evitar duplicación injustificada, sin crear abstracciones prematuras.

### YAGNI

No implementar funcionalidades especulativas.

### Otros principios

- Separation of Concerns.
- High Cohesion / Low Coupling.
- Composition over Inheritance.
- Explicit over Implicit.
- Fail Fast.
- Defensive Programming.
- Clean Code.
- Least Privilege.
- Secure by Design.
- Testability.
- Maintainability.
- Observability.

## 12.3. Aplicación contextual

No aplicar principios dogmáticamente.

Ejemplos:

- SOLID no significa crear interfaces para cada clase.
- DRY no significa centralizar todo en abstracciones complejas.
- KISS no significa ignorar requisitos de seguridad.
- Microservicios no son automáticamente mejores que un monolito modular.
- Clean Architecture no debe imponerse cuando agrega complejidad sin beneficio.

El harness debe justificar las decisiones importantes.

## 12.4. Niveles de reglas

**Global Policies**
- Restricciones obligatorias.
- Seguridad.
- TDD.
- Integridad.
- Auditoría.

**Project Rules**
- Convenciones.
- Stack.
- Arquitectura.
- Nomenclatura.
- Organización.

**Skills**
- Procedimientos especializados.
- Conocimiento técnico.

**Workflow Policies**
- Reglas de ejecución.
- Transiciones.
- Validaciones.

Las reglas críticas deben implementarse en código ejecutable y verificable, no solamente en archivos Markdown.

---

# 13. Architecture Intelligence

## 13.1. Propósito

Proponer arquitecturas modernas, mantenibles, seguras y fáciles de evolucionar.

No limitarse a producir código funcional.

## 13.2. Criterios

Evaluar:

- Mantenibilidad.
- Escalabilidad.
- Seguridad.
- Rendimiento.
- Costos.
- Complejidad operativa.
- Facilidad de pruebas.
- Observabilidad.
- Despliegue.
- Madurez tecnológica.
- Disponibilidad de talento.
- Evolución futura.

## 13.3. Patrones y arquitecturas

Conocer y evaluar:

- Clean Architecture.
- Hexagonal Architecture.
- Modular Monolith.
- Microservices.
- Vertical Slice Architecture.
- CQRS.
- Event-Driven Architecture.
- Domain-Driven Design.
- Layered Architecture.
- Serverless.
- Ports and Adapters.

## 13.4. Recomendaciones

No recomendar una arquitectura por moda.

Por ejemplo, para una aplicación SaaS nueva, considerar un monolito modular antes de distribuir prematuramente el sistema en múltiples microservicios.

Cada decisión arquitectónica importante debe producir un ADR con:

- Contexto.
- Problema.
- Alternativas.
- Decisión.
- Justificación.
- Ventajas.
- Desventajas.
- Consecuencias.
- Riesgos.
- Fecha.
- Responsable.

---

# 14. Security & Secrets Engine

## 14.1. Principios

- Least Privilege.
- Fail Closed.
- Secure by Default.
- Defense in Depth.
- Secret Isolation.
- Auditability.
- Supply Chain Security.

## 14.2. Protección de credenciales

Reglas obligatorias:

- Nunca almacenar credenciales reales en archivos versionados.
- No incluir contraseñas, tokens, API Keys o certificados privados en appsettings.json, settings.json, YAML, JSON, Markdown o código fuente.
- Utilizar variables de entorno, secret managers o mecanismos equivalentes.
- Excluir archivos .env locales de Git.
- Permitir .env.example con nombres de variables y valores ficticios.
- No registrar secretos en logs.
- No copiar secretos a la memoria.
- No enviar secretos a servicios externos sin autorización.
- Escanear secretos antes de commits y PR.
- Bloquear operaciones que expongan credenciales.

Cuando se detecte un secreto expuesto, recomendar revocación y rotación.

## 14.3. Entornos

Local:
- Variables de entorno.
- Secret manager local.

Development:
- Secret manager o variables protegidas.

Testing:
- Credenciales aisladas y datos de prueba.

Staging:
- Secret manager del proveedor.

Production:
- Azure Key Vault.
- AWS Secrets Manager.
- OCI Vault.
- HashiCorp Vault.
- Workload Identity o identidad administrada cuando esté disponible.

## 14.4. Otras reglas de seguridad

- Secret scanning.
- Dependency scanning.
- SBOM.
- License scanning.
- Protección contra prompt injection.
- Aislamiento de agentes.
- Restricción de rutas.
- Control de permisos.
- Auditoría de herramientas.
- Protección de datos sensibles.
- Validación de argumentos MCP.
- Límites de ejecución.
- Revisión de operaciones destructivas.

## 14.5. Operaciones que requieren autorización

- DROP DATABASE.
- DROP TABLE.
- Borrado masivo.
- Migraciones destructivas en producción.
- Despliegues productivos.
- Cambios de permisos.
- Eliminación de credenciales.
- Rotación de secretos.
- Force push.
- Eliminación de ramas protegidas.
- Cambios de infraestructura productiva.

El permiso de modificar código no implica permiso para ejecutar operaciones destructivas externas.

---

# 15. Quality Engine

Debe evaluar independientemente el resultado del trabajo.

Controles:

- Compilación.
- Unit Tests.
- Integration Tests.
- Contract Tests.
- E2E Tests.
- Coverage.
- Mutation Testing.
- Static Analysis.
- Formatting.
- Lint.
- Security Scanning.
- Dependency Audit.
- Performance.
- Accessibility.
- Visual Regression.

Estados:

- PASS.
- WARN.
- FAIL.
- NOT_APPLICABLE.

Un resultado crítico FAIL bloquea la entrega.

Una buena puntuación general nunca puede compensar una vulnerabilidad crítica.

La revisión debe ser independiente del agente implementador.

---

# 16. UI/UX Engineering

## 16.1. Objetivo

Producir interfaces profesionales y consistentes, no únicamente páginas que funcionen.

## 16.2. Proceso

1. Research.
2. Information Architecture.
3. User Flows.
4. Wireframes.
5. Visual Design.
6. Design System.
7. Implementation.
8. Browser QA.
9. Visual QA.
10. Accessibility Review.

## 16.3. Validaciones

- Responsive.
- Overflow.
- Clipping.
- Typography.
- Spacing.
- Contrast.
- Navigation.
- Form States.
- Empty States.
- Loading States.
- Error States.
- Accessibility.
- Usability.
- Visual Consistency.

Herramientas potenciales:

- Playwright.
- Chrome DevTools.
- Lighthouse.
- axe-core.
- Visual Regression.

Las herramientas deben seleccionarse según el stack y las capacidades verificadas.

El diseño visual debe revisarse independientemente de las pruebas funcionales.

---

# 17. MCP Manager

## 17.1. Propósito

Administrar integraciones con herramientas externas mediante Model Context Protocol.

## 17.2. Integraciones posibles

- GitHub.
- GitLab.
- Azure DevOps.
- Playwright.
- Chrome DevTools.
- Figma.
- PostgreSQL.
- SQL Server.
- MongoDB.
- Context7.
- Filesystem.
- Docker.
- Kubernetes.
- AWS.
- Azure.
- OCI.
- Grafana.
- Sentry.
- SonarQube.
- Jira.
- Linear.

No asumir que todos los proveedores tienen una implementación oficial y mantenida.

Antes de incorporar una integración, verificar su origen, mantenimiento, permisos, documentación y compatibilidad.

## 17.3. Seguridad

- Catálogo central.
- Configuración por proyecto.
- Configuración por agente.
- Permisos mínimos.
- Separación lectura/escritura.
- Credenciales fuera de configuraciones compartidas.
- Validación de argumentos.
- Logs.
- Timeouts.
- Límites.
- Versiones.
- Aprobación de operaciones destructivas.
- Detección de servidores no autorizados.

---

# 18. Hooks Manager

Debe integrar los hooks nativos disponibles en Antigravity.

Eventos candidatos a investigar y soportar según la versión real:

- SessionStart.
- PreInvocation.
- PreToolUse.
- PostToolUse.
- PostInvocation.
- Stop.

La disponibilidad, nomenclatura y contratos de cada evento deben validarse en la documentación oficial.

## 18.1. Antes de modificar

- Verificar tarea activa.
- Verificar autorización.
- Verificar workflow.
- Verificar fase TDD.
- Verificar evidencia RED cuando corresponda.
- Verificar permisos.

## 18.2. Después de modificar

- Registrar archivos afectados.
- Registrar cambios.
- Detectar pruebas pendientes.
- Ejecutar validaciones aplicables.
- Actualizar estado.
- Persistir auditoría.

## 18.3. Antes de terminar

- Revisar criterios.
- Verificar quality gates.
- Ejecutar revisión independiente.
- Comprobar evidencias.
- Identificar errores bloqueantes.
- Validar estado de entrega.

Los hooks no deben ser el único mecanismo de enforcement. Las autorizaciones críticas deben pasar por Governance Engine.

---

# 19. Documentation Engine

Debe mantener documentación técnica coherente con el código.

Artefactos:

- README.
- Architecture Overview.
- ADR.
- C4 Diagrams.
- API Documentation.
- Database Documentation.
- Setup Guides.
- Deployment Guides.
- Runbooks.
- Security Documentation.
- Troubleshooting.
- Changelog.
- Release Notes.

Cuando cambie un componente, el sistema debe evaluar qué documentación necesita actualizarse.

No generar documentación ficticia ni afirmar que una funcionalidad existe si no está implementada.

---

# 20. Audit Engine

Registrar:

- Usuario.
- Proyecto.
- Sesión.
- Task ID.
- Workflow.
- Agente.
- Acción.
- Herramienta.
- Archivos afectados.
- Cambios.
- Decisiones.
- Autorizaciones.
- Pruebas.
- Resultados.
- Commits.
- PR.
- Errores.
- Timestamps.

La auditoría debe ser consultable y no depender de la memoria conversacional.

Los registros deben evitar almacenar secretos.

---

# 21. Observability & Resource Management

Monitorear:

- Tiempo por tarea.
- Tiempo por workflow.
- Ejecuciones.
- Reintentos.
- Errores.
- Tokens cuando el runtime los exponga.
- Costos cuando sean medibles.
- Herramientas utilizadas.
- Agentes utilizados.
- Fallos de herramientas.
- Tareas bloqueadas.
- Ejecuciones detenidas.
- Consumo de recursos.

Controles:

- Token budgets.
- Timeouts.
- Límites de paralelismo.
- Checkpoints.
- Retry with backoff.
- Circuit breakers.
- Cancelación.
- Idempotencia.
- Detección de tareas estancadas.

No inventar métricas que el runtime no proporcione.

---

# 22. Parallel Execution & Git Worktrees

La ejecución paralela debe estar controlada por dependencias y conflictos potenciales.

Reglas:

- Paralelizar solo actividades independientes.
- Evitar agentes modificando los mismos archivos.
- Establecer contratos de entrada y salida.
- Utilizar worktrees cuando corresponda.
- Asignar un integrador responsable.
- Detectar conflictos.
- Ejecutar pruebas integrales.
- Verificar que ninguna tarea se haya perdido.

La ejecución paralela no debe aumentar la complejidad ni comprometer la integridad del proyecto.

---

# 23. Evaluation & Continuous Improvement

Se deben evaluar dos niveles:

## 23.1. Calidad del trabajo

- Criterios cumplidos.
- Tests.
- Cobertura.
- Defectos.
- Revisiones.
- Vulnerabilidades.
- Retrabajo.
- Tiempo.
- Evidencias.

## 23.2. Calidad del harness

- Clasificación correcta.
- Workflows exitosos.
- Cumplimiento TDD.
- Calidad de delegación.
- Calidad de recomendaciones.
- Recuperación de sesiones.
- Errores de herramientas.
- Falsos positivos.
- Falsos negativos.
- Consumo de recursos.

Los agentes no pueden modificar sus propios criterios de evaluación ni aprobarse a sí mismos.

---

# 24. Project Health Engine

Debe proporcionar una visión confiable del estado del proyecto.

Información consultable:

- Historias terminadas.
- Historias pendientes.
- Tareas en ejecución.
- Tareas bloqueadas.
- Dependencias pendientes.
- PR abiertos.
- PR integrados.
- Pruebas fallidas.
- Vulnerabilidades.
- Deuda técnica.
- Decisiones pendientes.
- Hitos.
- Riesgos.
- Porcentaje de avance calculado a partir de criterios explícitos.

Debe distinguir progreso de actividad: escribir mucho código no significa necesariamente que el proyecto esté más cerca de completarse.

---

# 25. Configuración inicial de proyectos

Al iniciar un proyecto, el harness debe realizar un proceso de discovery proporcional a su tamaño.

Identificar:

1. Nombre y objetivo.
2. Tipo de proyecto.
3. Stack.
4. Lenguajes.
5. Frameworks.
6. Bases de datos.
7. Arquitectura existente.
8. Estructura del repositorio.
9. Convenciones.
10. Pruebas.
11. Infraestructura.
12. CI/CD.
13. Git.
14. Proveedor remoto.
15. Rama principal.
16. Estrategia de ramas.
17. Políticas de PR.
18. Reglas de seguridad.
19. Entornos.
20. Documentación existente.

No volver a preguntar información que ya pueda detectar de manera confiable.

Si existen decisiones importantes sin definir, presentar las preguntas necesarias de manera progresiva.

No bloquear el inicio de una investigación por información que todavía no es necesaria.

---

# 26. Arquitectura técnica inicial

## 26.1. Stack propuesto

- Python.
- SDK oficial de Antigravity, si se confirma disponibilidad y compatibilidad.
- Pydantic.
- asyncio.
- SQLite.
- SQLAlchemy o acceso SQL directo.
- structlog.
- YAML.
- JSON.
- Typer.
- pytest.
- JSON Schema.
- MCP.
- GitPython o Git CLI.

La integración con el SDK debe estar detrás de un adapter.

No depender de interfaces internas o no documentadas.

La elección final de versiones y dependencias debe realizarse en la fase de investigación técnica.

## 26.2. Persistencia

Primera versión:

- SQLite para entidades operativas.
- JSON/YAML para configuración.
- Markdown para documentación.
- Índice semántico opcional.

Los contratos deben permitir evolucionar el almacenamiento.

---

# 27. Estructura inicial del repositorio

```text
dh-engineering-harness/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
├── AGENTS.md
├── GEMINI.md
│
├── .agents/
│   ├── rules/
│   ├── agents/
│   ├── skills/
│   ├── hooks.json
│   └── mcp_config.json
│
├── src/
│   └── dh_harness/
│       ├── core/
│       ├── sdk/
│       ├── interaction/
│       ├── orchestrator/
│       ├── governance/
│       ├── agents/
│       ├── skills/
│       ├── workflows/
│       ├── tdd/
│       ├── tasks/
│       ├── planning/
│       ├── dependencies/
│       ├── continuity/
│       ├── checkpoints/
│       ├── memory/
│       ├── quality/
│       ├── architecture/
│       ├── git/
│       ├── repositories/
│       ├── security/
│       ├── secrets/
│       ├── hooks/
│       ├── mcp/
│       ├── documentation/
│       ├── audit/
│       ├── observability/
│       ├── recovery/
│       ├── project_health/
│       ├── integrations/
│       ├── configuration/
│       └── cli/
│
├── config/
│   ├── defaults.yaml
│   ├── policies.yaml
│   ├── quality-gates.yaml
│   ├── agent-catalog.yaml
│   └── technology-profiles/
│
├── workflows/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── security/
│   └── e2e/
│
├── scripts/
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── guides/
│   ├── reference/
│   └── operations/
│
└── examples/
```

La estructura es una propuesta inicial. Debe validarse durante el diseño detallado para evitar módulos vacíos, duplicación de responsabilidades y complejidad prematura.

Las convenciones de archivos nativos de Antigravity deben confirmarse contra la documentación vigente antes de implementarlas.

---

# 28. Roadmap de implementación

Se propone construir el sistema incrementalmente.

## Fase 0. Foundation & Technical Research

Objetivos:
- Investigar Antigravity.
- Validar SDK y CLI.
- Verificar capacidades nativas.
- Confirmar hooks.
- Confirmar skills.
- Confirmar agentes.
- Confirmar MCP.
- Definir contratos.
- Definir arquitectura.
- Definir políticas.
- Preparar repositorio.

Entregables:
- Technical Research Report.
- Architecture Overview.
- ADR iniciales.
- Repository Structure.
- Core Contracts.
- Initial Backlog.

No asumir que las APIs propuestas existen hasta verificarlas.

## Fase 1. Core Harness

Implementar:
- Core.
- Orchestrator.
- Governance.
- Task Manager.
- Persistence.
- Registry.
- State Machine.
- Audit.
- CLI.

## Fase 2. Mandatory TDD

Implementar:
- TDD Engine.
- Evidencias.
- Validadores.
- Quality Gates.
- Enforcement.
- Pruebas negativas.

Criterio crítico: impedir modificaciones de código que requieren TDD cuando no existe evidencia RED válida.

## Fase 3. Interaction & Planning

Implementar:
- Clasificador.
- Modos de operación.
- Planificación proporcional.
- Dependency Graph.
- Task Management.
- Recomendaciones.

## Fase 4. Memory & Continuity

Implementar:
- Memory Engine.
- Checkpoints.
- Recovery.
- Project Continuity.
- Historial.
- Estado del proyecto.

## Fase 5. Agent Ecosystem

Implementar:
- Agent Registry.
- Agentes principales.
- Delegación.
- Contratos.
- Permisos.
- Evaluación.

Ampliar el catálogo progresivamente.

## Fase 6. Skills & Workflows

Implementar:
- Skills Registry.
- Skills base.
- Workflow Engine.
- Workflows principales.
- Validadores.

## Fase 7. Git & Repository Governance

Implementar:
- Git Manager.
- Repository Discovery.
- Branch Policies.
- Commit Policies.
- PR Integration.
- Git Worktrees.
- Delivery Tracking.

## Fase 8. Security, Hooks & MCP

Implementar:
- Secrets Engine.
- Security Policies.
- Hooks Manager.
- MCP Manager.
- Approval Gates.
- Secret Scanning.

## Fase 9. Quality, UI/UX & Architecture Intelligence

Implementar:
- Quality Engine avanzado.
- UI/UX workflows.
- Visual QA.
- Architecture Intelligence.
- ADR automation.
- Documentation Engine.

## Fase 10. Advanced Engineering & Hardening

Implementar:
- Parallel Execution.
- Advanced Observability.
- Recovery avanzado.
- Project Health.
- Continuous Improvement.
- Benchmarking.
- Security hardening.
- Release.

---

# 29. Criterios de aceptación globales

El harness se considerará funcionalmente preparado cuando pueda demostrar los siguientes escenarios:

### Interacción

- Responder preguntas conceptuales sin crear workflows innecesarios.
- Investigar errores sin modificar código.
- Diferenciar investigar de corregir.
- Transicionar entre modos conservando contexto.

### TDD

- Crear una prueba de regresión.
- Verificar RED.
- Implementar.
- Verificar GREEN.
- Detectar pruebas falsas.
- Bloquear cambios que incumplan el proceso.

### Gestión de tareas

- Crear épicas, historias y subtareas.
- Persistir estados.
- Registrar dependencias.
- Detectar bloqueos.
- Impedir cierres inválidos.
- Recuperar trabajo interrumpido.

### Continuidad

- Preguntar con qué continuar.
- Mostrar qué se terminó.
- Mostrar qué está pendiente.
- Identificar tareas ejecutables.
- Recomendar la siguiente tarea.
- Presentar opciones paralelizables.
- Permitir que el usuario seleccione.
- Recuperar checkpoints.

### Git

- Detectar repositorios.
- Identificar proveedores.
- Consultar ramas.
- Crear ramas de trabajo.
- Crear commits.
- Preparar PR.
- Consultar su estado.
- Verificar integración.
- Actualizar historias.

### Seguridad

- Detectar secretos.
- Bloquear exposición de credenciales.
- Aplicar permisos mínimos.
- Solicitar aprobación para operaciones críticas.
- Auditar operaciones.

### Calidad

- Ejecutar pruebas.
- Ejecutar análisis.
- Verificar criterios.
- Revisar código independientemente.
- Bloquear entregas con fallos críticos.

### Arquitectura

- Evaluar alternativas.
- Justificar decisiones.
- Generar ADR.
- Evitar complejidad innecesaria.
- Recomendar soluciones mantenibles.

---

# 30. Reglas de implementación del propio harness

El desarrollo de DH Engineering Harness debe estar sujeto a las mismas políticas que impondrá a los proyectos que administre.

Por tanto:

1. El harness debe construirse utilizando TDD.
2. Debe tener pruebas unitarias, de integración y de contrato.
3. Las reglas de gobernanza deben probarse con escenarios positivos y negativos.
4. No se deben implementar APIs del SDK sin verificar su documentación.
5. No se deben crear agentes, skills o módulos vacíos solamente para completar la estructura.
6. Cada módulo debe tener una responsabilidad clara.
7. Los contratos deben definirse antes de implementar integraciones complejas.
8. La arquitectura debe evolucionar con ADR.
9. La documentación debe acompañar la implementación.
10. Cada fase debe tener criterios de aceptación.
11. Las tareas deben registrarse en el Task Management Engine cuando esté disponible.
12. El repositorio debe utilizar ramas y PR según su política.
13. No declarar terminada una fase por haber creado archivos: debe existir funcionalidad y evidencia.
14. Evitar dependencias innecesarias.
15. Priorizar soluciones sencillas, mantenibles y extensibles.

---

# 31. Decisiones arquitectónicas pendientes de investigación

Los siguientes puntos requieren una decisión fundamentada antes de implementación:

1. Capacidades y limitaciones reales del SDK de Antigravity.
2. Integración entre runtime nativo y orquestación externa.
3. Contratos y eventos reales de hooks.
4. Formato nativo de agentes y skills.
5. Configuración MCP soportada.
6. Límites de concurrencia.
7. Persistencia y recuperación de sesiones.
8. Disponibilidad de información de uso y costos.
9. Mecanismo de permisos y aprobación.
10. Integraciones oficiales con GitHub, Azure DevOps, GitLab y Bitbucket.
11. Estrategia de aislamiento de agentes.
12. Estrategia de ejecución de comandos y herramientas.

Estas decisiones no deben resolverse mediante suposiciones.

---

# 32. Definición final del producto

DH Engineering Harness debe convertirse en una plataforma de ingeniería asistida por agentes capaz de gestionar el ciclo completo de desarrollo de software.

Debe poder responder como un experto cuando el usuario pregunta, investigar como un arquitecto cuando necesita comprender un problema, corregir como un ingeniero disciplinado cuando solicita un bugfix y operar como un equipo de ingeniería cuando desarrolla funcionalidades o productos completos.

Debe recordar dónde quedó cada proyecto, organizar su trabajo, identificar qué falta, recomendar qué hacer, ejecutar tareas secuenciales o paralelas, controlar calidad, proteger recursos y garantizar que las entregas sean verificables.

El usuario no debería tener que administrar manualmente el proceso de ingeniería.

El harness debe encargarse de la organización, coordinación y control, manteniendo al usuario como responsable de las decisiones que requieren su criterio o autorización.

**Principio final:**

> No queremos agentes que simplemente escriban código. Queremos un sistema de ingeniería que comprenda, planifique, ejecute, verifique, documente, recuerde y entregue software de calidad, de manera disciplinada, segura y sostenible.
