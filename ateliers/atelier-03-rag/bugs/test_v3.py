"""Bug v3 test — Index FAISS non chargé avant la recherche.

search_cvs() doit gérer le cas où l'index FAISS n'existe pas encore.
Ce test vérifie que l'erreur est claire ou que l'index est construit.
"""

import pytest
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings


class TestBugV3:
    """Bug v3 : search_cvs doit gérer l'absence d'index FAISS."""

    def test_search_cvs_with_explicit_store(self, tmp_path: Path):
        """search_cvs fonctionne si on passe un vectorstore explicite."""
        from hirekit.rag.vectorstore_faiss import build_faiss_index, search_cvs

        embeddings = FakeEmbeddings(size=384)
        docs = [
            Document(
                page_content=f"Candidat {i}: React {i} ans",
                metadata={"source": f"cv_{i:03d}.pdf", "filename": f"cv_{i:03d}"},
            )
            for i in range(3)
        ]
        store = build_faiss_index(
            docs, embeddings=embeddings, force_rebuild=True, save_dir=tmp_path
        )
        results = search_cvs("React", vectorstore=store, k=2)
        assert len(results) == 2

    def test_search_cvs_without_index_raises(self, tmp_path: Path):
        """search_cvs sans index doit lever une erreur claire."""
        from hirekit.rag.vectorstore_faiss import search_cvs
        from hirekit.config import FAISS_INDEX_DIR

        # Tenter de charger un index inexistant
        with pytest.raises(FileNotFoundError, match="non trouvé"):
            search_cvs("test", k=2)  # Pas de vectorstore, charge depuis le disque

    def test_load_faiss_index_raises_on_missing(self, tmp_path: Path):
        """load_faiss_index doit lever FileNotFoundError si l'index n'existe pas."""
        from hirekit.rag.vectorstore_faiss import load_faiss_index

        embeddings = FakeEmbeddings(size=384)
        with pytest.raises(FileNotFoundError, match="non trouvé"):
            load_faiss_index(embeddings, tmp_path / "nonexistent_index")