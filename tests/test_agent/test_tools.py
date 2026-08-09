"""Tests pour hirekit.agent.tools — AT04."""
import pytest


class TestGetAllTools:
    @pytest.mark.xfail(reason="AT04 non implémenté sur cette branche")
    def test_get_all_tools(self):
        from hirekit.agent.tools import get_all_tools
        tools = get_all_tools()
        assert len(tools) >= 4
