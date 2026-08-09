"""Bug v1 test — RunnableLambda n'extrait pas la bonne clé.

Le RunnableLambda doit extraire x["cv"] du dict, pas utiliser x directement.
Ce test vérifie que clean_cv_lambda fonctionne correctement avec un dict.
"""

import pytest


class TestBugV1:
    """Bug v1 : RunnableLambda doit extraire la bonne clé du dict."""

    def test_clean_cv_lambda_accepts_dict(self):
        """Le RunnableLambda doit accepter un dict et extraire cv."""
        from hirekit.services.matching import clean_cv_lambda

        result = clean_cv_lambda.invoke({"cv": "  Marie Dubois  "})
        assert "Marie Dubois" in result
        assert isinstance(result, str)

    def test_clean_cv_lambda_truncates(self):
        """Le RunnableLambda doit tronquer les CVs trop longs."""
        from hirekit.services.matching import clean_cv_lambda

        long_cv = "A" * 3000
        result = clean_cv_lambda.invoke({"cv": long_cv})
        assert len(result) <= 2003  # 2000 + "..."

    def test_clean_cv_function_expects_string(self):
        """La fonction clean_cv sous-jacente attend une string, pas un dict."""
        from hirekit.services.matching import clean_cv

        result = clean_cv("  test  ")
        assert result == "test"

        # Un dict doit lever une AttributeError
        with pytest.raises(AttributeError):
            clean_cv({"cv": "test"})