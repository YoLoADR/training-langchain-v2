"""Vector Store FAISS — index des CVs.

AT03 — Vector Stores : FAISS pour indexer les CVs.

FAISS est optimisé pour la recherche de similarité en mémoire.
On l'utilise pour les CVs car la recherche est rapide et l'index
peut être sauvegardé/chargé depuis le disque.
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from hirekit.config import FAISS_INDEX_DIR


def get_default_embeddings() -> Embeddings:
    """AT03 — retourne les embeddings par défaut (FastEmbeddings ou Fake).

    En production : FastEmbedEmbeddings (multilingue, 384d, CPU).
    En test/CI (sans modèle téléchargé) : FakeEmbeddings (384d déterministe).
    """
    try:
        from langchain_community.embeddings import FastEmbedEmbeddings

        return FastEmbedEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    except Exception:
        from langchain_core.embeddings import FakeEmbeddings

        return FakeEmbeddings(size=384)


def build_faiss_index(
    chunks: list[Document],
    embeddings: Embeddings | None = None,
    force_rebuild: bool = True,
    save_dir: str | Path | None = None,
) -> "FAISS":
    """AT03 — construit (ou recharge) l'index FAISS pour les CVs.

    Args:
        chunks: Documents chunkés à indexer.
        embeddings: modèle d'embeddings (défaut: get_default_embeddings()).
        force_rebuild: si True, reconstruit l'index même s'il existe déjà.
        save_dir: dossier de sauvegarde (défaut: data/faiss_index).

    Returns:
        L'index FAISS prêt pour la recherche.
    """
    from langchain_community.vectorstores import FAISS

    if embeddings is None:
        embeddings = get_default_embeddings()

    save_path = Path(save_dir) if save_dir else FAISS_INDEX_DIR

    # Tentative de rechargement depuis le disque
    if not force_rebuild and save_path.exists():
        return load_faiss_index(embeddings, save_path)

    if not chunks:
        # FAISS nécessite au moins un document pour construire l'index
        chunks = [
            Document(
                page_content="Placeholder vide",
                metadata={"type": "placeholder"},
            )
        ]

    # Construire l'index FAISS
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Sauvegarder sur le disque
    vectorstore.save_local(str(save_path))

    return vectorstore


def load_faiss_index(
    embeddings: Embeddings | None = None,
    load_dir: str | Path | None = None,
) -> "FAISS":
    """AT03 — recharge un index FAISS existant depuis le disque.

    Args:
        embeddings: modèle d'embeddings (doit être le même qu'à la construction).
        load_dir: dossier de l'index (défaut: data/faiss_index).

    Returns:
        L'index FAISS chargé.
    """
    from langchain_community.vectorstores import FAISS

    if embeddings is None:
        embeddings = get_default_embeddings()

    load_path = Path(load_dir) if load_dir else FAISS_INDEX_DIR

    if not load_path.exists():
        raise FileNotFoundError(
            f"Index FAISS non trouvé dans {load_path}. "
            f"Lancez build_faiss_index() d'abord."
        )

    return FAISS.load_local(
        str(load_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def search_cvs(
    query: str,
    vectorstore: "FAISS | None" = None,
    k: int = 4,
) -> list[Document]:
    """AT03 — recherche de similarité dans les CVs via FAISS.

    Args:
        query: question/requête en langage naturel.
        vectorstore: index FAISS (défaut: load_faiss_index()).
        k: nombre de résultats à retourner.

    Returns:
        Liste de k Documents les plus similaires à la query.
    """
    if vectorstore is None:
        vectorstore = load_faiss_index()

    return vectorstore.similarity_search(query, k=k)