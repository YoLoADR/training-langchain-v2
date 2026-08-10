"""Tests unitaires pour hirekit.deep_agent.middleware — build_context_prompt 9 combinaisons.

Inspiré de sellkit/tests/unit/v3/middleware/recruitment-context.test.ts (161 lignes).
Tests purs, pas de LLM, pas de réseau.
"""

import pytest
from hirekit.deep_agent.middleware import (
    RecruitmentContext,
    build_context_prompt,
    read_skill_for_context,
)


def make_ctx(overrides: dict | None = None) -> RecruitmentContext:
    """Crée un RecruitmentContext avec les valeurs par défaut."""
    defaults = {
        "qual_count": 0,
        "stage": "new",
        "memory_prompt": None,
        "next_field": None,
        "objection_key": None,
        "objection_tactic": None,
        "link_being_sent": False,
        "link_already_sent": False,
        "is_closing": False,
        "show_test_and_link": False,
        "refusal": False,
    }
    if overrides:
        defaults.update(overrides)
    return RecruitmentContext(**defaults)


class TestBuildContextPrompt:
    """9 combinaisons de contexte — inspiré de recruitment-context.test.ts."""

    def test_1_empty_context_returns_empty_string(self):
        ctx = make_ctx()
        prompt = build_context_prompt(ctx)
        assert prompt == ""

    def test_2_memory_prompt_only_produces_infos_section(self):
        ctx = make_ctx({"memory_prompt": "- Nom: Nathan\n- Experience: aucune"})
        prompt = build_context_prompt(ctx)
        assert "Infos candidat" in prompt
        assert "- Nom: Nathan" in prompt
        assert "Prochaine question" not in prompt
        assert "Objection" not in prompt

    def test_3_next_field_in_qualification_produces_question_section(self):
        ctx = make_ctx({"qual_count": 3, "next_field": "location"})
        prompt = build_context_prompt(ctx)
        assert "Prochaine question" in prompt
        assert "secteur" in prompt  # FIELD_QUESTIONS.location contient "secteur"

    def test_3b_next_field_experience(self):
        ctx = make_ctx({"qual_count": 1, "next_field": "experience"})
        prompt = build_context_prompt(ctx)
        assert "Prochaine question" in prompt
        assert "experience" in prompt.lower()

    def test_3c_qual_count_6_no_question_section(self):
        ctx = make_ctx({"qual_count": 6, "next_field": None})
        prompt = build_context_prompt(ctx)
        assert "Prochaine question" not in prompt

    def test_4_link_being_sent_produces_link_section(self):
        ctx = make_ctx({"link_being_sent": True})
        prompt = build_context_prompt(ctx)
        assert "Lien fiches de poste" in prompt
        assert "NE dis PAS" in prompt

    def test_5_link_already_sent_produces_link_section(self):
        ctx = make_ctx({"link_already_sent": True})
        prompt = build_context_prompt(ctx)
        assert "Lien fiches de poste" in prompt
        assert "déjà" in prompt.lower()
        assert "NE renvoie PAS" in prompt

    def test_5b_link_being_sent_takes_priority_over_already_sent(self):
        ctx = make_ctx({"link_being_sent": True, "link_already_sent": True})
        prompt = build_context_prompt(ctx)
        assert "NE dis PAS" in prompt
        assert "déjà" not in prompt.lower()

    def test_6_objection_in_qualification_priority_question(self):
        ctx = make_ctx(
            {
                "qual_count": 3,
                "objection_key": "trop_cher",
                "objection_tactic": "Reformuler la valeur perçue.",
            }
        )
        prompt = build_context_prompt(ctx)
        assert "Objection détectée" in prompt
        assert "Type: trop_cher" in prompt
        assert "TACTIQUE: Reformuler la valeur perçue." in prompt
        assert "question de qualification" in prompt

    def test_7_objection_in_closing_priority_phase(self):
        ctx = make_ctx(
            {
                "qual_count": 6,
                "stage": "interested",
                "objection_key": "fixe",
                "objection_tactic": "Expliquer le modèle de rémunération.",
            }
        )
        prompt = build_context_prompt(ctx)
        assert "Objection détectée" in prompt
        assert "Type: fixe" in prompt
        assert "phase en cours" in prompt
        assert "question de qualification" not in prompt

    def test_8_full_combination(self):
        ctx = make_ctx(
            {
                "qual_count": 2,
                "stage": "contacted",
                "memory_prompt": "- Nom: Francis\n- Experience: commercial",
                "next_field": "availability",
                "objection_key": "temps",
                "objection_tactic": "Proposer un format flexible.",
                "link_being_sent": True,
            }
        )
        prompt = build_context_prompt(ctx)
        assert "Infos candidat" in prompt
        assert "Francis" in prompt
        assert "Prochaine question" in prompt
        assert "disponible" in prompt.lower()
        assert "Lien fiches de poste" in prompt
        assert "Objection détectée" in prompt
        assert "Type: temps" in prompt

    def test_9_refusal_opt_out_priority_absolute(self):
        ctx = make_ctx(
            {
                "refusal": True,
                "memory_prompt": "- Nom: Nathan",
                "next_field": "experience",
                "qual_count": 3,
                "objection_key": "temps",
                "objection_tactic": "Proposer un format flexible.",
                "link_being_sent": True,
            }
        )
        prompt = build_context_prompt(ctx)
        assert "OPT-OUT" in prompt
        assert "Accepter" in prompt
        assert "Infos candidat" not in prompt
        assert "Prochaine question" not in prompt
        assert "Lien fiches de poste" not in prompt
        assert "Objection détectée" not in prompt


class TestReadSkillForContext:
    """Vérifie que le bon SKILL.md est chargé selon le contexte."""

    def test_qual_count_0_loads_first_contact(self):
        ctx = make_ctx({"qual_count": 0, "stage": "new"})
        skill = read_skill_for_context(ctx)
        assert "phase-first-contact" in skill or "Premier Contact" in skill

    def test_qual_count_3_loads_qualification(self):
        ctx = make_ctx({"qual_count": 3, "stage": "contacted"})
        skill = read_skill_for_context(ctx)
        assert "phase-qualification" in skill or "Qualification" in skill

    def test_qual_count_6_loads_reformulation(self):
        ctx = make_ctx({"qual_count": 6, "stage": "contacted"})
        skill = read_skill_for_context(ctx)
        assert "phase-reformulation" in skill or "Reformulation" in skill

    def test_is_closing_loads_closing(self):
        ctx = make_ctx({"qual_count": 6, "stage": "interested", "is_closing": True})
        skill = read_skill_for_context(ctx)
        assert "phase-closing" in skill or "Closing" in skill

    def test_show_test_and_link_adds_test_technique(self):
        ctx = make_ctx(
            {
                "qual_count": 6,
                "stage": "interested",
                "is_closing": True,
                "show_test_and_link": True,
            }
        )
        skill = read_skill_for_context(ctx)
        assert "phase-closing" in skill or "Closing" in skill
        assert "phase-test-technique" in skill or "Test Technique" in skill

    def test_refusal_returns_empty(self):
        ctx = make_ctx({"refusal": True})
        skill = read_skill_for_context(ctx)
        assert skill == ""
