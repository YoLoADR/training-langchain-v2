"""Bug v2 test — max_iterations=1 (l'agent ne peut pas terminer).

L'AgentExecutor doit avoir max_iterations > 1 pour permettre le cycle
Thought → Action → Observation → Final Answer.
"""

import pytest
from unittest.mock import MagicMock


class TestBugV2:
    """Bug v2 : max_iterations doit être > 1."""

    def test_agent_executor_max_iterations_is_reasonable(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, max_iterations=8, verbose=False)
        assert executor.max_iterations >= 3, "max_iterations should be >= 3 for ReAct"

    def test_agent_executor_default_iterations(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, verbose=False)
        assert executor.max_iterations == 8, "Default should be 8"

    def test_agent_executor_custom_iterations(self):
        from hirekit.agent.react_agent import get_agent_executor

        mock_llm = MagicMock()
        executor = get_agent_executor(llm=mock_llm, max_iterations=5, verbose=False)
        assert executor.max_iterations == 5