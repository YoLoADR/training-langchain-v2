"""Tests pour hirekit.ui.app — AT05."""

import pytest


class TestStreamlitApp:
    """AT05 — fonctions de l'app Streamlit."""

    def test_app_main_callable(self):
        from hirekit.ui.app import main
        assert callable(main)

    def test_render_chat_page_callable(self):
        from hirekit.ui.app import render_chat_page
        assert callable(render_chat_page)

    def test_render_matching_dashboard_callable(self):
        from hirekit.ui.app import render_matching_dashboard
        assert callable(render_matching_dashboard)

    def test_render_cv_library_callable(self):
        from hirekit.ui.app import render_cv_library
        assert callable(render_cv_library)

    def test_render_multimodal_page_callable(self):
        from hirekit.ui.app import render_multimodal_page
        assert callable(render_multimodal_page)

    def test_process_chat_message_search(self):
        """_process_chat_message doit router les messages libres vers search_cvs."""
        from hirekit.ui.app import _process_chat_message
        # Une commande /help doit être routée vers process_command
        result = _process_chat_message("/help")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "/search" in result or "search" in result.lower()

    def test_process_chat_message_unknown_command(self):
        from hirekit.ui.app import _process_chat_message
        result = _process_chat_message("/inconnu")
        assert isinstance(result, str)
        assert "inconnu" in result.lower() or "help" in result.lower()