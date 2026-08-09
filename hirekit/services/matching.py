"""Matching service — chaîne LCEL de matching CV↔offre.

AT02 — LCEL : composer des chaînes de manière déclarative.
"""

from __future__ import annotations

from langchain_core.runnables import Runnable


def get_matching_chain() -> Runnable:
    """AT02 — retourne la chaîne LCEL de matching CV↔offre.

    Chaîne : RunnablePassthrough | prompt | llm | parser → MatchResult
    """
    raise NotImplementedError(
        "AT02 — implémentez get_matching_chain() dans hirekit/services/matching.py"
    )
