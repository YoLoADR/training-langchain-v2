"""Tests pour hirekit.rag.chunking — AT03."""

import pytest
from langchain_core.documents import Document


def make_doc(text: str, meta: dict | None = None) -> Document:
    """Crée un Document de test."""
    return Document(page_content=text, metadata=meta or {"source": "test"})


class TestChunkRecursive:
    """AT03 — chunk_recursive() avec RecursiveCharacterTextSplitter."""

    def test_chunk_recursive_empty(self):
        from hirekit.rag.chunking import chunk_recursive

        chunks = chunk_recursive([], chunk_size=512, chunk_overlap=50)
        assert isinstance(chunks, list)
        assert len(chunks) == 0

    def test_chunk_recursive_short_text(self):
        from hirekit.rag.chunking import chunk_recursive

        doc = make_doc("Texte court", {"source": "cv_001"})
        chunks = chunk_recursive([doc], chunk_size=512, chunk_overlap=50)
        assert len(chunks) == 1
        assert chunks[0].page_content == "Texte court"

    def test_chunk_recursive_long_text(self):
        from hirekit.rag.chunking import chunk_recursive

        long_text = "A" * 1200
        doc = make_doc(long_text, {"source": "cv_001"})
        chunks = chunk_recursive([doc], chunk_size=512, chunk_overlap=50)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.page_content) <= 512 + 50  # chunk_size + tolerance

    def test_chunk_recursive_preserves_metadata(self):
        from hirekit.rag.chunking import chunk_recursive

        doc = make_doc("Texte " * 200, {"source": "cv_001", "type": "cv"})
        chunks = chunk_recursive([doc], chunk_size=100, chunk_overlap=10)
        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk.metadata["source"] == "cv_001"
            assert chunk.metadata["type"] == "cv"

    def test_chunk_recursive_default_params(self):
        from hirekit.rag.chunking import chunk_recursive

        doc = make_doc("Texte court")
        chunks = chunk_recursive([doc])
        assert isinstance(chunks, list)
        assert len(chunks) == 1


class TestChunkFixedSize:
    """AT03 — chunk_fixed_size() avec CharacterTextSplitter."""

    def test_chunk_fixed_size_empty(self):
        from hirekit.rag.chunking import chunk_fixed_size

        chunks = chunk_fixed_size([], chunk_size=512, chunk_overlap=50)
        assert isinstance(chunks, list)
        assert len(chunks) == 0

    def test_chunk_fixed_size_long_text(self):
        from hirekit.rag.chunking import chunk_fixed_size

        long_text = "Ligne1\nLigne2\nLigne3\n" * 100
        doc = make_doc(long_text, {"source": "cv_001"})
        chunks = chunk_fixed_size([doc], chunk_size=100, chunk_overlap=10)
        assert len(chunks) > 1


class TestChunkCvs:
    """AT03 — chunk_cvs() chunking optimisé pour les CVs."""

    def test_chunk_cvs_smaller_chunks(self):
        from hirekit.rag.chunking import chunk_cvs

        long_text = "A" * 1000
        doc = make_doc(long_text, {"source": "cv_001"})
        chunks = chunk_cvs([doc], chunk_size=400, chunk_overlap=50)
        for chunk in chunks:
            assert len(chunk.page_content) <= 400 + 50


class TestCompareChunking:
    """AT03 — compare_chunking_strategies() pour le mini-lab."""

    def test_compare_returns_stats(self):
        from hirekit.rag.chunking import compare_chunking_strategies

        doc = make_doc("Mot " * 200)
        result = compare_chunking_strategies([doc], chunk_size=200)

        assert "fixed_size" in result
        assert "recursive" in result
        assert "count" in result["fixed_size"]
        assert "avg_size" in result["fixed_size"]
        assert "min_size" in result["fixed_size"]
        assert "max_size" in result["fixed_size"]