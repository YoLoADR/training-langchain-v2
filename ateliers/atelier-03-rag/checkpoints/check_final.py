"""Checkpoint final — Validation AT03 (RAG).

5 questions à choix multiples. Oriente vers Sprint/Bonus/continuation.
Lancez: python ateliers/atelier-03-rag/checkpoints/check_final.py
"""

import sys

QUESTIONS = [
    {
        "question": "Quelle est la différence entre FAISS et ChromaDB ?",
        "choices": [
            "a) FAISS est en mémoire, ChromaDB persiste sur disque avec filtrage de métadonnées",
            "b) FAISS est plus lent que ChromaDB",
            "c) ChromaDB ne supporte pas la similarité cosinus",
            "d) Ils sont identiques",
        ],
        "answer": "a",
        "explanation": "FAISS est optimisé pour la recherche en mémoire (rapide, sauve/charge depuis le disque). "
                       "ChromaDB persiste sur disque et supporte le filtrage par métadonnées (categorie, localisation).",
    },
    {
        "question": "Que fait MMR (Maximal Marginal Relevance) ?",
        "choices": [
            "a) Il trie les résultats par date",
            "b) Il équilibre pertinence et diversité des résultats",
            "c) Il augmente le nombre de résultats",
            "d) Il filtre les résultats par langue",
        ],
        "answer": "b",
        "explanation": "MMR sélectionne des documents qui sont à la fois pertinents pour la query "
                       "et diversifiés entre eux. lambda_mult=0 = max diversité, 1 = max pertinence.",
    },
    {
        "question": "Pourquoi le chunking récursif est-il recommandé ?",
        "choices": [
            "a) Il est plus rapide",
            "b) Il préserve la structure sémantique (paragraphes → lignes → mots)",
            "c) Il produit moins de chunks",
            "d) Il ne nécessite pas de paramètres",
        ],
        "answer": "b",
        "explanation": "RecursiveCharacterTextSplitter essaie d'abord \\n\\n (paragraphes), puis \\n (lignes), "
                       "puis espace (mots). Cela préserve la cohérence sémantique des chunks.",
    },
    {
        "question": "Comment le RAG réduit-il les hallucinations ?",
        "choices": [
            "a) En abaissant la temperature du LLM",
            "b) En injectant le contexte des vrais documents dans le prompt",
            "c) En utilisant un modèle plus grand",
            "d) En limitant le nombre de tokens",
        ],
        "answer": "b",
        "explanation": "Le RAG récupère les documents pertinents et les injecte dans le prompt. "
                       "Le LLM répond basé sur ce contexte au lieu d'inventer. C'est l'anti-hallucination.",
    },
    {
        "question": "Qu'est-ce que Recall@k ?",
        "choices": [
            "a) Le nombre de tokens récupérés",
            "b) La proportion de documents pertinents retrouvés parmi les k premiers résultats",
            "c) La vitesse de récupération",
            "d) Le score de similarité",
        ],
        "answer": "b",
        "explanation": "Recall@k mesure la qualité du retriever : sur tous les documents pertinents, "
                       "quelle proportion apparaît dans les k premiers résultats. Recall@5 >= 0.80 est un bon seuil.",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint Final — AT03 (RAG)")
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
        print("  Excellent ! Prêt pour AT04 (Agents + Tools).")
        print("  → Passez au Bonus pour aller plus loin (MMR tuning, EnsembleRetriever).")
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