"""Checkpoint 1 — Après l'étape 1 (Bot Telegram simulé).

3 questions QCM. Seuil: 2/3.
Lancez: python ateliers/atelier-05-chatbot-code-review/checkpoints/check_1.py
"""

import sys

QUESTIONS = [
    {
        "question": "Quelle est la limite de caractères par message Telegram ?",
        "choices": [
            "a) 1024 caractères",
            "b) 4096 caractères",
            "c) 10000 caractères",
            "d) Aucune limite",
        ],
        "answer": "b",
        "explanation": "Telegram limite les messages à 4096 caractères. "
                       "format_response() tronque et ajoute [...tronqué] si nécessaire.",
    },
    {
        "question": "Comment le bot Telegram simulé teste-t-il les commandes sans API ?",
        "choices": [
            "a) Il utilise un webhook mock",
            "b) Il lit les commandes depuis stdin et répond via process_command()",
            "c) Il simule l'API Telegram avec un serveur local",
            "d) Il utilise l'API Telegram en mode test",
        ],
        "answer": "b",
        "explanation": "Le bot simulé lit depuis stdin (input) et route les commandes "
                       "via process_command(). Aucun token API nécessaire.",
    },
    {
        "question": "Que fait process_command('search', 'React Python') ?",
        "choices": [
            "a) Il affiche l'aide de la commande search",
            "b) Il recherche des candidats via search_cvs_tool (RAG FAISS)",
            "c) Il lance une recherche Google",
            "d) Il affiche un message d'erreur",
        ],
        "answer": "b",
        "explanation": "process_command route /search vers search_cvs_tool qui interroge "
                       "l'index FAISS des CVs. Retourne les candidats pertinents.",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint 1 — Bot Telegram simulé")
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
        print("  ✓ Checkpoint réussi ! Passez à l'étape 2 (Code Reviewer).")
    else:
        print("  ✗ Checkpoint échoué. Revoyez le bot Telegram.")
    print("=" * 60)
    return 0 if score >= 2 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())