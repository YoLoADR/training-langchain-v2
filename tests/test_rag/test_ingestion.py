"""Tests pour hirekit.rag.ingestion — AT03."""
import pytest


class TestLoadCVPdf:
    @pytest.mark.xfail(reason="AT03 non implémenté sur cette branche")
    def test_load_cv_pdf(self):
        from hirekit.rag.ingestion import load_cv_pdf
        docs = load_cv_pdf("data/cvs/test.pdf")
        assert len(docs) > 0
