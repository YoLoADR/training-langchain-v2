"""Agent ReAct — raisonnement + actions en boucle.

AT04 — Agent : raisonnement (ReAct) et cycle de l'Agent Executor.
"""

from __future__ import annotations

from langchain.agents import AgentExecutor


def get_agent_executor(
    tools: list | None = None,
    memory_k: int = 10,
    max_iterations: int = 8,
    verbose: bool = True,
) -> AgentExecutor:
    """AT04 — assemble l'AgentExecutor ReAct avec mémoire."""
    raise NotImplementedError(
        "AT04 — implémentez get_agent_executor() dans hirekit/agent/react_agent.py"
    )
