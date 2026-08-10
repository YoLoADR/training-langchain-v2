"""Tools — outils pour l'agent ReAct.

AT04 — Tools : appeler des APIs (search_cvs, match) + exécuter du code (python_repl)
+ recherches web.

4 outils implémentés :
1. search_cvs — recherche de candidats dans la base de CVs (RAG FAISS)
2. match_candidate — matching candidat↔offre via la chaîne LCEL
3. web_search — recherche web (simulée en local, DuckDuckGo en option)
4. python_repl — exécution de code Python (calcul de score composite)
"""

from __future__ import annotations

import json
from typing import Any

from langchain_core.tools import BaseTool, tool


# ─── Outil 1 : search_cvs (RAG) ─────────────────────────────────────────────


@tool("search_cvs")
def search_cvs_tool(query: str) -> str:
    """AT04 — recherche de candidats dans la base de CVs (RAG).

    Utilise l'index FAISS construit en AT03 pour trouver les CVs
    les plus pertinents pour une requête.

    Args:
        query: requête en langage naturel (ex: "qui a de l'expérience en React ?")

    Returns:
        Chaîne formatée avec les candidats trouvés et leurs extraits.
    """
    from hirekit.rag.vectorstore_faiss import search_cvs

    try:
        results = search_cvs(query, k=4)
        if not results:
            return "Aucun candidat trouvé pour cette requête."

        output_parts = [f"Found {len(results)} candidates:"]
        for i, doc in enumerate(results, 1):
            filename = doc.metadata.get("filename", "unknown")
            content = doc.page_content[:200].replace("\n", " ")
            output_parts.append(f"\n{i}. [{filename}] {content}...")
        return "\n".join(output_parts)
    except FileNotFoundError:
        return (
            "Index FAISS non trouvé. Lancez d'abord: "
            "python ateliers/atelier-03-rag/solution.py pour construire l'index."
        )
    except Exception as e:
        return f"Erreur lors de la recherche: {e}"


# ─── Outil 2 : match_candidate (LCEL) ────────────────────────────────────────


@tool("match_candidate")
def match_candidate_tool(cv_text: str, offer_text: str) -> str:
    """AT04 — matching candidat↔offre via la chaîne LCEL.

    Utilise la chaîne LCEL de matching construite en AT02 pour
    évaluer la correspondance entre un CV et une offre.

    Args:
        cv_text: texte du CV du candidat.
        offer_text: texte de l'offre d'emploi.

    Returns:
        Score de matching, justification et recommandation.
    """
    from hirekit.services.matching import get_matching_chain

    try:
        chain = get_matching_chain()
        result = chain.invoke({"cv": cv_text, "offer": offer_text})

        output = (
            f"Match Score: {result.score:.2f}\n"
            f"Justification: {result.justification}\n"
            f"Points forts: {', '.join(result.points_forts)}\n"
            f"Points faibles: {', '.join(result.points_faibles)}\n"
            f"Recommandation: {result.recommandation}"
        )
        return output
    except Exception as e:
        return f"Erreur lors du matching: {e}"


# ─── Outil 3 : web_search (simulé) ──────────────────────────────────────────


# Réponses simulées pour les recherches web (reproductible, sans API externe)
_WEB_SEARCH_MOCK = {
    "github": "GitHub: profil trouvé. Contributions régulières, 3 repos publics, spécialisation en React/TypeScript.",
    "linkedin": "LinkedIn: profil professionnel trouvé. 500+ connexions, poste actuel: Senior Developer.",
    "stackoverflow": "StackOverflow: profil actif. Reputation: 5234, top 5% en Python, 234 réponses.",
    "react": "Recherche web: React.js est un framework frontend populaire. 42% des offres demandent React en 2024.",
    "python": "Recherche web: Python reste #1 dans le classement TIOBE. 48% des offres backend demandent Python.",
    "devops": "Recherche web: Le marché DevOps croît de 21% par an. Kubernetes et AWS sont les skills les plus demandées.",
    "default": "Recherche web: résultats trouvés. Le candidat a une présence en ligne notable avec des contributions techniques.",
}


@tool("web_search")
def web_search_tool(query: str) -> str:
    """AT04 — recherche web (simulée en local).

    Simule une recherche web pour vérifier la réputation en ligne d'un candidat
    ou chercher des informations sur une technologie.

    En production, remplacer par DuckDuckGoSearchRun ou SerpAPI.

    Args:
        query: requête de recherche (ex: "Marie Dubois développeur React")

    Returns:
        Résultats de recherche simulés.
    """
    query_lower = query.lower()

    # Recherche dans les réponses simulées
    for keyword, response in _WEB_SEARCH_MOCK.items():
        if keyword in query_lower:
            return f"[Web Search] '{query}': {response}"

    return f"[Web Search] '{query}': {_WEB_SEARCH_MOCK['default']}"


# ─── Outil 4 : python_repl (exécution de code) ───────────────────────────────


@tool("python_repl")
def python_repl_tool(code: str) -> str:
    """AT04 — exécution de code Python (PythonREPLTool).

    Permet à l'agent d'exécuter du code Python pour calculer un score
    composite, faire des statistiques ou manipuler des données.

    Args:
        code: code Python à exécuter.

    Returns:
        Résultat de l'exécution (stdout) ou message d'erreur.
    """
    try:
        import io
        from contextlib import redirect_stdout

        # Capturer la sortie stdout
        stdout_capture = io.StringIO()
        local_vars: dict[str, Any] = {}

        with redirect_stdout(stdout_capture):
            # Exécuter le code dans un namespace restreint
            exec(code, {"__builtins__": __builtins__}, local_vars)

        output = stdout_capture.getvalue()

        # Inclure les variables résultantes si pertinentes
        result_vars = {}
        for k, v in local_vars.items():
            if not k.startswith("_"):
                try:
                    result_vars[k] = str(v)
                except Exception:
                    result_vars[k] = "<non-serializable>"

        if output:
            return f"Output:\n{output}\nVariables: {json.dumps(result_vars, indent=2)}"
        elif result_vars:
            return f"Variables: {json.dumps(result_vars, indent=2)}"
        else:
            return "Code exécuté avec succès (aucune sortie)."

    except Exception as e:
        return f"Erreur d'exécution: {type(e).__name__}: {e}"


# ─── Outil bonus : check_availability (planning) ────────────────────────────


@tool("check_availability")
def check_availability_agent_tool(date: str, duration_minutes: int = 60) -> str:
    """AT04 — vérifie les disponibilités des candidats pour une date.

    Args:
        date: date au format "YYYY-MM-DD".
        duration_minutes: durée minimum en minutes (défaut: 60).

    Returns:
        Liste des candidats disponibles à cette date.
    """
    from hirekit.services.availability import check_availability

    try:
        result = check_availability(date, duration_minutes)

        if not result["available_candidates"]:
            return f"Aucun candidat disponible le {date}."

        parts = [f"Candidats disponibles le {date} ({result['total_available']}/{result['total_checked']}):"]
        for c in result["available_candidates"]:
            parts.append(f"  - {c['name']} ({c['candidate_id']}): {c['total_available_hours']}h disponibles")
        return "\n".join(parts)
    except FileNotFoundError:
        return "Calendrier non trouvé. Lancez: python scripts/generate_availability.py"
    except Exception as e:
        return f"Erreur: {e}"


# ─── Liste de tous les outils ────────────────────────────────────────────────


def get_all_tools() -> list[BaseTool]:
    """AT04 — retourne la liste des 4 outils pour l'agent ReAct.

    Outils:
    1. search_cvs — recherche RAG dans les CVs
    2. match_candidate — matching CV↔offre (LCEL)
    3. web_search — recherche web (simulée)
    4. python_repl — exécution de code Python

    Returns:
        Liste de 4 BaseTool décorés avec @tool.
    """
    return [
        search_cvs_tool,
        match_candidate_tool,
        web_search_tool,
        python_repl_tool,
    ]


def get_all_tools_with_availability() -> list[BaseTool]:
    """AT04 — retourne les 4 outils + check_availability (5 outils).

    Version étendue avec l'outil de planning pour les scénarios complexes.
    """
    return get_all_tools() + [check_availability_agent_tool]