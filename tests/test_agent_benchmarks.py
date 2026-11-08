import pytest
from dh_harness.governance.benchmarks import AgentBenchmarkEngine

def test_agent_benchmark_calculates_perfect_first_pass_accuracy():
    engine = AgentBenchmarkEngine()
    task_history = [
        {"task_id": "T1", "passed_first_try": True, "tool_calls_total": 5, "tool_calls_blocked": 0, "layer_violations": 0},
        {"task_id": "T2", "passed_first_try": True, "tool_calls_total": 4, "tool_calls_blocked": 0, "layer_violations": 0}
    ]

    card = engine.evaluate_agent("dotnet-lead-engineer", task_history)

    assert card.agent_id == "dotnet-lead-engineer"
    assert card.first_pass_accuracy == 100.0
    assert card.total_tasks_evaluated == 2
    assert card.tool_efficiency_ratio == 1.0
    assert card.architecture_adherence_score == 100.0
    assert card.overall_rating == "EXCELLENT"

def test_agent_benchmark_penalizes_regressions_and_blocked_tools():
    engine = AgentBenchmarkEngine()
    task_history = [
        {"task_id": "T1", "passed_first_try": False, "tool_calls_total": 10, "tool_calls_blocked": 3, "layer_violations": 1},
        {"task_id": "T2", "passed_first_try": True, "tool_calls_total": 5, "tool_calls_blocked": 0, "layer_violations": 0}
    ]

    card = engine.evaluate_agent("junior-developer", task_history)

    assert card.first_pass_accuracy == 50.0
    assert card.tool_efficiency_ratio < 0.9
    assert card.architecture_adherence_score < 100.0
    assert card.overall_rating in ("ACCEPTABLE", "NEEDS_IMPROVEMENT")

def test_agent_benchmark_generates_leaderboard():
    engine = AgentBenchmarkEngine()
    agents_data = {
        "dotnet-lead-engineer": [{"task_id": "T1", "passed_first_try": True, "tool_calls_total": 5, "tool_calls_blocked": 0, "layer_violations": 0}],
        "python-lead-engineer": [{"task_id": "T2", "passed_first_try": False, "tool_calls_total": 5, "tool_calls_blocked": 1, "layer_violations": 0}]
    }

    leaderboard = engine.generate_leaderboard(agents_data)
    assert len(leaderboard.scorecards) == 2
    # Dotnet lead should be ranked first because of higher FPA
    assert leaderboard.scorecards[0].agent_id == "dotnet-lead-engineer"
