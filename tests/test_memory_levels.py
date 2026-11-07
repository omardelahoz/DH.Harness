import pytest
from dh_harness.core.contracts import MemoryLevel, KnowledgeItem
from dh_harness.memory.levels import MultiLevelMemory, SecretDetectedError

def test_memory_store_and_retrieve_global(tmp_path):
    mem = MultiLevelMemory(storage_dir=str(tmp_path))
    mem.store(
        level=MemoryLevel.GLOBAL,
        key="engineering_principles",
        content="Clean Architecture, SOLID, Zero fake data in production code."
    )

    retrieved = mem.get(level=MemoryLevel.GLOBAL, key="engineering_principles")
    assert retrieved is not None
    assert "Clean Architecture" in retrieved["content"]
    assert retrieved["level"] == MemoryLevel.GLOBAL.value

def test_memory_store_project_and_task(tmp_path):
    mem = MultiLevelMemory(storage_dir=str(tmp_path))
    mem.store(
        level=MemoryLevel.PROJECT,
        key="tech_stack",
        content={"backend": "python", "runtime": "antigravity", "distribution": "npm+pip"}
    )
    mem.store(
        level=MemoryLevel.TASK,
        key="DH-005",
        content={"status": "IN_PROGRESS", "objective": "Memory Engine Implementation"}
    )

    proj = mem.get(level=MemoryLevel.PROJECT, key="tech_stack")
    task = mem.get(level=MemoryLevel.TASK, key="DH-005")

    assert proj is not None
    assert proj["content"]["backend"] == "python"
    assert task is not None
    assert task["content"]["objective"] == "Memory Engine Implementation"

def test_memory_store_and_search_knowledge(tmp_path):
    mem = MultiLevelMemory(storage_dir=str(tmp_path))
    item = KnowledgeItem(
        key="sqlite_concurrency",
        category="KNOWN_BUG",
        summary="SQLite database lock under high concurrency",
        content="Always configure WAL journal mode and busy_timeout = 5000ms.",
        tags=["sqlite", "database", "concurrency"]
    )

    mem.store_knowledge(item)
    found = mem.find_knowledge(tag="sqlite")
    assert len(found) == 1
    assert found[0].key == "sqlite_concurrency"
    assert found[0].category == "KNOWN_BUG"

def test_memory_rejects_secrets(tmp_path):
    mem = MultiLevelMemory(storage_dir=str(tmp_path))
    leak_content = "Here is the production token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    with pytest.raises(SecretDetectedError) as exc_info:
        mem.store(level=MemoryLevel.SESSION, key="session_notes", content=leak_content)

    assert "secret detected" in str(exc_info.value).lower()
