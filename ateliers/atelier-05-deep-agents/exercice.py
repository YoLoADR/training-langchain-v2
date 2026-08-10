"""
═══════════════════════════════════════════════════════════════════════════
Atelier 05 — Deep Agents (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : créer un Deep Agent 4 couches et simuler une conversation
           de recrutement avec un candidat.

5 TODOs :
  1. Importer get_deep_agent et run_deep_turn depuis hirekit.deep_agent
  2. Créer un RecruitmentContext avec qual_count=0, stage="new"
  3. Appeler read_skill_for_context() et vérifier le skill chargé
  4. Construire un contexte de qualification (qual_count=3, next_field="location")
     et appeler build_context_prompt() — vérifier les sections
  5. (Bonus) Créer un contexte de closing et vérifier le skill chargé

Lancer :  python ateliers/atelier-05-deep-agents/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# ─── Imports déjà fournis ────────────────────────────────────────────────────
from langchain_core.messages import HumanMessage

# TODO 1 — importer get_deep_agent et run_deep_turn depuis hirekit.deep_agent.recruiter_agent
# from hirekit.deep_agent.recruiter_agent import get_deep_agent, run_deep_turn

# TODO 1 — importer RecruitmentContext, build_context_prompt, read_skill_for_context
# from hirekit.deep_agent.middleware import RecruitmentContext, build_context_prompt, read_skill_for_context


def main() -> None:
    # TODO 1 — Vérifier que l'agent peut être créé
    # agent = get_deep_agent()
    # print(f"✅ Agent créé: {agent is not None}")
    raise NotImplementedError("TODO 1 — importer et créer le Deep Agent")

    # TODO 2 — Créer un contexte de premier contact
    # ctx_first = RecruitmentContext(qual_count=0, stage="new")
    # print(f"\nContexte premier contact: qual_count={ctx_first.qual_count}, stage={ctx_first.stage}")

    # TODO 3 — Vérifier le skill chargé pour le premier contact
    # skill = read_skill_for_context(ctx_first)
    # print(f"Skill chargé (premier contact):\n{skill[:200]}...")
    # assert "phase-first-contact" in skill or "Premier Contact" in skill, "Mauvais skill!"

    # TODO 4 — Construire un contexte de qualification et vérifier build_context_prompt
    # ctx_qual = RecruitmentContext(
    #     qual_count=3,
    #     stage="contacted",
    #     memory_prompt="## Mémoire du candidat\n- Nom: Nathan\n- Expérience: aucune",
    #     next_field="location",
    # )
    # prompt = build_context_prompt(ctx_qual)
    # print(f"\nContexte de qualification:\n{prompt}")
    # assert "Infos candidat" in prompt, "Section infos candidat manquante"
    # assert "Prochaine question" in prompt, "Section prochaine question manquante"

    # TODO 5 (Bonus) — Contexte de closing
    # ctx_closing = RecruitmentContext(
    #     qual_count=6,
    #     stage="interested",
    #     is_closing=True,
    #     show_test_and_link=True,
    #     link_being_sent=True,
    # )
    # skill_closing = read_skill_for_context(ctx_closing)
    # print(f"\nSkill closing:\n{skill_closing[:200]}...")
    # assert "phase-closing" in skill_closing or "Closing" in skill_closing, "Mauvais skill!"
    # assert "phase-test-technique" in skill_closing or "Test Technique" in skill_closing, "Skill test manquant!"

    print("\n✅ Tous les TODOs sont validés !")


if __name__ == "__main__":
    main()
