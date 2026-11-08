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
    MOBILE_DEVELOPER = "MOBILE_DEVELOPER"
    DEVOPS_ENGINEER = "DEVOPS_ENGINEER"

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
    MOBILE = "MOBILE"
    CLOUD = "CLOUD"

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

class QualityControlStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class QualityReport(BaseModel):
    task_id: str
    controls: Dict[str, QualityControlStatus] = Field(default_factory=dict)
    passed: bool = True
    critical_failures: List[str] = Field(default_factory=list)
    score: float = 100.0
    evaluated_by: str = ""
    timestamp: str = ""

class AccessibilityImpact(str, Enum):
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    SERIOUS = "SERIOUS"
    CRITICAL = "CRITICAL"

class AccessibilityViolation(BaseModel):
    rule_id: str
    element: str
    description: str
    impact: AccessibilityImpact = AccessibilityImpact.SERIOUS
    help_url: str = ""

class UIUXAuditReport(BaseModel):
    file_path: str
    responsive_ok: bool = True
    has_empty_states: bool = True
    has_loading_states: bool = True
    has_error_states: bool = True
    violations: List[AccessibilityViolation] = Field(default_factory=list)
    contrast_issues: List[str] = Field(default_factory=list)
    score: float = 100.0

class HookEventType(str, Enum):
    SESSION_START = "SESSION_START"
    PRE_INVOCATION = "PRE_INVOCATION"
    PRE_TOOL_USE = "PRE_TOOL_USE"
    POST_TOOL_USE = "POST_TOOL_USE"
    PRE_FILE_WRITE = "PRE_FILE_WRITE"
    POST_FILE_WRITE = "POST_FILE_WRITE"
    PRE_GIT_PUSH = "PRE_GIT_PUSH"
    ON_TASK_BLOCKED = "ON_TASK_BLOCKED"
    POST_INVOCATION = "POST_INVOCATION"
    STOP = "STOP"

class HookExecutionResult(BaseModel):
    event_type: HookEventType
    allowed: bool = True
    reason: Optional[str] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)

class ADRStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    SUPERSEDED = "SUPERSEDED"
    DEPRECATED = "DEPRECATED"
    REJECTED = "REJECTED"

class ArchitectureDecisionRecord(BaseModel):
    number: int
    title: str
    status: ADRStatus = ADRStatus.ACCEPTED
    context: str = ""
    decision: str = ""
    consequences: str = ""
    date: str = ""
    path: str = ""

class CleanArchViolation(BaseModel):
    source_file: str
    imported_module: str
    violation_type: str
    rule_description: str
    severity: str = "CRITICAL"

class C4DiagramType(str, Enum):
    CONTEXT = "CONTEXT"
    CONTAINER = "CONTAINER"
    COMPONENT = "COMPONENT"
    CODE = "CODE"

class C4DiagramDefinition(BaseModel):
    title: str
    diagram_type: C4DiagramType
    mermaid_code: str
    elements: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)

class ArchitectureHealthReport(BaseModel):
    is_clean_arch: bool = True
    layer_violations: List[str] = Field(default_factory=list)
    adr_coverage: float = 100.0
    docs_synchronized: bool = True

class ProjectHealthScore(BaseModel):
    overall_score: float = 100.0
    tdd_compliance: float = 100.0
    security_score: float = 100.0
    git_governance_score: float = 100.0
    architecture_health: float = 100.0
    uiux_score: float = 100.0
    active_blockers: List[str] = Field(default_factory=list)
    is_production_ready: bool = True

class ReleaseManifest(BaseModel):
    version: str = "1.0.0"
    git_commit: str = ""
    tests_count: int = 0
    adrs_count: int = 0
    spdx_compliance: str = "100% Permissive (MIT / Apache-2.0)"
    release_date: str = ""
    artifacts: List[str] = Field(default_factory=list)

# --- Wave 2: Advanced Security, SAST, SCA, STRIDE, MCP & Complexity Models ---

class SASTFinding(BaseModel):
    rule_id: str
    file_path: str
    line_number: int
    severity: SecuritySeverity = SecuritySeverity.HIGH
    cwe_id: str = "CWE-Unknown"
    description: str
    code_snippet: str = ""
    remediation: str = ""

class SASTScanResult(BaseModel):
    findings: List[SASTFinding] = Field(default_factory=list)
    total_files_scanned: int = 0
    passed: bool = True

class SCAVulnerabilityFinding(BaseModel):
    package_name: str
    installed_version: str
    cve_id: str
    severity: SecuritySeverity = SecuritySeverity.HIGH
    description: str = ""
    fixed_version: str = ""
    advisory_url: str = ""

class SCAScanResult(BaseModel):
    manifest_path: str
    vulnerabilities: List[SCAVulnerabilityFinding] = Field(default_factory=list)
    total_dependencies: int = 0
    passed: bool = True

class STRIDECategory(str, Enum):
    SPOOFING = "SPOOFING"
    TAMPERING = "TAMPERING"
    REPUDIATION = "REPUDIATION"
    INFORMATION_DISCLOSURE = "INFORMATION_DISCLOSURE"
    DENIAL_OF_SERVICE = "DENIAL_OF_SERVICE"
    ELEVATION_OF_PRIVILEGE = "ELEVATION_OF_PRIVILEGE"

class ThreatFinding(BaseModel):
    id: str
    category: STRIDECategory
    component: str
    risk_level: SecuritySeverity = SecuritySeverity.HIGH
    threat_description: str
    mitigation_strategy: str

class ThreatModelReport(BaseModel):
    target: str
    threats: List[ThreatFinding] = Field(default_factory=list)
    risk_score: float = 100.0

class MCPServerState(str, Enum):
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    UNRESPONSIVE = "UNRESPONSIVE"

class MCPToolSchema(BaseModel):
    name: str
    description: str = ""
    server_name: str
    input_schema: Dict[str, Any] = Field(default_factory=dict)

class MCPServerInfo(BaseModel):
    name: str
    command: str
    args: List[str] = Field(default_factory=list)
    description: str = ""
    state: MCPServerState = MCPServerState.STOPPED
    tool_count: int = 0
    latency_ms: Optional[float] = None

class ComplexityViolation(BaseModel):
    file_path: str
    function_name: str
    complexity_score: int
    max_allowed: int = 10
    line_number: int = 1

class ComplexityReport(BaseModel):
    violations: List[ComplexityViolation] = Field(default_factory=list)
    files_analyzed: int = 0
    passed: bool = True
