"""Output Parsers — extraction structurée des sorties du LLM.

AT01 — Output Parsers : PydanticOutputParser, CommaSeparatedListOutputParser.
AT02 — Output Parser pour le matching : MatchResult.
"""

from __future__ import annotations

from langchain_core.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser

from pydantic import BaseModel, Field


# ─── Modèles Pydantic pour les sorties structurées ──────────────────────────


class Skill(BaseModel):
    nom: str = Field(description="Nom de la compétence")
    niveau: str = Field(description="Niveau: débutant, intermédiaire, avancé, expert")
    annees: int = Field(description="Années d'expérience avec cette compétence")


class Experience(BaseModel):
    poste: str = Field(description="Intitulé du poste")
    entreprise: str = Field(description="Nom de l'entreprise")
    duree: str = Field(description="Durée (ex: '2 ans', '6 mois')")
    description: str = Field(description="Description courte des responsabilités")


class CVInfo(BaseModel):
    """Structure extraite d'un CV par le PydanticOutputParser (AT01)."""

    nom: str = Field(description="Nom et prénom du candidat")
    email: str = Field(description="Adresse email")
    telephone: str | None = Field(default=None, description="Numéro de téléphone")
    competences: list[Skill] = Field(description="Liste des compétences")
    experiences: list[Experience] = Field(description="Liste des expériences")
    formations: list[str] = Field(default_factory=list, description="Liste des diplômes/formations")


class MatchResult(BaseModel):
    """Résultat d'un matching candidat↔offre (AT02)."""

    score: float = Field(description="Score de matching entre 0.0 et 1.0")
    justification: str = Field(description="Justification du score en 2-3 phrases")
    points_forts: list[str] = Field(description="Points forts du candidat pour cette offre")
    points_faibles: list[str] = Field(description="Points faibles ou manquants")
    recommandation: str = Field(description="Recommandation: shortlister, refuser, à voir")


class InterviewGuide(BaseModel):
    """Grille d'entretien générée (AT04)."""

    questions_techniques: list[str] = Field(description="Questions techniques basées sur le CV")
    questions_comportementnelles: list[str] = Field(description="Questions comportementales")
    questions_offre: list[str] = Field(description="Questions spécifiques à l'offre")


# ─── Parsers ─────────────────────────────────────────────────────────────────


def get_cv_parser() -> PydanticOutputParser:
    """AT01 — retourne un PydanticOutputParser pour CVInfo."""
    return PydanticOutputParser(pydantic_object=CVInfo)


def get_match_parser() -> PydanticOutputParser:
    """AT02 — retourne un PydanticOutputParser pour MatchResult."""
    return PydanticOutputParser(pydantic_object=MatchResult)


def get_skills_list_parser() -> CommaSeparatedListOutputParser:
    """AT01 — retourne un CommaSeparatedListOutputParser pour extraire une liste de compétences."""
    return CommaSeparatedListOutputParser()