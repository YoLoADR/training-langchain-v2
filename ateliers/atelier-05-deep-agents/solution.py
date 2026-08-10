"""
═══════════════════════════════════════════════════════════════════════════
Atelier 05 — Solution de référence
═══════════════════════════════════════════════════════════════════════════

Cette solution importe depuis le package hirekit/ (implémenté sur la branche main).
Ne pas projeter pendant l'atelier — c'est la référence pour le formateur.
"""

from langchain_core.messages import HumanMessage

from hirekit.deep_agent.recruiter_agent import get_deep_agent, run_deep_turn
from hirekit.deep_agent.middleware import (
    RecruitmentContext,
    build_context_prompt,
    read_skill_for_context,
)


def main() -> None:
    # TODO 1 — Vérifier que l'agent peut être créé
    agent = get_deep_agent()
    print(f"✅ Agent créé: {agent is not None}")

    # TODO 2 — Créer un contexte de premier contact
    ctx_first = RecruitmentContext(qual_count=0, stage="new")
    print(f"\nContexte premier contact: qual_count={ctx_first.qual_count}, stage={ctx_first.stage}")

    # TODO 3 — Vérifier le skill chargé pour le premier contact
    skill = read_skill_for_context(ctx_first)
    print(f"Skill chargé (premier contact):\n{skill[:200]}...")
    assert "phase-first-contact" in skill or "Premier Contact" in skill, "Mauvais skill!"

    # TODO 4 — Construire un contexte de qualification et vérifier build_context_prompt
    ctx_qual = RecruitmentContext(
        qual_count=3,
        stage="contacted",
        memory_prompt="## Mémoire du candidat\n- Nom: Nathan\n- Expérience: aucune",
        next_field="location",
    )
    prompt = build_context_prompt(ctx_qual)
    print(f"\nContexte de qualification:\n{prompt}")
    assert "Infos candidat" in prompt, "Section infos candidat manquante"
    assert "Prochaine question" in prompt, "Section prochaine question manquante"

    # TODO 5 (Bonus) — Contexte de closing
    ctx_closing = RecruitmentContext(
        qual_count=6,
        stage="interested",
        is_closing=True,
        show_test_and_link=True,
        link_being_sent=True,
    )
    skill_closing = read_skill_for_context(ctx_closing)
    print(f"\nSkill closing:\n{skill_closing[:200]}...")
    assert "phase-closing" in skill_closing or "Closing" in skill_closing, "Mauvais skill!"
    assert "phase-test-technique" in skill_closing or "Test Technique" in skill_closing, (
        "Skill test manquant!"
    )

    print("\n✅ Tous les TODOs sont validés !")


if __name__ == "__main__":
    main()
