"""Tests pour hirekit.rag.vectorstore_faiss et chroma — AT03."""
import pytest


class TestBuildFaissIndex:
    @pytest.mark.xfail(reason="AT03 non implémenté sur cette branche")
    def test_build_faiss_index(self):
        from hirekit.rag.vectorstore_faiss import build_faiss_index
        store = build_faiss_index([], embeddings=None)
        assert store is not None
