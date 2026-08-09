"""Tests pour hirekit.agent.react_agent — AT04."""
import pytest


class TestGetAgentExecutor:
    @pytest.mark.xfail(reason="AT04 non implémenté sur cette branche")
    def test_get_agent_executor(self):
        from hirekit.agent.react_agent import get_agent_executor
        executor = get_agent_executor()
        assert hasattr(executor, "invoke")
