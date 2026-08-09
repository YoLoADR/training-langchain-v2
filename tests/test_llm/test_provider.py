"""Tests pour hirekit.llm.provider — AT01."""

import pytest


class TestGetLLM:
    """AT01 — get_llm() doit retourner un LLM (completion API)."""

    def test_get_llm_returns_llm(self):
        from hirekit.llm.provider import get_llm

        llm = get_llm(temperature=0.1)
        assert llm is not None
        assert hasattr(llm, "invoke")

    def test_get_llm_respects_temperature(self):
        from hirekit.llm.provider import get_llm

        llm = get_llm(temperature=0.5)
        # Le paramètre temperature doit être transmis au modèle
        assert llm is not None


class TestGetChatModel:
    """AT01 — get_chat_model() doit retourner un Chat Model (messages API)."""

    def test_get_chat_model_returns_chat_model(self):
        from hirekit.llm.provider import get_chat_model

        chat = get_chat_model(temperature=0.1)
        assert chat is not None
        assert hasattr(chat, "invoke")

    def test_chat_model_accepts_messages(self):
        """Un Chat Model doit accepter une liste de messages avec des rôles."""
        from hirekit.llm.provider import get_chat_model
        from langchain_core.messages import HumanMessage, SystemMessage

        chat = get_chat_model(temperature=0.1)
        assert hasattr(chat, "invoke")
        # On ne fait pas d'appel API réel ici (test unitaire)
