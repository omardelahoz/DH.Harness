import pytest
from dh_harness.agents.registry import AgentRegistry
from dh_harness.core.contracts import AgentRole

def test_extended_catalog_contains_specialized_leads():
    registry = AgentRegistry()
    registry.load_defaults()

    agents = registry.list_agents()
    assert len(agents) >= 12

    # Verify specialized stack leads
    dotnet_agent = registry.get_agent("dotnet-lead-engineer")
    assert dotnet_agent is not None
    assert dotnet_agent.role == AgentRole.BACKEND_DEVELOPER
    assert "dotnet-clean-architecture" in dotnet_agent.required_skills

    python_agent = registry.get_agent("python-lead-engineer")
    assert python_agent is not None
    assert python_agent.role == AgentRole.BACKEND_DEVELOPER
    assert "python-fastapi-clean-architecture" in python_agent.required_skills

    react_agent = registry.get_agent("react-frontend-lead")
    assert react_agent is not None
    assert react_agent.role == AgentRole.FRONTEND_DEVELOPER
    assert "react-nextjs-ui" in react_agent.required_skills

    angular_agent = registry.get_agent("angular-frontend-lead")
    assert angular_agent is not None
    assert angular_agent.role == AgentRole.FRONTEND_DEVELOPER
    assert "angular-enterprise-ui" in angular_agent.required_skills

    mobile_agent = registry.get_agent("mobile-engineer")
    assert mobile_agent is not None
    assert mobile_agent.role == AgentRole.MOBILE_DEVELOPER
    assert "mobile-flutter-engineering" in mobile_agent.required_skills

    devops_agent = registry.get_agent("devops-cloud-engineer")
    assert devops_agent is not None
    assert devops_agent.role == AgentRole.DEVOPS_ENGINEER
    assert "devops-ci-cd-pipelines" in devops_agent.required_skills

def test_find_agents_by_extended_roles():
    registry = AgentRegistry()
    registry.load_defaults()

    mobiles = registry.find_by_role(AgentRole.MOBILE_DEVELOPER)
    assert len(mobiles) >= 1
    assert mobiles[0].id == "mobile-engineer"

    devops = registry.find_by_role(AgentRole.DEVOPS_ENGINEER)
    assert len(devops) >= 1
    assert devops[0].id == "devops-cloud-engineer"
