"""Tests pour hirekit.rag.retriever — AT03."""

import pytest
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings


class TestGetCVRetriever:
    """AT03 — get_cv_retriever() retourne un BaseRetriever."""

    def test_get_cv_retriever(self, tmp_path: Path):
        """Le retriever doit être un BaseRetriever avec .invoke()."""
        from hirekit.rag.retriever import get_cv_retriever
        from hirekit.rag.vectorstore_faiss import build_faiss_index
        from langchain_core.retrievers import BaseRetriever

        # Construire un index FAISS de test
        embeddings = FakeEmbeddings(size=384)
        docs = [
            Document(
                page_content=f"Candidat {i}: React {i} ans",
                metadata={"source": f"cv_{i:03d}.pdf", "type": "cv", "filename": f"cv_{i:03d}"},
            )
            for i in range(5)
        ]
        build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )

        # Monkey-patcher le FAISS_INDEX_DIR pour pointer vers tmp_path
        import hirekit.rag.vectorstore_faiss as vs_faiss
        original_load = vs_faiss.load_faiss_index

        def mock_load(emb=None, load_dir=None):
            return original_load(emb or embeddings, load_dir or tmp_path)

        import unittest.mock as mock
        with mock.patch.object(vs_faiss, "load_faiss_index", mock_load):
            retriever = get_cv_retriever(search_type="similarity", k=4)
            assert retriever is not None
            assert hasattr(retriever, "invoke")

    def test_get_cv_retriever_invalid_search_type(self, tmp_path: Path):
        from hirekit.rag.retriever import get_cv_retriever
        from hirekit.rag.vectorstore_faiss import build_faiss_index
        from langchain_core.embeddings import FakeEmbeddings

        embeddings = FakeEmbeddings(size=384)
        docs = [Document(page_content="test", metadata={"source": "test"})]
        build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )

        import hirekit.rag.vectorstore_faiss as vs_faiss
        original_load = vs_faiss.load_faiss_index

        def mock_load(emb=None, load_dir=None):
            return original_load(emb or embeddings, load_dir or tmp_path)

        import unittest.mock as mock
        with mock.patch.object(vs_faiss, "load_faiss_index", mock_load):
            with pytest.raises(ValueError, match="non supporté"):
                get_cv_retriever(search_type="invalid")


class TestBuildRagChain:
    """AT03 — build_rag_chain() construit la chaîne RAG."""

    def test_build_rag_chain_returns_runnable(self):
        from hirekit.rag.retriever import build_rag_chain
        from langchain_core.retrievers import BaseRetriever
        from unittest.mock import MagicMock

        mock_retriever = MagicMock(spec=BaseRetriever)
        mock_retriever.invoke.return_value = [
            Document(page_content="Marie Dubois a 4 ans en React", metadata={"filename": "cv_001"})
        ]

        from langchain_core.language_models.fake_chat_models import FakeListChatModel
        fake_llm = FakeListChatModel(responses=["Marie Dubois a 4 ans d'expérience en React."])

        chain = build_rag_chain(retriever=mock_retriever, llm=fake_llm)
        assert chain is not None
        assert hasattr(chain, "invoke")

    def test_build_rag_chain_invokes(self):
        from hirekit.rag.retriever import build_rag_chain
        from langchain_core.retrievers import BaseRetriever
        from unittest.mock import MagicMock

        mock_retriever = MagicMock(spec=BaseRetriever)
        mock_retriever.invoke.return_value = [
            Document(page_content="Marie Dubois a 4 ans en React", metadata={"filename": "cv_001"})
        ]

        from langchain_core.language_models.fake_chat_models import FakeListChatModel
        fake_llm = FakeListChatModel(responses=["Marie Dubois a 4 ans d'expérience en React."])

        chain = build_rag_chain(retriever=mock_retriever, llm=fake_llm)
        result = chain.invoke({"question": "Qui a de l'expérience en React ?"})
        assert isinstance(result, str)
        assert len(result) > 0