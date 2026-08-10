"""
═══════════════════════════════════════════════════════════════════════════
Atelier 05 — Solution de référence
═══════════════════════════════════════════════════════════════════════════

Cette solution importe depuis le package hirekit/ (implémenté sur la branche main).
Ne pas projeter pendant l'atelier — c'est la référence pour le formateur.
"""

from hirekit.ui.telegram_bot import process_command
from hirekit.ui.code_reviewer import index_code_repo, ask_code_question, get_code_summary


def main() -> None:
    print("=== AT05 — Chatbots + Code Analysis + Multimodal ===\n")

    # TODO 1 — Bot Telegram simulé
    print("=== Étape 1: Bot Telegram simulé ===\n")
    print(process_command("start"))
    print()
    print(process_command("help"))
    print()
    print(process_command("search", "qui a de l'expérience en React ?"))
    print()
    print(process_command("web", "Marie Dubois développeur React"))

    # TODO 2 — Indexer le repo Python
    print("\n=== Étape 2: Code Reviewer — indexation ===\n")
    retriever = index_code_repo("data/code_repo")
    print(f"Repo indexé: retriever prêt ({type(retriever).__name__})")

    # TODO 3 — Q&A sur le code
    print("\n=== Étape 3: Q&A sur le code ===\n")
    questions = [
        "Où est gérée l'authentification ?",
        "Que fait la fonction hash_password ?",
        "Quels sont les modèles de la base de données ?",
        "Comment fonctionne le rate limiting ?",
    ]
    for question in questions:
        print(f"\nQ: {question}")
        answer = ask_code_question(question, retriever)
        print(f"A: {answer[:300]}...")

    # TODO 4 — Résumé du repo
    print("\n=== Étape 4: Résumé du repo ===\n")
    summary = get_code_summary("data/code_repo")
    print(f"Total fichiers: {summary['total_files']}")
    for f in summary["files"]:
        print(f"  {f['filename']}: {f['num_classes']} classes, {f['num_functions']} fonctions")

    # TODO 5 (Bonus) — Streamlit
    print("\n=== Bonus: Streamlit ===")
    print("Lancez: streamlit run hirekit/ui/app.py")
    print("Pages disponibles: Chat, Dashboard Matching, Bibliothèque CVs, Multimodal")


if __name__ == "__main__":
    main()