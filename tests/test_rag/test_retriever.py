"""Tests pour hirekit.rag.retriever — AT03."""
import pytest


class TestGetCVRetriever:
    @pytest.mark.xfail(reason="AT03 non implémenté sur cette branche")
    def test_get_cv_retriever(self):
        from hirekit.rag.retriever import get_cv_retriever
        retriever = get_cv_retriever()
        assert retriever is not None
