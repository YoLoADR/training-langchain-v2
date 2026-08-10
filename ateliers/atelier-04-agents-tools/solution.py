"""
═══════════════════════════════════════════════════════════════════════════
Atelier 04 — Solution de référence
═══════════════════════════════════════════════════════════════════════════

Cette solution importe depuis le package hirekit/ (implémenté sur la branche main).
Ne pas projeter pendant l'atelier — c'est la référence pour le formateur.
"""

from hirekit.agent.tools import get_all_tools
from hirekit.agent.react_agent import get_agent_executor, run_autonomous_agent


def main() -> None:
    print("=== AT04 — Agent ReAct + Tools ===\n")

    # TODO 1 — Récupérer les 4 outils
    print("Outils disponibles:")
    tools = get_all_tools()
    for t in tools:
        print(f"  - {t.name}: {t.description[:80]}...")

    # TODO 2 — Assembler l'AgentExecutor
    print("\nConstruction de l'agent ReAct...")
    executor = get_agent_executor(tools=tools, max_iterations=8, verbose=True)
    print(f"  AgentExecutor prêt (max_iterations=8)")

    # TODO 3 — Exécuter l'agent sur une requête complexe
    query = (
        "Trouve les 3 meilleurs profils DevOps, vérifie leur réputation "
        "en ligne, et calcule un score composite (exp * 0.5 + reputation * 0.3 + dispo * 0.2)"
    )
    print(f"\nRequête: {query}\n")
    print("-" * 72)

    result = executor.invoke({"input": query})
    print(f"\n{'=' * 72}")
    print(f"Réponse finale: {result['output']}")
    print(f"{'=' * 72}")

    # TODO 4 — Afficher la trace ReAct (intermediate_steps)
    print("\n=== Trace ReAct (intermediate_steps) ===")
    for i, step in enumerate(result.get("intermediate_steps", []), 1):
        action = step[0]
        observation = step[1]
        tool_name = action.tool if hasattr(action, "tool") else "unknown"
        tool_input = action.tool_input if hasattr(action, "tool_input") else ""
        print(f"\nÉtape {i}:")
        print(f"  Action: {tool_name}")
        print(f"  Input: {str(tool_input)[:100]}")
        print(f"  Observation: {str(observation)[:200]}...")

    # Vérifier que l'agent a utilisé plusieurs outils
    tools_used = set()
    for step in result.get("intermediate_steps", []):
        if hasattr(step[0], "tool"):
            tools_used.add(step[0].tool)
    print(f"\nOutils utilisés: {tools_used}")

    # TODO 5 (Bonus) — Scénario autonome multi-requêtes
    print("\n\n=== Bonus: Scénario autonome ===")
    scenario = [
        "Qui a de l'expérience en Kubernetes ?",
        "Vérifie la réputation en ligne de Léa Chen",
        "Calcule un score: 4 * 0.5 + 0.8 * 0.3 + 0.6 * 0.2",
    ]

    results = run_autonomous_agent(scenario)
    for r in results:
        print(f"\nQ: {r['query']}")
        print(f"A: {r['output'][:200]}")
        print(f"Steps: {r['intermediate_steps']}")


if __name__ == "__main__":
    main()