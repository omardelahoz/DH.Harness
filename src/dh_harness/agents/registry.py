from __future__ import annotations
from typing import Dict, List, Optional
from dh_harness.core.contracts import AgentDefinition, AgentRole, ToolPermission
from dh_harness.agents.catalog import get_default_catalog

class DuplicateAgentError(Exception):
    """Raised when attempting to register an agent with an already existing ID."""
    pass

class AgentRegistry:
    """
    Extensible registry for discovering, registering, and leasing specialized agents.
    Complies with Section 4 of info.md.
    """

    def __init__(self):
        self._agents: Dict[str, AgentDefinition] = {}

    def register_agent(self, agent: AgentDefinition):
        """Registers a new agent definition into the catalog."""
        if agent.id in self._agents:
            raise DuplicateAgentError(f"Agent with ID '{agent.id}' is already registered.")
        self._agents[agent.id] = agent

    def get_agent(self, agent_id: str) -> Optional[AgentDefinition]:
        """Retrieves an agent by its unique identifier."""
        return self._agents.get(agent_id)

    def list_agents(self) -> List[AgentDefinition]:
        """Lists all registered specialized agents."""
        return list(self._agents.values())

    def find_by_role(self, role: AgentRole) -> List[AgentDefinition]:
        """Finds all agents matching a specific role."""
        return [a for a in self._agents.values() if a.role == role]

    def find_by_tool(self, tool: ToolPermission) -> List[AgentDefinition]:
        """Finds all agents possessing a specific tool permission."""
        return [a for a in self._agents.values() if tool in a.allowed_tools]

    def load_defaults(self):
        """Loads canonical specialized agents from the default catalog."""
        for agent in get_default_catalog():
            if agent.id not in self._agents:
                self.register_agent(agent)
