"""Prompt Templates et ExampleSelectors pour ai-hirekit.

AT01 — Prompt Engineering Dynamique : Prompt Templates + sélecteurs d'exemples.
AT02 — ChatPromptTemplate pour le matching CV↔offre.
"""

from __future__ import annotations

from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    FewShotPromptTemplate,
)
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.vectorstores import InMemoryVectorStore

# ─── System prompts ─────────────────────────────────────────────────────────
SYSTEM_PROMPT_RECRUITER = (
    "Tu es HireKit, un assistant IA pour recruteurs. Tu analyses des CVs, "
    "matches des candidats avec des offres d'emploi, et génères des grilles "
    "d'entretien. Tu réponds en français, de manière structurée et professionnelle."
)

# ─── Prompt Templates ─────────────────────────────────────────────────────────

CV_EXTRACTION_TEMPLATE = (
    "Extrais les informations structurées de ce CV:\n\n{cv}\n\n"
    "{format_instructions}"
)

MATCHING_SYSTEM = (
    "Tu es un expert en recrutement. Analyse la correspondance entre le candidat "
    "et l'offre d'emploi. Sois objectif et factuel. Ton analyse doit inclure un "
    "score de matching (0.0 à 1.0), une justification, les points forts, les "
    "points faibles et une recommandation."
)

MATCHING_HUMAN = (
    "Candidat:\n{cv}\n\n"
    "Offre d'emploi:\n{offer}\n\n"
    "Évalue la correspondance entre ce candidat et cette offre.\n\n"
    "{format_instructions}"
)

INTERVIEW_TEMPLATE = (
    "Génère une grille d'entretien personnalisée pour le candidat suivant, "
    "en tenant compte de l'offre d'emploi.\n\n"
    "CV du candidat:\n{cv}\n\n"
    "Offre d'emploi:\n{offer}\n\n"
    "{format_instructions}"
)

# ─── Exemples few-shot pour l'extraction de CV ──────────────────────────────

FEW_SHOT_EXAMPLES = [
    {
        "cv": "Marie Dubois\nDéveloppeuse Fullstack\nmarie@email.fr\nCompétences: React, Python, Docker",
        "output": "nom: Marie Dubois, email: marie@email.fr, competences: React, Python, Docker",
    },
    {
        "cv": "Karim Benali\nBackend Engineer\nkarim@email.fr\nCompétences: Python, Django, PostgreSQL",
        "output": "nom: Karim Benali, email: karim@email.fr, competences: Python, Django, PostgreSQL",
    },
    {
        "cv": "Léa Chen\nDevOps Engineer\nlea@email.fr\nCompétences: Kubernetes, Terraform, AWS",
        "output": "nom: Léa Chen, email: lea@email.fr, competences: Kubernetes, Terraform, AWS",
    },
]


def get_cv_extraction_prompt() -> PromptTemplate:
    """AT01 — retourne le PromptTemplate d'extraction de CV.

    Le template contient {cv} et {format_instructions} pour être utilisé
    avec un PydanticOutputParser.
    """
    return PromptTemplate.from_template(CV_EXTRACTION_TEMPLATE)


def get_matching_prompt() -> ChatPromptTemplate:
    """AT02 — retourne le ChatPromptTemplate de matching CV↔offre.

    Le template contient {cv}, {offer} et {format_instructions}.
    Utilisé avec get_match_parser() dans la chaîne LCEL de matching.
    """
    return ChatPromptTemplate.from_messages([
        ("system", MATCHING_SYSTEM),
        ("human", MATCHING_HUMAN),
    ])


def get_interview_prompt() -> PromptTemplate:
    """AT04 — retourne le PromptTemplate de génération de grille d'entretien."""
    return PromptTemplate.from_template(INTERVIEW_TEMPLATE)


def get_few_shot_example_selector() -> SemanticSimilarityExampleSelector:
    """AT01 (Bonus) — retourne un ExampleSelector dynamique pour le few-shot prompting.

    Utilise SemanticSimilarityExampleSelector pour choisir les exemples
    sémantiquement proches du CV à analyser.
    """
    from langchain_core.embeddings import FakeEmbeddings

    # Utilise des embeddings factices pour les tests (sans API key).
    # En production, remplacez par FastEmbedEmbeddings ou OpenAIEmbeddings.
    embeddings = FakeEmbeddings(size=384)

    return SemanticSimilarityExampleSelector.from_examples(
        examples=FEW_SHOT_EXAMPLES,
        embeddings=embeddings,
        vectorstore_cls=InMemoryVectorStore,
        k=2,
    )