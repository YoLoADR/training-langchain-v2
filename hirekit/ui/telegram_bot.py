"""Bot Telegram — handler complet inspiré de sellkit/src/telegram/handler.ts.

AT06 — Chatbots + Telegram + CRM

Flux à chaque message entrant (inspiré sellkit/src/telegram/handler.ts:45-226):
  1. Détection d'objection (LLM → fallback keyword)
  2. Détection de closing (LLM → fallback keyword → stage CRM)
  3. Extraction mémoire (LLM → 6 champs → merge → stockage DB)
  4. CRM: get_or_create, update_stage, add_message
  5. Deep Agent (beforeModel injecte SKILL.md + contexte)
  6. Reply + log structuré

Le bot simulé permet de tester le flux sans configuration API Telegram.
"""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from hirekit.crm.store import CrmStore

_store: CrmStore | None = None


def _crm() -> CrmStore:
    global _store
    if _store is None:
        _store = CrmStore()
    return _store


from hirekit.pipeline.objections import detect_sync as detect_objection
from hirekit.pipeline.closing import detect_closing_sync
from hirekit.pipeline.memory import (
    extract_memory_sync,
    merge_memory,
    parse_memory,
    serialize_memory,
    count_qualification_fields,
    next_missing_field,
    format_memory_for_prompt,
)
from hirekit.pipeline.qualification import FIELD_QUESTIONS, CLOSING_STAGES
from hirekit.telemetry import log
from hirekit.deep_agent.middleware import RecruitmentContext

BOT_COMMANDS = {
    "/start": "Affiche le message de bienvenue.",
    "/help": "Affiche l'aide et les commandes disponibles.",
    "/status": "Affiche le pipeline CRM (stats).",
    "/candidates": "Liste tous les candidats.",
    "/quit": "Quitte le bot simulé.",
}

WELCOME_MESSAGE = (
    "🤖 HireKit Bot — Recruteur IA\n\n"
    "Je filtre les candidats via des conversations de screening.\n"
    "Je mets à jour le CRM automatiquement.\n\n"
    "Commandes:\n"
    "  /status — Pipeline CRM\n"
    "  /candidates — Liste des candidats\n"
    "  /help — Aide\n"
    "  /quit — Quitter"
)


async def handle_message(text: str, phone: str, first_name: str | None = None) -> str:
    """AT06 — handler complet: objection→closing→memory→CRM→agent→reply.

    Inspiré de sellkit/src/telegram/handler.ts:48-223.

    Args:
        text: message entrant du candidat.
        phone: identifiant du candidat (clé CRM).
        first_name: prénom du candidat (optionnel).

    Returns:
        La réponse à envoyer au candidat.
    """
    if text.startswith("/"):
        return process_command(text[1:].split(" ", 1)[0])

    # ── 1. Détection d'objection ──
    log.msg_in(first_name or phone, phone, text)
    detection = detect_objection(text)
    if detection["objection"]:
        log.objection(
            detection["objection"].key,
            detection["source"],
            detection["objection"].tactic,
        )
    if detection["refusal"]:
        log.refusal(detection["source"])

    # ── 2. Détection de closing ──
    closing = detect_closing_sync(text)
    if closing.type != "none":
        log.closing(closing.type, closing.source, closing.target_stage, closing.should_send_link)

    # ── 3. Extraction mémoire ──
    new_info = extract_memory_sync(text)
    existing_json = _crm().get_qual_json(phone)
    existing_memory = parse_memory(existing_json)
    merged_memory = merge_memory(existing_memory, new_info)
    qual_count = count_qualification_fields(merged_memory)

    if qual_count > 0:
        _crm().set_qual_json(phone, serialize_memory(merged_memory))
    if new_info:
        log.memory(new_info)

    # ── 4. CRM: register + update ──
    _crm().get_or_create(phone, {"first_name": first_name})
    _crm().add_message(
        phone, "in", text, detection["objection"].key if detection["objection"] else None
    )

    current_candidate = _crm().get(phone)
    current_stage = current_candidate.stage if current_candidate else "new"

    # Guard: ignore job_interest/commitment si pas fully qualified
    if qual_count < 6 and closing.type in ("job_interest", "commitment_signal"):
        log.closing_ignored(closing.type, qual_count)
        closing.type = "none"
        closing.target_stage = None
        closing.should_send_link = False

    # Stage update
    if closing.target_stage:
        _crm().update_stage(phone, closing.target_stage)
        log.stage_update(phone, closing.target_stage)

    # Conversion link
    link_appended = False
    if closing.should_send_link:
        existing_link = _crm().get_conversion_link(phone)
        if not existing_link:
            link = _crm().set_conversion_link(phone)
            log.conversion_link(phone, link)
            link_appended = True
        else:
            log.conversion_link(phone, None)

    # ── 5. Deep Agent ──
    history = _crm().get_messages(phone)
    memory_prompt = format_memory_for_prompt(merged_memory)
    next_field = next_missing_field(merged_memory)
    candidate = _crm().get(phone)
    stage = candidate.stage if candidate else "new"

    from langchain_core.messages import HumanMessage, AIMessage

    messages = [
        HumanMessage(m.text) if m.direction == "in" else AIMessage(m.text) for m in history[-20:]
    ]

    recruitment_ctx = RecruitmentContext(
        qual_count=qual_count,
        stage=stage,
        memory_prompt=memory_prompt,
        next_field=next_field,
        objection_key=detection["objection"].key if detection["objection"] else None,
        objection_tactic=detection["objection"].tactic if detection["objection"] else None,
        link_being_sent=link_appended,
        link_already_sent=not link_appended and _crm().get_conversion_link(phone) is not None,
        is_closing=stage in CLOSING_STAGES and qual_count >= 6,
        show_test_and_link=stage in CLOSING_STAGES or qual_count >= 6,
        refusal=detection["refusal"],
    )

    log.llm_calling("deep_agent", phone)
    reply = ""
    try:
        from hirekit.deep_agent.recruiter_agent import run_deep_turn

        reply = run_deep_turn(phone, messages, recruitment_ctx)

        if link_appended:
            link = _crm().get_conversion_link(phone)
            if link:
                reply = f"{reply}\n\n📋 Voici les fiches de poste :\n🔗 {link}"

        _crm().add_message(phone, "out", reply)

        current_cand = _crm().get(phone)
        if current_cand and current_cand.stage == "new":
            _crm().update_stage(phone, "contacted")

        if detection["refusal"]:
            if current_cand and current_cand.stage != "closed_lost":
                _crm().update_stage(phone, "closed_lost")

        log.msg_out(first_name or phone, reply)
    except Exception as err:
        log.llm_error(phone, err)
        fallback_question = FIELD_QUESTIONS.get(next_field) if next_field else None
        reply = (
            f"Désolé, petit souci technique. {fallback_question}"
            if fallback_question
            else "Désolé, j'ai eu un problème technique. Pouvez-vous reformuler ?"
        )
        _crm().add_message(phone, "out", reply)

    return reply


def process_command(command: str) -> str:
    """Traite une commande admin (/status, /candidates, /help)."""
    command = command.lower().strip()

    if command == "start":
        return WELCOME_MESSAGE

    if command == "help":
        lines = ["📋 Commandes disponibles:\n"]
        for cmd, desc in BOT_COMMANDS.items():
            lines.append(f"  {cmd} — {desc}")
        return "\n".join(lines)

    if command == "status":
        stats = _crm().stats()
        lines = [
            "📊 Pipeline CRM:\n",
            f"  Total candidats: {stats['total_candidates']}",
            f"  Total messages: {stats['total_messages']}",
            "\n  Par stage:",
        ]
        for stage, count in stats.get("by_stage", {}).items():
            lines.append(f"    {stage}: {count}")
        return "\n".join(lines)

    if command == "candidates":
        candidates = _crm().get_all()
        if not candidates:
            return "Aucun candidat dans le CRM."
        lines = ["📋 Candidats:\n"]
        for c in candidates[:20]:
            lines.append(
                f"  {c.first_name or c.phone} — stage: {c.stage} — msgs: {c.message_count}"
            )
        return "\n".join(lines)

    if command == "quit":
        return "Au revoir ! 👋"

    return f"Commande inconnue: /{command}\nTape /help pour voir les commandes."


def start_telegram_bot_simulated() -> None:
    """AT06 — démarre le bot Telegram en mode simulé (mock local).

    Le bot simulé lit les messages depuis stdin et les passe à handle_message().
    Chaque message est traité via le flux complet: objection→closing→memory→CRM→agent→reply.
    """
    print(WELCOME_MESSAGE)
    print("\n--- Mode simulé (tapez vos messages, /quit pour arrêter) ---\n")
    print("Vous jouez le rôle d'un candidat. Le bot va vous qualifier.\n")

    phone = "+33600000000"
    first_name = "Candidat Test"

    while True:
        try:
            user_input = input("👤 Candidat > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nAu revoir ! 👋")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd = user_input[1:].split(" ", 1)[0]
            if cmd.lower() == "quit":
                print("🤖 Bot > Au revoir ! 👋")
                break
            response = process_command(cmd)
            print(f"🤖 Bot > {response}\n")
            continue

        try:
            response = asyncio.run(handle_message(user_input, phone, first_name))
            print(f"🤖 Bot > {response}\n")
        except Exception as e:
            print(f"🤖 Bot > ❌ Erreur: {e}\n")


def start_telegram_bot_real() -> None:
    """AT06 (Bonus) — démarre le vrai bot Telegram avec python-telegram-bot.

    Nécessite TELEGRAM_BOT_TOKEN dans .env.
    """
    import os

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN non trouvé dans .env")
        return

    try:
        from telegram import Update
        from telegram.ext import (
            ApplicationBuilder,
            CommandHandler,
            MessageHandler,
            ContextTypes,
            filters,
        )
    except ImportError:
        print("❌ python-telegram-bot non installé: pip install python-telegram-bot")
        return

    async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(WELCOME_MESSAGE)

    async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(process_command("help"))

    async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(process_command("status"))

    async def handle_message_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
        sender = update.message.from_user
        phone = f"+{sender.id}"
        first_name = sender.first_name
        text = update.message.text

        if not text:
            return

        try:
            reply = await handle_message(text, phone, first_name)
            if reply and reply.strip():
                await update.message.reply_text(reply[:4096])
        except Exception as e:
            await update.message.reply_text(f"Erreur: {e}")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("status", handle_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_telegram))

    print("🤖 Bot Telegram démarré (flux sellkit: objection→closing→memory→CRM→agent→reply)")
    app.run_polling()
