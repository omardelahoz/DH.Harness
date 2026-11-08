import pytest
from dh_harness.skills.registry import SkillsRegistry
from dh_harness.core.contracts import SkillCategory

def test_extended_skills_catalog_contains_18_skills():
    registry = SkillsRegistry()
    registry.load_defaults()

    skills = registry.list_skills()
    assert len(skills) >= 18

def test_extended_skill_lookups():
    registry = SkillsRegistry()
    registry.load_defaults()

    # Check .NET Clean Architecture skill
    dotnet_skill = registry.get_skill("dotnet-clean-architecture")
    assert dotnet_skill is not None
    assert dotnet_skill.category == SkillCategory.BACKEND
    assert "dapper" in dotnet_skill.triggers

    # Check Mobile Flutter skill
    mobile_skill = registry.get_skill("mobile-flutter-engineering")
    assert mobile_skill is not None
    assert mobile_skill.category == SkillCategory.MOBILE
    assert "flutter" in mobile_skill.triggers

    # Check Docker & Kubernetes skill
    k8s_skill = registry.get_skill("docker-kubernetes-iac")
    assert k8s_skill is not None
    assert k8s_skill.category == SkillCategory.CLOUD
    assert "kubernetes" in k8s_skill.triggers

def test_dynamic_matching_for_new_stacks():
    registry = SkillsRegistry()
    registry.load_defaults()

    matched_dotnet = registry.match_skills_for_task("Implement a CQRS handler with Dapper in C#")
    matched_ids = [s.id for s in matched_dotnet]
    assert "dotnet-clean-architecture" in matched_ids

    matched_mobile = registry.match_skills_for_task("Create a responsive mobile screen in Flutter with BLoC")
    matched_mobile_ids = [s.id for s in matched_mobile]
    assert "mobile-flutter-engineering" in matched_mobile_ids

    matched_devops = registry.match_skills_for_task("Build a production Dockerfile and Kubernetes helm chart")
    matched_devops_ids = [s.id for s in matched_devops]
    assert "docker-kubernetes-iac" in matched_devops_ids
