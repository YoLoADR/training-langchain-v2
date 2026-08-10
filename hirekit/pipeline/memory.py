"""Extraction mémoire candidat — LLM-powered.

Inspiration: sellkit/src/pipeline/memory.ts

6 champs de qualification (adapté de sellkit):
  name, experience, availability, location, riskAppetite, revenueGoal

À chaque message entrant, un LLM rapide (gpt-4o-mini) extrait les infos clés
que le candidat partage. Ces infos sont stockées (qual_json) et injectées
dans le contexte du LLM principal.
"""

from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, Field

from hirekit.config import OPENAI_API_KEY, OPENAI_MODEL

QUALIFICATION_FIELDS = [
    "name",
    "experience",
    "availability",
    "location",
    "revenueGoal",
    "riskAppetite",
]


class ProspectMemory(BaseModel):
    """Mémoire d'un candidat (champs de qualification)."""

    name: str | None = Field(default=None, description="Nom ou prénom du candidat")
    experience: str | None = Field(
        default=None, description="Expérience professionnelle mentionnée"
    )
    availability: str | None = Field(default=None, description="Disponibilité pour commencer")
    location: str | None = Field(default=None, description="Ville ou secteur géographique")
    riskAppetite: str | None = Field(
        default=None, description="Appétence aux risques (zones grises startup)"
    )
    revenueGoal: str | None = Field(default=None, description="Objectif de revenu mensuel")
    motivation: str | None = Field(default=None, description="Motivation ou objectif du candidat")
    notes: str | None = Field(default=None, description="Autre information notable")


EMPTY_MEMORY = ProspectMemory()


class MemorySchema(BaseModel):
    """Schéma pour l'extraction LLM."""

    name: str | None = Field(
        description="Nom ou prénom du candidat s'il se présente (null si non mentionné)"
    )
    experience: str | None = Field(
        description="Expérience professionnelle. 'pas d'expérience', 'aucune', 'débutant' SONT des valeurs valides. null UNIQUEMENT si non mentionné"
    )
    availability: str | None = Field(
        description="Disponibilité pour commencer (ex: 'immédiat', '2 semaines')"
    )
    location: str | None = Field(description="Ville ou secteur géographique mentionné")
    riskAppetite: str | None = Field(
        description="Appétence aux risques: comfort avec startup en zones grises"
    )
    revenueGoal: str | None = Field(
        description="Objectif de revenu mensuel mentionné (ex: '2000 euros')"
    )
    motivation: str | None = Field(description="Motivation ou objectif du candidat")
    notes: str | None = Field(description="Autre information notable partagée par le candidat")


EXTRACTION_PROMPT = """Tu extrais les informations clés que le candidat partage dans son message.
Ne déduis rien -- extrais UNIQUEMENT ce qui est explicitement dit.
Si une information n'est pas présente dans ce message, mets null.

Champs à extraire:
- name: prénom ou nom si le candidat se présente. 'Je m'appelle X' = name=X
- experience: expérience professionnelle UNIQUEMENT si le candidat parle de son parcours.
  IMPORTANT: 'pas d'expérience', 'aucune expérience', 'je suis débutant' = experience='aucune'.
  MAIS 'je cherche du travail' n'est PAS de l'expérience — c'est de la MOTIVATION.
- availability: disponibilité pour commencer (immédiat, 2 semaines, ce soir, etc.)
- location: ville, quartier, région
- riskAppetite: appétence aux risques — comfort avec startup en zones grises
- revenueGoal: objectif de revenu mensuel (montant, complément, vrai revenu)
- motivation: pourquoi il cherche, ce qu'il veut
- notes: toute autre info utile (compétences, langues, véhicule, etc.)

EXEMPLES:
- "Il fait super beau aujourd'hui" → {name:null, experience:null, motivation:null}
- "Oui, je cherche un job" → {name:null, experience:null, motivation:"Je cherche un job"}
- "Je m'appelle Nathan" → {name:"Nathan", experience:null, motivation:null}
- "J'ai pas d'expérience mais je souhaite travailler" → {name:null, experience:"aucune", motivation:"souhaite travailler"}
- "J'ai travaillé 5 ans dans la vente" → {name:null, experience:"5 ans dans la vente", motivation:null}

Réponds UNIQUEMENT avec le JSON structuré."""


def _is_real(v: object) -> bool:
    """Vérifie qu'une valeur est une vraie chaîne non-nulle."""
    return isinstance(v, str) and v.strip() != "" and v.lower() != "null"


def extract_memory_sync(text: str) -> dict:
    """Extrait les infos clés d'un message candidat via LLM.

    Returns: dict partiel avec les champs extraits (seulement les non-null).
    """
    if not OPENAI_API_KEY:
        return {}

    try:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
        structured = llm.with_structured_output(MemorySchema)
        result = structured.invoke(
            [
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": text},
            ],
            tags=["hirekit", "memory-extraction"],
        )

        extracted: dict = {}
        if _is_real(result.name):
            extracted["name"] = result.name
        if _is_real(result.experience):
            low_text = text.lower()
            mentions_experience = any(
                kw in low_text
                for kw in [
                    "experience",
                    "expérience",
                    "debutant",
                    "débutant",
                    "pas d'exp",
                    "travaille",
                    "travaillé",
                    "parcours",
                    "professionnel",
                    "métier",
                ]
            )
            if mentions_experience or result.experience not in ("aucune", "debutant"):
                extracted["experience"] = result.experience
        if _is_real(result.availability):
            extracted["availability"] = result.availability
        if _is_real(result.location):
            extracted["location"] = result.location
        if _is_real(result.riskAppetite):
            extracted["riskAppetite"] = result.riskAppetite
        if _is_real(result.revenueGoal):
            extracted["revenueGoal"] = result.revenueGoal
        if _is_real(result.motivation):
            extracted["motivation"] = result.motivation
        if _is_real(result.notes):
            extracted["notes"] = result.notes

        return extracted
    except Exception as e:
        print(f"  🟡 [MEMORY] Extraction failed: {str(e)[:60]}")
        return {}


async def extract_memory(text: str) -> dict:
    """Version asynchrone de extract_memory_sync."""
    if not OPENAI_API_KEY:
        return {}

    try:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
        structured = llm.with_structured_output(MemorySchema)
        result = await structured.ainvoke(
            [
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": text},
            ],
            tags=["hirekit", "memory-extraction"],
        )

        extracted: dict = {}
        if _is_real(result.name):
            extracted["name"] = result.name
        if _is_real(result.experience):
            low_text = text.lower()
            mentions_experience = any(
                kw in low_text
                for kw in [
                    "experience",
                    "expérience",
                    "debutant",
                    "débutant",
                    "pas d'exp",
                    "travaille",
                    "travaillé",
                    "parcours",
                    "professionnel",
                    "métier",
                ]
            )
            if mentions_experience or result.experience not in ("aucune", "debutant"):
                extracted["experience"] = result.experience
        if _is_real(result.availability):
            extracted["availability"] = result.availability
        if _is_real(result.location):
            extracted["location"] = result.location
        if _is_real(result.riskAppetite):
            extracted["riskAppetite"] = result.riskAppetite
        if _is_real(result.revenueGoal):
            extracted["revenueGoal"] = result.revenueGoal
        if _is_real(result.motivation):
            extracted["motivation"] = result.motivation
        if _is_real(result.notes):
            extracted["notes"] = result.notes

        return extracted
    except Exception as e:
        print(f"  🟡 [MEMORY] Extraction failed: {str(e)[:60]}")
        return {}


def merge_memory(existing: ProspectMemory, new_info: dict) -> ProspectMemory:
    """Fusionne les infos existantes avec les nouvelles sans écraser."""
    return ProspectMemory(
        name=new_info.get("name") or existing.name,
        experience=new_info.get("experience") or existing.experience,
        availability=new_info.get("availability") or existing.availability,
        location=new_info.get("location") or existing.location,
        riskAppetite=new_info.get("riskAppetite") or existing.riskAppetite,
        revenueGoal=new_info.get("revenueGoal") or existing.revenueGoal,
        motivation=new_info.get("motivation") or existing.motivation,
        notes=new_info.get("notes") or existing.notes,
    )


def count_qualification_fields(memory: ProspectMemory) -> int:
    """Compte combien de champs de qualification (parmi les 6) sont remplis."""
    count = 0
    if memory.name:
        count += 1
    if memory.experience:
        count += 1
    if memory.availability:
        count += 1
    if memory.location:
        count += 1
    if memory.revenueGoal:
        count += 1
    if memory.riskAppetite:
        count += 1
    return count


def next_missing_field(memory: ProspectMemory) -> str | None:
    """Retourne le prochain champ de qualification manquant.

    Ordre: name → experience → availability → location → revenueGoal → riskAppetite
    """
    if not memory.name:
        return "name"
    if not memory.experience:
        return "experience"
    if not memory.availability:
        return "availability"
    if not memory.location:
        return "location"
    if not memory.revenueGoal:
        return "revenueGoal"
    if not memory.riskAppetite:
        return "riskAppetite"
    return None


def format_memory_for_prompt(memory: ProspectMemory) -> str | None:
    """Formate la mémoire pour injection dans le prompt du LLM."""
    lines: list[str] = []
    if memory.name:
        lines.append(f"- Nom: {memory.name}")
    if memory.experience:
        lines.append(f"- Expérience: {memory.experience}")
    if memory.availability:
        lines.append(f"- Disponibilité: {memory.availability}")
    if memory.location:
        lines.append(f"- Localisation: {memory.location}")
    if memory.riskAppetite:
        lines.append(f"- Appétence aux risques: {memory.riskAppetite}")
    if memory.revenueGoal:
        lines.append(f"- Objectif revenu: {memory.revenueGoal}")
    if memory.motivation:
        lines.append(f"- Motivation: {memory.motivation}")
    if memory.notes:
        lines.append(f"- Notes: {memory.notes}")

    if not lines:
        return None

    return "## Mémoire du candidat\n" + "\n".join(lines)


def parse_memory(json_str: str | None) -> ProspectMemory:
    """Parse le JSON stocké en ProspectMemory."""
    if not json_str:
        return ProspectMemory()
    try:
        data = json.loads(json_str)
        return ProspectMemory(**data)
    except (json.JSONDecodeError, TypeError):
        return ProspectMemory()


def serialize_memory(memory: ProspectMemory) -> str:
    """Sérialise ProspectMemory en JSON pour stockage."""
    return memory.model_dump_json()
