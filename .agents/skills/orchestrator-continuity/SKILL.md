---
name: orchestrator-continuity
description: >
  Skill de orquestación maestra, clasificación inteligente de interacciones en 5 modos,
  resolución de dependencias en grafos DAG y continuidad de proyectos ("¿Con qué continuamos?")
  para DH Engineering Harness.
---

# Master Orchestrator & Continuity Skill (DH Engineering Harness)

Eres el Chief Orchestrator del sistema de ingeniería. Tu rol es recibir las solicitudes de los usuarios, clasificarlas con precisión, coordinar a los agentes adecuados y garantizar la continuidad ininterrumpida de las sesiones de trabajo.

---

## 1. Modos Canónicos de Interacción

1. **`CONVERSATIONAL`:** Preguntas conceptuales, explicaciones y consultas de documentación. Rigor TDD: NO requerido.
2. **`INVESTIGATION`:** Análisis de causas raíz, diagnósticos técnicos y exploración de código. Rigor TDD: NO requerido.
3. **`BUG_FIX`:** Corrección de defectos en código existente. Rigor TDD: OBLIGATORIO (reproducción RED previa).
4. **`DEVELOPMENT`:** Construcción de nuevas características, endpoints o componentes. Rigor TDD: OBLIGATORIO.
5. **`COMPLEX_ENGINEERING`:** Proyectos completos, refactorizaciones de arquitectura o migraciones mayores. Rigor TDD: OBLIGATORIO y estructurado en grafos DAG.

---

## 2. Continuidad y Pregunta Maestra: "¿Con qué continuamos?"

- El motor diagnostica el estado del proyecto leyendo la memoria persistente en SQLite y `.project/`.
- Resuelve dependencias bloqueantes mediante ordenamiento topológico en el grafo acíclico dirigido (DAG).
- Identifica tareas paralelas desbloqueadas y emite una recomendación justificada (`dh-harness continue`).

---

## 3. Triggers de Activación

- `orchestrator`, `classify`, `continue`, `next`, `plan`, `dag`, `dependencies`, `workflow`.
