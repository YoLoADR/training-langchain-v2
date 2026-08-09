"""Prompt Templates et ExampleSelectors pour ai-hirekit.

AT01 — Prompt Engineering Dynamique : Prompt Templates + sélecteurs d'exemples.
"""

from __future__ import annotations

# ─── System prompts ─────────────────────────────────────────────────────────
SYSTEM_PROMPT_RECRUITER = (
    "Tu es HireKit, un assistant IA pour recruteurs. Tu analyses des CVs, "
    "matches des candidats avec des offres d'emploi, et génères des grilles "
    "d'entretien. Tu réponds en français, de manière structurée et professionnelle."
)

# ─── Prompt Templates (à définir en AT01) ────────────────────────────────────
CV_EXTRACTION_TEMPLATE = None  # AT01: PromptTemplate pour extraction CV→JSON
MATCHING_TEMPLATE = None  # AT02: ChatPromptTemplate pour matching CV↔offre
INTERVIEW_TEMPLATE = None  # AT04: PromptTemplate pour grille d'entretien


def get_cv_extraction_prompt() -> None:
    """AT01 — retourne le PromptTemplate d'extraction de CV."""
    raise NotImplementedError("AT01 — implémentez dans hirekit/llm/prompts.py")


def get_matching_prompt() -> None:
    """AT02 — retourne le ChatPromptTemplate de matching CV↔offre."""
    raise NotImplementedError("AT02 — implémentez dans hirekit/llm/prompts.py")


def get_few_shot_example_selector() -> None:
    """AT01 — retourne un ExampleSelector dynamique pour le few-shot prompting."""
    raise NotImplementedError("AT01 — implémentez l'ExampleSelector dans hirekit/llm/prompts.py")
