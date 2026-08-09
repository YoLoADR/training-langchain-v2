"""Tests pour hirekit.llm.prompts — AT01."""

import pytest


class TestSystemPrompt:
    """AT01 — le system prompt recruteur doit être défini."""

    def test_system_prompt_recruiter_exists(self):
        from hirekit.llm.prompts import SYSTEM_PROMPT_RECRUITER

        assert isinstance(SYSTEM_PROMPT_RECRUITER, str)
        assert len(SYSTEM_PROMPT_RECRUITER) > 50


class TestGetCVExtractionPrompt:
    """AT01 — get_cv_extraction_prompt() doit retourner un PromptTemplate."""

    @pytest.mark.xfail(reason="AT01 non implémenté sur cette branche")
    def test_get_cv_extraction_prompt(self):
        from hirekit.llm.prompts import get_cv_extraction_prompt

        prompt = get_cv_extraction_prompt()
        assert prompt is not None
        assert hasattr(prompt, "format")


class TestFewShotExampleSelector:
    """AT01 (Bonus) — ExampleSelector dynamique."""

    @pytest.mark.xfail(reason="AT01 Bonus non implémenté sur cette branche")
    def test_get_few_shot_example_selector(self):
        from hirekit.llm.prompts import get_few_shot_example_selector

        selector = get_few_shot_example_selector()
        assert selector is not None
