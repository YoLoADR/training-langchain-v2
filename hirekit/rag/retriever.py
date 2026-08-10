"""Retriever — récupération optimisée pour limiter les hallucinations.

AT03 — Le Retriever : optimiser la récupération pour limiter les hallucinations.
AT04 — EnsembleRetriever FAISS + ChromaDB.

Le retriever MMR (Maximal Marginal Relevance) équilibre pertinence
et diversité des résultats, ce qui réduit les doublons et améliore
la couverture du contexte pour le LLM.
"""

from __future__ import annotations

from langchain_core.retrievers import BaseRetriever


def get_cv_retriever(
    search_type: str = "mmr",
    k: int = 4,
    fetch_k: int = 20,
    lambda_mult: float = 0.5,
) -> BaseRetriever:
    """AT03 — retourne le retriever FAISS pour les CVs.

    Args:
        search_type: "mmr" (Maximal Marginal Relevance, recommandé) ou
                     "similarity" (cosinus simple).
        k: nombre de documents à récupérer (défaut: 4).
        fetch_k: nombre de documents à considérer avant le MMR (défaut: 20).
        lambda_mult: équilibre pertinence/diversité pour MMR
                     (0 = max diversité, 1 = max pertinence, défaut: 0.5).

    Returns:
        BaseRetriever configuré pour chercher dans les CVs.
    """
    from hirekit.rag.vectorstore_faiss import load_faiss_index

    vectorstore = load_faiss_index()

    if search_type == "mmr":
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
        )
    elif search_type == "similarity":
        return vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
    else:
        raise ValueError(
            f"search_type non supporté: '{search_type}'. "
            f"Choisissez: 'mmr' ou 'similarity'."
        )


def get_offer_retriever(
    search_type: str = "mmr",
    k: int = 4,
    fetch_k: int = 20,
) -> BaseRetriever:
    """AT03 — retourne le retriever ChromaDB pour les offres.

    Args:
        search_type: "mmr" ou "similarity".
        k: nombre de documents à récupérer (défaut: 4).
        fetch_k: nombre de documents pour MMR (défaut: 20).

    Returns:
        BaseRetriever configuré pour chercher dans les offres.
    """
    from hirekit.rag.vectorstore_chroma import load_chroma_index

    vectorstore = load_chroma_index()

    if search_type == "mmr":
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": fetch_k},
        )
    elif search_type == "similarity":
        return vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
    else:
        raise ValueError(
            f"search_type non supporté: '{search_type}'. "
            f"Choisissez: 'mmr' ou 'similarity'."
        )


def get_ensemble_retriever(
    faiss_k: int = 8,
    chroma_k: int = 8,
    weights: list[float] | None = None,
) -> BaseRetriever:
    """AT04 — retourne l'EnsembleRetriever FAISS + ChromaDB.

    Combine les résultats du retriever FAISS (CVs) et ChromaDB (offres)
    pour une recherche croisée. Les weights contrôlent l'importance
    de chaque retriever (défaut: [0.5, 0.5] = équilibré).

    Args:
        faiss_k: nombre de résultats depuis FAISS (défaut: 8).
        chroma_k: nombre de résultats depuis ChromaDB (défaut: 8).
        weights: poids de chaque retriever (défaut: [0.5, 0.5]).

    Returns:
        EnsembleRetriever combinant FAISS et ChromaDB.
    """
    from langchain.retrievers import EnsembleRetriever

    cv_retriever = get_cv_retriever(search_type="similarity", k=faiss_k)
    offer_retriever = get_offer_retriever(search_type="similarity", k=chroma_k)

    if weights is None:
        weights = [0.5, 0.5]

    return EnsembleRetriever(
        retrievers=[cv_retriever, offer_retriever],
        weights=weights,
    )


def build_rag_chain(
    retriever: BaseRetriever | None = None,
    llm=None,
) -> "Runnable":
    """AT03 — construit la chaîne RAG (Retriever + LLM) pour le Q&A sourcé.

    Chaîne LCEL :
        RunnablePassthrough.assign(context=retriever)
        | prompt (context + question)
        | llm
        | StrOutputParser

    Args:
        retriever: retriever à utiliser (défaut: get_cv_retriever()).
        llm: chat model (défaut: get_chat_model()).

    Returns:
        Chaîne LCEL RAG prête pour .invoke().
    """
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    if retriever is None:
        retriever = get_cv_retriever()
    if llm is None:
        from hirekit.llm.provider import get_chat_model

        llm = get_chat_model(temperature=0.1)

    rag_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es un assistant recruteur. Réponds à la question en te basant "
         "UNIQUEMENT sur le contexte fourni. Si la réponse n'est pas dans le "
         "contexte, dis 'Je n'ai pas cette information dans les CVs disponibles.' "
         "Cite toujours le candidat ou l'offre source."),
        ("human",
         "Contexte:\n{context}\n\nQuestion: {question}\n\nRéponse sourcée:"),
    ])

    def format_docs(docs):
        return "\n\n".join(
            f"[{doc.metadata.get('filename', doc.metadata.get('id', 'source'))}] {doc.page_content}"
            for doc in docs
        )

    rag_chain = (
        RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["question"])))
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain