"""Text Splitters — stratégies de chunking pour les CVs et offres.

AT03 — Text Splitters : RecursiveCharacterTextSplitter, CharacterTextSplitter.
"""

from __future__ import annotations

from langchain_core.documents import Document


def chunk_fixed_size(
    documents: list[Document], chunk_size: int = 512, chunk_overlap: int = 50
) -> list[Document]:
    """AT03 — chunking à taille fixe."""
    raise NotImplementedError("AT03 — implémentez chunk_fixed_size() dans hirekit/rag/chunking.py")


def chunk_recursive(
    documents: list[Document], chunk_size: int = 512, chunk_overlap: int = 50
) -> list[Document]:
    """AT03 — chunking récursif (recommandé)."""
    raise NotImplementedError("AT03 — implémentez chunk_recursive() dans hirekit/rag/chunking.py")
