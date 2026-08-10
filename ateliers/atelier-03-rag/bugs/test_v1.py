"""Bug v1 test — Mauvais séparateur dans CharacterTextSplitter.

Le chunk_fixed_size avec separator="\n\n" ne découpe pas les CVs correctement.
Ce test vérifie que chunk_fixed_size utilise bien "\n" comme séparateur.
"""

import pytest
from langchain_core.documents import Document


class TestBugV1:
    """Bug v1 : CharacterTextSplitter doit utiliser \n comme séparateur."""

    def test_chunk_fixed_size_splits_on_newline(self):
        """Le chunking doit découper sur les nouvelles lignes."""
        from hirekit.rag.chunking import chunk_fixed_size

        # Texte avec des sauts de ligne simples (pas de \n\n)
        text = "Ligne 1\nLigne 2\nLigne 3\n" * 50
        doc = Document(page_content=text, metadata={"source": "test"})
        chunks = chunk_fixed_size([doc], chunk_size=100, chunk_overlap=10)

        # Si le séparateur est \n, on devrait avoir plusieurs chunks
        assert len(chunks) > 1, "Le chunking doit produire plusieurs chunks"

    def test_chunk_recursive_handles_single_newlines(self):
        """Le chunking récursif doit gérer les sauts de ligne simples."""
        from hirekit.rag.chunking import chunk_recursive

        text = "Ligne 1\nLigne 2\nLigne 3\n" * 50
        doc = Document(page_content=text, metadata={"source": "test"})
        chunks = chunk_recursive([doc], chunk_size=100, chunk_overlap=10)
        assert len(chunks) > 1

    def test_chunk_size_respected(self):
        """Chaque chunk doit respecter la taille maximum (avec séparateur \n)."""
        from hirekit.rag.chunking import chunk_recursive

        # Texte avec des sauts de ligne pour que le splitter puisse découper
        text = "Mot " * 100 + "\n" + "Mot " * 100 + "\n" + "Mot " * 100
        doc = Document(page_content=text, metadata={"source": "test"})
        chunks = chunk_recursive([doc], chunk_size=200, chunk_overlap=20)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.page_content) <= 200 + 50  # tolerance pour overlap