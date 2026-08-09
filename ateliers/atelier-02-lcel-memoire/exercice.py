"""
═══════════════════════════════════════════════════════════════════════════
Atelier 02 — LCEL + Mémoire conversationnelle (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : construire une chaîne LCEL de matching CV↔offre avec une
           mémoire recruteur persistée entre sessions.

4 TODOs :
  1. Construire une chaîne LCEL de matching CV↔offre
  2. Utiliser RunnableLambda pour le prétraitement du CV
  3. Sauvegarder et charger une mémoire recruteur en JSON
  4. Traiter 3 CVs en parallèle avec .batch()

Lancer :  python ateliers/atelier-02-lcel-memoire/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# ─── Imports déjà fournis ────────────────────────────────────────────────────
import json
from pathlib import Path

# TODO 1 — importer get_matching_chain depuis hirekit.services.matching
# from hirekit.services.matching import get_matching_chain

# TODO 2 — importer RunnableLambda, RunnablePassthrough depuis langchain_core.runnables
# from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# TODO 3 — importer get_recruiter_memory, save_memory, load_memory
# from hirekit.services.matching import get_recruiter_memory, save_memory, load_memory

# TODO 4 — importer batch_match depuis hirekit.services.matching
# from hirekit.services.matching import batch_match


# ─── Données d'exemple ──────────────────────────────────────────────────────
CV_EXAMPLE = """
Marie Dubois
Développeuse Fullstack — 5 ans d'expérience
marie.dubois@email.fr

Compétences :
- React (avancé, 4 ans)
- TypeScript (intermédiaire, 3 ans)
- Node.js (avancé, 4 ans)
- Python (intermédiaire, 2 ans)
- Docker (débutant, 1 an)

Expériences :
- Développeuse Fullstack chez TechCorp (2022-2024) : Refonte d'une app React/Node.js
- Développeuse Frontend chez StartupXYZ (2020-2022) : Migration Angular vers React
"""

OFFER_EXAMPLE = """
Poste : Développeur React Senior
Entreprise : TechVibes
Compétences requises : React, TypeScript, Next.js, Redux, Node.js
Localisation : Paris
Salaire : 65-85K€
"""

CVS_BATCH = [
    "Marie Dubois - React 4 ans, TypeScript 3 ans, Node.js 4 ans",
    "Karim Benali - Python 6 ans, Django 5 ans, FastAPI 3 ans",
    "Léa Chen - Kubernetes 4 ans, Docker 5 ans, Terraform 3 ans",
]

OFFER_BATCH = "DevOps Engineer — Kubernetes, Docker, AWS, Terraform"


def main() -> None:
    # TODO 1 — Construire la chaîne LCEL de matching
    # chain = get_matching_chain()
    # result = chain.invoke({"cv": CV_EXAMPLE, "offer": OFFER_EXAMPLE})
    # print(f"Score: {result.score}")
    # print(f"Justification: {result.justification}")
    # print(f"Points forts: {result.points_forts}")
    # print(f"Recommandation: {result.recommandation}")
    raise NotImplementedError("TODO 1 — construire get_matching_chain()")

    # TODO 2 — Prétraitement avec RunnableLambda
    # from hirekit.services.matching import clean_cv
    # clean_lambda = RunnableLambda(lambda x: clean_cv(x["cv"]))
    # cleaned = clean_lambda.invoke({"cv": CV_EXAMPLE})
    # print(f"CV nettoyé (100 premiers chars): {cleaned[:100]}")

    # TODO 3 — Mémoire recruteur persistée
    # memory = get_recruiter_memory(k=10)
    # from langchain_core.messages import HumanMessage, AIMessage
    # memory.chat_memory.add_message(HumanMessage(content="Je cherche un dev React"))
    # memory.chat_memory.add_message(AIMessage(content="Marie Dubois a 4 ans d'expérience."))
    #
    # # Sauvegarder
    # memory_path = Path("data/recruiter_memory.json")
    # save_memory(memory, memory_path)
    # print(f"Mémoire sauvegardée dans {memory_path}")
    #
    # # Charger
    # loaded = load_memory(memory_path, k=10)
    # print(f"Mémoire chargée: {len(loaded.chat_memory.messages)} messages")

    # TODO 4 — Batch processing
    # results = batch_match(CVS_BATCH, OFFER_BATCH)
    # for i, result in enumerate(results, 1):
    #     print(f"\nCV {i}: score={result.score:.2f} — {result.recommandation}")


if __name__ == "__main__":
    main()