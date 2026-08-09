"""
═══════════════════════════════════════════════════════════════════════════
Atelier 01 — Solution de référence
═══════════════════════════════════════════════════════════════════════════

Cette solution importe depuis le package hirekit/ (implémenté sur la branche main).
Ne pas projeter pendant l'atelier — c'est la référence pour le formateur.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

from hirekit.llm.provider import get_llm, get_chat_model
from hirekit.llm.parsers import CVInfo, get_cv_parser
from hirekit.llm.prompts import SYSTEM_PROMPT_RECRUITER

QUESTIONS_CV = [
    "Quelle est l'expérience de Marie Dubois en React ?",
    "Combien d'années d'expérience en Python a Karim Benali ?",
    "Quel est le dernier poste de Sophie Martin ?",
    "Quelles compétences DevOps a Léa Chen ?",
    "Quel est le niveau d'anglais de Thomas Petit ?",
]

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
    print(f"\n{'═' * 72}\n{label}\n{'═' * 72}")
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}] {q}")
        response = model.invoke([HumanMessage(content=q)])
        content = response.content if hasattr(response, "content") else str(response)
        print(f"    → {content[:300]}")


def main() -> None:
    # TODO 1 — LLM + Chat Model
    llm = get_llm(temperature=0.1)
    chat = get_chat_model(temperature=0.1)

    # TODO 2 — Questions privées → hallucinations
    poser_questions(llm, QUESTIONS_CV, "LLM (completion API) — hallucinations attendues")
    poser_questions(chat, QUESTIONS_CV, "Chat Model (messages API) — hallucinations attendues")

    # TODO 3 — Temperature 0.9
    llm_aleatoire = get_llm(temperature=0.9)
    for run in (1, 2):
        resp = llm_aleatoire.invoke([HumanMessage(content=QUESTIONS_CV[0])])
        print(f"\nRun aléatoire #{run} : {str(resp)[:200]}")

    # TODO 4 — Extraction CV→JSON avec PydanticOutputParser
    parser = get_cv_parser()
    prompt = PromptTemplate(
        template="Extrais les informations de ce CV:\n{cv}\n\n{format_instructions}",
        input_variables=["cv"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | get_chat_model() | parser
    result = chain.invoke({"cv": CV_EXAMPLE})
    print(f"\nExtraction : {result}")
    print(f"  Nom : {result.nom}")
    print(f"  Compétences : {[s.nom for s in result.competences]}")
    print(f"  Expériences : {[(e.poste, e.entreprise) for e in result.experiences]}")


if __name__ == "__main__":
    main()
