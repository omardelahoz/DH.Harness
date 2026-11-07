import pytest
from dh_harness.core.contracts import AgentRole, ToolPermission, AgentDefinition
from dh_harness.agents.catalog import get_default_catalog
from dh_harness.agents.registry import AgentRegistry, DuplicateAgentError

def test_default_catalog_contains_canonical_agents():
    catalog = get_default_catalog()
    assert len(catalog) >= 8
    agent_ids = [a.id for a in catalog]
    assert "chief-orchestrator" in agent_ids
    assert "solution-architect" in agent_ids
    assert "developer-backend" in agent_ids
    assert "developer-frontend" in agent_ids
    assert "database-engineer" in agent_ids
    assert "independent-code-reviewer" in agent_ids
    assert "security-engineer" in agent_ids
    assert "qa-engineer" in agent_ids

def test_agent_registry_load_and_lookup():
    registry = AgentRegistry()
    registry.load_defaults()

    reviewer = registry.get_agent("independent-code-reviewer")
    assert reviewer is not None
    assert reviewer.role == AgentRole.CODE_REVIEWER
    assert ToolPermission.READ_ONLY in reviewer.allowed_tools
    # Independent reviewer must NOT have write tools to prevent tampering
    assert ToolPermission.FILE_WRITE not in reviewer.allowed_tools

def test_agent_registry_find_by_role():
    registry = AgentRegistry()
    registry.load_defaults()

    architects = registry.find_by_role(AgentRole.SOLUTION_ARCHITECT)
    assert len(architects) == 1
    assert architects[0].id == "solution-architect"

def test_agent_registry_prevent_duplicates():
    registry = AgentRegistry()
    agent = AgentDefinition(
        id="custom-agent",
        name="Custom",
        role=AgentRole.TECHNICAL_WRITER
    )
    registry.register_agent(agent)
    with pytest.raises(DuplicateAgentError):
        registry.register_agent(agent)
