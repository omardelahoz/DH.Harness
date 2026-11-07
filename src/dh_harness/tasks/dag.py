from __future__ import annotations
from typing import Dict, List, Set, Optional

class CircularDependencyError(Exception):
    """Raised when a cycle is detected in the task dependency graph."""
    pass

class DependencyGraph:
    """
    Directed Acyclic Graph (DAG) for task dependency resolution,
    parallel execution scheduling, and circular dependency detection.
    """

    def __init__(self):
        # node -> list of prerequisites that must complete before node can start
        self._dependencies: Dict[str, Set[str]] = {}
        # node -> list of dependents that wait for this node
        self._dependents: Dict[str, Set[str]] = {}

    def add_node(self, node_id: str, dependencies: Optional[List[str]] = None):
        """Adds a task node with its direct dependencies."""
        if node_id not in self._dependencies:
            self._dependencies[node_id] = set()
            self._dependents[node_id] = set()

        if dependencies:
            for dep in dependencies:
                if dep not in self._dependencies:
                    self._dependencies[dep] = set()
                    self._dependents[dep] = set()
                self._dependencies[node_id].add(dep)
                self._dependents[dep].add(node_id)

    def topological_sort(self) -> List[str]:
        """
        Computes a linear order of tasks adhering to all dependencies.
        Raises CircularDependencyError if a cycle is detected.
        """
        # Kahn's algorithm
        in_degree = {u: len(self._dependencies[u]) for u in self._dependencies}
        queue = [u for u, deg in in_degree.items() if deg == 0]
        result = []

        while queue:
            u = queue.pop(0)
            result.append(u)
            for v in self._dependents.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(result) != len(self._dependencies):
            cycle_nodes = [u for u, deg in in_degree.items() if deg > 0]
            raise CircularDependencyError(
                f"Circular dependency detected involving tasks: {cycle_nodes}"
            )

        return result

    def get_ready_tasks(self, completed_nodes: List[str]) -> List[str]:
        """
        Returns all task nodes that have not yet completed and whose
        dependencies are fully satisfied by completed_nodes.
        These tasks can be executed in parallel!
        """
        completed_set = set(completed_nodes)
        ready = []
        for node, deps in self._dependencies.items():
            if node not in completed_set:
                if deps.issubset(completed_set):
                    ready.append(node)
        return sorted(ready)

    def get_blocking_dependencies(self, node_id: str, completed_nodes: List[str]) -> List[str]:
        """
        Returns the dependencies of node_id that are not yet completed.
        """
        completed_set = set(completed_nodes)
        deps = self._dependencies.get(node_id, set())
        return sorted(list(deps - completed_set))
