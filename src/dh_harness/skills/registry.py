from __future__ import annotations
import re
from typing import Dict, List, Optional
from dh_harness.core.contracts import SkillDefinition, SkillCategory, ToolPermission
from dh_harness.skills.catalog import get_default_skills_catalog

class DuplicateSkillError(Exception):
    """Raised when attempting to register a skill with an ID that already exists."""
    pass

class SkillsRegistry:
    """
    Registry for managing and discovering reusable engineering skills (info.md Section 5).
    """

    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}

    def register_skill(self, skill: SkillDefinition):
        """Registers a new skill definition."""
        if skill.id in self._skills:
            raise DuplicateSkillError(f"Skill with ID '{skill.id}' is already registered.")
        self._skills[skill.id] = skill

    def get_skill(self, skill_id: str) -> Optional[SkillDefinition]:
        """Retrieves a skill definition by its ID."""
        return self._skills.get(skill_id)

    def list_skills(self) -> List[SkillDefinition]:
        """Lists all registered skills."""
        return list(self._skills.values())

    def find_by_category(self, category: SkillCategory) -> List[SkillDefinition]:
        """Finds skills matching a specific category."""
        return [s for s in self._skills.values() if s.category == category]

    def find_by_tool(self, tool: ToolPermission) -> List[SkillDefinition]:
        """Finds skills requiring a specific tool permission."""
        return [s for s in self._skills.values() if tool in s.required_tools]

    def match_skills_for_task(self, prompt: str) -> List[SkillDefinition]:
        """
        Dynamically matches relevant skills for a given task prompt based on
        trigger keywords while honoring anti-triggers (info.md § 5.1).
        """
        normalized_prompt = prompt.lower()
        matched: List[SkillDefinition] = []

        for skill in self._skills.values():
            # Check if any anti-trigger matches
            has_anti_trigger = any(
                re.search(r"\b" + re.escape(at.lower()) + r"\b", normalized_prompt)
                for at in skill.anti_triggers
            )
            if has_anti_trigger:
                continue

            # Check if any trigger matches
            has_trigger = any(
                re.search(r"\b" + re.escape(tr.lower()) + r"\b", normalized_prompt)
                for tr in skill.triggers
            )
            if has_trigger:
                matched.append(skill)

        return matched

    def load_defaults(self):
        """Loads the canonical engineering skills into the registry."""
        for skill in get_default_skills_catalog():
            if skill.id not in self._skills:
                self.register_skill(skill)
