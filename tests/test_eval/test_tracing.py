"""Tests pour hirekit.eval.tracing — AT06."""
import pytest


class TestGetLangsmithCallback:
    @pytest.mark.xfail(reason="AT06 non implémenté sur cette branche")
    def test_get_langsmith_callback(self):
        from hirekit.eval.tracing import get_langsmith_callback
        callback = get_langsmith_callback()
        assert callback is not None
