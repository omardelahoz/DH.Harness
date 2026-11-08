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
        ),
        WorkflowDefinition(
            id="mobile-feature-development",
            name="Mobile Multiplatform Feature Composable Workflow",
            description="Mobile specification -> BLoC state TDD -> Flutter presentation & data -> independent review.",
            stages=[
                WorkflowStage(
                    id="mobile_spec",
                    name="Mobile Architecture & Specification",
                    required_role=AgentRole.SOLUTION_ARCHITECT,
                    required_skills=["system-architecture-c4"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="bloc_state_tdd",
                    name="BLoC State Machine Contract TDD",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["tdd-test-automation"],
                    is_mandatory=True,
                    depends_on=["mobile_spec"]
                ),
                WorkflowStage(
                    id="flutter_implementation",
                    name="Flutter UI & Data Layer Implementation",
                    required_role=AgentRole.MOBILE_DEVELOPER,
                    required_skills=["mobile-flutter-engineering"],
                    is_mandatory=True,
                    depends_on=["bloc_state_tdd"]
                ),
                WorkflowStage(
                    id="independent_review",
                    name="Independent Review & Offline Testing",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["clean-code"],
                    is_mandatory=True,
                    depends_on=["flutter_implementation"]
                )
            ]
        ),
        WorkflowDefinition(
            id="devops-pipeline-release",
            name="DevOps Infrastructure & Continuous Delivery Workflow",
            description="IaC/Container security audit -> CI/CD pipeline definition -> Quality Gate -> independent review.",
            stages=[
                WorkflowStage(
                    id="iac_container_audit",
                    name="IaC & Dockerfile Security Audit",
                    required_role=AgentRole.SECURITY_ENGINEER,
                    required_skills=["docker-kubernetes-iac", "appsec-threat-modeling"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="pipeline_definition",
                    name="CI/CD Pipeline Definition & Automation",
                    required_role=AgentRole.DEVOPS_ENGINEER,
                    required_skills=["devops-ci-cd-pipelines"],
                    is_mandatory=True,
                    depends_on=["iac_container_audit"]
                ),
                WorkflowStage(
                    id="quality_gate_audit",
                    name="Quality Gate & Pipeline Dry Run",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["quality-engineering"],
                    is_mandatory=True,
                    depends_on=["pipeline_definition"]
                ),
                WorkflowStage(
                    id="release_review",
                    name="Release Governance & PR Integration",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["git-governance"],
                    is_mandatory=True,
                    depends_on=["quality_gate_audit"]
                )
            ]
        ),
        WorkflowDefinition(
            id="architecture-refactoring",
            name="Clean Architecture Deep Refactoring Workflow",
            description="Clean architecture layer audit -> characterization tests -> surgical refactoring -> review.",
            stages=[
                WorkflowStage(
                    id="clean_arch_audit",
                    name="Layer Boundary & Anti-Bypass Audit",
                    required_role=AgentRole.SOLUTION_ARCHITECT,
                    required_skills=["system-architecture-c4"],
                    is_mandatory=True,
                    depends_on=[]
                ),
                WorkflowStage(
                    id="characterization_tests",
                    name="Failing Characterization Tests (RED)",
                    required_role=AgentRole.QA_ENGINEER,
                    required_skills=["tdd-test-automation"],
                    is_mandatory=True,
                    depends_on=["clean_arch_audit"]
                ),
                WorkflowStage(
                    id="layer_refactoring",
                    name="Surgical Layer Refactoring (GREEN)",
                    required_role=AgentRole.BACKEND_DEVELOPER,
                    required_skills=["clean-architecture-backend"],
                    is_mandatory=True,
                    depends_on=["characterization_tests"]
                ),
                WorkflowStage(
                    id="independent_review",
                    name="Independent Peer Code Review",
                    required_role=AgentRole.CODE_REVIEWER,
                    required_skills=["clean-code"],
                    is_mandatory=True,
                    depends_on=["layer_refactoring"]
                )
            ]
        )
    ]
