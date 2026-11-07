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

class AgentRole(str, Enum):
    ORCHESTRATOR = "ORCHESTRATOR"
    SOLUTION_ARCHITECT = "SOLUTION_ARCHITECT"
    BACKEND_DEVELOPER = "BACKEND_DEVELOPER"
    FRONTEND_DEVELOPER = "FRONTEND_DEVELOPER"
    DATABASE_ENGINEER = "DATABASE_ENGINEER"
    SECURITY_ENGINEER = "SECURITY_ENGINEER"
    CODE_REVIEWER = "CODE_REVIEWER"
    QA_ENGINEER = "QA_ENGINEER"
    TECHNICAL_WRITER = "TECHNICAL_WRITER"

class ToolPermission(str, Enum):
    READ_ONLY = "READ_ONLY"
    FILE_WRITE = "FILE_WRITE"
    RUN_COMMAND = "RUN_COMMAND"
    TERMINAL_SANDBOX = "TERMINAL_SANDBOX"
    GIT_OPERATIONS = "GIT_OPERATIONS"
    MCP_TOOLS = "MCP_TOOLS"

class AgentDefinition(BaseModel):
    id: str
    name: str
    role: AgentRole
    description: str = ""
    allowed_tools: List[ToolPermission] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    evaluation_criteria: List[str] = Field(default_factory=list)
    system_prompt_template: str = ""

class AgentTaskContract(BaseModel):
    task_id: str
    agent_id: str
    objective: str
    context: Dict[str, Any] = Field(default_factory=dict)
    input_artifacts: List[str] = Field(default_factory=list)
    expected_outputs: List[str] = Field(default_factory=list)

class AgentExecutionResult(BaseModel):
    task_id: str
    agent_id: str
    status: str
    changes_made: List[str] = Field(default_factory=list)
    tests_run: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    output_artifacts: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)

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

class MemoryLevel(str, Enum):
    GLOBAL = "GLOBAL"
    PROJECT = "PROJECT"
    TASK = "TASK"
    SESSION = "SESSION"
    KNOWLEDGE = "KNOWLEDGE"

class SessionCheckpoint(BaseModel):
    session_id: str
    active_task_id: Optional[str] = None
    active_branch: str = "main"
    recent_actions: List[str] = Field(default_factory=list)
    pending_steps: List[str] = Field(default_factory=list)
    created_at: str = ""
    checksum: str = ""

class KnowledgeItem(BaseModel):
    key: str
    category: str
    summary: str
    content: str
    tags: List[str] = Field(default_factory=list)

class SkillCategory(str, Enum):
    ENGINEERING_CORE = "ENGINEERING_CORE"
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    DATABASE = "DATABASE"
    UI_UX = "UI_UX"
    TESTING = "TESTING"
    SECURITY = "SECURITY"
    DEVOPS = "DEVOPS"
    ARCHITECTURE = "ARCHITECTURE"

class SkillDefinition(BaseModel):
    id: str
    name: str
    category: SkillCategory
    description: str = ""
    triggers: List[str] = Field(default_factory=list)
    anti_triggers: List[str] = Field(default_factory=list)
    required_tools: List[ToolPermission] = Field(default_factory=list)
    guidelines: List[str] = Field(default_factory=list)

class WorkflowStage(BaseModel):
    id: str
    name: str
    required_role: AgentRole
    required_skills: List[str] = Field(default_factory=list)
    is_mandatory: bool = True
    depends_on: List[str] = Field(default_factory=list)

class WorkflowDefinition(BaseModel):
    id: str
    name: str
    description: str = ""
    stages: List[WorkflowStage] = Field(default_factory=list)

class WorkflowExecutionResult(BaseModel):
    workflow_id: str
    task_id: str
    status: str
    completed_stages: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

class GitProvider(str, Enum):
    GITHUB = "GITHUB"
    AZURE_DEVOPS = "AZURE_DEVOPS"
    GITLAB = "GITLAB"
    BITBUCKET = "BITBUCKET"
    LOCAL = "LOCAL"

class RepoDiagnostics(BaseModel):
    is_git: bool
    active_branch: str
    remote_provider: GitProvider
    remote_url: Optional[str] = None
    is_clean: bool = True
    modified_files: List[str] = Field(default_factory=list)
    untracked_files: List[str] = Field(default_factory=list)

class DoDVerificationResult(BaseModel):
    task_id: str
    satisfied: bool
    missing_criteria: List[str] = Field(default_factory=list)
    evidence_collected: List[str] = Field(default_factory=list)

class SecuritySeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class SecretFinding(BaseModel):
    file_path: str
    line_number: int
    secret_type: str
    snippet_redacted: str
    severity: SecuritySeverity = SecuritySeverity.HIGH

class LicenseAuditFinding(BaseModel):
    package_name: str
    version: str
    license_spdx: str
    is_allowed: bool
    risk_level: str

class DestructiveOpCheckResult(BaseModel):
    command: str
    is_destructive: bool
    operation_type: Optional[str] = None
    reason: str = ""
