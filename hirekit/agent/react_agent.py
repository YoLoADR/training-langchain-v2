"""Agent ReAct — raisonnement + actions en boucle.

AT04 — Agent : raisonnement (ReAct) et cycle de l'Agent Executor.

L'agent ReAct (Reasoning + Acting) suit le cycle :
    Thought → Action → Observation → Thought → ... → Final Answer

Il choisit intelligemment parmi 4 outils :
1. search_cvs (RAG) — chercher des candidats dans les CVs
2. match_candidate (LCEL) — évaluer la correspondance CV↔offre
3. web_search — vérifier la réputation en ligne
4. python_repl — calculer un score composite
"""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from hirekit.agent.tools import get_all_tools


# ─── Prompt ReAct ────────────────────────────────────────────────────────────

REACT_SYSTEM_PROMPT = """Tu es HireKit Agent, un assistant recruteur intelligent qui peut
utiliser des outils pour aider les recruteurs.

Tu as accès aux outils suivants :
{tools}

Pour répondre à la question du recruteur, suis ce cycle :
Thought: réfléchis à ce qu'il faut faire
Action: choisis un outil parmi {tool_names}
Action Input: l'input pour l'outil
Observation: le résultat de l'outil
... (Thought/Action/Action Input/Observation peut se répéter N fois)
Thought: I now know the final answer
Final Answer: donne ta réponse finale au recruteur

Réponds toujours en français, de manière professionnelle et structurée.
Cite tes sources (CVs trouvés, résultats de recherche web).

Commence toujours par réfléchir (Thought) avant d'agir."""


def get_agent_executor(
    tools: list | None = None,
    memory_k: int = 10,
    max_iterations: int = 8,
    verbose: bool = True,
    llm: BaseChatModel | None = None,
):
    """AT04 — assemble l'AgentExecutor ReAct avec mémoire.

    Args:
        tools: liste d'outils (défaut: get_all_tools() = 4 outils).
        memory_k: taille de la fenêtre de mémoire (défaut: 10 échanges).
        max_iterations: nombre max d'itérations avant arrêt (défaut: 8).
        verbose: afficher la trace ReAct (défaut: True).
        llm: chat model (défaut: get_chat_model()).

    Returns:
        AgentExecutor configuré et prêt pour .invoke().
    """
    # LangChain v1.x: les classes agents sont dans langchain_classic
    try:
        from langchain_classic.agents import create_react_agent, AgentExecutor
    except ImportError:
        from langchain.agents import create_react_agent, AgentExecutor

    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    if tools is None:
        tools = get_all_tools()

    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    # Prompt ReAct standard avec variables obligatoires: tools, tool_names, agent_scratchpad
    # L'ancien create_react_agent passe agent_scratchpad comme string (log accumulé),
    # pas comme liste de messages — on utilise donc un template string, pas MessagesPlaceholder.
    react_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", REACT_SYSTEM_PROMPT),
            ("human", "{input}\n\n{agent_scratchpad}"),
        ]
    )

    # Construire l'agent ReAct
    agent = create_react_agent(llm, tools, react_prompt)

    # Assembler l'AgentExecutor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=max_iterations,
        verbose=verbose,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    return executor


def get_agent_executor_with_memory(
    tools: list | None = None,
    memory_k: int = 10,
    max_iterations: int = 8,
    verbose: bool = True,
    llm: BaseChatModel | None = None,
):
    """AT04 — assemble l'AgentExecutor ReAct avec ConversationBufferWindowMemory.

    Version étendue avec mémoire conversationnelle pour se souvenir
    des critères du recruteur entre les échanges.

    Args:
        tools: liste d'outils (défaut: get_all_tools()).
        memory_k: taille de la fenêtre de mémoire (défaut: 10).
        max_iterations: nombre max d'itérations (défaut: 8).
        verbose: afficher la trace (défaut: True).
        llm: chat model (défaut: get_chat_model()).

    Returns:
        AgentExecutor avec mémoire.
    """
    try:
        from langchain_classic.agents import create_react_agent, AgentExecutor
    except ImportError:
        from langchain.agents import create_react_agent, AgentExecutor

    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables import RunnablePassthrough

    if tools is None:
        tools = get_all_tools()

    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    # Mémoire conversationnelle
    try:
        from langchain_classic.memory import ConversationBufferWindowMemory
    except ImportError:
        from langchain.memory import ConversationBufferWindowMemory

    memory = ConversationBufferWindowMemory(
        k=memory_k,
        memory_key="history",
        return_messages=True,
    )

    # Prompt avec mémoire + variables obligatoires ReAct
    # agent_scratchpad est passé comme string par l'ancien create_react_agent
    react_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", REACT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", "{input}\n\n{agent_scratchpad}"),
        ]
    )

    agent = create_react_agent(llm, tools, react_prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        max_iterations=max_iterations,
        verbose=verbose,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    return executor


def run_agent(
    query: str,
    tools: list | None = None,
    max_iterations: int = 8,
    verbose: bool = True,
    llm: BaseChatModel | None = None,
) -> dict:
    """AT04 — exécute l'agent sur une requête et retourne le résultat complet.

    Fonction utilitaire qui assemble l'agent, l'exécute et retourne
    la réponse + les étapes intermédiaires (audit trail ReAct).

    Args:
        query: question du recruteur en langage naturel.
        tools: liste d'outils (défaut: get_all_tools()).
        max_iterations: nombre max d'itérations (défaut: 8).
        verbose: afficher la trace (défaut: True).
        llm: chat model (défaut: get_chat_model()).

    Returns:
        Dictionnaire avec:
        - "output": réponse finale de l'agent
        - "intermediate_steps": liste des étapes (Thought/Action/Observation)
        - "num_steps": nombre d'étapes
    """
    executor = get_agent_executor(
        tools=tools,
        max_iterations=max_iterations,
        verbose=verbose,
        llm=llm,
    )

    result = executor.invoke({"input": query})

    intermediate_steps = result.get("intermediate_steps", [])

    return {
        "output": result.get("output", ""),
        "intermediate_steps": [
            {
                "thought": str(step[0].log) if hasattr(step[0], "log") else str(step[0]),
                "action": step[0].tool if hasattr(step[0], "tool") else "unknown",
                "observation": str(step[1]) if len(step) > 1 else "",
            }
            for step in intermediate_steps
        ],
        "num_steps": len(intermediate_steps),
    }


def run_autonomous_agent(
    scenario: list[str],
    tools: list | None = None,
    max_iterations: int = 8,
    llm: BaseChatModel | None = None,
) -> list[dict]:
    """AT04 — exécute l'agent sur un scénario sans input utilisateur (agent autonome).

    L'agent reçoit une série de requêtes et les exécute en séquence,
    en accumulant le contexte via la mémoire.

    Args:
        scenario: liste de requêtes à exécuter en séquence.
        tools: liste d'outils (défaut: get_all_tools()).
        max_iterations: nombre max d'itérations par requête.
        llm: chat model (défaut: get_chat_model()).

    Returns:
        Liste de résultats (un par requête du scénario).
    """
    executor = get_agent_executor_with_memory(
        tools=tools,
        max_iterations=max_iterations,
        verbose=True,
        llm=llm,
    )

    results = []
    for query in scenario:
        result = executor.invoke({"input": query})
        results.append(
            {
                "query": query,
                "output": result.get("output", ""),
                "intermediate_steps": len(result.get("intermediate_steps", [])),
            }
        )

    return results
