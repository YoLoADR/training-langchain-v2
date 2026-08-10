"""Text Splitters — stratégies de chunking pour les CVs et offres.

AT03 — Text Splitters : RecursiveCharacterTextSplitter (recommandé),
CharacterTextSplitter (taille fixe).

Le chunking récursif préserve la structure sémantique en découpant
d'abord sur les séparateurs de paragraphes, puis de phrases, puis de mots.
"""

from __future__ import annotations

from langchain_core.documents import Document


def chunk_fixed_size(
    documents: list[Document], chunk_size: int = 512, chunk_overlap: int = 50
) -> list[Document]:
    """AT03 — chunking à taille fixe avec CharacterTextSplitter.

    Découpe le texte à intervalles réguliers (chunk_size caractères) avec
    un chevauchement (chunk_overlap) pour préserver le contexte entre chunks.

    Moins intelligent que le chunking récursif mais utile pour la comparaison.

    Args:
        documents: liste de Documents à chunker.
        chunk_size: taille maximum de chaque chunk en caractères (défaut: 512).
        chunk_overlap: chevauchement entre chunks en caractères (défaut: 50).

    Returns:
        Liste de Documents chunkés (les métadonnées sont préservées).
    """
    from langchain_text_splitters import CharacterTextSplitter

    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n",
    )
    return splitter.split_documents(documents)


def chunk_recursive(
    documents: list[Document], chunk_size: int = 512, chunk_overlap: int = 50
) -> list[Document]:
    """AT03 — chunking récursif avec RecursiveCharacterTextSplitter (recommandé).

    Le splitter récursif essaie d'abord de découper sur "\n\n" (paragraphes),
    puis "\n" (lignes), puis " " (mots), puis "" (caractères). Cela préserve
    la structure sémantique du document.

    C'est la stratégie recommandée par LangChain pour la plupart des use cases.

    Args:
        documents: liste de Documents à chunker.
        chunk_size: taille maximum de chaque chunk en caractères (défaut: 512).
        chunk_overlap: chevauchement entre chunks en caractères (défaut: 50).

    Returns:
        Liste de Documents chunkés (métadonnées préservées).
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def chunk_cvs(documents: list[Document], chunk_size: int = 400, chunk_overlap: int = 50) -> list[Document]:
    """AT03 — chunking optimisé pour les CVs (chunks plus petits).

    Les CVs sont courts (1-2 pages) : on utilise des chunks de 400 caractères
    pour capturer des sections cohérentes (compétences, expériences).

    Args:
        documents: CVs chargés via load_all_cvs().
        chunk_size: taille maximum (défaut: 400 pour les CVs).
        chunk_overlap: chevauchement (défaut: 50).

    Returns:
        Liste de Documents chunkés.
    """
    return chunk_recursive(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)


def chunk_offers(documents: list[Document], chunk_size: int = 600, chunk_overlap: int = 100) -> list[Document]:
    """AT03 — chunking optimisé pour les offres (chunks plus grands).

    Les offres sont structurées : on garde des chunks plus larges (600 chars)
    pour préserver le contexte complet de l'offre (titre + compétences + description).

    Args:
        documents: offres chargées via load_all_offers().
        chunk_size: taille maximum (défaut: 600 pour les offres).
        chunk_overlap: chevauchement (défaut: 100).

    Returns:
        Liste de Documents chunkés.
    """
    return chunk_recursive(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)


def compare_chunking_strategies(
    documents: list[Document], chunk_size: int = 512
) -> dict:
    """AT03 — compare les deux stratégies de chunking (pour le mini-lab).

    Retourne des statistiques comparatives : nombre de chunks, taille moyenne,
    taille min/max. Permet de visualiser pourquoi le chunking récursif est
    recommandé.

    Args:
        documents: documents à chunker.
        chunk_size: taille de chunk pour la comparaison.

    Returns:
        Dictionnaire avec les stats des deux stratégies.
    """
    fixed = chunk_fixed_size(documents, chunk_size=chunk_size, chunk_overlap=50)
    recursive = chunk_recursive(documents, chunk_size=chunk_size, chunk_overlap=50)

    def stats(chunks: list[Document]) -> dict:
        if not chunks:
            return {"count": 0, "avg_size": 0, "min_size": 0, "max_size": 0}
        sizes = [len(c.page_content) for c in chunks]
        return {
            "count": len(chunks),
            "avg_size": sum(sizes) / len(sizes),
            "min_size": min(sizes),
            "max_size": max(sizes),
        }

    return {
        "fixed_size": stats(fixed),
        "recursive": stats(recursive),
    }