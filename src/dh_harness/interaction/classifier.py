import re
from dh_harness.core.contracts import InteractionMode, ClassificationResult

def classify_interaction(prompt: str) -> ClassificationResult:
    """
    Classifies a user prompt into one of the 5 canonical interaction modes:
    - CONVERSATIONAL
    - INVESTIGATION
    - BUG_FIX
    - DEVELOPMENT
    - COMPLEX_ENGINEERING
    """
    text = prompt.lower().strip()

    # COMPLEX_ENGINEERING triggers
    complex_triggers = [
        "nueva plataforma", "nuevo producto", "arquitectura distribuida",
        "microservicios distribuidos", "transformación tecnológica",
        "migración completa", "event-driven", "sistema distribuido",
        "new platform", "new product", "distributed architecture", "complete migration"
    ]
    if any(k in text for k in complex_triggers):
        return ClassificationResult(
            mode=InteractionMode.COMPLEX_ENGINEERING,
            tdd_required=True,
            confidence=0.95,
            rationale="High complexity scope affecting multiple domains/architectural layers.",
            suggested_workflow="complex_engineering_workflow"
        )

    # BUG_FIX triggers
    bug_triggers = [
        "bug", "error", "fallo", "corrige", "corregir", "soluciona", "solucionar",
        "crash", "fix", "issue", "nullreference", "excepción", "exception", "roto"
    ]
    if any(re.search(rf"\b{re.escape(k)}\b", text) for k in bug_triggers):
        return ClassificationResult(
            mode=InteractionMode.BUG_FIX,
            tdd_required=True,
            confidence=0.92,
            rationale="Identified explicit defect correction request.",
            suggested_workflow="bug_fixing_workflow"
        )

    # INVESTIGATION triggers
    investigation_triggers = [
        "investiga", "investigar", "diagnostica", "diagnosticar", "analiza el rendimiento",
        "troubleshooting", "análisis de rendimiento", "vulnerabilidades", "averigua",
        "investigate", "diagnose", "root cause", "causa raíz"
    ]
    if any(k in text for k in investigation_triggers):
        return ClassificationResult(
            mode=InteractionMode.INVESTIGATION,
            tdd_required=False,
            confidence=0.90,
            rationale="Diagnostic or troubleshooting request without executable code change authorization.",
            suggested_workflow="investigation_workflow"
        )

    # DEVELOPMENT triggers
    dev_triggers = [
        "implementa", "implementar", "agrega", "agregar", "crea", "crear",
        "desarrolla", "desarrollar", "nuevo endpoint", "nueva funcionalidad",
        "construye", "construir", "refactoriza", "feature", "endpoint"
    ]
    if any(k in text for k in dev_triggers):
        return ClassificationResult(
            mode=InteractionMode.DEVELOPMENT,
            tdd_required=True,
            confidence=0.88,
            rationale="Feature development or code modification requiring strict TDD.",
            suggested_workflow="feature_development_workflow"
        )

    # Default to CONVERSATIONAL
    return ClassificationResult(
        mode=InteractionMode.CONVERSATIONAL,
        tdd_required=False,
        confidence=0.85,
        rationale="General conceptual question or architectural discussion.",
        suggested_workflow="conversational_workflow"
    )
