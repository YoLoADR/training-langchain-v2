"""Détection de closing — LLM + fallback keyword matching.

Inspiration: sellkit/src/pipeline/closing.ts

5 types de signaux:
  closing_cue, commitment_signal, call_request, job_interest, refusal

Approche: LLM (gpt-4o-mini ou équivalent) classifie le message.
Fallback: keyword matching si le LLM est indisponible.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from hirekit.config import OPENAI_API_KEY, OPENAI_MODEL

ClosingType = Literal[
    "closing_cue",
    "commitment_signal",
    "call_request",
    "job_interest",
    "refusal",
    "none",
]

STAGE_MAP: dict[ClosingType, str | None] = {
    "closing_cue": None,
    "commitment_signal": "closed_won",
    "call_request": "qualified",
    "job_interest": "interested",
    "refusal": "closed_lost",
    "none": None,
}


class ClosingResult(BaseModel):
    type: ClosingType = Field(default="none")
    should_send_link: bool = Field(default=False)
    target_stage: str | None = Field(default=None)
    source: Literal["llm", "keyword", "none"] = Field(default="none")


class ClosingSchema(BaseModel):
    """Schéma pour la détection LLM."""

    type: ClosingType = Field(description="Type de signal détecté dans le message")
    shouldSendLink: bool = Field(description="True si le candidat est prêt à recevoir le lien")
    confidence: float = Field(ge=0, le=1, description="Niveau de confiance (0-1)")


DETECTION_PROMPT = """Tu es un classifieur de signaux de closing pour un agent de recrutement.
Analyse le message du candidat et classifie-le.

Contexte: les échanges se font par MESSAGES (WhatsApp/Telegram). Pas de rendez-vous physique.

Types de signaux:
- closing_cue: le candidat met fin à la conversation poliment (ex: "au revoir", "bonne journée")
- commitment_signal: le candidat est prêt à démarrer (ex: "je suis prêt", "ça marche", "c'est parti")
- call_request: le candidat demande un appel téléphonique (ex: "on peut s'appeler ?")
- job_interest: le candidat exprime un intérêt fort (ex: "ça m'intéresse", "je veux postuler")
- refusal: le candidat demande d'arrêter le contact (ex: "ne me recontactez plus")
- none: aucun signal détecté

shouldSendLink: True si c'est un commitment_signal ou job_interest.

Réponds UNIQUEMENT avec le JSON structuré."""


_closing_cues = [
    "au revoir",
    "bonne journée",
    "bonne soirée",
    "bon week-end",
    "à bientôt",
    "à plus",
    "merci et",
    "je vous laisse",
    "bonne continuation",
    "parfait merci",
    "ok c'est noté",
    "c'est tout",
    "c'est bon",
]
_commitment_cues = [
    "ok pour",
    "ça marche",
    "ca marche",
    "je prends",
    "je suis prêt",
    "je suis pret",
    "je démarre",
    "je demarre",
    "je le fais",
    "c'est parti",
    "d'accord pour",
    "je valide",
    "je signe",
]
_call_cues = [
    "s'appeler",
    "appelez",
    "appeler",
    "au téléphone",
    "au telephone",
    "un appel",
    "par téléphone",
    "par telephone",
    "je préfère en parler",
    "je prefere en parler",
]
_job_interest_cues = [
    "ça m'intéresse",
    "ca m interesse",
    "je suis intéressé par",
    "je suis interesse par",
    "je veux postuler",
    "j'aimerais",
    "j aimerais",
    "intéressé par le poste",
    "interesse par le poste",
    "je veux le poste",
]
_refusal_cues = [
    "ne me recontactez",
    "ne me recontacte",
    "stop",
    "ne plus me contacter",
    "pas intéressé",
    "pas interesse",
    "je ne suis pas",
]


def _detect_keywords(text: str) -> ClosingResult:
    """Fallback: détection par keyword matching."""
    low = text.lower()

    if any(c in low for c in _refusal_cues):
        return ClosingResult(
            type="refusal", should_send_link=False, target_stage="closed_lost", source="keyword"
        )

    if any(c in low for c in _commitment_cues):
        return ClosingResult(
            type="commitment_signal",
            should_send_link=True,
            target_stage="closed_won",
            source="keyword",
        )

    if any(c in low for c in _call_cues):
        return ClosingResult(
            type="call_request", should_send_link=False, target_stage="qualified", source="keyword"
        )

    if any(c in low for c in _job_interest_cues):
        return ClosingResult(
            type="job_interest", should_send_link=True, target_stage="interested", source="keyword"
        )

    if any(c in low for c in _closing_cues):
        return ClosingResult(
            type="closing_cue", should_send_link=False, target_stage=None, source="keyword"
        )

    return ClosingResult(type="none", should_send_link=False, target_stage=None, source="none")


async def detect_closing(text: str) -> ClosingResult:
    """Détecte le signal de closing dans le texte du candidat.

    1. Essaie le LLM (si configuré) — robuste, comprend le contexte
    2. Fallback: keyword matching
    """
    if OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
            structured = llm.with_structured_output(ClosingSchema)
            result = await structured.ainvoke(
                [
                    {"role": "system", "content": DETECTION_PROMPT},
                    {"role": "user", "content": text},
                ],
                tags=["hirekit", "closing-detection"],
            )

            type_ = result.type
            should_send = type_ in ("commitment_signal", "job_interest")
            return ClosingResult(
                type=type_,
                should_send_link=should_send,
                target_stage=STAGE_MAP.get(type_),
                source="llm",
            )
        except Exception as e:
            print(f"  🟡 [CLOSING] LLM detection failed, fallback: {str(e)[:60]}")

    return _detect_keywords(text)


def detect_closing_sync(text: str) -> ClosingResult:
    """Version synchrone de detect_closing()."""
    if OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, max_retries=1, timeout=5)
            structured = llm.with_structured_output(ClosingSchema)
            result = structured.invoke(
                [
                    {"role": "system", "content": DETECTION_PROMPT},
                    {"role": "user", "content": text},
                ],
                tags=["hirekit", "closing-detection"],
            )

            type_ = result.type
            should_send = type_ in ("commitment_signal", "job_interest")
            return ClosingResult(
                type=type_,
                should_send_link=should_send,
                target_stage=STAGE_MAP.get(type_),
                source="llm",
            )
        except Exception as e:
            print(f"  🟡 [CLOSING] LLM detection failed, fallback: {str(e)[:60]}")

    return _detect_keywords(text)
