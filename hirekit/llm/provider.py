"""LLM Provider — abstraction Claude / OpenAI / Ollama.

AT01 — LLMs vs Chat Models : ce module expose les deux interfaces.
Le provider est sélectionné via la variable d'environnement LLM_PROVIDER.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.llms import LLM

from hirekit.config import (
    LLM_PROVIDER,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OLLAMA_HOST,
    OLLAMA_MODEL,
)


def get_llm(temperature: float = 0.1, max_tokens: int = 1024, **kwargs: Any) -> LLM:
    """Retourne un LLM (completion API) selon LLM_PROVIDER.

    AT01 : utilisez cette fonction pour comparer LLMs vs Chat Models.

    Providers supportés : "anthropic", "openai", "ollama".
    """
    provider = LLM_PROVIDER.lower()

    if provider == "anthropic":
        from langchain_anthropic import AnthropicLLM

        return AnthropicLLM(
            model=ANTHROPIC_MODEL,
            api_key=ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    if provider == "openai":
        from langchain_openai import OpenAI

        return OpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    if provider == "ollama":
        from langchain_ollama import OllamaLLM

        return OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_HOST,
            temperature=temperature,
            **kwargs,
        )

    raise ValueError(
        f"Provider LLM non supporté: '{provider}'. "
        f"Choisissez: anthropic, openai, ou ollama."
    )


def get_chat_model(
    temperature: float = 0.1, max_tokens: int = 1024, **kwargs: Any
) -> BaseChatModel:
    """Retourne un Chat Model (messages API) selon LLM_PROVIDER.

    AT01 : utilisez cette fonction pour comparer LLMs vs Chat Models.

    Providers supportés : "anthropic", "openai", "ollama".
    """
    provider = LLM_PROVIDER.lower()

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=ANTHROPIC_MODEL,
            api_key=ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_HOST,
            temperature=temperature,
            **kwargs,
        )

    raise ValueError(
        f"Provider Chat Model non supporté: '{provider}'. "
        f"Choisissez: anthropic, openai, ou ollama."
    )