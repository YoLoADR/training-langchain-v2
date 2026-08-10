"""
═══════════════════════════════════════════════════════════════════════════
Atelier 04 — Agents ReAct + Tools (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : construire un agent ReAct qui orchestre 4 outils (search_cvs,
           match_candidate, web_search, python_repl) pour trouver et
           scorer des candidats automatiquement.

5 TODOs :
  1. Définir les 4 outils avec @tool decorator
  2. Assembler l'AgentExecutor ReAct
  3. Exécuter l'agent sur une requête complexe
  4. Afficher la trace ReAct (intermediate_steps)
  5. (Bonus) Exécuter un scénario autonome multi-requêtes

Lancer :  python ateliers/atelier-04-agents-tools/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# ─── Imports déjà fournis ────────────────────────────────────────────────────

# TODO 1 — importer les tools depuis hirekit.agent.tools
# from hirekit.agent.tools import get_all_tools, search_cvs_tool, web_search_tool, python_repl_tool

# TODO 2 — importer get_agent_executor depuis hirekit.agent.react_agent
# from hirekit.agent.react_agent import get_agent_executor

# TODO 4 — importer run_agent pour la trace
# from hirekit.agent.react_agent import run_agent


def main() -> None:
    print("=== AT04 — Agent ReAct + Tools ===\n")

    # TODO 1 — Récupérer les 4 outils
    # print("Outils disponibles:")
    # tools = get_all_tools()
    # for t in tools:
    #     print(f"  - {t.name}: {t.description[:60]}...")
    raise NotImplementedError("TODO 1 — récupérer les 4 outils")

    # TODO 2 — Assembler l'AgentExecutor
    # print("\nConstruction de l'agent ReAct...")
    # executor = get_agent_executor(tools=tools, max_iterations=8, verbose=True)
    # print(f"  AgentExecutor prêt (max_iterations=8)")

    # TODO 3 — Exécuter l'agent sur une requête complexe
    # query = ("Trouve les 3 meilleurs profils DevOps, vérifie leur réputation "
    #          "en ligne, et calcule un score composite (exp * 0.5 + reputation * 0.3 + dispo * 0.2)")
    # print(f"\nRequête: {query}\n")
    # result = executor.invoke({"input": query})
    # print(f"\nRéponse finale: {result['output']}")

    # TODO 4 — Afficher la trace ReAct (intermediate_steps)
    # print("\n=== Trace ReAct (intermediate_steps) ===")
    # for i, step in enumerate(result.get("intermediate_steps", []), 1):
    #     action = step[0]
    #     observation = step[1]
    #     print(f"\nÉtape {i}:")
    #     print(f"  Action: {action.tool}")
    #     print(f"  Input: {action.tool_input}")
    #     print(f"  Observation: {str(observation)[:200]}...")

    # TODO 5 (Bonus) — Scénario autonome multi-requêtes
    # from hirekit.agent.react_agent import run_autonomous_agent
    # scenario = [
    #     "Qui a de l'expérience en Kubernetes ?",
    #     "Vérifie la réputation en ligne de Léa Chen",
    #     "Calcule un score: 4 * 0.5 + 0.8 * 0.3 + 0.6 * 0.2",
    # ]
    # results = run_autonomous_agent(scenario)
    # for r in results:
    #     print(f"\nQ: {r['query']}")
    #     print(f"A: {r['output'][:200]}")
    #     print(f"Steps: {r['intermediate_steps']}")


if __name__ == "__main__":
    main()