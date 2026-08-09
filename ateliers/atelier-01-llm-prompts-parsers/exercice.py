"""
═══════════════════════════════════════════════════════════════════════════
Atelier 01 — LLM + Prompts + Output Parsers (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : observer un LLM sans contexte → hallucinations, puis extraire
           un CV en JSON structuré avec un Output Parser.

5 TODOs :
  1. Instancier un LLM et un Chat Model via get_llm() / get_chat_model()
  2. Poser 5 questions privées sur des CVs → constater les hallucinations
  3. Comparer temperature=0.1 vs temperature=0.9
  4. Extraire un CV en JSON avec PydanticOutputParser
  5. (Bonus) Ajouter un ExampleSelector pour du few-shot dynamique

Lancer :  python ateliers/atelier-01-llm-prompts-parsers/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# ─── Imports déjà fournis ────────────────────────────────────────────────────
from langchain_core.messages import HumanMessage, SystemMessage

# TODO 1 — importer get_llm et get_chat_model depuis hirekit.llm.provider
# from hirekit.llm.provider import get_llm, get_chat_model

# TODO 4 — importer CVInfo et get_cv_parser depuis hirekit.llm.parsers
# from hirekit.llm.parsers import CVInfo, get_cv_parser

# TODO 4 — importer PromptTemplate depuis langchain_core.prompts
# from langchain_core.prompts import PromptTemplate


# ─── Questions privées sur des CVs (le LLM ne les a jamais vus) ─────────────
QUESTIONS_CV = [
    "Quelle est l'expérience de Marie Dubois en React ?",
    "Combien d'années d'expérience en Python a Karim Benali ?",
    "Quel est le dernier poste de Sophie Martin ?",
    "Quelles compétences DevOps a Léa Chen ?",
    "Quel est le niveau d'anglais de Thomas Petit ?",
]

# ─── CV d'exemple pour l'extraction (AT01 Étape 2) ───────────────────────────
CV_EXAMPLE = """
Marie Dubois
Développeuse Fullstack — 5 ans d'expérience
marie.dubois@email.fr — 06 12 34 56 78

Compétences :
- React (avancé, 4 ans)
- TypeScript (intermédiaire, 3 ans)
- Node.js (avancé, 4 ans)
- Python (intermédiaire, 2 ans)
- Docker (débutant, 1 an)

Expériences :
- Développeuse Fullstack chez TechCorp (2022-2024) : Refonte d'une app React/Node.js
- Développeuse Frontend chez StartupXYZ (2020-2022) : Migration Angular vers React

Formation :
- Master Informatique, Université Paris-Saclay (2019)
"""


def poser_questions(model, questions: list[str], label: str = "") -> None:
    """Pose une liste de questions au modèle et affiche les réponses."""
    print(f"\n{'═' * 72}\n{label}\n{'═' * 72}")
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}] {q}")
        response = model.invoke([HumanMessage(content=q)])
        content = response.content if hasattr(response, "content") else str(response)
        print(f"    → {content[:300]}")
        if len(content) > 300:
            print("      [...]")


def main() -> None:
    # TODO 1 — Instancier un LLM (completion API) et un Chat Model (messages API)
    # llm = get_llm(temperature=0.1)
    # chat = get_chat_model(temperature=0.1)
    raise NotImplementedError("TODO 1 — instancier get_llm() et get_chat_model()")

    # TODO 2 — Poser les 5 questions privées à chaque modèle
    # Question : la réponse est-elle vraie ? Comment le savoir ?
    # poser_questions(llm, QUESTIONS_CV, "LLM (completion API)")
    # poser_questions(chat, QUESTIONS_CV, "Chat Model (messages API)")

    # TODO 3 — Recréer un LLM avec temperature=0.9 et reposer la MÊME question
    # (la première). Lancer 2 fois → observer si la réponse change.
    # llm_aleatoire = get_llm(temperature=0.9)
    # for run in (1, 2):
    #     resp = llm_aleatoire.invoke([HumanMessage(content=QUESTIONS_CV[0])])
    #     print(f"\nRun aléatoire #{run} : {resp.content[:200]}")

    # TODO 4 — Extraire le CV en JSON structuré avec PydanticOutputParser
    # parser = get_cv_parser()
    # prompt = PromptTemplate(
    #     template="Extrais les informations de ce CV:\n{cv}\n\n{format_instructions}",
    #     input_variables=["cv"],
    #     partial_variables={"format_instructions": parser.get_format_instructions()},
    # )
    # chain = prompt | get_chat_model() | parser
    # result = chain.invoke({"cv": CV_EXAMPLE})
    # print(f"\nExtraction : {result}")
    # print(f"  Nom : {result.nom}")
    # print(f"  Compétences : {[s.nom for s in result.competences]}")

    # TODO 5 (Bonus) — Ajouter un ExampleSelector pour du few-shot dynamique
    # from hirekit.llm.prompts import get_few_shot_example_selector
    # selector = get_few_shot_example_selector()


if __name__ == "__main__":
    main()
