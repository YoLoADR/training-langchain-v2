"""Checkpoint final — Atelier 05 Deep Agents (fin d'atelier).

5 questions QCM sur tous les concepts Deep Agents.
"""

import sys

QUESTIONS = [
    {
        "question": "À quoi sert create_deep_agent() ?",
        "options": [
            "Créer un simple ChatModel",
            "Assembler un agent harness avec capabilities built-in",
            "Créer un vector store",
            "Compiler un prompt template",
        ],
        "reponse": "Assembler un agent harness avec capabilities built-in",
        "explication": "create_deep_agent() fournit planning, filesystem, subagents, context management sans les coder manuellement.",
    },
    {
        "question": "Quelle est la différence entre AGENTS.md et SKILL.md ?",
        "options": [
            "AGENTS.md = règles globales, SKILL.md = règles par phase",
            "AGENTS.md = règles par phase, SKILL.md = règles globales",
            "Ils sont identiques",
            "AGENTS.md est optionnel, SKILL.md est obligatoire",
        ],
        "reponse": "AGENTS.md = règles globales, SKILL.md = règles par phase",
        "explication": "AGENTS.md contient les règles qui s'appliquent à toutes les phases (langue, recadrage, URLs). SKILL.md contient les règles spécifiques à une phase (first-contact, qualification, closing).",
    },
    {
        "question": "Quand le skill phase-reformulation est-il chargé ?",
        "options": [
            "Quand qual_count=0",
            "Quand qual_count=3",
            "Quand qual_count=6",
            "Quand is_closing=True",
        ],
        "reponse": "Quand qual_count=6",
        "explication": "phase-reformulation est chargé quand les 6 champs sont remplis (qual_count >= 6) et qu'on n'est pas encore en closing.",
    },
    {
        "question": "À quoi sert le HarnessProfile ?",
        "options": [
            "Configurer le modèle LLM",
            "Exclure des tools et middleware non nécessaires",
            "Définir le system prompt",
            "Créer le contexte dynamique",
        ],
        "reponse": "Exclure des tools et middleware non nécessaires",
        "explication": "HarnessProfile permet d'exclure write_todos, task, SummarizationMiddleware, etc. quand on n'en a pas besoin.",
    },
    {
        "question": "Que fait build_context_prompt() quand refusal=True ?",
        "options": [
            "Elle ignore le refusal",
            "Elle produit la section OPT-OUT en priorité absolue",
            "Elle produit la section Objection",
            "Elle retourne une chaîne vide",
        ],
        "reponse": "Elle produit la section OPT-OUT en priorité absolue",
        "explication": "L'opt-out est traité en priorité absolue. Les autres sections (infos, question, lien, objection) ne sont pas incluses.",
    },
]


def main():
    score = 0
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n{i}. {q['question']}")
        for j, opt in enumerate(q["options"], 1):
            print(f"   {j}. {opt}")
        reponse = input("   Votre réponse (numéro): ").strip()
        try:
            idx = int(reponse) - 1
            reponse_text = q["options"][idx]
        except (ValueError, IndexError):
            reponse_text = reponse

        if reponse_text == q["reponse"]:
            print(f"   ✅ Correct ! {q['explication']}")
            score += 1
        else:
            print(f"   ❌ Incorrect. Réponse: {q['reponse']}. {q['explication']}")

    print(f"\n{'=' * 40}")
    print(f"Score: {score}/{len(QUESTIONS)}")

    if score >= 4:
        print("✅ Checkpoint final validé — pars en Bonus !")
    elif score >= 3:
        print("✅ Checkpoint final validé")
    else:
        print("❌ Score < 3/5 — refais le Sprint")

    return 0 if score >= 3 else 1


if __name__ == "__main__":
    sys.exit(main())
