"""Checkpoint 1 — Après l'étape 1 (chaîne LCEL de base).

3 questions à choix multiples. Seuil de réussite: 2/3.
Lancez: python ateliers/atelier-02-lcel-memoire/checkpoints/check_1.py
"""

import sys

QUESTIONS = [
    {
        "question": "Que fait l'opérateur pipe (|) en LCEL ?",
        "choices": [
            "a) Il exécute une commande shell",
            "b) Il compose deux Runnables en séquence (output de l'un = input de l'autre)",
            "c) Il compare deux objets Runnable",
            "d) Il crée un thread parallèle",
        ],
        "answer": "b",
        "explanation": "Le pipe | en LCEL chaîne les Runnables: prompt | llm | parser signifie "
                       "que la sortie de prompt est l'entrée de llm, dont la sortie est l'entrée de parser.",
    },
    {
        "question": "Quel composant LCEL permet d'appliquer une fonction Python arbitraire dans une chaîne ?",
        "choices": [
            "a) RunnablePassthrough",
            "b) RunnableParallel",
            "c) RunnableLambda",
            "d) RunnableBranch",
        ],
        "answer": "c",
        "explanation": "RunnableLambda wrappe une fonction Python en Runnable. "
                       "Exemple: RunnableLambda(lambda x: clean_cv(x['cv'])).",
    },
    {
        "question": "Quelle est la sortie de la chaîne: prompt | llm | PydanticOutputParser ?",
        "choices": [
            "a) Une string JSON",
            "b) Un objet Pydantic typé (ex: MatchResult)",
            "c) Une liste de strings",
            "d) Un dictionnaire non typé",
        ],
        "answer": "b",
        "explanation": "Le PydanticOutputParser valide le JSON retourné par le LLM et le convertit "
                       "en objet Pydantic typé (ex: MatchResult avec score, justification, etc.).",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint 1 — LCEL de base")
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
            print(f"  ✗ Incorrect. La bonne réponse était '{q['answer']}'.")
            print(f"    {q['explanation']}")
        print()

    print("=" * 60)
    print(f"  Score: {score}/{len(QUESTIONS)}")

    if score >= 2:
        print("  ✓ Checkpoint réussi ! Vous pouvez passer à l'étape 2 (mémoire).")
    else:
        print("  ✗ Checkpoint échoué. Revoyez la section LCEL du carnet de bord.")
    print("=" * 60)

    return 0 if score >= 2 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())