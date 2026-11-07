from __future__ import annotations
import os
import json
import time
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any

from dh_harness.core.contracts import SessionCheckpoint

class CorruptedCheckpointError(Exception):
    """Raised when a checkpoint's cryptographic SHA-256 checksum does not match its contents."""
    pass

def compute_checkpoint_checksum(payload: Dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 checksum over the payload dictionary."""
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

class CheckpointManager:
    """
    Manages session checkpoints, persistent recovery and integrity validation.
    Complies with info.md § 8 and § 28.
    """

    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        self.checkpoints_dir = os.path.join(storage_dir, "checkpoints")
        os.makedirs(self.checkpoints_dir, exist_ok=True)
        self.latest_pointer_file = os.path.join(self.checkpoints_dir, "latest.json")

    def create_checkpoint(
        self,
        session_id: str,
        active_task_id: Optional[str],
        active_branch: str,
        recent_actions: List[str],
        pending_steps: List[str]
    ) -> SessionCheckpoint:
        """Creates and stores a cryptographically verified session checkpoint."""
        time.sleep(0.005)  # Guarantees strictly distinct monotonic timestamps
        created_at = datetime.now().isoformat()
        payload = {
            "session_id": session_id,
            "active_task_id": active_task_id,
            "active_branch": active_branch,
            "recent_actions": list(recent_actions),
            "pending_steps": list(pending_steps),
            "created_at": created_at
        }

        checksum = compute_checkpoint_checksum(payload)
        chk_data = dict(payload)
        chk_data["checksum"] = checksum

        file_path = os.path.join(self.checkpoints_dir, f"{session_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chk_data, f, indent=2)

        # Update latest pointer
        with open(self.latest_pointer_file, "w", encoding="utf-8") as f:
            json.dump({"latest_session_id": session_id, "updated_at": created_at}, f, indent=2)

        return SessionCheckpoint(**chk_data)

    def restore_checkpoint(self, session_id: str) -> SessionCheckpoint:
        """Loads and validates a session checkpoint by its ID."""
        file_path = os.path.join(self.checkpoints_dir, f"{session_id}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Checkpoint for session '{session_id}' not found at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        stored_checksum = raw_data.pop("checksum", None)
        computed_checksum = compute_checkpoint_checksum(raw_data)

        if stored_checksum != computed_checksum:
            raise CorruptedCheckpointError(
                f"Checksum mismatch for checkpoint '{session_id}'. Expected {computed_checksum}, got {stored_checksum}."
            )

        raw_data["checksum"] = stored_checksum
        return SessionCheckpoint(**raw_data)

    def get_latest_checkpoint(self) -> Optional[SessionCheckpoint]:
        """Retrieves the most recent verified session checkpoint."""
        if os.path.exists(self.latest_pointer_file):
            try:
                with open(self.latest_pointer_file, "r", encoding="utf-8") as f:
                    ptr = json.load(f)
                    latest_id = ptr.get("latest_session_id")
                    if latest_id:
                        return self.restore_checkpoint(latest_id)
            except Exception:
                pass

        # Fallback to file scan
        checkpoints = self.list_checkpoints()
        return checkpoints[0] if checkpoints else None

    def list_checkpoints(self) -> List[SessionCheckpoint]:
        """Lists all valid checkpoints in reverse chronological order."""
        results: List[SessionCheckpoint] = []
        for name in os.listdir(self.checkpoints_dir):
            if name.endswith(".json") and name != "latest.json":
                sess_id = name[:-5]
                try:
                    chk = self.restore_checkpoint(sess_id)
                    results.append(chk)
                except Exception:
                    continue

        results.sort(key=lambda c: c.created_at, reverse=True)
        return results
