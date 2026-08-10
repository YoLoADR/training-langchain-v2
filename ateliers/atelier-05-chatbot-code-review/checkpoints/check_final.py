"""Checkpoint final — Validation AT05 (Chatbots + Code Analysis + Multimodal).

5 questions QCM. Oriente vers Sprint/Bonus/continuation.
Lancez: python ateliers/atelier-05-chatbot-code-review/checkpoints/check_final.py
"""

import sys

QUESTIONS = [
    {
        "question": "Quels composants Streamlit créent l'UX ChatGPT-like ?",
        "choices": [
            "a) st.text_input + st.button",
            "b) st.chat_message + st.chat_input",
            "c) st.form + st.text_area",
            "d) st.sidebar + st.selectbox",
        ],
        "answer": "b",
        "explanation": "st.chat_message (bulles de chat avec avatar) et st.chat_input "
                       "(input en bas de page) recréent l'UX ChatGPT.",
    },
    {
        "question": "Que fait GenericLoader avec LanguageParser pour le code Python ?",
        "choices": [
            "a) Il compile le code Python",
            "b) Il parse les fichiers .py en préservant la structure (classes, fonctions)",
            "c) Il exécute le code et capture la sortie",
            "d) Il convertit le Python en JavaScript",
        ],
        "answer": "b",
        "explanation": "LanguageParser identifie les blocs de code (classes, fonctions, "
                       "imports) et les sépare en Documents avec des métadonnées de structure.",
    },
    {
        "question": "Pourquoi le chunking du code utilise-t-il des séparateurs spéciaux ?",
        "choices": [
            "a) Pour accélérer l'indexation",
            "b) Pour préserver les blocs logiques (class, def) et ne pas couper au milieu d'une fonction",
            "c) Pour réduire le nombre de chunks",
            "d) Pour des raisons de sécurité",
        ],
        "answer": "b",
        "explanation": "Les séparateurs ['\\nclass ', '\\ndef ', '\\n\\n', '\\n', ' '] "
                       "découpent d'abord sur les classes/fonctions, préservant la cohérence sémantique.",
    },
    {
        "question": "Que permet le bot Telegram simulé ?",
        "choices": [
            "a) De tester le flux Telegram sans token API (depuis stdin)",
            "b) De contourner les limites de l'API Telegram",
            "c) De simuler plusieurs utilisateurs simultanés",
            "d) De compresser les messages",
        ],
        "answer": "a",
        "explanation": "Le bot simulé lit depuis stdin et route via process_command(). "
                       "Permet de tester sans TELEGRAM_BOT_TOKEN ni configuration API.",
    },
    {
        "question": "Qu'est-ce que le multimodal dans cet atelier ?",
        "choices": [
            "a) La gestion multi-langues",
            "b) La transcription vocale (STT) → texte → LLM, et TTS pour la réponse",
            "c) Le support multi-modèles (Claude + GPT)",
            "d) Le déploiement multi-plateforme",
        ],
        "answer": "b",
        "explanation": "Le multimodal audio/vocal: Speech-to-Text (transcription) pour "
                       "l'input, et Text-to-Speech pour la réponse vocale (mock dans cet atelier).",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint Final — AT05 (Chatbots + Code Analysis)")
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
            print(f"  ✗ Incorrect. Réponse: '{q['answer']}'. {q['explanation']}")
        print()
    print("=" * 60)
    print(f"  Score: {score}/{len(QUESTIONS)}")
    print()
    if score >= 4:
        print("  Excellent ! Prêt pour AT06 (Éval + Déploiement).")
        print("  → Passez au Bonus (Streamlit, vrai bot Telegram).")
    elif score >= 3:
        print("  Bien ! Faites le Sprint pour renforcer les bases.")
    else:
        print("  Concepts à revoir. Refaites le tronc commun.")
    print("=" * 60)
    return 0 if score >= 3 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())