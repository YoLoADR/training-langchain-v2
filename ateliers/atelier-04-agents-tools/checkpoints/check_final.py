"""Checkpoint final — Validation AT04 (Agents ReAct + Tools).

5 questions à choix multiples. Oriente vers Sprint/Bonus/continuation.
Lancez: python ateliers/atelier-04-agents-tools/checkpoints/check_final.py
"""

import sys

QUESTIONS = [
    {
        "question": "Que signifie ReAct ?",
        "choices": [
            "a) Reactive Programming",
            "b) Reasoning + Acting (Thought → Action → Observation)",
            "c) Real-time Action",
            "d) React Framework Agent",
        ],
        "answer": "b",
        "explanation": "ReAct = Reasoning + Acting. L'agent réfléchit (Thought), agit (Action), "
                       "observe le résultat (Observation), puis répète jusqu'à la réponse finale.",
    },
    {
        "question": "À quoi sert return_intermediate_steps=True dans AgentExecutor ?",
        "choices": [
            "a) À afficher les logs en temps réel",
            "b) À retourner la trace complète Thought/Action/Observation (audit trail)",
            "c) À accélérer l'exécution",
            "d) À limiter le nombre d'itérations",
        ],
        "answer": "b",
        "explanation": "return_intermediate_steps=True permet de récupérer la trace complète "
                       "du cycle ReAct (quels outils, quels inputs, quelles observations).",
    },
    {
        "question": "Que fait handle_parsing_errors=True ?",
        "choices": [
            "a) Il ignore les erreurs de parsing",
            "b) Il affiche les erreurs de parsing en verbose",
            "c) Il transforme les erreurs de parsing en feedback pour l'agent (au lieu de crasher)",
            "d) Il désactive le parsing",
        ],
        "answer": "c",
        "explanation": "handle_parsing_errors=True permet à l'agent de récupérer gracieusement "
                       "des erreurs de parsing du LLM (format Action/Input incorrect) en lui "
                       "renvoyant l'erreur comme observation pour qu'il ajuste.",
    },
    {
        "question": "Que se passe-t-il si max_iterations est trop bas (ex: 1) ?",
        "choices": [
            "a) L'agent répond plus vite",
            "b) L'agent ne peut pas terminer son cycle et s'arrête sans réponse finale",
            "c) L'agent utilise moins de tokens",
            "d) Rien, c'est la valeur recommandée",
        ],
        "answer": "b",
        "explanation": "max_iterations=1 ne permet qu'un seul appel d'outil. L'agent n'a pas "
                       "le temps de faire Thought → Action → Observation → Final Answer.",
    },
    {
        "question": "Qu'est-ce qu'un agent autonome ?",
        "choices": [
            "a) Un agent qui ne nécessite pas de LLM",
            "b) Un agent qui exécute une série de requêtes sans input utilisateur, en accumulant le contexte",
            "c) Un agent qui tourne en arrière-plan indéfiniment",
            "d) Un agent qui choisit ses propres outils",
        ],
        "answer": "b",
        "explanation": "Un agent autonome reçoit un scénario (liste de requêtes) et l'exécute "
                       "en séquence, en accumulant le contexte via la mémoire entre chaque requête.",
    },
]


def run_checkpoint():
    print("=" * 60)
    print("  Checkpoint Final — AT04 (Agents ReAct + Tools)")
    print("=" * 60)
    print()
    score = 0
    for i, q in enumerate(QUESTIONS, 1):
        print(f"Question {i}/{len(QUESTIONS)}: {q['question']}")
        for choice in q["choices"]:
            print(f"  {choice}")
        answer = input("\n  Votre réponse (a/b/c/d): ").strip().lower()
        if answer == q["answer"]:
            print(f"  ✓ Correct !")
            score += 1
        else:
            print(f"  ✗ Incorrect. Réponse: '{q['answer']}'. {q['explanation']}")
        print()
    print("=" * 60)
    print(f"  Score: {score}/{len(QUESTIONS)}")
    print()
    if score >= 4:
        print("  Excellent ! Prêt pour AT05 (Chatbots + Code Analysis).")
        print("  → Passez au Bonus (agent autonome, check_availability).")
    elif score >= 3:
        print("  Bien ! Faites le Sprint pour renforcer les bases.")
    else:
        print("  Concepts à revoir. Refaites le tronc commun.")
    print("=" * 60)
    return 0 if score >= 3 else 1


if __name__ == "__main__":
    sys.exit(run_checkpoint())