from __future__ import annotations
from typing import Dict, Any, Optional
from dh_harness.core.contracts import InteractionMode
from dh_harness.interaction.classifier import classify_interaction
from dh_harness.tasks.manager import TaskManager
from dh_harness.continuity.engine import ContinuityEngine
from dh_harness.workflows.engine import (
    BaseWorkflow,
    BugFixWorkflow,
    FeatureDevelopmentWorkflow,
    InvestigationWorkflow,
)

class MasterOrchestrator:
    """
    Chief Orchestrator coordinating interaction classification, workflow selection,
    task scheduling, and continuity. Complies with Section 3 of info.md.
    """

    def __init__(self, task_manager: Optional[TaskManager] = None):
        self.task_manager = task_manager or TaskManager()
        self.continuity_engine = ContinuityEngine(self.task_manager)
        self._workflows = {
            InteractionMode.BUG_FIX: BugFixWorkflow(),
            InteractionMode.DEVELOPMENT: FeatureDevelopmentWorkflow(),
            InteractionMode.INVESTIGATION: InvestigationWorkflow(),
            InteractionMode.COMPLEX_ENGINEERING: FeatureDevelopmentWorkflow(),
        }

    def select_workflow(self, mode: InteractionMode) -> Optional[BaseWorkflow]:
        """Selects the corresponding workflow based on interaction mode."""
        return self._workflows.get(mode)

    def handle_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Receives user prompt, classifies the request, determines required rigor and workflow.
        """
        classification = classify_interaction(prompt)
        workflow = self.select_workflow(classification.mode)

        if classification.mode == InteractionMode.CONVERSATIONAL:
            return {
                "prompt": prompt,
                "mode": classification.mode.value,
                "tdd_required": False,
                "workflow": None,
                "status": "ANSWERED_DIRECTLY",
                "message": "Conversational request resolved directly without heavy formal tasks."
            }

        return {
            "prompt": prompt,
            "mode": classification.mode.value,
            "tdd_required": classification.tdd_required,
            "workflow": workflow.name if workflow else None,
            "status": "READY_FOR_EXECUTION",
            "message": f"Workflow '{workflow.name if workflow else 'None'}' selected. Strict TDD: {classification.tdd_required}."
        }
