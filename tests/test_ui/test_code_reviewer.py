"""Tests pour hirekit.ui.code_reviewer — AT05."""

import pytest
from pathlib import Path


class TestLoadPythonFiles:
    """AT05 — load_python_files() charge les fichiers .py."""

    def test_load_python_files(self, project_root: Path):
        from hirekit.ui.code_reviewer import load_python_files

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        docs = load_python_files(str(code_dir))
        assert len(docs) > 0
        assert all(hasattr(d, "page_content") for d in docs)
        assert all(d.metadata.get("type") == "code" for d in docs)

    def test_load_python_files_filenames(self, project_root: Path):
        from hirekit.ui.code_reviewer import load_python_files

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        docs = load_python_files(str(code_dir))
        filenames = {d.metadata.get("filename") for d in docs}
        assert "auth.py" in filenames or "main.py" in filenames

    def test_load_python_files_empty_dir(self, tmp_path: Path):
        from hirekit.ui.code_reviewer import load_python_files

        docs = load_python_files(str(tmp_path))
        assert len(docs) == 0


class TestChunkCodeDocuments:
    """AT05 — chunk_code_documents() avec séparateurs adaptés au code."""

    def test_chunk_code_documents(self):
        from hirekit.ui.code_reviewer import chunk_code_documents
        from langchain_core.documents import Document

        code = "def hello():\n    return 'world'\n\nclass Test:\n    pass\n"
        doc = Document(page_content=code, metadata={"source": "test.py", "type": "code"})
        chunks = chunk_code_documents([doc], chunk_size=100, chunk_overlap=10)
        assert len(chunks) >= 1

    def test_chunk_code_preserves_metadata(self):
        from hirekit.ui.code_reviewer import chunk_code_documents
        from langchain_core.documents import Document

        code = "x = 1\n" * 100
        doc = Document(page_content=code, metadata={"source": "test.py", "filename": "test.py", "type": "code"})
        chunks = chunk_code_documents([doc], chunk_size=200, chunk_overlap=20)
        for chunk in chunks:
            assert chunk.metadata.get("type") == "code"


class TestIndexCodeRepo:
    """AT05 — index_code_repo() indexe un repo Python."""

    def test_index_code_repo(self, project_root: Path):
        from hirekit.ui.code_reviewer import index_code_repo
        from langchain_core.retrievers import BaseRetriever

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        retriever = index_code_repo(str(code_dir))
        assert retriever is not None
        assert hasattr(retriever, "invoke")

    def test_index_code_repo_returns_retriever(self, project_root: Path):
        from hirekit.ui.code_reviewer import index_code_repo
        from langchain_core.retrievers import BaseRetriever

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        retriever = index_code_repo(str(code_dir))
        assert isinstance(retriever, BaseRetriever)


class TestAskCodeQuestion:
    """AT05 — ask_code_question() répond avec des extraits de code."""

    def test_ask_code_question(self, project_root: Path):
        from hirekit.ui.code_reviewer import index_code_repo, ask_code_question

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        retriever = index_code_repo(str(code_dir))
        result = ask_code_question("Où est gérée l'authentification ?", retriever)
        assert isinstance(result, str)
        assert len(result) > 0
        # Doit contenir un extrait de code ou un nom de fichier
        assert ".py" in result or "Extrait" in result

    def test_ask_code_question_returns_sources(self, project_root: Path):
        from hirekit.ui.code_reviewer import index_code_repo, ask_code_question

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        retriever = index_code_repo(str(code_dir))
        result = ask_code_question("Que fait la fonction hash_password ?", retriever)
        assert "Question" in result


class TestGetCodeSummary:
    """AT05 — get_code_summary() génère un résumé du repo."""

    def test_get_code_summary(self, project_root: Path):
        from hirekit.ui.code_reviewer import get_code_summary

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        summary = get_code_summary(str(code_dir))
        assert isinstance(summary, dict)
        assert "total_files" in summary
        assert summary["total_files"] == 10
        assert "files" in summary
        assert len(summary["files"]) == 10

    def test_get_code_summary_has_classes_and_functions(self, project_root: Path):
        from hirekit.ui.code_reviewer import get_code_summary

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        summary = get_code_summary(str(code_dir))
        # Au moins un fichier doit avoir des classes ou des fonctions
        has_code = any(
            f["num_classes"] > 0 or f["num_functions"] > 0
            for f in summary["files"]
        )
        assert has_code, "Le repo doit contenir des classes ou des fonctions"

    def test_get_code_summary_auth_file(self, project_root: Path):
        from hirekit.ui.code_reviewer import get_code_summary

        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        summary = get_code_summary(str(code_dir))
        auth_file = next((f for f in summary["files"] if f["filename"] == "auth.py"), None)
        assert auth_file is not None
        assert "hash_password" in auth_file["functions"] or len(auth_file["functions"]) > 0