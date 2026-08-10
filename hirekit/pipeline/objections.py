"""Détection d'objections — LLM + fallback keyword matching.

Inspiration: sellkit/src/pipeline/objections.ts

8 types d'objections avec tactiques:
  trop_cher, arnaque, reflechir, pas_interesse, fixe, legalite, famille, temps

Approche: LLM (gpt-4o-mini ou équivalent) classifie le message.
Fallback: keyword matching si le LLM est indisponible.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from hirekit.config import OPENAI_API_KEY, OPENAI_MODEL

ObjectionKey = Literal[
    "trop_cher",
    "arnaque",
    "reflechir",
    "pas_interesse",
    "fixe",
    "legalite",
    "famille",
    "temps",
    "aucune",
]


class Objection(BaseModel):
    key: str = Field(description="Type d'objection détectée")
    tactic: str = Field(description="Tactique de réponse à l'objection")


OBJECTION_CATALOG: dict[str, dict[str, list[str] | str]] = {
    "trop_cher": {
        "tactic": "Reformuler la valeur perçue. Ne pas justifier le prix, montrer ce que le candidat y gagne.",
        "description": "Le candidat trouve que c'est trop cher, s'inquiète du budget ou des frais",
        "triggers": ["trop cher", "trop coûteux", "pas le budget", "c'est cher", "frais"],
    },
    "arnaque": {
        "tactic": "Démontrer la transparence. Pas de promesses de gains, pas de pression. Donner des faits concrets.",
        "description": "Le candidat pense que c'est une arnaque, une pyramide, un schéma douteux",
        "triggers": ["arnaque", "escroquerie", "pyramide", "pyramidale", "mlm"],
    },
    "reflechir": {
        "tactic": "Donner de l'espace. Pas de pression. Proposer un délai court.",
        "description": "Le candidat veut réfléchir, demande du temps avant de décider",
        "triggers": ["réfléchir", "reflechir", "donnez-moi du temps", "laissez-moi réfléchir"],
    },
    "pas_interesse": {
        "tactic": "Accepter le refus avec respect. Proposer de garder contact pour plus tard. Ne pas insister.",
        "description": "Le candidat dit qu'il n'est pas intéressé, refuse poliment",
        "triggers": ["pas intéressé", "pas interesse", "non merci", "ça ne m'intéresse pas"],
    },
    "fixe": {
        "tactic": "Expliquer le modèle de rémunération. Montrer les revenus potentiels réalistes sans promettre de miracle.",
        "description": "Le candidat veut un salaire fixe, demande combien ça paie",
        "triggers": [
            "fixe",
            "salaire fixe",
            "minimum garanti",
            "combien ça paie",
            "ça paie combien",
        ],
    },
    "legalite": {
        "tactic": "Renvoyer vers les informations officielles. Pas de promesses juridiques. Rester factuel.",
        "description": "Le candidat questionne la légalité, s'inquiète des zones grises",
        "triggers": ["légalité", "c'est légal", "zone grise", "l'argent vient d'où"],
    },
    "famille": {
        "tactic": "Reconnaître les responsabilités familiales. Proposer de la flexibilité. Pas de culpabilisation.",
        "description": "Le candidat évoque sa famille, ses enfants, ses responsabilités",
        "triggers": ["ma femme", "mon enfant", "mes enfants", "famille", "je viens d'accoucher"],
    },
    "temps": {
        "tactic": "Proposer un format flexible. Montrer que c'est compatible avec un emploi actuel.",
        "description": "Le candidat dit qu'il n'a pas le temps, est trop occupé",
        "triggers": ["pas le temps", "trop occupé", "je travaille déjà", "pas de disponibilité"],
    },
}


class DetectionSchema(BaseModel):
    """Schéma pour la détection LLM."""

    objection: ObjectionKey = Field(description="Type d'objection détectée")
    refusal: bool = Field(description="True si le candidat demande d'arrêter le contact")
    confidence: float = Field(ge=0, le=1, description="Niveau de confiance (0-1)")


DETECTION_PROMPT = """Tu es un classifieur d'objections pour un agent de recrutement.
Analyse le message du candidat et classifie-le.

Catégories d'objections:
- trop_cher: le candidat trouve que c'est trop cher, s'inquiète du budget ou des frais
- arnaque: le candidat pense que c'est une arnaque, une pyramide, un schéma douteux
- reflechir: le candidat veut réfléchir, demande du temps avant de décider
- pas_interesse: le candidat dit qu'il n'est pas intéressé, refuse poliment
- fixe: le candidat veut un salaire fixe, demande combien ça paie
- legalite: le candidat questionne la légalité, s'inquiète des zones grises
- famille: le candidat évoque sa famille, ses enfants, ses responsabilités
- temps: le candidat dit qu'il n'a pas le temps, est trop occupé
- aucune: aucune objection détectée

Refusal (opt-out): True si le candidat demande explicitement d'arrêter le contact
(ex: "ne me recontactez plus", "stop", "laissez tomber", "je ne veux plus")

Réponds UNIQUEMENT avec le JSON structuré."""


_refusal_patterns = [
    "ne me recontactez",
    "ne me recontacte",
    "ne plus me contacter",
    "stop",
    "laissez tomber",
    "oubliez",
    "je ne veux plus",
    "cesser le contact",
    "ne me contactez plus",
]


def _detect_keywords(text: str) -> tuple[Objection | None, bool, str]:
    """Fallback: détection par keyword matching."""
    low = text.lower()
    refusal = any(p in low for p in _refusal_patterns)

    for key, data in OBJECTION_CATALOG.items():
        for trigger in data["triggers"]:
            if trigger in low:
                return Objection(key=key, tactic=str(data["tactic"])), refusal, "keyword"

    return None, refusal, "none"


async def detect(text: str) -> dict:
    """Détecte l'objection dans le texte du candidat.

    1. Essaie le LLM (si configuré) — robuste, comprend le contexte
    2. Fallback: keyword matching

    Returns:
        {"objection": Objection | None, "refusal": bool, "source": "llm" | "keyword" | "none"}
    """
    if OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
            structured = llm.with_structured_output(DetectionSchema)
            result = await structured.ainvoke(
                [
                    {"role": "system", "content": DETECTION_PROMPT},
                    {"role": "user", "content": text},
                ],
                tags=["hirekit", "objection-detection"],
            )

            objection_key = None if result.objection == "aucune" else result.objection
            objection = (
                Objection(
                    key=objection_key,
                    tactic=OBJECTION_CATALOG.get(objection_key, {}).get("tactic", ""),
                )
                if objection_key
                else None
            )
            return {"objection": objection, "refusal": result.refusal, "source": "llm"}
        except Exception as e:
            print(f"  🟡 [OBJECTION] LLM detection failed, fallback: {str(e)[:60]}")

    objection, refusal, source = _detect_keywords(text)
    return {"objection": objection, "refusal": refusal, "source": source}


def detect_sync(text: str) -> dict:
    """Version synchrone de detect()."""
    if OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
            structured = llm.with_structured_output(DetectionSchema)
            result = structured.invoke(
                [
                    {"role": "system", "content": DETECTION_PROMPT},
                    {"role": "user", "content": text},
                ],
                tags=["hirekit", "objection-detection"],
            )

            objection_key = None if result.objection == "aucune" else result.objection
            objection = (
                Objection(
                    key=objection_key,
                    tactic=OBJECTION_CATALOG.get(objection_key, {}).get("tactic", ""),
                )
                if objection_key
                else None
            )
            return {"objection": objection, "refusal": result.refusal, "source": "llm"}
        except Exception as e:
            print(f"  🟡 [OBJECTION] LLM detection failed, fallback: {str(e)[:60]}")

    objection, refusal, source = _detect_keywords(text)
    return {"objection": objection, "refusal": refusal, "source": source}


def list_objections() -> list[str]:
    """Liste toutes les objections disponibles."""
    return list(OBJECTION_CATALOG.keys())
