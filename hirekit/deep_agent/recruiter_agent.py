"""Deep Agent recruteur — create_deep_agent() 4 couches.

Inspiration: sellkit/src/agent/deep-agent.ts

Architecture native Deep Agents: 4 couches
  Couche 1: systemPrompt  — Identité statique (nom, entreprise, ton) + AGENTS.md
  Couche 2: memory        — AGENTS.md injecté dans systemPrompt (fs.readFileSync)
  Couche 3: skills        — SKILL.md injecté par middleware beforeModel
  Couche 4: contextSchema  — RecruitmentContext (Pydantic) + contexte dynamique

Docs: https://docs.langchain.com/oss/python/deepagents/overview
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from hirekit.config import (
    LLM_PROVIDER,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from hirekit.deep_agent.middleware import (
    RecruitmentContext,
    create_recruitment_context_middleware,
)
from hirekit.deep_agent.harness_profile import register_recruiter_harness_profile

AGENT_DIR = Path(__file__).resolve().parent.parent.parent / ".agent"

agents_md_path = AGENT_DIR / "memory" / "recruiter" / "AGENTS.md"
AGENTS_MD = agents_md_path.read_text(encoding="utf-8") if agents_md_path.exists() else ""

IDENTITY_PROMPT = f"""Tu es HireKit, un assistant IA pour recruteurs.
Tu analyses des CVs, matches des candidats avec des offres d'emploi, et génères des grilles d'entretien.
Tu réponds en français, de manière structurée et professionnelle.
Ton ton est friendly, professional, conversational.
Tes réponses sont courtes (3 phrases max).

{AGENTS_MD}"""

_agent: Any = None


def _get_model():
    """Retourne le LLM selon le provider configuré."""
    if LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=ANTHROPIC_MODEL, temperature=0.7, max_retries=5)
    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=OPENAI_MODEL, temperature=0.7, max_retries=5)
    else:
        raise RuntimeError(f"LLM provider {LLM_PROVIDER} non configuré ou sans clé API")


def get_deep_agent():
    """Crée ou retourne l'agent Deep Agent (singleton).

    Returns un compiled LangGraph avec .invoke() et .withConfig().
    """
    global _agent
    if _agent is not None:
        return _agent

    from deepagents import create_deep_agent

    register_recruiter_harness_profile()

    model = _get_model()
    middleware = create_recruitment_context_middleware(str(AGENT_DIR))

    _agent = create_deep_agent(
        model=model,
        system_prompt=IDENTITY_PROMPT,
        context_schema=RecruitmentContext,
        middleware=[middleware],
        checkpointer=False,
        tools=[],
        subagents=[],
        name="hirekit-recruiter",
    )

    return _agent


def run_deep_turn(
    candidate_phone: str,
    messages: list,
    context: RecruitmentContext | dict,
) -> str:
    """Exécute un tour de conversation avec le Deep Agent.

    Args:
        candidate_phone: identifiant candidat (clé CRM)
        messages: historique de conversation (BaseMessage[])
        context: RecruitmentContext (qualCount, stage, memory, objection, etc.)

    Returns:
        La réponse texte du LLM
    """
    agent = get_deep_agent()

    formatted_messages = []
    for m in messages:
        msg_type = m._getType() if hasattr(m, "_getType") else "human"
        role = "user" if msg_type == "human" else "system" if msg_type == "system" else "assistant"
        content = m.content if isinstance(m.content, str) else str(m.content)
        formatted_messages.append({"role": role, "content": content})

    agent_with_limit = agent.withConfig(recursion_limit=200)

    if isinstance(context, dict):
        context = RecruitmentContext(**context)

    result = agent_with_limit.invoke(
        {"messages": formatted_messages},
        {"context": context},
    )

    ai_messages = [
        m
        for m in (result.get("messages") or [])
        if hasattr(m, "_getType") and m._getType() == "ai" and m.content
    ]
    if not ai_messages:
        return ""

    reply = ai_messages[-1]
    content = reply.content if isinstance(reply.content, str) else str(reply.content)
    return content
