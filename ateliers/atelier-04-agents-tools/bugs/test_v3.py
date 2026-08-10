"""Bug v3 test — python_repl n'attrape pas les erreurs.

python_repl_tool doit attraper les exceptions et les retourner comme
observation (string) au lieu de les laisser remonter et crasher l'agent.
"""

import pytest


class TestBugV3:
    """Bug v3 : python_repl_tool doit gérer les erreurs gracieusement."""

    def test_python_repl_handles_division_by_zero(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "1/0"})
        assert isinstance(result, str)
        assert "Erreur" in result or "Error" in result

    def test_python_repl_handles_syntax_error(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "def broken("})
        assert isinstance(result, str)
        assert "Erreur" in result or "Error" in result

    def test_python_repl_handles_name_error(self):
        from hirekit.agent.tools import python_repl_tool

        result = python_repl_tool.invoke({"code": "print(undefined_variable)"})
        assert isinstance(result, str)
        assert "Erreur" in result or "Error" in result

    def test_python_repl_returns_string_not_exception(self):
        """L'outil doit toujours retourner une string, jamais lever une exception."""
        from hirekit.agent.tools import python_repl_tool

        # Même avec du code qui crash, l'outil doit retourner une string
        result = python_repl_tool.invoke({"code": "raise ValueError('test')"})
        assert isinstance(result, str)
        assert "ValueError" in result or "Erreur" in result