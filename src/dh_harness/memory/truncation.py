from __future__ import annotations
from typing import List, Dict, Any, Optional

from dh_harness.core.contracts import SessionCheckpoint, MemoryLevel
from dh_harness.memory.levels import MultiLevelMemory

class ContextTruncationGuard:
    """
    Monitors session token consumption and generates high-density
    compact context digests to prevent conversational context truncation
    and memory loss in Antigravity agents (info.md § 8.2 and § 8.3).
    """

    def __init__(self, max_tokens: int = 8000, chars_per_token: float = 4.0):
        self.max_tokens = max_tokens
        self.chars_per_token = chars_per_token

    def estimate_tokens(self, text: str) -> int:
        """Estimates the token count based on character density."""
        if not text:
            return 0
        return max(1, int(len(text) / self.chars_per_token))

    def should_compact(self, message_history: List[Dict[str, Any]]) -> bool:
        """Determines if the current message history exceeds the safety token threshold."""
        total_tokens = sum(
            self.estimate_tokens(str(m.get("content", "")))
            for m in message_history
        )
        return total_tokens >= self.max_tokens

    def generate_compact_digest(
        self,
        checkpoint: SessionCheckpoint,
        memory: Optional[MultiLevelMemory] = None,
        recent_events: Optional[List[str]] = None
    ) -> str:
        """
        Synthesizes an ultra-compact, high-density Markdown context digest
        preserving 100% of the active architectural and task state.
        """
        lines = [
            "# Compact Session Context Digest",
            f"- **Active Task:** {checkpoint.active_task_id or 'None'}",
            f"- **Branch:** {checkpoint.active_branch}",
            f"- **Session ID:** {checkpoint.session_id}",
            f"- **Timestamp:** {checkpoint.created_at}",
            "",
            "## Recent Completed Actions"
        ]

        if checkpoint.recent_actions:
            for action in checkpoint.recent_actions:
                lines.append(f"- {action}")
        else:
            lines.append("- (No actions recorded)")

        lines.append("")
        lines.append("## Pending Steps")
        if checkpoint.pending_steps:
            for step in checkpoint.pending_steps:
                lines.append(f"- {step}")
        else:
            lines.append("- (No pending steps)")

        if recent_events:
            lines.append("")
            lines.append("## Recent Events")
            for ev in recent_events:
                lines.append(f"- {ev}")

        if memory:
            project_entries = memory.list_by_level(MemoryLevel.PROJECT)
            if project_entries:
                lines.append("")
                lines.append("## Project Context")
                for entry in project_entries:
                    lines.append(f"- **{entry['key']}:** {entry['content']}")

        return "\n".join(lines)
