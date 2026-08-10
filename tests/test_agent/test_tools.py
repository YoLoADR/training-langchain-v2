"""Tests pour hirekit.agent.tools — AT04."""

import pytest


class TestSearchCvsTool:
    """AT04 — search_cvs_tool recherche dans les CVs via RAG."""

    def test_search_cvs_tool_is_decorated(self):
        from hirekit.agent.tools import search_cvs_tool
        from langchain_core.tools import BaseTool

        assert isinstance(search_cvs_tool, BaseTool)

    def test_search_cvs_tool_name(self):
        from hirekit.agent.tools import search_cvs_tool

        assert search_cvs_tool.name == "search_cvs"

    def test_search_cvs_tool_has_description(self):
        from hirekit.agent.tools import search_cvs_tool

        assert len(search_cvs_tool.description) > 10

    def test_search_cvs_tool_returns_string(self):
        """L'outil doit retourner une string même en cas d'erreur."""
        from hirekit.agent.tools import search_cvs_tool

        # Sans index FAISS, doit retourner un message d'erreur clair
        result = search_cvs_tool.invoke({"query": "React Python"})
        assert isinstance(result, str)
        assert len(result) > 0


class TestWebSearchTool:
    """AT04 — web_search_tool simule une recherche web."""

    def test_web_search_tool_is_decorated(self):
        from hirekit.agent.tools import web_search_tool
        from langchain_core.tools import BaseTool

        assert isinstance(web_search_tool, BaseTool)

    def test_web_search_tool_returns_string(self):
        from hirekit.agent.tools import web_search_tool

        result = web_search_tool.invoke({"query": "Marie Dubois développeur React"})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_web_search_mock_responses(self):
        """Les réponses simulées doivent contenir des mots-clés pertinents."""
        from hirekit.agent.tools import web_search_tool

        result = web_search_tool.invoke({"query": "github profile"})
        assert "GitHub" in result or "github" in result.lower()

    def test_web_search_default_response(self):
        """Les requêtes sans mot-clé connu doivent avoir une réponse par défaut."""
        from hirekit.agent.tools import web_search_tool

        result = web_search_tool.invoke({"query": "technologie inconnue xyz123"})
        assert "Web Search" in result


class TestPythonReplTool:
    """AT04 — python_repl_tool exécute du code Python."""

    def test_python_repl_tool_is_decorated(self):
        from hirekit.agent.tools import python_repl_tool
        from langchain_core.tools import BaseTool

        assert isinstance(python_repl_tool, BaseTool)

    def test_python_repl_executes_code(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "print('Hello World')"})
        assert "Hello World" in result

    def test_python_repl_computes_math(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "x = 2 + 3; print(x)"})
        assert "5" in result

    def test_python_repl_returns_variables(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "score = 0.85; name = 'Marie'"})
        assert "score" in result
        assert "0.85" in result
        assert "Marie" in result

    def test_python_repl_handles_errors(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "1/0"})
        assert "Erreur" in result or "Error" in result


class TestMatchCandidateTool:
    """AT04 — match_candidate_tool matching CV↔offre via LCEL."""

    def test_match_candidate_tool_is_decorated(self):
        from hirekit.agent.tools import match_candidate_tool
        from langchain_core.tools import BaseTool

        assert isinstance(match_candidate_tool, BaseTool)

    def test_match_candidate_tool_name(self):
        from hirekit.agent.tools import match_candidate_tool

        assert match_candidate_tool.name == "match_candidate"


class TestGetAllTools:
    """AT04 — get_all_tools() retourne 4 outils."""

    def test_get_all_tools_returns_4(self):
        from hirekit.agent.tools import get_all_tools

        tools = get_all_tools()
        assert len(tools) >= 4

    def test_get_all_tools_names(self):
        from hirekit.agent.tools import get_all_tools

        tools = get_all_tools()
        names = {t.name for t in tools}
        assert "search_cvs" in names
        assert "match_candidate" in names
        assert "web_search" in names
        assert "python_repl" in names

    def test_all_tools_are_base_tool(self):
        from hirekit.agent.tools import get_all_tools
        from langchain_core.tools import BaseTool

        tools = get_all_tools()
        for tool in tools:
            assert isinstance(tool, BaseTool)