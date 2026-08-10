"""Bot Telegram simulé — interface chat pour recruteurs mobiles.

AT05 — UX Chatbot : bot Telegram (simulé en local, vrai bot en bonus).

Le bot simulé permet de tester le flux Telegram sans configuration API.
Il lit les messages depuis stdin et répond via l'agent hirekit.
"""

from __future__ import annotations

import sys
from typing import Any


# ─── Commandes supportées par le bot ────────────────────────────────────────

BOT_COMMANDS = {
    "/start": "Affiche le message de bienvenue et la liste des commandes.",
    "/help": "Affiche l'aide et les commandes disponibles.",
    "/search <query>": "Recherche des candidats dans la base de CVs.",
    "/match <cv> <offer>": "Évalue la correspondance entre un CV et une offre.",
    "/web <query>": "Recherche web (réputation, technologie).",
    "/code <question>": "Pose une question sur le code du repo.",
    "/quit": "Quitte le bot simulé.",
}

WELCOME_MESSAGE = (
    "🤖 HireKit Bot — Assistant recruteur\n\n"
    "Je peux t'aider à :\n"
    "  🔍 Rechercher des candidats (/search)\n"
    "  📋 Matcher un CV avec une offre (/match)\n"
    "  🌐 Vérifier la réputation en ligne (/web)\n"
    "  💻 Analyser du code (/code)\n\n"
    "Tape /help pour voir toutes les commandes."
)


def format_response(text: str, max_length: int = 4096) -> str:
    """Formate une réponse pour Telegram (limite 4096 caractères par message).

    Args:
        text: texte à formater.
        max_length: limite de caractères Telegram (défaut: 4096).

    Returns:
        Texte tronqué si nécessaire.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 20] + "\n\n[...tronqué]"


def process_command(command: str, args: str = "") -> str:
    """AT05 — traite une commande du bot et retourne la réponse.

    Cette fonction est testable sans LLM ni API externe. Elle route
    les commandes vers les bons outils ou messages.

    Args:
        command: commande sans le slash (ex: "search", "help", "start").
        args: arguments de la commande (ex: "React Python" pour "search").

    Returns:
        Réponse formatée pour Telegram.
    """
    command = command.lower().strip()

    if command == "start":
        return WELCOME_MESSAGE

    if command == "help":
        lines = ["📋 Commandes disponibles:\n"]
        for cmd, desc in BOT_COMMANDS.items():
            lines.append(f"  {cmd} — {desc}")
        return "\n".join(lines)

    if command == "search":
        if not args:
            return "Usage: /search <requête>\nExemple: /search qui a de l'expérience en React ?"
        # Tenter d'utiliser le tool search_cvs
        try:
            from hirekit.agent.tools import search_cvs_tool
            result = search_cvs_tool.invoke({"query": args})
            return format_response(result)
        except Exception as e:
            return f"Erreur lors de la recherche: {e}"

    if command == "web":
        if not args:
            return "Usage: /web <requête>\nExemple: /web Marie Dubois développeur"
        try:
            from hirekit.agent.tools import web_search_tool
            result = web_search_tool.invoke({"query": args})
            return format_response(result)
        except Exception as e:
            return f"Erreur lors de la recherche web: {e}"

    if command == "match":
        if not args:
            return ("Usage: /match <CV> | <offre>\n"
                    "Exemple: /match Marie Dubois React 4 ans | Dev React Senior")
        # Séparer le CV et l'offre
        if "|" in args:
            cv_text, offer_text = args.split("|", 1)
            try:
                from hirekit.agent.tools import match_candidate_tool
                result = match_candidate_tool.invoke({
                    "cv_text": cv_text.strip(),
                    "offer_text": offer_text.strip(),
                })
                return format_response(result)
            except Exception as e:
                return f"Erreur lors du matching: {e}"
        return "Format invalide. Utilisez: /match <CV> | <offre>"

    if command == "code":
        if not args:
            return "Usage: /code <question>\nExemple: /code Où est gérée l'authentification ?"
        try:
            from hirekit.ui.code_reviewer import index_code_repo, ask_code_question
            retriever = index_code_repo("data/code_repo")
            result = ask_code_question(args, retriever)
            return format_response(result)
        except Exception as e:
            return f"Erreur lors de l'analyse du code: {e}"

    if command == "quit":
        return "Au revoir ! 👋"

    return f"Commande inconnue: /{command}\nTape /help pour voir les commandes disponibles."


def start_telegram_bot_simulated() -> None:
    """AT05 — démarre le bot Telegram en mode simulé (mock local).

    Le bot simulé lit les messages depuis stdin et répond via process_command().
    Permet de tester le flux Telegram sans configuration API.

    Tapez /quit pour arrêter.
    """
    print(WELCOME_MESSAGE)
    print("\n--- Mode simulé (tapez vos commandes, /quit pour arrêter) ---\n")

    while True:
        try:
            user_input = input("👤 You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nAu revoir ! 👋")
            break

        if not user_input:
            continue

        # Parser la commande
        if user_input.startswith("/"):
            parts = user_input[1:].split(" ", 1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""
        else:
            # Message libre → traiter comme une recherche
            command = "search"
            args = user_input

        if command.lower() == "quit":
            print("🤖 Bot > Au revoir ! 👋")
            break

        response = process_command(command, args)
        print(f"🤖 Bot > {response}\n")


def start_telegram_bot_real() -> None:
    """AT05 (Bonus) — démarre le vrai bot Telegram avec python-telegram-bot.

    Nécessite TELEGRAM_BOT_TOKEN dans .env.
    """
    import os

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN non trouvé dans .env")
        print("   Pour utiliser le bot simulé: start_telegram_bot_simulated()")
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
        print("❌ python-telegram-bot non installé. Lancez: pip install python-telegram-bot")
        return

    async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(WELCOME_MESSAGE)

    async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = process_command("help")
        await update.message.reply_text(response)

    async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = " ".join(context.args) if context.args else ""
        response = process_command("search", args)
        await update.message.reply_text(response)

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Message libre → recherche
        response = process_command("search", update.message.text)
        await update.message.reply_text(response)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("search", handle_search))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot Telegram démarré. Ctrl+C pour arrêter.")
    app.run_polling()