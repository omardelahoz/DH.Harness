import pytest
from dh_harness.core.contracts import InteractionMode
from dh_harness.interaction.classifier import classify_interaction

def test_classify_conversational():
    prompts = [
        "¿Cómo funciona la inyección de dependencias en .NET?",
        "Explícame la diferencia entre CQRS y arquitectura hexagonal",
        "¿Qué patrones de diseño me recomiendas para este caso?",
    ]
    for prompt in prompts:
        result = classify_interaction(prompt)
        assert result.mode == InteractionMode.CONVERSATIONAL
        assert result.tdd_required is False

def test_classify_investigation():
    prompts = [
        "Investiga por qué la aplicación tiene alto consumo de memoria",
        "Analiza el rendimiento de esta consulta SQL y diagnostica",
        "Revisa posibles vulnerabilidades en las dependencias",
    ]
    for prompt in prompts:
        result = classify_interaction(prompt)
        assert result.mode == InteractionMode.INVESTIGATION
        assert result.tdd_required is False

def test_classify_bug_fix():
    prompts = [
        "Corrige el bug en el login cuando el token expira",
        "Hay un error de NullReferenceException al procesar el pago, soluciónalo",
        "Fix the issue where items are not persisted in SQLite",
    ]
    for prompt in prompts:
        result = classify_interaction(prompt)
        assert result.mode == InteractionMode.BUG_FIX
        assert result.tdd_required is True

def test_classify_development():
    prompts = [
        "Implementa un nuevo endpoint para listar usuarios activos",
        "Agrega la funcionalidad de exportar reportes a CSV",
        "Crea el componente de formulario de registro",
    ]
    for prompt in prompts:
        result = classify_interaction(prompt)
        assert result.mode == InteractionMode.DEVELOPMENT
        assert result.tdd_required is True

def test_classify_complex_engineering():
    prompts = [
        "Diseña y construye una nueva plataforma de microservicios distribuidos",
        "Migración completa de arquitectura monolítica a arquitectura event-driven",
        "Nuevo producto SaaS con autenticación multi-tenant y pagos",
    ]
    for prompt in prompts:
        result = classify_interaction(prompt)
        assert result.mode == InteractionMode.COMPLEX_ENGINEERING
        assert result.tdd_required is True
