"""Code Reviewer — indexation et Q&A sur un repo de code.

AT05 — Compréhension du code : indexation et assistant d'aide au développement.
"""

from __future__ import annotations

from langchain_core.retrievers import BaseRetriever


def index_code_repo(repo_path: str) -> BaseRetriever:
    """AT05 — indexe un repo Python comme corpus RAG pour le Q&A sur le code."""
    raise NotImplementedError(
        "AT05 — implémentez index_code_repo() dans hirekit/ui/code_reviewer.py"
    )


def ask_code_question(question: str, retriever: BaseRetriever) -> str:
    """AT05 — pose une question sur le code indexé et retourne une réponse sourcée."""
    raise NotImplementedError(
        "AT05 — implémentez ask_code_question() dans hirekit/ui/code_reviewer.py"
    )
