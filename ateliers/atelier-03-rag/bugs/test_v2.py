"""Bug v2 test — Retriever avec k=0 (aucun résultat).

Le retriever doit retourner au moins 1 document pour que le RAG fonctionne.
Ce test vérifie que get_cv_retriever retourne bien des documents avec k>0.
"""

import pytest
from pathlib import Path
from unittest.mock import patch
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings


class TestBugV2:
    """Bug v2 : le retriever doit retourner k > 0 documents."""

    def test_retriever_returns_documents(self, tmp_path: Path):
        """Le retriever doit retourner au moins 1 document."""
        from hirekit.rag.retriever import get_cv_retriever
        from hirekit.rag.vectorstore_faiss import build_faiss_index, load_faiss_index
        import hirekit.rag.vectorstore_faiss as vs_faiss

        embeddings = FakeEmbeddings(size=384)
        docs = [
            Document(
                page_content=f"Candidat {i}: React {i} ans, Python {i+1} ans",
                metadata={"source": f"cv_{i:03d}.pdf", "type": "cv", "filename": f"cv_{i:03d}"},
            )
            for i in range(5)
        ]
        build_faiss_index(docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path)

        original_load = vs_faiss.load_faiss_index

        def mock_load(emb=None, load_dir=None):
            return original_load(emb or embeddings, load_dir or tmp_path)

        with patch.object(vs_faiss, "load_faiss_index", mock_load):
            retriever = get_cv_retriever(search_type="similarity", k=4)
            results = retriever.invoke("React Python")
            assert len(results) > 0, "Le retriever doit retourner au moins 1 document"

    def test_retriever_k_is_positive(self, tmp_path: Path):
        """k doit être > 0."""
        from hirekit.rag.retriever import get_cv_retriever
        from hirekit.rag.vectorstore_faiss import build_faiss_index, load_faiss_index
        import hirekit.rag.vectorstore_faiss as vs_faiss

        embeddings = FakeEmbeddings(size=384)
        docs = [Document(page_content="test", metadata={"source": "test"})]
        build_faiss_index(docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path)

        original_load = vs_faiss.load_faiss_index

        def mock_load(emb=None, load_dir=None):
            return original_load(emb or embeddings, load_dir or tmp_path)

        with patch.object(vs_faiss, "load_faiss_index", mock_load):
            retriever = get_cv_retriever(search_type="similarity", k=4)
            results = retriever.invoke("test")
            assert len(results) <= 4  # k=4 maximum
            assert len(results) > 0  # k > 0