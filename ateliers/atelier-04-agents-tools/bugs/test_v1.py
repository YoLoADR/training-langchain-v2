"""Bug v1 test — Outil sans description (@tool decorator).

L'outil doit avoir un nom explicite et une description claire pour
que l'agent ReAct sache quand l'utiliser.
"""

import pytest


class TestBugV1:
    """Bug v1 : les outils doivent avoir un nom et une description."""

    def test_search_cvs_tool_has_name(self):
        from hirekit.agent.tools import search_cvs_tool

        assert search_cvs_tool.name == "search_cvs"

    def test_search_cvs_tool_has_description(self):
        from hirekit.agent.tools import search_cvs_tool

        assert len(search_cvs_tool.description) > 10
        assert "recherche" in search_cvs_tool.description.lower() or "cv" in search_cvs_tool.description.lower()

    def test_all_tools_have_descriptions(self):
        from hirekit.agent.tools import get_all_tools

        tools = get_all_tools()
        for tool in tools:
            assert len(tool.description) > 10, f"Tool {tool.name} has no description"

    def test_all_tools_have_names(self):
        from hirekit.agent.tools import get_all_tools

        tools = get_all_tools()
        names = {t.name for t in tools}
        assert "search_cvs" in names
        assert "match_candidate" in names
        assert "web_search" in names
        assert "python_repl" in names