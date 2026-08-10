"""Checkpoint 1 — Après l'étape 1 (définir les 4 outils).

3 questions à choix multiples. Seuil: 2/3.
Lancez: python ateliers/atelier-04-agents-tools/checkpoints/check_1.py
"""

import sys

QUESTIONS = [
    {
        "question": "Que fait le décorateur @tool ?",
        "choices": [
            "a) Il chronomètre l'exécution d'une fonction",
            "b) Il transforme une fonction Python en BaseTool utilisable par un agent",
            "c) Il ajoute la fonction à un registre global",
            "d) Il active le mode verbose",
        ],
        "answer": "b",
        "explanation": "@tool transforme une fonction en BaseTool avec un nom, une description "
                       "et un schema d'input. L'agent peut alors l'appeler automatiquement.",
    },
    {
        "question": "Pourquoi le python_repl_tool doit-il attraper les exceptions ?",
        "choices": [
            "a) Pour des raisons de performance",
            "b) Pour que l'erreur soit retournée comme observation à l'agent (string) au lieu de le crasher",
            "c) Pour logger les erreurs dans un fichier",
            "d) Ce n'est pas nécessaire",
        ],
        "answer": "b",
        "explanation": "Si l'outil lève une exception, l'AgentExecutor s'arrête. En retournant "
                       "l'erreur comme string, l'agent peut la lire et ajuster son code.",
    },
    {
        "question": "Combien d'outils l'agent ai-hirekit a-t-il à sa disposition ?",
        "choices": [
            "a) 2 (search_cvs + match_candidate)",
            "b) 3 (search_cvs + web_search + python_repl)",
            "c) 4 (search_cvs + match_candidate + web_search + python_repl)",
            "d) 5",
        ],
        "answer": "c",
        "explanation": "4 outils: search_cvs (RAG), match_candidate (LCEL), "
                       "web_search (simulé), python_repl (exécution de code).",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint 1 — Tools (@tool decorator)")
    print("=" * 60)
    print()
    score = 0
    for i, q in enumerate(QUESTIONS, 1):
        print(f"Question {i}/{len(QUESTIONS)}: {q['question']}")
        for choice in q["choices"]:
            print(f"  {choice}")
        answer = input("\n  Votre réponse (a/b/c/d): ").strip().lower()
        if answer == q["answer"]:
            print(f"  ✓ Correct ! {q['explanation']}")
            score += 1
        else:
            print(f"  ✗ Incorrect. Réponse: '{q['answer']}'. {q['explanation']}")
        print()
    print("=" * 60)
    print(f"  Score: {score}/{len(QUESTIONS)}")
    if score >= 2:
        print("  ✓ Checkpoint réussi ! Passez à l'étape 2 (AgentExecutor).")
    else:
        print("  ✗ Checkpoint échoué. Revoyez les tools.")
    print("=" * 60)
    return 0 if score >= 2 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())