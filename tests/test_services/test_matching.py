"""Tests pour hirekit.services.matching — AT02."""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestMatchingChain:
    """AT02 — get_matching_chain() doit retourner une chaîne LCEL."""

    def test_get_matching_chain_returns_runnable(self):
        """La chaîne de matching doit être un Runnable avec .invoke."""
        from hirekit.services.matching import get_matching_chain

        # Mock le LLM pour éviter un appel API
        mock_llm = MagicMock()
        chain = get_matching_chain(llm=mock_llm)
        assert chain is not None
        assert hasattr(chain, "invoke")
        assert hasattr(chain, "batch")

    def test_get_matching_chain_accepts_cv_and_offer(self):
        """La chaîne doit accepter un dict avec 'cv' et 'offer'."""
        from hirekit.services.matching import get_matching_chain
        from hirekit.llm.parsers import MatchResult
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        valid_json = json.dumps({
            "score": 0.85,
            "justification": "Bonne correspondance",
            "points_forts": ["React 4 ans"],
            "points_faibles": ["Pas de TypeScript"],
            "recommandation": "shortlister",
        })
        fake_llm = FakeListChatModel(responses=[valid_json])

        chain = get_matching_chain(llm=fake_llm)
        result = chain.invoke({
            "cv": "Marie Dubois, React 4 ans",
            "offer": "Développeur React",
        })

        assert isinstance(result, MatchResult)
        assert 0.0 <= result.score <= 1.0
        assert len(result.justification) > 0


class TestCleanCV:
    """AT02 — prétraitement RunnableLambda."""

    def test_clean_cv_strips_whitespace(self):
        from hirekit.services.matching import clean_cv

        result = clean_cv("  Marie Dubois  ")
        assert result == "Marie Dubois"

    def test_clean_cv_truncates_long_text(self):
        from hirekit.services.matching import clean_cv

        long_cv = "A" * 3000
        result = clean_cv(long_cv)
        assert len(result) == 2003  # 2000 + "..."

    def test_clean_cv_lambda_is_runnable(self):
        from hirekit.services.matching import clean_cv_lambda

        assert hasattr(clean_cv_lambda, "invoke")
        result = clean_cv_lambda.invoke({"cv": "  test  "})
        assert "test" in result


class TestBatchMatch:
    """AT02 — .batch() pour traiter plusieurs CVs."""

    def test_batch_match_returns_list(self):
        from hirekit.services.matching import batch_match
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        valid_json = json.dumps({
            "score": 0.5,
            "justification": "Test",
            "points_forts": [],
            "points_faibles": [],
            "recommandation": "à voir",
        })
        fake_llm = FakeListChatModel(responses=[valid_json, valid_json, valid_json])

        results = batch_match(
            ["CV 1", "CV 2", "CV 3"],
            "Offre test",
            llm=fake_llm,
        )

        assert isinstance(results, list)
        assert len(results) == 3


class TestRecruiterMemory:
    """AT02 — ConversationBufferWindowMemory."""

    def test_get_recruiter_memory_returns_memory(self):
        from hirekit.services.matching import get_recruiter_memory
        from langchain_classic.memory import ConversationBufferWindowMemory

        memory = get_recruiter_memory(k=10)
        assert isinstance(memory, ConversationBufferWindowMemory)
        assert memory.k == 10


class TestMemoryPersistence:
    """AT02 — save/load mémoire en JSON."""

    def test_load_nonexistent_memory_returns_empty(self, tmp_path: Path):
        from hirekit.services.matching import load_memory

        memory = load_memory(tmp_path / "nonexistent.json")
        assert memory is not None

    def test_save_and_load_memory(self, tmp_path: Path):
        from hirekit.services.matching import save_memory, load_memory, get_recruiter_memory
        from langchain_core.messages import HumanMessage, AIMessage

        memory = get_recruiter_memory(k=10)
        memory.chat_memory.add_message(HumanMessage(content="Qui a de l'expérience en React ?"))
        memory.chat_memory.add_message(AIMessage(content="Marie Dubois a 4 ans d'expérience."))

        path = tmp_path / "memory.json"
        save_memory(memory, path)
        assert path.exists()

        loaded = load_memory(path, k=10)
        assert loaded is not None