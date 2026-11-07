import pytest
from dh_harness.core.contracts import ADRStatus
from dh_harness.docs.engine import ADRManager

def test_adr_manager_lists_existing_adrs():
    manager = ADRManager(docs_dir="docs/decisions")
    adrs = manager.list_adrs()

    assert len(adrs) >= 11
    assert adrs[0].number == 1
    assert "tdd" in adrs[0].title.lower()
    assert any(a.number == 11 for a in adrs)

def test_adr_manager_calculates_next_number():
    manager = ADRManager(docs_dir="docs/decisions")
    next_num = manager.get_next_adr_number()

    assert next_num >= 12

def test_adr_manager_creates_and_parses_new_adr(tmp_path):
    manager = ADRManager(docs_dir=str(tmp_path))

    adr = manager.create_adr(
        title="Event-Driven Microservices Architecture",
        context="We need to decouple ingestion from background processing.",
        decision="Adopt RabbitMQ native client for event bus.",
        consequences="Lower coupling, async scalability, message queuing.",
        status=ADRStatus.ACCEPTED
    )

    assert adr.number == 1
    assert "event-driven" in adr.path.lower()
    assert (tmp_path / f"ADR-001-event-driven-microservices-architecture.md").exists()

    # Re-read
    reloaded = manager.list_adrs()
    assert len(reloaded) == 1
    assert reloaded[0].title == "Event-Driven Microservices Architecture"
    assert reloaded[0].status == ADRStatus.ACCEPTED
    assert "decouple" in reloaded[0].context

def test_adr_manager_validates_required_sections():
    manager = ADRManager()

    valid_md = """# ADR-001: Example
## Estado
Aprobado
## Contexto
Background info
## Decisión
We decided X
## Consecuencias
Outcome Y
"""
    assert manager.validate_adr_content(valid_md) is True

    invalid_md = """# ADR-001: Bad ADR
Just some plain text without headers.
"""
    assert manager.validate_adr_content(invalid_md) is False
