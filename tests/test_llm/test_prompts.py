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

    def test_get_cv_extraction_prompt(self):
        from hirekit.llm.prompts import get_cv_extraction_prompt

        prompt = get_cv_extraction_prompt()
        assert prompt is not None
        assert hasattr(prompt, "format")


class TestGetMatchingPrompt:
    """AT02 — get_matching_prompt() doit retourner un ChatPromptTemplate."""

    def test_get_matching_prompt(self):
        from hirekit.llm.prompts import get_matching_prompt

        prompt = get_matching_prompt()
        assert prompt is not None
        assert hasattr(prompt, "format")


class TestFewShotExampleSelector:
    """AT01 (Bonus) — ExampleSelector dynamique."""

    def test_get_few_shot_example_selector(self):
        from hirekit.llm.prompts import get_few_shot_example_selector

        selector = get_few_shot_example_selector()
        assert selector is not None