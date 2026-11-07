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

class TaskState(str, Enum):
    BACKLOG = "BACKLOG"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    IN_REVIEW = "IN_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    READY_FOR_PR = "READY_FOR_PR"
    PR_OPEN = "PR_OPEN"
    MERGED = "MERGED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

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

class HierarchicalTask(BaseModel):
    id: str
    title: str
    description: str = ""
    state: TaskState = TaskState.BACKLOG
    priority: int = 1
    mode: InteractionMode = InteractionMode.DEVELOPMENT
    epic_id: Optional[str] = None
    story_id: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    optional_dependencies: List[str] = Field(default_factory=list)
    assigned_agent: Optional[str] = None
    branch_name: Optional[str] = None
    pr_number: Optional[int] = None
    evidence: List[str] = Field(default_factory=list)

class ContinuityReport(BaseModel):
    completed_count: int = 0
    in_progress_count: int = 0
    pending_count: int = 0
    blocked_count: int = 0
    completed_tasks: List[str] = Field(default_factory=list)
    in_progress_tasks: List[str] = Field(default_factory=list)
    pending_tasks: List[str] = Field(default_factory=list)
    blocked_tasks: List[str] = Field(default_factory=list)
    parallel_candidates: List[str] = Field(default_factory=list)
    recommended_task: Optional[str] = None
    rationale: str = ""

class QualityGateResult(BaseModel):
    gate_name: str
    passed: bool
    details: Dict[str, Any] = Field(default_factory=dict)
    message: str = ""
