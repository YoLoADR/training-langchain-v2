"""Tests pour hirekit.llm.parsers — AT01."""

import pytest


class TestCVInfo:
    """AT01 — le modèle Pydantic CVInfo doit être correctement défini."""

    def test_cv_info_has_required_fields(self):
        from hirekit.llm.parsers import CVInfo

        cv = CVInfo(
            nom="Marie Dubois",
            email="marie.dubois@email.fr",
            competences=[],
            experiences=[],
        )
        assert cv.nom == "Marie Dubois"
        assert cv.email == "marie.dubois@email.fr"

    def test_cv_info_telephone_optional(self):
        from hirekit.llm.parsers import CVInfo

        cv = CVInfo(nom="Test", email="test@test.fr", competences=[], experiences=[])
        assert cv.telephone is None  # optionnel


class TestGetCVParser:
    """AT01 — get_cv_parser() doit retourner un PydanticOutputParser."""

    def test_get_cv_parser_returns_parser(self):
        from hirekit.llm.parsers import get_cv_parser

        parser = get_cv_parser()
        assert parser is not None

    def test_cv_parser_has_format_instructions(self):
        from hirekit.llm.parsers import get_cv_parser

        parser = get_cv_parser()
        instructions = parser.get_format_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0


class TestGetMatchParser:
    """AT02 — get_match_parser() doit retourner un PydanticOutputParser pour MatchResult."""

    def test_get_match_parser_returns_parser(self):
        from hirekit.llm.parsers import get_match_parser

        parser = get_match_parser()
        assert parser is not None

    def test_match_parser_has_format_instructions(self):
        from hirekit.llm.parsers import get_match_parser

        parser = get_match_parser()
        instructions = parser.get_format_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0


class TestGetSkillsListParser:
    """AT01 — get_skills_list_parser() doit retourner un CommaSeparatedListOutputParser."""

    def test_get_skills_list_parser_returns_parser(self):
        from hirekit.llm.parsers import get_skills_list_parser

        parser = get_skills_list_parser()
        assert parser is not None


class TestMatchResult:
    """AT02 — le modèle Pydantic MatchResult."""

    def test_match_result_has_score_and_justification(self):
        from hirekit.llm.parsers import MatchResult

        result = MatchResult(
            score=0.85,
            justification="Bonne correspondance sur React",
            points_forts=["React 4 ans"],
            points_faibles=["Pas de TypeScript"],
            recommandation="shortlister",
        )
        assert 0.0 <= result.score <= 1.0
        assert len(result.justification) > 0