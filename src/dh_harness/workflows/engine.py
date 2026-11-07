from __future__ import annotations
from typing import List, Dict, Any, Optional
from dh_harness.core.contracts import InteractionMode

class WorkflowStep:
    def __init__(self, order: int, name: str, description: str):
        self.order = order
        self.name = name
        self.description = description
        self.completed = False

class BaseWorkflow:
    def __init__(self, name: str, mode: InteractionMode, steps: List[WorkflowStep]):
        self.name = name
        self.mode = mode
        self.steps = steps

    def get_step(self, order: int) -> Optional[WorkflowStep]:
        for s in self.steps:
            if s.order == order:
                return s
        return None

class BugFixWorkflow(BaseWorkflow):
    def __init__(self):
        steps = [
            WorkflowStep(1, "Reproduce Defect", "Reproduce the issue and isolate root cause."),
            WorkflowStep(2, "Test RED", "Create a failing regression test capturing the defect."),
            WorkflowStep(3, "Implement GREEN", "Apply the minimal code change to satisfy the test."),
            WorkflowStep(4, "Refactor & Verify", "Clean up structure and verify all tests pass."),
            WorkflowStep(5, "Delivery Gate", "Audit quality gates and prepare for PR.")
        ]
        super().__init__("BugFixWorkflow", InteractionMode.BUG_FIX, steps)

class FeatureDevelopmentWorkflow(BaseWorkflow):
    def __init__(self):
        steps = [
            WorkflowStep(1, "Define Acceptance Criteria", "Document acceptance criteria and scope."),
            WorkflowStep(2, "Contract & Test RED", "Write contract specifications and failing tests."),
            WorkflowStep(3, "Implement GREEN", "Implement business logic and persistence."),
            WorkflowStep(4, "Quality Gates & Refactor", "Run static analysis, coverage, and security checks."),
            WorkflowStep(5, "PR & Documentation", "Update architecture documentation and open PR.")
        ]
        super().__init__("FeatureDevelopmentWorkflow", InteractionMode.DEVELOPMENT, steps)

class InvestigationWorkflow(BaseWorkflow):
    def __init__(self):
        steps = [
            WorkflowStep(1, "Define Hypothesis", "Specify research objective and hypothesis."),
            WorkflowStep(2, "Collect Evidence", "Inspect logs, performance profiles, or code without modifying files."),
            WorkflowStep(3, "Root Cause Report", "Present findings, root cause, and recommendations.")
        ]
        super().__init__("InvestigationWorkflow", InteractionMode.INVESTIGATION, steps)
