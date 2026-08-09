"""Retriever — récupération optimisée pour limiter les hallucinations.

AT03 — Le Retriever : optimiser la récupération pour limiter les hallucinations.
AT04 — EnsembleRetriever FAISS + ChromaDB.
"""

from __future__ import annotations

from langchain_core.retrievers import BaseRetriever


def get_cv_retriever(
    search_type: str = "mmr",
    k: int = 4,
    fetch_k: int = 20,
) -> BaseRetriever:
    """AT03 — retourne le retriever FAISS pour les CVs."""
    raise NotImplementedError("AT03 — implémentez get_cv_retriever() dans hirekit/rag/retriever.py")


def get_ensemble_retriever(
    faiss_k: int = 8,
    chroma_k: int = 8,
    weights: list[float] | None = None,
) -> BaseRetriever:
    """AT04 — retourne l'EnsembleRetriever FAISS + ChromaDB."""
    raise NotImplementedError(
        "AT04 — implémentez get_ensemble_retriever() dans hirekit/rag/retriever.py"
    )
