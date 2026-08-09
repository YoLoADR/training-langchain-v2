"""Tests pour hirekit.rag.chunking — AT03."""
import pytest


class TestChunkRecursive:
    @pytest.mark.xfail(reason="AT03 non implémenté sur cette branche")
    def test_chunk_recursive(self):
        from hirekit.rag.chunking import chunk_recursive
        chunks = chunk_recursive([], chunk_size=512, chunk_overlap=50)
        assert isinstance(chunks, list)
