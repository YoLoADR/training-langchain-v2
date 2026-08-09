"""Tests pour hirekit.ui.telegram_bot — AT05."""
import pytest


class TestTelegramBotSimulated:
    @pytest.mark.xfail(reason="AT05 non implémenté sur cette branche")
    def test_start_simulated(self):
        from hirekit.ui.telegram_bot import start_telegram_bot_simulated
        assert callable(start_telegram_bot_simulated)
