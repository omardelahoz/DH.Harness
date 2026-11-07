import pytest
from dh_harness.tasks.dag import DependencyGraph, CircularDependencyError

def test_topological_sort_linear():
    graph = DependencyGraph()
    graph.add_node("TaskA")
    graph.add_node("TaskB", dependencies=["TaskA"])
    graph.add_node("TaskC", dependencies=["TaskB"])

    order = graph.topological_sort()
    assert order == ["TaskA", "TaskB", "TaskC"]

def test_topological_sort_branching():
    graph = DependencyGraph()
    graph.add_node("Base")
    graph.add_node("Service", dependencies=["Base"])
    graph.add_node("UI", dependencies=["Base"])
    graph.add_node("E2E", dependencies=["Service", "UI"])

    order = graph.topological_sort()
    assert order.index("Base") < order.index("Service")
    assert order.index("Base") < order.index("UI")
    assert order.index("Service") < order.index("E2E")
    assert order.index("UI") < order.index("E2E")

def test_cycle_detection():
    graph = DependencyGraph()
    graph.add_node("A", dependencies=["C"])
    graph.add_node("B", dependencies=["A"])
    graph.add_node("C", dependencies=["B"])

    with pytest.raises(CircularDependencyError) as exc_info:
        graph.topological_sort()
    assert "Circular dependency" in str(exc_info.value)

def test_get_parallel_ready_tasks():
    graph = DependencyGraph()
    graph.add_node("Task1")
    graph.add_node("Task2")
    graph.add_node("Task3", dependencies=["Task1"])
    graph.add_node("Task4", dependencies=["Task2"])

    # Initially, Task1 and Task2 have zero dependencies completed
    ready = graph.get_ready_tasks(completed_nodes=[])
    assert set(ready) == {"Task1", "Task2"}

    # After Task1 completes, Task3 becomes ready along with Task2
    ready_after_1 = graph.get_ready_tasks(completed_nodes=["Task1"])
    assert set(ready_after_1) == {"Task2", "Task3"}

def test_get_blocking_dependencies():
    graph = DependencyGraph()
    graph.add_node("A")
    graph.add_node("B", dependencies=["A"])
    graph.add_node("C", dependencies=["B"])

    blockers = graph.get_blocking_dependencies("C", completed_nodes=[])
    assert set(blockers) == {"B"}
