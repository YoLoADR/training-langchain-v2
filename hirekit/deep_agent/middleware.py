"""Middleware beforeModel — injection dynamique de skills + contexte.

Inspiration: sellkit/src/agent/middleware/recruitment-context.ts

Couche 3: Skills — SKILL.md injecté par beforeModel (lu avec fs.readFileSync)
Couche 4: Contexte dynamique — contextSchema (Pydantic) + build_context_prompt

Ce que beforeModel injecte (SystemMessage prependu avant les messages):
1. Le bon SKILL.md selon la phase (qualCount, stage, isClosing)
2. Le SKILL.md test technique (si showTestAndLink)
3. Le contexte dynamique (infos candidat, prochaine question, lien, objection, opt-out)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from hirekit.pipeline.qualification import FIELD_QUESTIONS, CLOSING_STAGES


class RecruitmentContext(BaseModel):
    """Contexte dynamique injecté avant chaque appel LLM."""

    qual_count: int = Field(
        default=0, description="Nombre de champs de qualification remplis (0-6)"
    )
    stage: str = Field(default="new", description="Stage CRM actuel du candidat")
    memory_prompt: str | None = Field(
        default=None, description="Mémoire du candidat formatée pour le prompt"
    )
    next_field: str | None = Field(
        default=None, description="Prochain champ de qualification à demander"
    )
    objection_key: str | None = Field(default=None, description="Type d'objection détectée")
    objection_tactic: str | None = Field(
        default=None, description="Tactique de réponse à l'objection"
    )
    link_being_sent: bool = Field(default=False, description="True si le lien est en cours d'envoi")
    link_already_sent: bool = Field(default=False, description="True si le lien a déjà été envoyé")
    is_closing: bool = Field(default=False, description="True si on est en phase de closing")
    show_test_and_link: bool = Field(
        default=False, description="True si on doit présenter le test + lien"
    )
    refusal: bool = Field(default=False, description="True si le candidat demande opt-out")


AGENT_DIR = Path(__file__).resolve().parent.parent.parent / ".agent"


def _read_skill(skill_dir: str) -> str:
    """Lit un fichier SKILL.md depuis .agent/skills/recruiter/<skill_dir>/SKILL.md."""
    skill_path = AGENT_DIR / "skills" / "recruiter" / skill_dir / "SKILL.md"
    if not skill_path.exists():
        return ""
    return skill_path.read_text(encoding="utf-8")


def read_skill_for_context(ctx: RecruitmentContext) -> str:
    """Détermine quel skill de phase charger selon le contexte.

    - refusal → pas de skill (juste OPT-OUT)
    - qualCount=0, stage=new → phase-first-contact
    - qualCount 1-5 → phase-qualification
    - qualCount=6, stage < interested → phase-reformulation
    - isClosing (stage in CLOSING_STAGES, qualCount >= 6) → phase-closing
    - showTestAndLink → ajoute aussi phase-test-technique
    """
    if ctx.refusal:
        return ""

    parts: list[str] = []

    if ctx.is_closing:
        parts.append(_read_skill("phase-closing"))
    elif ctx.qual_count >= 6:
        parts.append(_read_skill("phase-reformulation"))
    elif ctx.qual_count > 0:
        parts.append(_read_skill("phase-qualification"))
    else:
        parts.append(_read_skill("phase-first-contact"))

    if ctx.show_test_and_link:
        parts.append(_read_skill("phase-test-technique"))

    return "\n\n".join(p for p in parts if p)


def build_context_prompt(ctx: RecruitmentContext) -> str:
    """Construit le prompt de contexte dynamique.

    Sections injectées (par ordre de priorité):
    1. Refusal (OPT-OUT) — priorité absolue, traité en premier
    2. Infos candidat (mémoire)
    3. Prochaine question (qualification uniquement)
    4. Lien fiches de poste (envoi ou déjà envoyé)
    5. Objection détectée + tactique
    """
    parts: list[str] = []

    if ctx.refusal:
        parts.append("## OPT-OUT")
        parts.append(
            "Le candidat a demandé d'arrêter le contact. Accepter avec respect. Ne pas insister."
        )
        parts.append("")
        return "\n".join(parts)

    if ctx.memory_prompt:
        parts.append("## Infos candidat")
        parts.append(ctx.memory_prompt)
        parts.append("")

    if 0 < ctx.qual_count < 6 and ctx.next_field:
        parts.append("## Prochaine question (OBLIGATOIRE — pose cette question maintenant)")
        parts.append(FIELD_QUESTIONS.get(ctx.next_field, FIELD_QUESTIONS["name"]))
        parts.append("")

    if ctx.link_being_sent:
        parts.append("## Lien fiches de poste")
        parts.append(
            "Le système ajoute les fiches de poste à la fin de ton message. NE dis PAS 'Voici les fiches de poste'."
        )
        parts.append("")
    elif ctx.link_already_sent:
        parts.append("## Lien fiches de poste")
        parts.append("Le lien a déjà été envoyé. Tu peux y faire référence. NE renvoie PAS l'URL.")
        parts.append("")

    if ctx.objection_key and ctx.objection_tactic:
        parts.append("## Objection détectée")
        parts.append(f"Type: {ctx.objection_key}")
        parts.append(f"TACTIQUE: {ctx.objection_tactic}")
        if 0 < ctx.qual_count < 6:
            parts.append(
                "PRIORITÉ: réponds d'abord à l'objection, puis pose la question de qualification."
            )
        else:
            parts.append(
                "PRIORITÉ: réponds d'abord à l'objection, puis poursuis la phase en cours."
            )
        parts.append("")

    return "\n".join(parts) if parts else ""


def create_recruitment_context_middleware(agent_dir: str | None = None):
    """Factory du middleware beforeModel pour Deep Agents.

    Returns un dict avec la structure attendue par les middlewares LangChain:
    {"name": str, "context_schema": Pydantic, "before_model": callable}
    """
    global AGENT_DIR
    if agent_dir:
        AGENT_DIR = Path(agent_dir)

    def before_model(state: dict, runtime: Any) -> dict:
        ctx = getattr(runtime, "context", None) if runtime else None
        if ctx is None:
            return state

        if isinstance(ctx, dict):
            ctx = RecruitmentContext(**ctx)

        skill_content = read_skill_for_context(ctx)
        context_prompt = build_context_prompt(ctx)

        full_prompt = "\n\n".join(p for p in [skill_content, context_prompt] if p)
        if not full_prompt:
            return state

        from langchain_core.messages import SystemMessage

        context_message = SystemMessage(content=full_prompt)
        messages = state.get("messages", [])
        return {**state, "messages": [context_message, *messages]}

    return {
        "name": "RecruitmentContextMiddleware",
        "context_schema": RecruitmentContext,
        "before_model": before_model,
    }
