"""Vector Store ChromaDB — index des offres avec métadonnées.

AT03 — Vector Stores : ChromaDB pour indexer les offres avec filtres.

ChromaDB est optimisé pour les requêtes avec filtrage de métadonnées
(catégorie, localisation, etc.). On l'utilise pour les offres car
le recruteur veut souvent filtrer par localisation ou catégorie.
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from hirekit.config import CHROMA_DB_DIR


def build_chroma_index(
    chunks: list[Document],
    embeddings: Embeddings | None = None,
    collection_name: str = "offres",
    persist_directory: str | Path | None = None,
) -> "Chroma":
    """AT03 — construit l'index ChromaDB pour les offres.

    Args:
        chunks: Documents chunkés à indexer.
        embeddings: modèle d'embeddings (défaut: get_default_embeddings()).
        collection_name: nom de la collection ChromaDB (défaut: "offres").
        persist_directory: dossier de persistence (défaut: data/chroma_db).

    Returns:
        L'index ChromaDB prêt pour la recherche.
    """
    from langchain_community.vectorstores import Chroma

    if embeddings is None:
        from hirekit.rag.vectorstore_faiss import get_default_embeddings

        embeddings = get_default_embeddings()

    persist_path = str(persist_directory) if persist_directory else str(CHROMA_DB_DIR)

    if not chunks:
        chunks = [
            Document(
                page_content="Placeholder vide",
                metadata={"type": "placeholder"},
            )
        ]

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_path,
    )

    return vectorstore


def load_chroma_index(
    embeddings: Embeddings | None = None,
    collection_name: str = "offres",
    persist_directory: str | Path | None = None,
) -> "Chroma":
    """AT03 — recharge un index ChromaDB existant depuis le disque.

    Args:
        embeddings: modèle d'embeddings (doit être le même qu'à la construction).
        collection_name: nom de la collection (défaut: "offres").
        persist_directory: dossier de persistence (défaut: data/chroma_db).

    Returns:
        L'index ChromaDB chargé.
    """
    from langchain_community.vectorstores import Chroma

    if embeddings is None:
        from hirekit.rag.vectorstore_faiss import get_default_embeddings

        embeddings = get_default_embeddings()

    persist_path = str(persist_directory) if persist_directory else str(CHROMA_DB_DIR)

    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_path,
    )


def search_offers(
    query: str,
    vectorstore: "Chroma | None" = None,
    k: int = 4,
    filter: dict | None = None,
) -> list[Document]:
    """AT03 — recherche de similarité dans les offres via ChromaDB.

    Args:
        query: question/requête en langage naturel.
        vectorstore: index ChromaDB (défaut: load_chroma_index()).
        k: nombre de résultats à retourner.
        filter: filtre de métadonnées (ex: {"categorie": "frontend"}).

    Returns:
        Liste de k Documents les plus similaires à la query.
    """
    if vectorstore is None:
        vectorstore = load_chroma_index()

    if filter:
        return vectorstore.similarity_search(query, k=k, filter=filter)
    return vectorstore.similarity_search(query, k=k)