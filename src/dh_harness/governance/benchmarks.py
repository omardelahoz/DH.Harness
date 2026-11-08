"""Agent Benchmark Engine for First-Pass Accuracy (FPA) and Governance Scoring."""
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from dh_harness.core.contracts import AgentScorecard, BenchmarkLeaderboard


class AgentBenchmarkEngine:
    """Evaluates agent execution metrics, efficiency, architecture compliance, and rankings."""

    def evaluate_agent(
        self,
        agent_id: str,
        task_history: List[Dict[str, Any]],
        agent_name: Optional[str] = None
    ) -> AgentScorecard:
        """Calculates FPA, tool efficiency, and architecture adherence score for an agent."""
        total_tasks = len(task_history)
        if total_tasks == 0:
            return AgentScorecard(
                agent_id=agent_id,
                agent_name=agent_name or agent_id,
                first_pass_accuracy=0.0,
                total_tasks_evaluated=0,
                tool_efficiency_ratio=1.0,
                architecture_adherence_score=100.0,
                overall_rating="NEEDS_IMPROVEMENT"
            )

        passed_first_try = sum(1 for t in task_history if t.get("passed_first_try", False))
        fpa = round((passed_first_try / total_tasks) * 100.0, 2)

        total_tools = sum(t.get("tool_calls_total", 0) for t in task_history)
        blocked_tools = sum(t.get("tool_calls_blocked", 0) for t in task_history)

        if total_tools > 0:
            tool_efficiency = round(max(0.0, 1.0 - (blocked_tools / total_tools)), 2)
        else:
            tool_efficiency = 1.0

        layer_violations = sum(t.get("layer_violations", 0) for t in task_history)
        adherence_score = max(0.0, 100.0 - (layer_violations * 25.0))

        # Overall composite rating
        composite_score = (fpa * 0.5) + (tool_efficiency * 100.0 * 0.25) + (adherence_score * 0.25)

        if composite_score >= 90.0 and fpa >= 80.0:
            rating = "EXCELLENT"
        elif composite_score >= 70.0:
            rating = "ACCEPTABLE"
        else:
            rating = "NEEDS_IMPROVEMENT"

        return AgentScorecard(
            agent_id=agent_id,
            agent_name=agent_name or agent_id,
            first_pass_accuracy=fpa,
            total_tasks_evaluated=total_tasks,
            tool_efficiency_ratio=tool_efficiency,
            architecture_adherence_score=round(adherence_score, 1),
            overall_rating=rating
        )

    def generate_leaderboard(
        self,
        agents_data: Dict[str, List[Dict[str, Any]]]
    ) -> BenchmarkLeaderboard:
        """Generates a ranked leaderboard of all evaluated agents sorted by FPA and adherence."""
        scorecards: List[AgentScorecard] = []
        for agent_id, task_history in agents_data.items():
            card = self.evaluate_agent(agent_id, task_history)
            scorecards.append(card)

        # Sort descending by First Pass Accuracy, then adherence, then efficiency
        scorecards.sort(
            key=lambda c: (c.first_pass_accuracy, c.architecture_adherence_score, c.tool_efficiency_ratio),
            reverse=True
        )

        return BenchmarkLeaderboard(
            scorecards=scorecards,
            generated_at=datetime.now(timezone.utc).isoformat()
        )
