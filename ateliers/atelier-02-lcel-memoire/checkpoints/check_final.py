"""Checkpoint final — Validation AT02 (LCEL + Mémoire).

5 questions à choix multiples. Oriente vers Sprint/Bonus/continuation.
Lancez: python ateliers/atelier-02-lcel-memoire/checkpoints/check_final.py
"""

import sys

QUESTIONS = [
    {
        "question": "Quelle est la différence entre RunnablePassthrough et RunnableLambda ?",
        "choices": [
            "a) Passthrough filtre les données, Lambda les transforme",
            "b) Passthrough passe l'input inchangé, Lambda applique une fonction",
            "c) Ils sont identiques",
            "d) Passthrough est synchrone, Lambda est asynchrone",
        ],
        "answer": "b",
        "explanation": "RunnablePassthrough transmet l'input tel quel (identité). "
                       "RunnableLambda applique une fonction Python arbitraire à l'input.",
    },
    {
        "question": "Que fait RunnablePassthrough.assign(cv=lambda x: clean_cv(x['cv'])) ?",
        "choices": [
            "a) Remplace la clé cv par une nouvelle valeur nettoyée",
            "b) Ajoute ou met à jour la clé cv avec le résultat de la lambda",
            "c) Supprime la clé cv du dictionnaire",
            "d) Crée un nouveau dictionnaire sans cv",
        ],
        "answer": "b",
        "explanation": "assign() ajoute ou met à jour une clé dans le dictionnaire d'input, "
                       "sans modifier les autres clés. C'est utile pour les variables d'état.",
    },
    {
        "question": "Que fait ConversationBufferWindowMemory(k=10) ?",
        "choices": [
            "a) Sauvegarde les 10 derniers tokens",
            "b) Garde les 10 derniers échanges (20 messages)",
            "c) Limite la mémoire à 10 caractères",
            "d) Crée 10 instances de mémoire",
        ],
        "answer": "b",
        "explanation": "k=10 signifie que la mémoire garde les 10 derniers échanges "
                       "(un échange = un message humain + un message AI, soit 20 messages max).",
    },
    {
        "question": "Comment persister une mémoire entre deux sessions ?",
        "choices": [
            "a) Impossible, la mémoire est volatile par défaut",
            "b) Utiliser save_memory(memory, path) pour sauver en JSON, puis load_memory(path) pour restaurer",
            "c) Configurer un fichier .env avec MEMORY_PATH",
            "d) Utiliser une base de données SQL",
        ],
        "answer": "b",
        "explanation": "Dans ai-hirekit, save_memory() sérialise la mémoire en JSON. "
                       "load_memory() la restaure. La mémoire survit aux redémarrages.",
    },
    {
        "question": "Que fait .batch([cv1, cv2, cv3]) sur une chaîne LCEL ?",
        "choices": [
            "a) Traite les 3 CVs séquentiellement",
            "b) Traite les 3 CVs en parallèle et retourne une liste de résultats",
            "c) Concatène les 3 CVs en un seul input",
            "d) Traite seulement le dernier CV",
        ],
        "answer": "b",
        "explanation": "batch() traite plusieurs inputs en parallèle de manière efficace. "
                       "Retourne une liste de résultats dans le même ordre que les inputs.",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint Final — AT02 (LCEL + Mémoire)")
    print("=" * 60)
    print()

    score = 0
    for i, q in enumerate(QUESTIONS, 1):
        print(f"Question {i}/{len(QUESTIONS)}: {q['question']}")
        for choice in q["choices"]:
            print(f"  {choice}")
        answer = input("\n  Votre réponse (a/b/c/d): ").strip().lower()

        if answer == q["answer"]:
            print(f"  ✓ Correct !")
            score += 1
        else:
            print(f"  ✗ Incorrect. La bonne réponse était '{q['answer']}'.")
            print(f"    {q['explanation']}")
        print()

    print("=" * 60)
    print(f"  Score: {score}/{len(QUESTIONS)}")
    print()

    if score >= 4:
        print("  Excellent ! Prêt pour AT03 (RAG).")
        print("  → Passez au Bonus pour aller plus loin.")
    elif score >= 3:
        print("  Bien ! Quelques concepts à consolider.")
        print("  → Faites le Sprint pour renforcer les bases.")
    else:
        print("  Concepts à revoir.")
        print("  → Refaites le tronc commun et le carnet de bord.")
    print("=" * 60)

    return 0 if score >= 3 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())