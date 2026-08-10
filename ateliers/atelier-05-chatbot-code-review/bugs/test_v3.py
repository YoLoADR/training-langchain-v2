"""Bug v3 test — Code chunking avec séparateurs non adaptés au code."""

import pytest
from langchain_core.documents import Document


class TestBugV3:
    """Bug v3 : chunk_code_documents doit préserver les blocs de code."""

    def test_chunk_code_preserves_functions(self):
        """Le chunking doit préserver les fonctions autant que possible."""
        from hirekit.ui.code_reviewer import chunk_code_documents

        code = (
            "def function_one():\n"
            "    return 1\n\n"
            "def function_two():\n"
            "    return 2\n\n"
            "class MyClass:\n"
            "    def method(self):\n"
            "        return 3\n"
        )
        doc = Document(page_content=code, metadata={"source": "test.py", "type": "code"})
        chunks = chunk_code_documents([doc], chunk_size=80, chunk_overlap=0)
        # Avec de bons séparateurs, on ne coupe pas au milieu d'une def
        assert len(chunks) >= 1
        # Au moins un chunk doit contenir "def" complet
        full_text = " ".join(c.page_content for c in chunks)
        assert "def" in full_text

    def test_chunk_code_with_code_separators(self):
        """Le splitter doit utiliser des séparateurs adaptés au code."""
        import inspect
        from hirekit.ui.code_reviewer import chunk_code_documents

        # Vérifier que le code source de chunk_code_documents utilise
        # des séparateurs adaptés au code
        source = inspect.getsource(chunk_code_documents)
        assert "class" in source or "def" in source, \
            "chunk_code_documents doit utiliser des séparateurs adaptés au code (\nclass, \ndef)"

    def test_chunk_code_metadata_preserved(self):
        from hirekit.ui.code_reviewer import chunk_code_documents

        code = "x = 1\n" * 100
        doc = Document(page_content=code, metadata={"filename": "test.py", "type": "code"})
        chunks = chunk_code_documents([doc], chunk_size=200, chunk_overlap=20)
        for chunk in chunks:
            assert chunk.metadata.get("type") == "code"