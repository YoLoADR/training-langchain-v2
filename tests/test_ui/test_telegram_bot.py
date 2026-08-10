"""Tests pour hirekit.ui.telegram_bot — AT05."""

import pytest


class TestTelegramBotSimulated:
    """AT05 — start_telegram_bot_simulated() et process_command()."""

    def test_start_simulated(self):
        from hirekit.ui.telegram_bot import start_telegram_bot_simulated
        assert callable(start_telegram_bot_simulated)

    def test_welcome_message(self):
        from hirekit.ui.telegram_bot import WELCOME_MESSAGE
        assert "HireKit" in WELCOME_MESSAGE
        assert "/search" in WELCOME_MESSAGE or "search" in WELCOME_MESSAGE.lower()

    def test_bot_commands_defined(self):
        from hirekit.ui.telegram_bot import BOT_COMMANDS
        assert "/start" in BOT_COMMANDS
        assert "/help" in BOT_COMMANDS
        # /search est préfixé avec <query> dans les clés
        assert any(k.startswith("/search") for k in BOT_COMMANDS)


class TestProcessCommand:
    """AT05 — process_command() route les commandes du bot."""

    def test_start_command(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("start")
        assert "HireKit" in result or "Bienvenue" in result

    def test_help_command(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("help")
        assert "/search" in result
        assert "/help" in result

    def test_unknown_command(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("inconnue")
        assert "inconnu" in result.lower() or "help" in result.lower()

    def test_search_without_args(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("search")
        assert "Usage" in result or "requête" in result

    def test_web_without_args(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("web")
        assert "Usage" in result or "requête" in result

    def test_web_with_args(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("web", "Marie Dubois développeur")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_match_without_args(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("match")
        assert "Usage" in result or "Format" in result

    def test_match_wrong_format(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("match", "juste un cv sans separateur")
        assert "Format" in result or "| " in result

    def test_code_without_args(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("code")
        assert "Usage" in result or "question" in result

    def test_quit_command(self):
        from hirekit.ui.telegram_bot import process_command
        result = process_command("quit")
        assert "revoir" in result.lower() or "bye" in result.lower()


class TestFormatResponse:
    """AT05 — format_response() respecte la limite Telegram."""

    def test_format_short_text(self):
        from hirekit.ui.telegram_bot import format_response
        result = format_response("Texte court")
        assert result == "Texte court"

    def test_format_long_text(self):
        from hirekit.ui.telegram_bot import format_response
        long_text = "A" * 5000
        result = format_response(long_text, max_length=4096)
        assert len(result) <= 4096
        assert "tronqué" in result

    def test_format_exact_limit(self):
        from hirekit.ui.telegram_bot import format_response
        exact_text = "A" * 100
        result = format_response(exact_text, max_length=100)
        assert len(result) == 100