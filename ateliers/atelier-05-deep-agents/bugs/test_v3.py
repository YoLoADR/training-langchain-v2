"""Test bug v3 — build_context_prompt opt-out non géré."""

import pytest
from hirekit.deep_agent.middleware import RecruitmentContext, build_context_prompt


def test_refusal_produces_opt_out_section():
    """Quand refusal=True, build_context_prompt doit produire une section OPT-OUT."""
    ctx = RecruitmentContext(
        refusal=True,
        memory_prompt="- Nom: Nathan",
        next_field="experience",
        qual_count=3,
    )
    prompt = build_context_prompt(ctx)
    assert "OPT-OUT" in prompt, f"Section OPT-OUT manquante: {prompt[:100]}"
    assert "Accepter" in prompt or "respect" in prompt.lower(), "Message d'acceptation manquant"


def test_refusal_takes_priority():
    """L'opt-out doit prendre priorité sur les autres sections."""
    ctx = RecruitmentContext(
        refusal=True,
        memory_prompt="- Nom: Nathan",
        next_field="experience",
        qual_count=3,
        objection_key="trop_cher",
        objection_tactic="Reformuler la valeur",
        link_being_sent=True,
    )
    prompt = build_context_prompt(ctx)
    assert "OPT-OUT" in prompt
    assert "Infos candidat" not in prompt, "L'opt-out doit prendre priorité sur les infos candidat"
    assert "Prochaine question" not in prompt, "L'opt-out doit prendre priorité sur la question"
    assert "Objection" not in prompt, "L'opt-out doit prendre priorité sur l'objection"
