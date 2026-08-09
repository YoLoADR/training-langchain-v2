"""Tests pour hirekit.services.matching — AT02."""
import pytest


class TestMatchingChain:
    """AT02 — get_matching_chain() doit retourner une chaîne LCEL."""

    @pytest.mark.xfail(reason="AT02 non implémenté sur cette branche")
    def test_get_matching_chain(self):
        from hirekit.services.matching import get_matching_chain
        chain = get_matching_chain()
        assert hasattr(chain, "invoke")
