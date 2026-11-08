from __future__ import annotations
import os
import re
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from dh_harness.core.contracts import MemoryLevel, KnowledgeItem

class SecretDetectedError(Exception):
    """Raised when an attempt is made to store sensitive tokens, secrets or credentials in memory."""
    pass

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{36,}"),
    re.compile(r"gho_[A-Za-z0-9_]{36,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
    re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH)? ?PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[0-9a-zA-Z-]{10,}"),
]

def scan_for_secrets(data: Any) -> None:
    serialized = json.dumps(data) if not isinstance(data, str) else data
    for pattern in SECRET_PATTERNS:
        if pattern.search(serialized):
            raise SecretDetectedError("Secret detected in content: credentials, tokens or private keys are strictly forbidden in persistent memory.")

class MultiLevelMemory:
    """
    Manages multi-level persistent memory (GLOBAL, PROJECT, TASK, SESSION, KNOWLEDGE)
    as defined in info.md Section 8.
    """

    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.db_path = os.path.join(storage_dir, "memory.db")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                key TEXT NOT NULL,
                content TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(level, key)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                key TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def store(self, level: MemoryLevel, key: str, content: Union[str, Dict[str, Any], List[Any]]):
        """Stores or updates a memory entry under the specified memory level."""
        scan_for_secrets(content)

        serialized_content = json.dumps(content) if not isinstance(content, str) else content
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO memory_entries (level, key, content, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(level, key) DO UPDATE SET
                content = excluded.content,
                updated_at = excluded.updated_at
        """, (level.value, key, serialized_content, now))
        conn.commit()
        conn.close()

    def get(self, level: MemoryLevel, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves a memory entry by level and key."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT level, key, content, updated_at FROM memory_entries WHERE level = ? AND key = ?", (level.value, key))
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        lvl, k, raw_content, updated_at = row
        try:
            content = json.loads(raw_content)
        except (json.JSONDecodeError, TypeError):
            content = raw_content

        return {
            "level": lvl,
            "key": k,
            "content": content,
            "updated_at": updated_at
        }

    def list_by_level(self, level: MemoryLevel) -> List[Dict[str, Any]]:
        """Lists all memory entries under a specific memory level."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT level, key, content, updated_at FROM memory_entries WHERE level = ? ORDER BY key ASC", (level.value,))
        rows = cur.fetchall()
        conn.close()

        results = []
        for lvl, k, raw_content, updated_at in rows:
            try:
                content = json.loads(raw_content)
            except Exception:
                content = raw_content
            results.append({
                "level": lvl,
                "key": k,
                "content": content,
                "updated_at": updated_at
            })
        return results

    def store_knowledge(self, item: KnowledgeItem):
        """Stores a curated knowledge item with categories and tags."""
        scan_for_secrets(item.content)
        scan_for_secrets(item.summary)

        now = datetime.now().isoformat()
        tags_str = json.dumps(item.tags)

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO knowledge_items (key, category, summary, content, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                category = excluded.category,
                summary = excluded.summary,
                content = excluded.content,
                tags = excluded.tags,
                created_at = excluded.created_at
        """, (item.key, item.category, item.summary, item.content, tags_str, now))
        conn.commit()
        conn.close()

    def find_knowledge(self, tag: Optional[str] = None, category: Optional[str] = None) -> List[KnowledgeItem]:
        """Finds knowledge items by tag or category."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT key, category, summary, content, tags FROM knowledge_items")
        rows = cur.fetchall()
        conn.close()

        items: List[KnowledgeItem] = []
        for key, cat, summary, content, raw_tags in rows:
            try:
                tags = json.loads(raw_tags)
            except Exception:
                tags = []

            if category and cat != category:
                continue
            if tag and tag not in tags:
                continue

            items.append(KnowledgeItem(
                key=key,
                category=cat,
                summary=summary,
                content=content,
                tags=tags
            ))
        return items

    def search_knowledge_semantic(self, query: str, top_k: int = 5) -> List[Any]:
        """Performs semantic vector search across all stored knowledge items."""
        from dh_harness.memory.semantic import LocalSemanticSearchEngine
        all_items = self.find_knowledge()

        if not all_items:
            default_items = [
                KnowledgeItem(
                    key="clean_architecture_rule",
                    category="architecture",
                    summary="Clean architecture, thin controllers, and repository isolation",
                    content="Keep controllers thin. All Dapper or EF Core database queries must live in the infrastructure layer repository. Controllers only invoke use cases.",
                    tags=["architecture", "backend", "clean-architecture"]
                ),
                KnowledgeItem(
                    key="tdd_cryptographic_evidence",
                    category="testing",
                    summary="Deterministic TDD RED-GREEN-REFACTOR cycle with RedEvidenceVault",
                    content="Every bug fix and feature implementation must record cryptographic RED test failure evidence before modifying files in src/.",
                    tags=["tdd", "testing", "quality"]
                ),
                KnowledgeItem(
                    key="appsec_security_governance",
                    category="security",
                    summary="AST secret scanner, SAST, SCA, and STRIDE threat modeling",
                    content="Zero plain-text secrets allowed. Dependencies must be 100% open source under permissive SPDX whitelist (MIT, Apache-2.0, BSD).",
                    tags=["security", "sast", "sca", "licenses"]
                ),
                KnowledgeItem(
                    key="visual_layout_and_a11y",
                    category="uiux",
                    summary="Headless visual layout QA, responsive viewports, and WCAG 2.1 AA",
                    content="Validate responsive containers without fixed pixel overflow, minimum 44x44px touch targets on mobile, and complete loading/empty/error states.",
                    tags=["uiux", "accessibility", "frontend"]
                ),
                KnowledgeItem(
                    key="database_persistence_standards",
                    category="database",
                    summary="Relational database design, migrations, and parameterized queries",
                    content="Use parameterized queries with PostgreSQL and SQL Server to prevent SQL injection. Migrations must be idempotent and transactional.",
                    tags=["database", "postgresql", "sqlserver", "dapper"]
                )
            ]
            for it in default_items:
                self.store_knowledge(it)
            all_items = default_items

        docs = [
            {
                "key": item.key,
                "category": item.category,
                "summary": item.summary,
                "content": item.content
            }
            for item in all_items
        ]
        engine = LocalSemanticSearchEngine()
        engine.index_documents(docs)
        return engine.search(query, top_k=top_k)
