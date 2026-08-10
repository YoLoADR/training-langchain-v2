"""Test d'intégration pour hirekit.deep_agent — create_deep_agent + invoke.

Inspiré de sellkit/tests/integration/v3-agent.test.ts (73 lignes).
Nécessite: une clé API (ANTHROPIC_API_KEY ou OPENAI_API_KEY) dans .env.

Skip si pas de clé API.
"""

import os

import pytest

from hirekit.config import ANTHROPIC_API_KEY, OPENAI_API_KEY

has_api_key = bool(ANTHROPIC_API_KEY or OPENAI_API_KEY)

pytestmark = pytest.mark.skipif(not has_api_key, reason="Pas de clé API configurée")


class TestDeepAgentIntegration:
    """Tests d'intégration: create_deep_agent + invoke (nécessite un LLM)."""

    @pytest.mark.timeout(60)
    def test_get_deep_agent_returns_compiled_agent(self):
        """get_deep_agent() doit retourner un agent compilé avec .invoke()."""
        from hirekit.deep_agent.recruiter_agent import get_deep_agent

        agent = get_deep_agent()
        assert agent is not None
        assert hasattr(agent, "invoke")

    @pytest.mark.timeout(60)
    def test_run_deep_turn_with_minimal_context(self):
        """run_deep_turn avec un contexte minimal doit retourner une réponse non vide."""
        from hirekit.deep_agent.recruiter_agent import run_deep_turn
        from hirekit.deep_agent.middleware import RecruitmentContext
        from langchain_core.messages import HumanMessage

        messages = [HumanMessage(content="Bonjour")]
        ctx = RecruitmentContext(qual_count=0, stage="new")

        reply = run_deep_turn("test-integration-phone", messages, ctx)
        assert reply is not None
        assert len(reply) > 0

    @pytest.mark.timeout(60)
    def test_run_deep_turn_with_qualification_context(self):
        """run_deep_turn avec un contexte de qualification doit retourner une réponse."""
        from hirekit.deep_agent.recruiter_agent import run_deep_turn
        from hirekit.deep_agent.middleware import RecruitmentContext
        from langchain_core.messages import HumanMessage

        messages = [HumanMessage(content="Je m'appelle Nathan, je n'ai pas d'expérience")]
        ctx = RecruitmentContext(
            qual_count=1,
            stage="contacted",
            memory_prompt="- Nom: Nathan",
            next_field="experience",
        )

        reply = run_deep_turn("test-integration-qual", messages, ctx)
        assert reply is not None
        assert len(reply) > 0
