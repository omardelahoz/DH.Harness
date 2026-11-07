import os
import sqlite3
from typing import Dict, Any, List

class MemoryEngine:
    """
    Synchronizes project memory between SQLite (.engine/agent_engine.db) and Markdown (.project/).
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.engine_db = os.path.join(workspace_root, ".engine", "agent_engine.db")
        self.project_dir = os.path.join(workspace_root, ".project")

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

        return {
            "workspace": self.workspace_root,
            "tasks_total": tasks_count,
            "completed": completed_count,
            "blocked": blocked_count,
            "running": running_count,
            "project_memory_exists": os.path.exists(self.project_dir)
        }
