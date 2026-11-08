"""Token usage and cost tracker for LLM model invocations."""
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from dh_harness.core.contracts import TokenUsageEntry, TokenUsageSummary

# Pricing in USD per 1,000,000 tokens
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}
DEFAULT_PRICING = {"input": 1.00, "output": 3.00}


class TokenUsageTracker:
    """Tracks token consumption and calculates costs across multiple models."""

    def __init__(self) -> None:
        self.entries: List[TokenUsageEntry] = []

    def record_usage(
        self,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
        cached_tokens: int = 0
    ) -> TokenUsageEntry:
        """Records token usage and calculates cost based on current model rates."""
        pricing = MODEL_PRICING.get(model_name.lower(), DEFAULT_PRICING)
        prompt_cost = (prompt_tokens / 1_000_000.0) * pricing["input"]
        completion_cost = (completion_tokens / 1_000_000.0) * pricing["output"]
        total_cost = round(prompt_cost + completion_cost, 6)

        total_tokens = prompt_tokens + completion_tokens

        entry = TokenUsageEntry(
            model_name=model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cached_tokens=cached_tokens,
            total_tokens=total_tokens,
            cost_usd=total_cost,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        self.entries.append(entry)
        return entry

    def get_summary(self) -> TokenUsageSummary:
        """Aggregates all recorded token usages into a breakdown summary."""
        total_prompt = 0
        total_completion = 0
        total_tokens = 0
        total_cost = 0.0
        model_breakdown: Dict[str, Dict[str, Any]] = {}

        for entry in self.entries:
            total_prompt += entry.prompt_tokens
            total_completion += entry.completion_tokens
            total_tokens += entry.total_tokens
            total_cost += entry.cost_usd

            if entry.model_name not in model_breakdown:
                model_breakdown[entry.model_name] = {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cost_usd": 0.0,
                    "invocations": 0
                }
            m = model_breakdown[entry.model_name]
            m["prompt_tokens"] += entry.prompt_tokens
            m["completion_tokens"] += entry.completion_tokens
            m["total_tokens"] += entry.total_tokens
            m["cost_usd"] = round(m["cost_usd"] + entry.cost_usd, 6)
            m["invocations"] += 1

        return TokenUsageSummary(
            total_prompt_tokens=total_prompt,
            total_completion_tokens=total_completion,
            total_tokens=total_tokens,
            total_cost_usd=round(total_cost, 4),
            model_breakdown=model_breakdown
        )

    def reset(self) -> None:
        """Clears all tracked entries."""
        self.entries.clear()
