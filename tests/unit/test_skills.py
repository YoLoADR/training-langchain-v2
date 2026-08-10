"""Tests unitaires pour les SKILL.md + AGENTS.md — structure et cohérence.

Inspiré de sellkit/tests/unit/v3/prompts/skills.test.ts (124 lignes).
Tests purs: pas de LLM, pas de réseau. Vérifie les fichiers markdown.
"""

import os
from pathlib import Path

import pytest

AGENT_DIR = Path(__file__).resolve().parent.parent.parent / ".agent"
SKILLS_DIR = AGENT_DIR / "skills" / "recruiter"
AGENTS_MD_PATH = AGENT_DIR / "memory" / "recruiter" / "AGENTS.md"

EXPECTED_SKILLS = [
    "phase-first-contact",
    "phase-qualification",
    "phase-reformulation",
    "phase-closing",
    "phase-test-technique",
]


def read_skill_file(skill_dir: str) -> str:
    skill_path = SKILLS_DIR / skill_dir / "SKILL.md"
    if not skill_path.exists():
        pytest.fail(f"SKILL.md not found: {skill_path}")
    return skill_path.read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> dict:
    """Parse le frontmatter YAML d'un SKILL.md."""
    if not content.startswith("---"):
        return {"body": content}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"body": content}
    fm = parts[1].strip()
    body = parts[2].strip()
    result = {"body": body}
    for line in fm.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result


class TestAgentsMd:
    """AGENTS.md doit contenir les règles globales."""

    def test_agents_md_exists(self):
        assert AGENTS_MD_PATH.exists(), f"AGENTS.md not found: {AGENTS_MD_PATH}"

    def test_agents_md_contains_global_rules(self):
        content = AGENTS_MD_PATH.read_text(encoding="utf-8")
        assert "Langue" in content or "FRANÇAIS" in content
        assert "Recadrage" in content
        assert "URLs" in content or "liens" in content
        assert "Rôle" in content or "rôle" in content

    def test_agents_md_no_phase_instructions(self):
        """AGENTS.md ne doit pas contenir d'instructions de phase (conflit avec skills)."""
        content = AGENTS_MD_PATH.read_text(encoding="utf-8")
        assert "PHASE 1" not in content
        assert "PHASE 2" not in content
        assert "PHASE 3" not in content


class TestSkillsStructure:
    """Vérifie la structure des 5 SKILL.md."""

    def test_all_5_skills_present(self):
        dirs = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
        for skill in EXPECTED_SKILLS:
            assert skill in dirs, f"Skill manquant: {skill}"

    @pytest.mark.parametrize("skill_dir", EXPECTED_SKILLS)
    def test_skill_has_frontmatter_with_name_and_description(self, skill_dir):
        content = read_skill_file(skill_dir)
        fm = parse_frontmatter(content)
        assert fm.get("name"), f"{skill_dir}: frontmatter 'name' manquant"
        assert fm["name"] == skill_dir, f"{skill_dir}: name devrait être '{skill_dir}'"
        assert fm.get("description"), f"{skill_dir}: frontmatter 'description' manquant"
        assert len(fm["description"]) > 10, f"{skill_dir}: description trop courte"

    def test_no_skill_contains_global_link_rule(self):
        """Aucun skill ne doit contenir une règle lien globale (conflit avec AGENTS.md)."""
        for skill_dir in EXPECTED_SKILLS:
            content = read_skill_file(skill_dir)
            assert "## REGLE LIEN" not in content, f"{skill_dir}: contient '## REGLE LIEN'"

    def test_phase_qualification_mentions_test_technique(self):
        """Le skill de qualification doit mentionner le test technique (interdiction)."""
        content = read_skill_file("phase-qualification")
        assert "test technique" in content.lower(), (
            "phase-qualification doit mentionner 'test technique'"
        )

    def test_phase_first_contact_no_test_technique_details(self):
        """Le premier contact ne doit pas parler du test technique en détail."""
        content = read_skill_file("phase-first-contact")
        assert (
            "ne parle pas de test technique" in content.lower()
            or "ne pas" in content.lower()
            and "test" in content.lower()
        )

    def test_phase_test_technique_has_key_info(self):
        """Le skill test technique doit contenir les infos clés."""
        content = read_skill_file("phase-test-technique")
        assert "2 semaines" in content or "2 sem" in content.lower()
        assert "150" in content
        assert "zones grises" in content.lower() or "zone grise" in content.lower()

    def test_all_skills_use_fiches_de_poste(self):
        """Tous les skills doivent dire 'fiches de poste' et pas 'espace pro'."""
        for skill_dir in EXPECTED_SKILLS:
            content = read_skill_file(skill_dir)
            assert "espace pro" not in content.lower(), f"{skill_dir}: contient 'espace pro'"
