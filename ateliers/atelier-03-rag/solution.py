"""
═══════════════════════════════════════════════════════════════════════════
Atelier 03 — Solution de référence
═══════════════════════════════════════════════════════════════════════════

Cette solution importe depuis le package hirekit/ (implémenté sur la branche main).
Ne pas projeter pendant l'atelier — c'est la référence pour le formateur.
"""

from pathlib import Path

from hirekit.rag.ingestion import load_all_cvs, load_all_offers, load_skills_csv
from hirekit.rag.chunking import chunk_cvs, chunk_offers, compare_chunking_strategies
from hirekit.rag.vectorstore_faiss import build_faiss_index, load_faiss_index, search_cvs
from hirekit.rag.vectorstore_chroma import build_chroma_index, search_offers
from hirekit.rag.retriever import get_cv_retriever, build_rag_chain

QUESTIONS_PRIVEES = [
    "Quelle est l'expérience de Marie Dubois en React ?",
    "Combien d'années d'expérience en Python a Karim Benali ?",
    "Quel est le dernier poste de Sophie Martin ?",
    "Quelles compétences DevOps a Léa Chen ?",
    "Quel est le niveau d'anglais de Thomas Petit ?",
]

REPONSES_ATTENDUES = {
    "Quelle est l'expérience de Marie Dubois en React ?": "Marie Dubois a 4 ans d'expérience en React (niveau avancé).",
    "Combien d'années d'expérience en Python a Karim Benali ?": "Karim Benali a 6 ans d'expérience en Python (niveau expert).",
    "Quel est le dernier poste de Sophie Martin ?": "Sophie Martin a été Senior Product Owner chez ProductCorp pendant 3 ans.",
    "Quelles compétences DevOps a Léa Chen ?": "Léa Chen maîtrise Kubernetes, Docker, Terraform, AWS, GitLab CI, Ansible, Prometheus et Linux.",
    "Quel est le niveau d'anglais de Thomas Petit ?": "Thomas Petit a un niveau d'anglais technique (B2).",
}


def main() -> None:
    print("=== AT03 — RAG sur CVs et offres ===\n")

    # TODO 1 — Charger les documents
    print("Chargement des CVs PDF...")
    cvs_docs = load_all_cvs("data/cvs")
    print(f"  {len(cvs_docs)} pages de CV chargées")

    print("Chargement des offres JSON...")
    offers_docs = load_all_offers("data/offers")
    print(f"  {len(offers_docs)} offres chargées")

    print("Chargement des skills CSV...")
    skills_docs = load_skills_csv("data/skills.csv")
    print(f"  {len(skills_docs)} compétences chargées")

    # TODO 2 — Chunker les documents
    print("\nChunking des CVs (RecursiveCharacterTextSplitter)...")
    cv_chunks = chunk_cvs(cvs_docs, chunk_size=400, chunk_overlap=50)
    print(f"  {len(cv_chunks)} chunks de CV")

    print("Chunking des offres...")
    offer_chunks = chunk_offers(offers_docs, chunk_size=600, chunk_overlap=100)
    print(f"  {len(offer_chunks)} chunks d'offres")

    # Mini-lab: comparer les stratégies de chunking
    print("\nMini-lab: comparaison des stratégies de chunking...")
    stats = compare_chunking_strategies(cvs_docs, chunk_size=400)
    print(
        f"  Fixed-size: {stats['fixed_size']['count']} chunks, "
        f"taille moy={stats['fixed_size']['avg_size']:.0f} chars"
    )
    print(
        f"  Recursive:  {stats['recursive']['count']} chunks, "
        f"taille moy={stats['recursive']['avg_size']:.0f} chars"
    )

    # TODO 3 — Construire les index vectoriels
    print("\nConstruction de l'index FAISS (CVs)...")
    faiss_store = build_faiss_index(cv_chunks, force_rebuild=True)
    print("  Index FAISS construit")

    print("Construction de l'index ChromaDB (offres)...")
    chroma_store = build_chroma_index(offer_chunks)
    print("  Index ChromaDB construit")

    # TODO 4 — Reposer les 5 questions privées avec le RAG (GÉNÉRATION RÉELLE)
    # ⚠️ La réponse doit être produite par le LLM (rag_chain.invoke), pas piochée
    # dans REPONSES_ATTENDUES. Ce dict n'est qu'un GROUND TRUTH pour comparer.
    print("\n=== Questions privées avec RAG (anti-hallucination) ===\n")
    retriever = get_cv_retriever(search_type="similarity", k=4)
    rag_chain = build_rag_chain(retriever=retriever)

    hallucination_count = 0
    for question in QUESTIONS_PRIVEES:
        docs = retriever.invoke(question)  # étape de récupération
        generated = rag_chain.invoke({"question": question})  # étape de GÉNÉRATION par le LLM
        ground_truth = REPONSES_ATTENDUES[question]  # référence pour comparer
        print(f"Q: {question}")
        print(f"  Sources: {[d.metadata.get('filename', '?') for d in docs[:2]]}")
        print(f"  A (LLM): {generated}")
        print(f"  A (vérité): {ground_truth}")

        # Heuristique de comparaison : mots-clés de la vérité absents de la sortie LLM
        keywords = [w for w in ground_truth.split() if len(w) > 3]
        missing = [w for w in keywords if w not in generated]
        if missing:
            hallucination_count += 1
            print(f"  [HALLUCINATION] mots-clés manquants: {missing}")
        print()

    hallucination_rate = hallucination_count / len(QUESTIONS_PRIVEES) * 100
    print(f"Hallucination rate: {hallucination_rate}% (cible: 0%)")

    # TODO 5 (Bonus) — Comparer MMR vs similarity
    print("\n=== Bonus: MMR vs Similarity ===\n")
    mmr_retriever = get_cv_retriever(search_type="mmr", k=4, lambda_mult=0.5)
    sim_retriever = get_cv_retriever(search_type="similarity", k=4)

    for question in QUESTIONS_PRIVEES[:2]:
        mmr_docs = mmr_retriever.invoke(question)
        sim_docs = sim_retriever.invoke(question)
        mmr_sources = set(d.metadata.get("filename") for d in mmr_docs)
        sim_sources = set(d.metadata.get("filename") for d in sim_docs)
        print(f"Q: {question[:50]}...")
        print(f"  MMR sources ({len(mmr_sources)}): {mmr_sources}")
        print(f"  Sim sources ({len(sim_sources)}): {sim_sources}")
        print(f"  MMR plus divers ? {len(mmr_sources) >= len(sim_sources)}")
        print()


if __name__ == "__main__":
    main()
