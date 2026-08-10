"""Tracing — intégration LangSmith pour l'évaluation des chaînes.

AT07 — Évaluation des chaînes et utilisation de LangSmith.

Inspiré de sellkit/src/index.ts:29-33 (LangSmith auto-tracing via env vars).
"""

from __future__ import annotations

import os
from typing import Any

from hirekit.config import LANGSMITH_API_KEY, LANGSMITH_PROJECT, LANGSMITH_TRACING


def get_langsmith_callback() -> Any:
    """AT07 — retourne le callback handler LangSmith pour tracer les chaînes.

    Si LangSmith n'est pas configuré (pas de clé API), retourne None.

    Returns:
        LangChainTracer ou None.
    """
    if not LANGSMITH_API_KEY:
        return None

    try:
        from langchain_core.tracers import LangChainTracer

        tracer = LangChainTracer(project_name=LANGSMITH_PROJECT)
        return tracer
    except ImportError:
        return None


def is_tracing_enabled() -> bool:
    """AT07 — vérifie si le tracing LangSmith est activé.

    Le tracing est activé si:
    1. LANGSMITH_TRACING=true dans .env
    2. LANGSMITH_API_KEY est présente
    """
    return LANGSMITH_TRACING and bool(LANGSMITH_API_KEY)


def enable_tracing() -> None:
    """AT07 — active le tracing LangSmith via les variables d'environnement.

    Inspire de sellkit/src/index.ts:29-33 qui définit les env vars automatiquement.
    """
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    if LANGSMITH_API_KEY:
        os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY


def get_run_tags(component: str, candidate: str | None = None) -> dict:
    """AT07 — retourne les tags pour une trace LangSmith.

    Args:
        component: nom du composant (ex: "rag", "agent", "deep_agent", "matching").
        candidate: identifiant candidat (optionnel).

    Returns:
        Dict de tags pour .invoke(..., tags=...).
    """
    tags = ["hirekit", component]
    if candidate:
        tags.append(f"candidate:{candidate}")
    return {"tags": tags}
