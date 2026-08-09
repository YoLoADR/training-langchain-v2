"""Bot Telegram simulé — interface chat pour recruteurs mobiles.

AT05 — UX Chatbot : bot Telegram (simulé en local, vrai bot en bonus).
"""

from __future__ import annotations


def start_telegram_bot_simulated() -> None:
    """AT05 — démarre le bot Telegram en mode simulé (mock local, pas de vrai bot API).

    Le bot simulé lit les messages depuis stdin et répond via l'agent hirekit.
    Permet de tester le flux Telegram sans configuration API.
    """
    raise NotImplementedError(
        "AT05 — implémentez start_telegram_bot_simulated() dans hirekit/ui/telegram_bot.py"
    )


def start_telegram_bot_real() -> None:
    """AT05 (Bonus) — démarre le vrai bot Telegram avec python-telegram-bot.

    Nécessite TELEGRAM_BOT_TOKEN dans .env.
    """
    raise NotImplementedError(
        "AT05 — implémentez start_telegram_bot_real() dans hirekit/ui/telegram_bot.py"
    )
