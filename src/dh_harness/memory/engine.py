from __future__ import annotations
import os
import sqlite3
from typing import Dict, Any, List, Optional

from dh_harness.core.contracts import MemoryLevel, SessionCheckpoint, KnowledgeItem
from dh_harness.memory.levels import MultiLevelMemory
from dh_harness.memory.checkpoints import CheckpointManager
from dh_harness.memory.truncation import ContextTruncationGuard

class MemoryEngine:
    """
    Synchronizes project memory between SQLite, Checkpoint JSONs, and Markdown (.project/).
    Implements multi-level memory, checkpoints, and context preservation (info.md Section 8).
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.engine_db = os.path.join(workspace_root, ".engine", "agent_engine.db")
        self.project_dir = os.path.join(workspace_root, ".project")
        self.memory_dir = os.path.join(self.project_dir, "memory")

        self.levels = MultiLevelMemory(self.memory_dir)
        self.checkpoints = CheckpointManager(self.memory_dir)
        self.truncation_guard = ContextTruncationGuard()

    def get_summary(self) -> Dict[str, Any]:
        tasks_count = 0
        completed_count = 0
        blocked_count = 0
        running_count = 0

        if os.path.exists(self.engine_db):
            try:
                conn = sqlite3.connect(self.engine_db)
                cur = conn.cursor()
                cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
                for status, count in cur.fetchall():
                    tasks_count += count
                    if status == "COMPLETED":
                        completed_count = count
                    elif status == "BLOCKED":
                        blocked_count = count
                    elif status == "RUNNING":
                        running_count = count
                conn.close()
            except Exception:
                pass

        global_entries = len(self.levels.list_by_level(MemoryLevel.GLOBAL))
        project_entries = len(self.levels.list_by_level(MemoryLevel.PROJECT))
        task_entries = len(self.levels.list_by_level(MemoryLevel.TASK))
        knowledge_entries = len(self.levels.find_knowledge())
        latest_chk = self.checkpoints.get_latest_checkpoint()

        return {
            "workspace": self.workspace_root,
            "tasks_total": tasks_count,
            "completed": completed_count,
            "blocked": blocked_count,
            "running": running_count,
            "project_memory_exists": os.path.exists(self.project_dir),
            "global_entries": global_entries,
            "project_entries": project_entries,
            "task_entries": task_entries,
            "knowledge_entries": knowledge_entries,
            "latest_checkpoint": latest_chk.model_dump() if latest_chk else None
        }
