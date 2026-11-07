from __future__ import annotations
from typing import List
from dh_harness.core.contracts import WorkflowDefinition, WorkflowStage, AgentRole

def get_default_workflow_catalog() -> List[WorkflowDefinition]:
    """
    Returns the canonical catalog of multi-stage composable workflows compliant with info.md § 6.
    """
    return [
        WorkflowDefinition(
            id="feature-development",
            name="Feature Development Composable Workflow",
            description="End-to-end feature workflow: specification -> TDD RED -> implementation GREEN -> independent review.",
            stages=[
                WorkflowStage(
                    id="specification",
                    name="Architecture & Specification",
                    required_role=AgentRole.SOLUTION_ARCHITECT,
                    required_skills=["system-architecture-c4"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="tdd_red",
                    name="TDD RED Contract Testing",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["tdd-test-automation"],
                    is_mandatory=True,
                    depends_on=["specification"]
                ),
                WorkflowStage(
                    id="implement_green",
                    name="Implementation GREEN & Persistence",
                    required_role=AgentRole.BACKEND_DEVELOPER,
                    required_skills=["clean-architecture-backend"],
                    is_mandatory=True,
                    depends_on=["tdd_red"]
                ),
                WorkflowStage(
                    id="independent_review",
                    name="Independent Code & Security Review",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["clean-code"],
                    is_mandatory=True,
                    depends_on=["implement_green"]
                )
            ]
        ),
        WorkflowDefinition(
            id="bug-fix",
            name="Defect Reproduction & TDD BugFix Workflow",
            description="Reproduce defect in RED test -> apply surgical GREEN fix -> independent review.",
            stages=[
                WorkflowStage(
                    id="reproduce_red",
                    name="Reproduce Defect in RED Test",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["tdd-test-automation"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="fix_green",
                    name="Apply Surgical GREEN Correction",
                    required_role=AgentRole.BACKEND_DEVELOPER,
                    required_skills=["clean-architecture-backend"],
                    is_mandatory=True,
                    depends_on=["reproduce_red"]
                ),
                WorkflowStage(
                    id="independent_review",
                    name="Independent Review & Verification",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["clean-code"],
                    is_mandatory=True,
                    depends_on=["fix_green"]
                )
            ]
        ),
        WorkflowDefinition(
            id="security-audit",
            name="Application Security & Threat Model Workflow",
            description="Static secret audit -> STRIDE threat modeling -> remediation architecture.",
            stages=[
                WorkflowStage(
                    id="secret_scan",
                    name="Secret & Credential Audit",
                    required_role=AgentRole.SECURITY_ENGINEER,
                    required_skills=["appsec-threat-modeling"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="threat_modeling",
                    name="Threat Modeling & OWASP Audit",
                    required_role=AgentRole.SECURITY_ENGINEER,
                    required_skills=["appsec-threat-modeling"],
                    is_mandatory=True,
                    depends_on=["secret_scan"]
                ),
                WorkflowStage(
                    id="remediation_plan",
                    name="Remediation Architecture & Plan",
                    required_role=AgentRole.SOLUTION_ARCHITECT,
                    required_skills=["system-architecture-c4"],
                    is_mandatory=True,
                    depends_on=["threat_modeling"]
                )
            ]
        ),
        WorkflowDefinition(
            id="api-development",
            name="API Endpoint & Schema Development Workflow",
            description="Database schema & migration -> contract test -> endpoint implementation -> review.",
            stages=[
                WorkflowStage(
                    id="schema_design",
                    name="Data Modeling & Migration",
                    required_role=AgentRole.DATABASE_ENGINEER,
                    required_skills=["database-migrations-dapper-ef"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="contract_tdd",
                    name="API Contract & Failing Tests",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["tdd-test-automation"],
                    is_mandatory=True,
                    depends_on=["schema_design"]
                ),
                WorkflowStage(
                    id="api_implementation",
                    name="Endpoint Implementation & Service Logic",
                    required_role=AgentRole.BACKEND_DEVELOPER,
                    required_skills=["clean-architecture-backend"],
                    is_mandatory=True,
                    depends_on=["contract_tdd"]
                ),
                WorkflowStage(
                    id="independent_review",
                    name="Independent Review",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["clean-code"],
                    is_mandatory=True,
                    depends_on=["api_implementation"]
                )
            ]
        )
    ]
