"""Vector Store FAISS — index des CVs.

AT03 — Vector Stores : FAISS pour indexer les CVs.
"""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS


def build_faiss_index(
    chunks: list[Document],
    embeddings: Embeddings,
    force_rebuild: bool = True,
) -> FAISS:
    """AT03 — construit (ou recharge) l'index FAISS pour les CVs."""
    raise NotImplementedError(
        "AT03 — implémentez build_faiss_index() dans hirekit/rag/vectorstore_faiss.py"
    )


def load_faiss_index(embeddings: Embeddings):
    """AT03 — recharge un index FAISS existant depuis le disque."""
    raise NotImplementedError(
        "AT03 — implémentez load_faiss_index() dans hirekit/rag/vectorstore_faiss.py"
    )
