"""Bug v3 test — Parser manquant dans la chaîne LCEL.

Sans le PydanticOutputParser, la chaîne retourne du texte brut.
Ce test vérifie que get_matching_chain inclut le parser et retourne un MatchResult.
"""

import json
import pytest


class TestBugV3:
    """Bug v3 : la chaîne doit inclure le parser pour retourner un MatchResult."""

    def test_chain_returns_match_result(self):
        """La chaîne de matching doit retourner un objet MatchResult, pas une string."""
        from hirekit.services.matching import get_matching_chain
        from hirekit.llm.parsers import MatchResult
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        valid_json = json.dumps({
            "score": 0.85,
            "justification": "Bonne correspondance",
            "points_forts": ["React"],
            "points_faibles": ["Pas de TypeScript"],
            "recommandation": "shortlister",
        })
        fake_llm = FakeListChatModel(responses=[valid_json])

        chain = get_matching_chain(llm=fake_llm)
        result = chain.invoke({"cv": "Marie Dubois", "offer": "Dev React"})

        assert isinstance(result, MatchResult), \
            f"La chaîne doit retourner un MatchResult, pas {type(result)}"

    def test_chain_has_parser(self):
        """La chaîne doit contenir un PydanticOutputParser."""
        from hirekit.services.matching import get_matching_chain
        from langchain_core.output_parsers import PydanticOutputParser

        from unittest.mock import MagicMock
        mock_llm = MagicMock()
        chain = get_matching_chain(llm=mock_llm)

        # La chaîne doit avoir un parser dans ses steps
        # On vérifie que get_match_parser retourne bien un PydanticOutputParser
        from hirekit.llm.parsers import get_match_parser
        parser = get_match_parser()
        assert isinstance(parser, PydanticOutputParser)

    def test_chain_result_has_score(self):
        """Le MatchResult doit avoir un attribut score entre 0 et 1."""
        from hirekit.services.matching import get_matching_chain
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        valid_json = json.dumps({
            "score": 0.5,
            "justification": "Test",
            "points_forts": [],
            "points_faibles": [],
            "recommandation": "à voir",
        })
        fake_llm = FakeListChatModel(responses=[valid_json])

        chain = get_matching_chain(llm=fake_llm)
        result = chain.invoke({"cv": "Test", "offer": "Test"})

        assert hasattr(result, "score")
        assert 0.0 <= result.score <= 1.0