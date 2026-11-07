from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InteractionMode(str, Enum):
    CONVERSATIONAL = "CONVERSATIONAL"
    INVESTIGATION = "INVESTIGATION"
    BUG_FIX = "BUG_FIX"
    DEVELOPMENT = "DEVELOPMENT"
    COMPLEX_ENGINEERING = "COMPLEX_ENGINEERING"

class TDDPhase(str, Enum):
    REQUIREMENT = "REQUIREMENT"
    TEST_RED = "TEST_RED"
    IMPLEMENT_GREEN = "IMPLEMENT_GREEN"
    REFACTOR = "REFACTOR"
    VERIFY = "VERIFY"
    DONE = "DONE"

class ClassificationResult(BaseModel):
    mode: InteractionMode
    tdd_required: bool
    confidence: float = 1.0
    rationale: str = ""
    suggested_workflow: str = ""

class TaskStep(BaseModel):
    order: int
    command: str
    verifier_expr: Optional[str] = None
    status: str = "PENDING"
    stdout: Optional[str] = None
    stderr: Optional[str] = None

class TaskDefinition(BaseModel):
    id: Optional[int] = None
    title: str
    description: str = ""
    mode: InteractionMode = InteractionMode.DEVELOPMENT
    status: str = "PENDING"
    steps: List[TaskStep] = Field(default_factory=list)

class QualityGateResult(BaseModel):
    gate_name: str
    passed: bool
    details: Dict[str, Any] = Field(default_factory=dict)
    message: str = ""
