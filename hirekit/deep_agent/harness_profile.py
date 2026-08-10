"""HarnessProfile pour Deep Agents — configuration du comportement de l'agent.

Inspiration: sellkit/src/harness-profile.ts

Enregistre le harness profile pour exclure les middleware et tools non nécessaires:
- excludedTools: write_todos, task, filesystem tools (non utilisés en conversation)
- excludedMiddleware: SummarizationMiddleware, todoListMiddleware
- generalPurposeSubagent: disabled

Docs: https://docs.langchain.com/oss/python/deepagents/overview
"""

from __future__ import annotations

from typing import Any


def register_recruiter_harness_profile() -> None:
    """Enregistre le harness profile pour le recruteur.

    Doit être appelé au niveau module (avant la création de l'agent).
    """
    try:
        from deepagents import register_harness_profile, create_harness_profile

        profile = create_harness_profile(
            base_system_prompt=None,
            system_prompt_suffix="",
            excluded_tools=[
                "write_todos",
                "task",
                "ls",
                "read_file",
                "write_file",
                "edit_file",
                "glob",
                "grep",
                "execute",
            ],
            excluded_middleware=[
                "SummarizationMiddleware",
                "todoListMiddleware",
            ],
            general_purpose_subagent={"enabled": False},
        )

        register_harness_profile("claude-sonnet-4-5", profile)
        register_harness_profile("claude-sonnet-4-6", profile)
        register_harness_profile("gpt-4o", profile)
        register_harness_profile("ollama", profile)
    except ImportError:
        pass


register_recruiter_harness_profile()
