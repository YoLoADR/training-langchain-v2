"""LLM Provider — abstraction Claude / OpenAI / Ollama.

AT01 — LLMs vs Chat Models : ce module expose les deux interfaces.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.llms import LLM


def get_llm(temperature: float = 0.1, max_tokens: int = 1024, **kwargs: Any) -> LLM:
    """Retourne un LLM (completion API) selon LLM_PROVIDER.

    AT01 : utilisez cette fonction pour comparer LLMs vs Chat Models.
    """
    raise NotImplementedError("AT01 — implémentez get_llm() dans hirekit/llm/provider.py")


def get_chat_model(
    temperature: float = 0.1, max_tokens: int = 1024, **kwargs: Any
) -> BaseChatModel:
    """Retourne un Chat Model (messages API) selon LLM_PROVIDER.

    AT01 : utilisez cette fonction pour comparer LLMs vs Chat Models.
    """
    raise NotImplementedError("AT01 — implémentez get_chat_model() dans hirekit/llm/provider.py")
