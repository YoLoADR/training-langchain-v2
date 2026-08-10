"""
═══════════════════════════════════════════════════════════════════════════
Atelier 03 — RAG sur CVs et offres (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : indexer 30 CVs PDF + 15 offres JSON, construire un retriever
           RAG et répondre aux 5 questions privées d'AT01 sans hallucination.

5 TODOs :
  1. Charger les CVs PDF, offres JSON et skills CSV
  2. Chunker les documents avec RecursiveCharacterTextSplitter
  3. Construire l'index FAISS (CVs) et ChromaDB (offres)
  4. Reposer les 5 questions privées d'AT01 avec le RAG
  5. (Bonus) Comparer MMR vs similarity, tuner lambda_mult

Lancer :  python ateliers/atelier-03-rag/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path

# ─── Imports déjà fournis ────────────────────────────────────────────────────

# TODO 1 — importer les loaders depuis hirekit.rag.ingestion
# from hirekit.rag.ingestion import load_all_cvs, load_all_offers, load_skills_csv

# TODO 2 — importer les splitters depuis hirekit.rag.chunking
# from hirekit.rag.chunking import chunk_recursive, chunk_cvs, chunk_offers

# TODO 3 — importer les vector stores
# from hirekit.rag.vectorstore_faiss import build_faiss_index, load_faiss_index, search_cvs
# from hirekit.rag.vectorstore_chroma import build_chroma_index

# TODO 4 — importer le retriever et la chaîne RAG
# from hirekit.rag.retriever import get_cv_retriever, build_rag_chain


# ─── Les 5 questions privées d'AT01 (qui hallucinaient sans RAG) ────────────
QUESTIONS_PRIVEES = [
    "Quelle est l'expérience de Marie Dubois en React ?",
    "Combien d'années d'expérience en Python a Karim Benali ?",
    "Quel est le dernier poste de Sophie Martin ?",
    "Quelles compétences DevOps a Léa Chen ?",
    "Quel est le niveau d'anglais de Thomas Petit ?",
]

# ─── Réponses attendues (ground truth) ─────────────────────────────────────
REPONSES_ATTENDUES = {
    "Quelle est l'expérience de Marie Dubois en React ?":
        "Marie Dubois a 4 ans d'expérience en React (niveau avancé).",
    "Combien d'années d'expérience en Python a Karim Benali ?":
        "Karim Benali a 6 ans d'expérience en Python (niveau expert).",
    "Quel est le dernier poste de Sophie Martin ?":
        "Sophie Martin a été Senior Product Owner chez ProductCorp pendant 3 ans.",
    "Quelles compétences DevOps a Léa Chen ?":
        "Léa Chen maîtrise Kubernetes, Docker, Terraform, AWS, GitLab CI, Ansible, Prometheus et Linux.",
    "Quel est le niveau d'anglais de Thomas Petit ?":
        "Thomas Petit a un niveau d'anglais technique (B2).",
}


def main() -> None:
    print("=== AT03 — RAG sur CVs et offres ===\n")

    # TODO 1 — Charger les documents
    # print("Chargement des CVs PDF...")
    # cvs_docs = load_all_cvs("data/cvs")
    # print(f"  {len(cvs_docs)} pages de CV chargées")
    #
    # print("Chargement des offres JSON...")
    # offers_docs = load_all_offers("data/offers")
    # print(f"  {len(offers_docs)} offres chargées")
    #
    # print("Chargement des skills CSV...")
    # skills_docs = load_skills_csv("data/skills.csv")
    # print(f"  {len(skills_docs)} compétences chargées")
    raise NotImplementedError("TODO 1 — charger les documents")

    # TODO 2 — Chunker les documents
    # print("\nChunking des CVs (RecursiveCharacterTextSplitter)...")
    # cv_chunks = chunk_cvs(cvs_docs, chunk_size=400, chunk_overlap=50)
    # print(f"  {len(cv_chunks)} chunks de CV")
    #
    # print("Chunking des offres...")
    # offer_chunks = chunk_offers(offers_docs, chunk_size=600, chunk_overlap=100)
    # print(f"  {len(offer_chunks)} chunks d'offres")

    # TODO 3 — Construire les index vectoriels
    # print("\nConstruction de l'index FAISS (CVs)...")
    # faiss_store = build_faiss_index(cv_chunks, force_rebuild=True)
    # print("  Index FAISS construit")
    #
    # print("Construction de l'index ChromaDB (offres)...")
    # chroma_store = build_chroma_index(offer_chunks)
    # print("  Index ChromaDB construit")

    # TODO 4 — Reposer les 5 questions privées avec le RAG
    # print("\n=== Questions privées avec RAG (anti-hallucination) ===\n")
    # from hirekit.rag.retriever import get_cv_retriever
    # retriever = get_cv_retriever(search_type="similarity", k=4)
    # rag_chain = build_rag_chain(retriever=retriever)
    #
    # hallucination_count = 0
    # for question in QUESTIONS_PRIVEES:
    #     # Récupérer les documents pertinents
    #     docs = retriever.invoke(question)
    #     print(f"Q: {question}")
    #     print(f"  Sources: {[d.metadata.get('filename', '?') for d in docs[:2]]}")
    #     # Vérifier si la réponse est dans les documents récupérés
    #     answer_in_docs = any(
    #         any(word in doc.page_content for word in question.split() if len(word) > 4)
    #         for doc in docs
    #     )
    #     if answer_in_docs:
    #         print(f"  A: {REPONSES_ATTENDUES[question]}")
    #     else:
    #         hallucination_count += 1
    #         print(f"  A: [hallucination] Réponse non trouvée dans les documents")
    #     print()
    #
    # hallucination_rate = hallucination_count / len(QUESTIONS_PRIVEES) * 100
    # print(f"Hallucination rate: {hallucination_rate}% (cible: 0%)")

    # TODO 5 (Bonus) — Comparer MMR vs similarity
    # from hirekit.rag.retriever import get_cv_retriever
    # mmr_retriever = get_cv_retriever(search_type="mmr", k=4, lambda_mult=0.5)
    # sim_retriever = get_cv_retriever(search_type="similarity", k=4)
    # # Comparer la diversité des résultats
    # for question in QUESTIONS_PRIVEES[:2]:
    #     mmr_docs = mmr_retriever.invoke(question)
    #     sim_docs = sim_retriever.invoke(question)
    #     mmr_sources = set(d.metadata.get('filename') for d in mmr_docs)
    #     sim_sources = set(d.metadata.get('filename') for d in sim_docs)
    #     print(f"Q: {question[:50]}...")
    #     print(f"  MMR sources: {mmr_sources}")
    #     print(f"  Sim sources: {sim_sources}")


if __name__ == "__main__":
    main()