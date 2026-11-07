import pytest
from dh_harness.architecture.intelligence import ArchitectureAuditor

def test_auditor_detects_db_import_in_controller():
    auditor = ArchitectureAuditor()
    code = """
import sqlite3
from fastapi import APIRouter

router = APIRouter()
"""
    violations = auditor.audit_source_code(code, file_path="src/api/controllers/user_controller.py")

    assert len(violations) >= 1
    v = [v for v in violations if v.violation_type == "DIRECT_DB_ACCESS_IN_CONTROLLER"][0]
    assert "sqlite3" in v.imported_module
    assert v.severity == "CRITICAL"

def test_auditor_detects_raw_sql_query_in_controller():
    auditor = ArchitectureAuditor()
    code = """
from fastapi import APIRouter
router = APIRouter()

@router.get("/users")
def get_users():
    sql = "SELECT id, name, email FROM users WHERE active = 1"
    return execute_query(sql)
"""
    violations = auditor.audit_source_code(code, file_path="src/controllers/users_controller.py")

    assert len(violations) >= 1
    v = [v for v in violations if v.violation_type == "SQL_IN_CONTROLLER"][0]
    assert "SELECT" in v.rule_description

def test_auditor_permits_clean_thin_controller():
    auditor = ArchitectureAuditor()
    code = """
from fastapi import APIRouter, Depends
from app.use_cases.get_users import GetUsersUseCase

router = APIRouter()

@router.get("/users")
def get_users(use_case: GetUsersUseCase = Depends()):
    return use_case.execute()
"""
    violations = auditor.audit_source_code(code, file_path="src/controllers/users_controller.py")

    assert len(violations) == 0

def test_auditor_permits_sql_in_repository():
    auditor = ArchitectureAuditor()
    code = """
import sqlite3

class UserRepository:
    def get_all(self):
        return self.db.query("SELECT * FROM users")
"""
    # Repositories in infrastructure are the sanctioned layer for SQL queries (Rule 4)
    violations = auditor.audit_source_code(code, file_path="src/infrastructure/repositories/user_repo.py")

    assert len(violations) == 0

def test_architecture_health_report_summary():
    auditor = ArchitectureAuditor()
    report = auditor.check_architecture_health(src_dir="src")

    assert report.is_clean_arch is True
    assert len(report.layer_violations) == 0
    assert report.docs_synchronized is True
