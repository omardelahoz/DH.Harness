import pytest
from dh_harness.core.contracts import InteractionMode, TaskState
from dh_harness.orchestrator.master import MasterOrchestrator
from dh_harness.workflows.engine import (
    BugFixWorkflow,
    FeatureDevelopmentWorkflow,
    InvestigationWorkflow,
)

def test_workflow_engine_selection():
    orchestrator = MasterOrchestrator()
    wf_bug = orchestrator.select_workflow(InteractionMode.BUG_FIX)
    assert isinstance(wf_bug, BugFixWorkflow)
    assert wf_bug.mode == InteractionMode.BUG_FIX

    wf_dev = orchestrator.select_workflow(InteractionMode.DEVELOPMENT)
    assert isinstance(wf_dev, FeatureDevelopmentWorkflow)

    wf_inv = orchestrator.select_workflow(InteractionMode.INVESTIGATION)
    assert isinstance(wf_inv, InvestigationWorkflow)

def test_master_orchestrator_process_bugfix():
    orchestrator = MasterOrchestrator()
    prompt = "Corrige el fallo en el cálculo de impuestos cuando la tasa es cero"
    response = orchestrator.handle_prompt(prompt)

    assert response["mode"] == InteractionMode.BUG_FIX.value
    assert response["tdd_required"] is True
    assert "workflow" in response
    assert response["workflow"] == "BugFixWorkflow"
    assert response["status"] == "READY_FOR_EXECUTION"

def test_master_orchestrator_process_conversational():
    orchestrator = MasterOrchestrator()
    prompt = "¿Qué ventajas tiene Clean Architecture frente a MVC tradicional?"
    response = orchestrator.handle_prompt(prompt)

    assert response["mode"] == InteractionMode.CONVERSATIONAL.value
    assert response["tdd_required"] is False
    assert response["status"] == "ANSWERED_DIRECTLY"
