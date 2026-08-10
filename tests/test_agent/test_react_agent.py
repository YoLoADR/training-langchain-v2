"""Tests pour hirekit.agent.react_agent — AT04."""

import pytest
from unittest.mock import MagicMock, patch


class TestGetAgentExecutor:
    """AT04 — get_agent_executor() assemble l'AgentExecutor ReAct."""

    def test_get_agent_executor(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, verbose=False)
        assert executor is not None
        assert hasattr(executor, "invoke")

    def test_get_agent_executor_has_tools(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, verbose=False)
        assert hasattr(executor, "tools")
        assert len(executor.tools) >= 4

    def test_get_agent_executor_max_iterations(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, max_iterations=5, verbose=False)
        assert executor.max_iterations == 5

    def test_get_agent_executor_return_intermediate_steps(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, verbose=False)
        assert executor.return_intermediate_steps is True

    def test_get_agent_executor_custom_tools(self):
        from hirekit.agent.react_agent import get_agent_executor
        from langchain_core.tools import tool

        @tool("custom_tool")
        def custom_tool(query: str) -> str:
            """A custom tool for testing."""
            return "custom result"

        mock_llm = MagicMock()
        executor = get_agent_executor(tools=[custom_tool], llm=mock_llm, verbose=False)
        assert len(executor.tools) == 1
        assert executor.tools[0].name == "custom_tool"


class TestGetAgentExecutorWithMemory:
    """AT04 — get_agent_executor_with_memory() ajoute la mémoire."""

    def test_get_agent_executor_with_memory(self):
        from hirekit.agent.react_agent import get_agent_executor_with_memory

        mock_llm = MagicMock()
        executor = get_agent_executor_with_memory(llm=mock_llm, verbose=False)
        assert executor is not None
        assert hasattr(executor, "invoke")
        # L'executor avec mémoire a un attribut memory
        assert hasattr(executor, "memory") or hasattr(executor, "agent")


class TestRunAgent:
    """AT04 — run_agent() exécute l'agent sur une requête."""

    def test_run_agent_returns_dict(self):
        from hirekit.agent.react_agent import run_agent

        mock_llm = MagicMock()
        # L'agent peut échouer sans vraie API, mais doit retourner un dict
        with patch("hirekit.agent.react_agent.get_agent_executor") as mock_get:
            mock_executor = MagicMock()
            mock_executor.invoke.return_value = {
                "output": "Marie Dubois a 4 ans en React.",
                "intermediate_steps": [],
            }
            mock_get.return_value = mock_executor

            result = run_agent("Qui a de l'expérience en React ?", llm=mock_llm)
            assert isinstance(result, dict)
            assert "output" in result
            assert "intermediate_steps" in result
            assert "num_steps" in result


class TestRunAutonomousAgent:
    """AT04 — run_autonomous_agent() exécute un scénario multi-requêtes."""

    def test_run_autonomous_agent_returns_list(self):
        from hirekit.agent.react_agent import run_autonomous_agent

        mock_llm = MagicMock()
        with patch("hirekit.agent.react_agent.get_agent_executor_with_memory") as mock_get:
            mock_executor = MagicMock()
            mock_executor.invoke.return_value = {
                "output": "Résultat",
                "intermediate_steps": [],
            }
            mock_get.return_value = mock_executor

            scenario = ["Qui a de l'expérience en React ?", "Match Marie avec l'offre"]
            results = run_autonomous_agent(scenario, llm=mock_llm)
            assert isinstance(results, list)
            assert len(results) == 2
            assert "query" in results[0]
            assert "output" in results[0]