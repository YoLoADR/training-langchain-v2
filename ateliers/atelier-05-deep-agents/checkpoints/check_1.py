"""Checkpoint 1 — Atelier 05 Deep Agents (mi-atelier).

3 questions QCM sur les concepts Deep Agents vus dans la première partie.
"""

import sys

QUESTIONS = [
    {
        "question": "Combien de couches comporte l'architecture Deep Agents ?",
        "options": ["2", "3", "4", "5"],
        "reponse": "4",
        "explication": "4 couches: systemPrompt (identité), memory (AGENTS.md), skills (SKILL.md), contextSchema (contexte dynamique)",
    },
    {
        "question": "Quel middleware injecte le SKILL.md avant chaque appel LLM ?",
        "options": ["afterModel", "beforeModel", "beforeInvoke", "onMessage"],
        "reponse": "beforeModel",
        "explication": "beforeModel est exécuté AVANT l'appel au modèle. Il peut injecter un SystemMessage avec le SKILL.md + contexte.",
    },
    {
        "question": "Quel skill est chargé quand qual_count=0 et stage='new' ?",
        "options": [
            "phase-qualification",
            "phase-first-contact",
            "phase-closing",
            "phase-reformulation",
        ],
        "reponse": "phase-first-contact",
        "explication": "qual_count=0 → phase-first-contact (recadrage + démarrage qualification)",
    },
]


def main():
    score = 0
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n{i}. {q['question']}")
        for j, opt in enumerate(q["options"], 1):
            print(f"   {j}. {opt}")
        reponse = input("   Votre réponse (numéro ou texte): ").strip()
        try:
            idx = int(reponse) - 1
            reponse_text = q["options"][idx]
        except (ValueError, IndexError):
            reponse_text = reponse

        if reponse_text == q["reponse"] or reponse == str(q["options"].index(q["reponse"]) + 1):
            print(f"   ✅ Correct ! {q['explication']}")
            score += 1
        else:
            print(f"   ❌ Incorrect. Réponse: {q['reponse']}. {q['explication']}")

    print(f"\n{'=' * 40}")
    print(f"Score: {score}/{len(QUESTIONS)}")
    if score >= 2:
        print("✅ Checkpoint 1 validé — continuez l'atelier")
    else:
        print("❌ Score < 2/3 — relisez le Carnet de bord")

    return 0 if score >= 2 else 1


if __name__ == "__main__":
    sys.exit(main())
