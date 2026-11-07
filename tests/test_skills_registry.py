import pytest
from dh_harness.core.contracts import SkillCategory, SkillDefinition, ToolPermission
from dh_harness.skills.registry import SkillsRegistry, DuplicateSkillError

def test_skills_registry_defaults_and_lookup():
    reg = SkillsRegistry()
    reg.load_defaults()

    skills = reg.list_skills()
    assert len(skills) >= 6

    backend_skill = reg.get_skill("clean-architecture-backend")
    assert backend_skill is not None
    assert backend_skill.category == SkillCategory.BACKEND
    assert "clean-architecture" in backend_skill.triggers
    assert ToolPermission.FILE_WRITE in backend_skill.required_tools

def test_skills_registry_filter_by_category():
    reg = SkillsRegistry()
    reg.load_defaults()

    backend_skills = reg.find_by_category(SkillCategory.BACKEND)
    assert len(backend_skills) >= 1
    assert any(s.id == "clean-architecture-backend" for s in backend_skills)

    sec_skills = reg.find_by_category(SkillCategory.SECURITY)
    assert len(sec_skills) >= 1
    assert any(s.id == "appsec-threat-modeling" for s in sec_skills)

def test_skills_registry_match_by_triggers():
    reg = SkillsRegistry()
    reg.load_defaults()

    # Prompt with "threat modeling" and "owasp" should match appsec skill
    matched = reg.match_skills_for_task("Please perform a threat modeling and OWASP audit on auth service")
    matched_ids = [s.id for s in matched]
    assert "appsec-threat-modeling" in matched_ids

    # Prompt with "ef core migration" should match database skill
    matched_db = reg.match_skills_for_task("Create an EF Core database migration for user table")
    matched_db_ids = [s.id for s in matched_db]
    assert "database-migrations-dapper-ef" in matched_db_ids

def test_skills_registry_anti_triggers():
    reg = SkillsRegistry()
    skill = SkillDefinition(
        id="backend-exclusive",
        name="Backend Exclusive",
        category=SkillCategory.BACKEND,
        triggers=["api", "endpoint"],
        anti_triggers=["frontend-only", "css-only"]
    )
    reg.register_skill(skill)

    # Should match without anti-trigger
    assert len(reg.match_skills_for_task("Develop new api endpoint")) == 1

    # Should NOT match when anti-trigger is present
    assert len(reg.match_skills_for_task("Develop new api endpoint for frontend-only styling")) == 0

def test_skills_registry_duplicate_error():
    reg = SkillsRegistry()
    skill = SkillDefinition(
        id="test-skill",
        name="Test",
        category=SkillCategory.ENGINEERING_CORE
    )
    reg.register_skill(skill)
    with pytest.raises(DuplicateSkillError):
        reg.register_skill(skill)
