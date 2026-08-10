"""Bug v1 test — format_response ne tronque pas (limite Telegram 4096)."""

import pytest


class TestBugV1:
    """Bug v1 : format_response doit respecter la limite de 4096 caractères."""

    def test_format_response_short_text(self):
        from hirekit.ui.telegram_bot import format_response
        result = format_response("Texte court")
        assert result == "Texte court"

    def test_format_response_long_text_truncated(self):
        from hirekit.ui.telegram_bot import format_response
        long_text = "A" * 5000
        result = format_response(long_text)
        assert len(result) <= 4096
        assert "tronqué" in result

    def test_format_response_default_limit_is_4096(self):
        """La limite par défaut doit être 4096 (limite Telegram)."""
        from hirekit.ui.telegram_bot import format_response
        long_text = "A" * 4097
        result = format_response(long_text)
        assert len(result) <= 4096