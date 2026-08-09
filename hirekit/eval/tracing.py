"""Tracing — intégration LangSmith pour l'évaluation des chaînes.

AT06 — Évaluation des chaînes et utilisation de LangSmith.
"""

from __future__ import annotations

from typing import Any


def get_langsmith_callback() -> Any:
    """AT06 — retourne le callback handler LangSmith pour tracer les chaînes."""
    raise NotImplementedError(
        "AT06 — implémentez get_langsmith_callback() dans hirekit/eval/tracing.py"
    )
