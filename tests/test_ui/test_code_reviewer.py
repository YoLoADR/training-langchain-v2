"""Tests pour hirekit.ui.code_reviewer — AT05."""
import pytest


class TestIndexCodeRepo:
    @pytest.mark.xfail(reason="AT05 non implémenté sur cette branche")
    def test_index_code_repo(self):
        from hirekit.ui.code_reviewer import index_code_repo
        retriever = index_code_repo("data/code_repo/")
        assert retriever is not None
