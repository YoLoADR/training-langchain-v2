"""Tools — outils pour l'agent ReAct.

AT04 — Tools : appeler des APIs (search_cvs, match) + exécuter du code (python_repl)
+ recherches web.
"""

from __future__ import annotations

from langchain_core.tools import BaseTool


def search_cvs_tool(query: str) -> str:
    """AT04 — recherche de candidats dans la base de CVs (RAG)."""
    raise NotImplementedError("AT04 — implémentez search_cvs_tool() dans hirekit/agent/tools.py")


def match_candidate_tool(cv_text: str, offer_text: str) -> str:
    """AT04 — matching candidat↔offre via la chaîne LCEL."""
    raise NotImplementedError(
        "AT04 — implémentez match_candidate_tool() dans hirekit/agent/tools.py"
    )


def web_search_tool(query: str) -> str:
    """AT04 — recherche web (simulée ou serpapi)."""
    raise NotImplementedError("AT04 — implémentez web_search_tool() dans hirekit/agent/tools.py")


def python_repl_tool(code: str) -> str:
    """AT04 — exécution de code Python (PythonREPLTool)."""
    raise NotImplementedError("AT04 — implémentez python_repl_tool() dans hirekit/agent/tools.py")


def get_all_tools() -> list[BaseTool]:
    """AT04 — retourne la liste des 4 outils pour l'agent ReAct."""
    raise NotImplementedError("AT04 — implémentez get_all_tools() dans hirekit/agent/tools.py")
