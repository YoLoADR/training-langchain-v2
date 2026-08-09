"""Matching service — chaîne LCEL de matching CV↔offre.

AT02 — LCEL : composer des chaînes de manière déclarative.
AT02 — Mémoire : ConversationBufferWindowMemory, persistence JSON.

Ce module implémente :
  - Chaîne LCEL de matching (RunnablePassthrough | prompt | llm | parser)
  - RunnableLambda pour le prétraitement du CV
  - RunnableParallel pour extraction + matching en parallèle
  - RunnablePassthrough.assign() pour les variables d'état
  - ConversationBufferWindowMemory (k=10)
  - Persistence save/load en JSON
  - .batch() pour traiter plusieurs CVs
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

# LangChain v1.x: les classes Memory sont dans langchain_classic
try:
    from langchain_classic.base_memory import BaseMemory
except ImportError:
    from langchain_core.memory import BaseMemory  # type: ignore

from hirekit.llm.parsers import MatchResult, get_match_parser
from hirekit.llm.prompts import get_matching_prompt


# ─── Prétraitement (RunnableLambda) ─────────────────────────────────────────


def clean_cv(cv_text: str) -> str:
    """Nettoie et tronque le texte du CV."""
    cleaned = cv_text.strip()
    # Troncature à 2000 caractères pour éviter les prompts trop longs
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + "..."
    return cleaned


def clean_offer(offer_text: str) -> str:
    """Nettoie le texte de l'offre d'emploi."""
    return offer_text.strip()


clean_cv_lambda = RunnableLambda(lambda x: clean_cv(x["cv"]), name="clean_cv")
clean_offer_lambda = RunnableLambda(lambda x: clean_offer(x["offer"]), name="clean_offer")


# ─── Chaîne LCEL de matching ─────────────────────────────────────────────────


def get_matching_chain(llm: BaseChatModel | None = None) -> Runnable:
    """AT02 — retourne la chaîne LCEL de matching CV↔offre.

    Chaîne :
        RunnablePassthrough
        → clean_cv (RunnableLambda)
        → ChatPromptTemplate (matching)
        → ChatModel
        → PydanticOutputParser (MatchResult)

    Entrée : dict avec clés "cv" et "offer"
    Sortie : MatchResult (objet Pydantic avec score, justification, etc.)

    Si llm=None, utilise get_chat_model() par défaut.
    """
    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    parser = get_match_parser()
    prompt = get_matching_prompt()

    chain = (
        RunnablePassthrough.assign(cv=lambda x: clean_cv(x["cv"]))
        .assign(offer=lambda x: clean_offer(x["offer"]))
        .assign(format_instructions=lambda _: parser.get_format_instructions())
        | prompt
        | llm
        | parser
    )

    return chain


# ─── Extraction + matching en parallèle (RunnableParallel) ─────────────────


def get_extraction_and_matching_chain(llm: BaseChatModel | None = None) -> Runnable:
    """AT02 — chaîne parallèle : extraction CV + matching en simultané.

    Utilise RunnableParallel pour lancer l'extraction et le matching
    en parallèle sur le même input.
    """
    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    from hirekit.llm.parsers import get_cv_parser
    from hirekit.llm.prompts import get_cv_extraction_prompt

    cv_parser = get_cv_parser()
    extraction_prompt = get_cv_extraction_prompt()
    match_chain = get_matching_chain(llm)

    extraction_chain = extraction_prompt | llm | cv_parser

    parallel = RunnableParallel(
        extraction=extraction_chain,
        matching=match_chain,
    )

    return parallel


# ─── Mémoire conversationnelle ───────────────────────────────────────────────


def get_recruiter_memory(k: int = 10) -> BaseMemory:
    """AT02 — retourne une ConversationBufferWindowMemory pour le recruteur.

    k=10 : garde les 10 derniers échanges (fenêtre glissante).
    """
    from langchain_classic.memory import ConversationBufferWindowMemory

    return ConversationBufferWindowMemory(
        k=k,
        memory_key="history",
        return_messages=True,
    )


def get_summary_memory(llm: BaseChatModel | None = None) -> BaseMemory:
    """AT02 — retourne une ConversationSummaryMemory pour auto-summarisation.

    La mémoire résume automatiquement les anciens échanges pour économiser
    des tokens tout en gardant le contexte.
    """
    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    from langchain_classic.memory import ConversationSummaryMemory

    return ConversationSummaryMemory(
        llm=llm,
        memory_key="history",
        return_messages=True,
    )


# ─── Persistence de la mémoire ──────────────────────────────────────────────


def save_memory(memory: BaseMemory, path: str | Path) -> None:
    """AT02 — sauvegarde la mémoire en JSON pour persistence entre sessions.

    Sérialise les variables de mémoire dans un fichier JSON.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "memory_variables": memory.memory_variables,
        "type": type(memory).__name__,
    }

    # Tenter d'extraire le buffer (ConversationBufferWindowMemory)
    if hasattr(memory, "buffer_window"):
        messages = memory.buffer_window
        data["messages"] = [
            {"type": m.__class__.__name__, "content": m.content}
            for m in messages
        ]

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_memory(path: str | Path, k: int = 10) -> BaseMemory:
    """AT02 — charge une mémoire depuis un fichier JSON.

    Reconstruit une ConversationBufferWindowMemory à partir des données
    sauvegardées. Retourne une mémoire vide si le fichier n'existe pas.
    """
    path = Path(path)
    if not path.exists():
        return get_recruiter_memory(k=k)

    data = json.loads(path.read_text(encoding="utf-8"))
    memory = get_recruiter_memory(k=k)

    # Reconstruire les messages
    messages_data = data.get("messages", [])
    from langchain_core.messages import HumanMessage, AIMessage

    for msg_data in messages_data[-k * 2 :]:  # k échanges = 2k messages
        msg_type = msg_data.get("type", "")
        content = msg_data.get("content", "")
        if "Human" in msg_type:
            memory.chat_memory.add_message(HumanMessage(content=content))
        elif "AI" in msg_type or "AIMessage" in msg_type:
            memory.chat_memory.add_message(AIMessage(content=content))

    return memory


# ─── Chaîne avec mémoire (variables d'état) ─────────────────────────────────


def get_matching_chain_with_memory(
    memory: BaseMemory | None = None,
    llm: BaseChatModel | None = None,
) -> Runnable:
    """AT02 — chaîne de matching avec mémoire conversationnelle.

    La chaîne injecte l'historique des échanges dans le prompt via
    RunnablePassthrough.assign() (variables d'état).
    """
    if memory is None:
        memory = get_recruiter_memory()
    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    base_chain = get_matching_chain(llm)

    def inject_memory(inputs: dict) -> dict:
        history = memory.load_memory_variables({}).get("history", [])
        inputs["history"] = history
        return inputs

    chain_with_memory = RunnableLambda(inject_memory) | base_chain

    return chain_with_memory


# ─── Batch processing ─────────────────────────────────────────────────────────


def batch_match(
    cvs: list[str],
    offer: str,
    llm: BaseChatModel | None = None,
) -> list[MatchResult]:
    """AT02 — traite plusieurs CVs en parallèle avec .batch().

    Exemple : matcher 3 CVs contre la même offre en un seul appel.
    """
    chain = get_matching_chain(llm)
    inputs = [{"cv": cv, "offer": offer} for cv in cvs]
    return chain.batch(inputs)