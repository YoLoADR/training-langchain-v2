"""Vector Store ChromaDB — index des offres avec métadonnées.

AT03 — Vector Stores : ChromaDB pour indexer les offres avec filtres.
"""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def build_chroma_index(
    chunks: list[Document],
    embeddings: Embeddings,
    collection_name: str = "offres",
    persist_directory: str | None = None,
):
    """AT03 — construit l'index ChromaDB pour les offres."""
    raise NotImplementedError(
        "AT03 — implémentez build_chroma_index() dans hirekit/rag/vectorstore_chroma.py"
    )
