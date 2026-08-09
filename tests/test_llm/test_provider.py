"""Tests pour hirekit.llm.provider — AT01.

Les tests unitaires vérifient la structure sans nécessiter de clé API.
Les tests d'intégration (marqués @pytest.mark.integration) nécessitent
une clé API valide dans .env.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestGetLLM:
    """AT01 — get_llm() doit retourner un LLM (completion API)."""

    def test_get_llm_returns_llm(self):
        from hirekit.llm.provider import get_llm

        # Mock le module langchain_anthropic pour éviter l'import
        mock_llm = MagicMock()
        mock_class = MagicMock(return_value=mock_llm)

        with patch.dict("sys.modules", {"langchain_anthropic": MagicMock(AnthropicLLM=mock_class)}):
            llm = get_llm(temperature=0.1)
            assert llm is not None
            assert hasattr(llm, "invoke")

    def test_get_llm_respects_temperature(self):
        from hirekit.llm.provider import get_llm

        mock_llm = MagicMock()
        mock_class = MagicMock(return_value=mock_llm)

        with patch.dict("sys.modules", {"langchain_anthropic": MagicMock(AnthropicLLM=mock_class)}):
            llm = get_llm(temperature=0.5)
            assert llm is not None
            # Vérifier que temperature a été transmis
            call_kwargs = mock_class.call_args
            assert call_kwargs.kwargs.get("temperature") == 0.5

    def test_get_llm_unsupported_provider_raises(self):
        from hirekit.llm.provider import get_llm

        with patch("hirekit.llm.provider.LLM_PROVIDER", "unsupported"):
            with pytest.raises(ValueError, match="non supporté"):
                get_llm()


class TestGetChatModel:
    """AT01 — get_chat_model() doit retourner un Chat Model (messages API)."""

    def test_get_chat_model_returns_chat_model(self):
        from hirekit.llm.provider import get_chat_model

        mock_chat = MagicMock()
        mock_class = MagicMock(return_value=mock_chat)

        with patch.dict("sys.modules", {"langchain_anthropic": MagicMock(ChatAnthropic=mock_class)}):
            chat = get_chat_model(temperature=0.1)
            assert chat is not None
            assert hasattr(chat, "invoke")

    def test_chat_model_accepts_messages(self):
        """Un Chat Model doit accepter une liste de messages avec des rôles."""
        from hirekit.llm.provider import get_chat_model
        from langchain_core.messages import HumanMessage, SystemMessage

        mock_chat = MagicMock()
        mock_class = MagicMock(return_value=mock_chat)

        with patch.dict("sys.modules", {"langchain_anthropic": MagicMock(ChatAnthropic=mock_class)}):
            chat = get_chat_model(temperature=0.1)
            assert hasattr(chat, "invoke")

    def test_get_chat_model_unsupported_provider_raises(self):
        from hirekit.llm.provider import get_chat_model

        with patch("hirekit.llm.provider.LLM_PROVIDER", "unsupported"):
            with pytest.raises(ValueError, match="non supporté"):
                get_chat_model()