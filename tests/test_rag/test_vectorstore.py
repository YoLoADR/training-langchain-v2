"""Tests pour hirekit.rag.vectorstore_faiss et chroma — AT03."""

import pytest
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings


def make_docs(count: int = 5) -> list[Document]:
    """Crée des Documents de test."""
    return [
        Document(
            page_content=f"Candidat {i}: React {i} ans, Python {i+1} ans",
            metadata={"source": f"cv_{i:03d}.pdf", "type": "cv", "filename": f"cv_{i:03d}"},
        )
        for i in range(count)
    ]


class TestBuildFaissIndex:
    """AT03 — build_faiss_index() construit un index FAISS."""

    def test_build_faiss_index_with_fake_embeddings(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(5)
        store = build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        assert store is not None
        assert hasattr(store, "similarity_search")

    def test_build_faiss_index_search(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(5)
        store = build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        results = store.similarity_search("React Python", k=3)
        assert len(results) == 3

    def test_build_faiss_index_empty_list(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index

        embeddings = FakeEmbeddings(size=384)
        store = build_faiss_index(
            [], embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        assert store is not None

    def test_build_faiss_index_saves_to_disk(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(3)
        build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        # FAISS crée un fichier index
        assert tmp_path.exists()


class TestLoadFaissIndex:
    """AT03 — load_faiss_index() recharge un index FAISS."""

    def test_load_faiss_index(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index, load_faiss_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(3)
        build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        loaded = load_faiss_index(embeddings, tmp_path)
        assert loaded is not None
        assert hasattr(loaded, "similarity_search")

    def test_load_faiss_index_not_found(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import load_faiss_index

        embeddings = FakeEmbeddings(size=384)
        with pytest.raises(FileNotFoundError, match="non trouvé"):
            load_faiss_index(embeddings, tmp_path / "nonexistent")


class TestBuildChromaIndex:
    """AT03 — build_chroma_index() construit un index ChromaDB."""

    def test_build_chroma_index_with_fake_embeddings(self, tmp_path: Path):
        from hirekit.rag.vectorstore_chroma import build_chroma_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(5)
        store = build_chroma_index(
            docs, embeddings=embeddings, persist_directory=tmp_path
        )
        assert store is not None
        assert hasattr(store, "similarity_search")

    def test_build_chroma_index_search(self, tmp_path: Path):
        from hirekit.rag.vectorstore_chroma import build_chroma_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(5)
        store = build_chroma_index(
            docs, embeddings=embeddings, persist_directory=tmp_path
        )
        results = store.similarity_search("React", k=3)
        assert len(results) == 3

    def test_load_chroma_index(self, tmp_path: Path):
        from hirekit.rag.vectorstore_chroma import build_chroma_index, load_chroma_index

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(3)
        build_chroma_index(
            docs, embeddings=embeddings, persist_directory=tmp_path
        )
        loaded = load_chroma_index(embeddings, persist_directory=tmp_path)
        assert loaded is not None


class TestSearchCvs:
    """AT03 — search_cvs() recherche dans les CVs."""

    def test_search_cvs(self, tmp_path: Path):
        from hirekit.rag.vectorstore_faiss import build_faiss_index, search_cvs

        embeddings = FakeEmbeddings(size=384)
        docs = make_docs(5)
        store = build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        results = search_cvs("React Python", vectorstore=store, k=3)
        assert len(results) == 3