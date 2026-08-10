"""Checkpoint 1 — Après l'étape 1 (Document Loaders).

3 questions à choix multiples. Seuil de réussite: 2/3.
Lancez: python ateliers/atelier-03-rag/checkpoints/check_1.py
"""

import sys

QUESTIONS = [
    {
        "question": "Quel Document Loader utilise-t-on pour les CVs PDF ?",
        "choices": [
            "a) CSVLoader",
            "b) PyMuPDFLoader",
            "c) JSONLoader",
            "d) TextLoader",
        ],
        "answer": "b",
        "explanation": "PyMuPDFLoader (fitz) est rapide et gère le texte extractible des PDFs. "
                       "Il ajoute les métadonnées 'source' et 'page' automatiquement.",
    },
    {
        "question": "Que retourne load_cv_pdf(path) ?",
        "choices": [
            "a) Une string avec tout le texte du PDF",
            "b) Un dictionnaire avec les métadonnées",
            "c) Une liste d'objets Document (un par page)",
            "d) Un objet PDF",
        ],
        "answer": "c",
        "explanation": "Les Document Loaders de LangChain retournent une liste de Document. "
                       "Chaque Document a page_content (texte) et metadata (source, page, etc.).",
    },
    {
        "question": "Pourquoi charge-t-on les offres en JSON plutôt qu'en PDF ?",
        "choices": [
            "a) Les PDFs sont trop lourds",
            "b) Le JSON est structuré, on peut extraire catégorie/localisation comme métadonnées",
            "c) LangChain ne supporte pas le PDF",
            "d) Le JSON est plus rapide à parser",
        ],
        "answer": "b",
        "explanation": "Le JSON est structuré : on peut extraire 'categorie', 'localisation' "
                       "comme métadonnées filtrables dans ChromaDB. Les PDFs n'ont pas cette structure.",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint 1 — Document Loaders")
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
        print("  ✓ Checkpoint réussi ! Vous pouvez passer à l'étape 2 (Vector Stores).")
    else:
        print("  ✗ Checkpoint échoué. Revoyez la section Document Loaders.")
    print("=" * 60)

    return 0 if score >= 2 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())