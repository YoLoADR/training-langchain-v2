"""Code Reviewer — indexation et Q&A sur un repo de code.

AT05 — Compréhension du code : indexation et assistant d'aide au développement.

Ce module indexe un repo Python (data/code_repo/) comme corpus RAG
pour répondre à des questions comme :
- "Où est gérée l'authentification ?"
- "Que fait la fonction X ?"
- "Quels sont les modèles de la base de données ?"

Utilise GenericLoader + LanguageParser pour parser les fichiers .py,
RecursiveCharacterTextSplitter pour le chunking, et FAISS pour l'index.
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def load_python_files(repo_path: str) -> list[Document]:
    """AT05 — charge les fichiers Python d'un repo avec GenericLoader.

    Utilise GenericLoader avec LanguageParser pour parser les fichiers .py
    en préservant la structure du code (classes, fonctions, imports).

    Args:
        repo_path: chemin vers le dossier contenant les fichiers .py.

    Returns:
        Liste de Document (un par fichier Python, avec métadonnées de source).
    """
    from langchain_community.document_loaders.generic import GenericLoader
    from langchain_community.document_loaders.parsers.language.language_parser import LanguageParser

    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*.py",
        parser=LanguageParser(parser_threshold=50),
    )

    documents = loader.load()

    # Enrichir les métadonnées
    for doc in documents:
        source = doc.metadata.get("source", "")
        filename = Path(source).name if source else "unknown"
        doc.metadata["filename"] = filename
        doc.metadata["type"] = "code"

    return documents


def chunk_code_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    """AT05 — chunk les documents de code avec RecursiveCharacterTextSplitter.

    Le chunking du code doit préserver les blocs logiques (fonctions, classes).
    On utilise RecursiveCharacterTextSplitter avec des séparateurs adaptés au code.

    Args:
        documents: documents de code chargés via load_python_files().
        chunk_size: taille maximum (défaut: 500, adapté au code).
        chunk_overlap: chevauchement (défaut: 50).

    Returns:
        Liste de Documents chunkés.
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Séparateurs adaptés au code Python : class, def, puis \n\n, \n, espace
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def index_code_repo(repo_path: str) -> BaseRetriever:
    """AT05 — indexe un repo Python comme corpus RAG pour le Q&A sur le code.

    Pipeline complet :
    1. Charge les fichiers .py avec GenericLoader + LanguageParser
    2. Chunk le code avec RecursiveCharacterTextSplitter (séparateurs adaptés)
    3. Construit un index FAISS
    4. Retourne un retriever pour la recherche

    Args:
        repo_path: chemin vers le dossier du repo Python.

    Returns:
        BaseRetriever configuré pour chercher dans le code.
    """
    from hirekit.rag.vectorstore_faiss import get_default_embeddings

    # 1. Charger les fichiers Python
    documents = load_python_files(repo_path)

    if not documents:
        # Si pas de fichiers .py, créer un document placeholder
        documents = [
            Document(
                page_content="Aucun fichier Python trouvé dans le repo.",
                metadata={"source": "placeholder", "type": "code", "filename": "empty"},
            )
        ]

    # 2. Chunker le code
    chunks = chunk_code_documents(documents)

    # 3. Construire l'index FAISS
    from langchain_community.vectorstores import FAISS

    embeddings = get_default_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 4. Retourner le retriever
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10},
    )


def ask_code_question(question: str, retriever: BaseRetriever) -> str:
    """AT05 — pose une question sur le code indexé et retourne une réponse sourcée.

    Récupère les chunks de code pertinents via le retriever, puis construit
    une réponse contextuelle. Sans LLM (pour les tests), retourne les
    extraits de code trouvés avec leurs sources.

    Args:
        question: question sur le code (ex: "Où est gérée l'authentification ?").
        retriever: retriever construit via index_code_repo().

    Returns:
        Réponse sourcée avec les extraits de code pertinents.
    """
    # Récupérer les chunks de code pertinents
    docs = retriever.invoke(question)

    if not docs:
        return "Aucun code pertinent trouvé pour cette question."

    # Construire la réponse avec les sources
    parts = [f"Question: {question}\n"]
    parts.append(f"Code pertinent trouvé ({len(docs)} extraits):\n")

    for i, doc in enumerate(docs, 1):
        filename = doc.metadata.get("filename", "unknown")
        content = doc.page_content[:300].strip()
        parts.append(f"\n--- Extrait {i} [{filename}] ---\n{content}\n")

    return "\n".join(parts)


def ask_code_question_with_llm(
    question: str,
    retriever: BaseRetriever,
    llm=None,
) -> str:
    """AT05 — pose une question sur le code avec un LLM pour une réponse naturelle.

    Version étendue qui utilise un LLM pour générer une réponse en langage
    naturel basée sur le code récupéré.

    Args:
        question: question sur le code.
        retriever: retriever du code indexé.
        llm: chat model (défaut: get_chat_model()).

    Returns:
        Réponse en langage naturel sourcée.
    """
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    if llm is None:
        from hirekit.llm.provider import get_chat_model
        llm = get_chat_model(temperature=0.1)

    code_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es un assistant de code. Réponds à la question en te basant sur "
         "le code fourni. Cite le fichier et la fonction concernée."),
        ("human",
         "Code:\n{context}\n\nQuestion: {question}\n\nRéponse:"),
    ])

    def format_code(docs):
        return "\n\n".join(
            f"[{doc.metadata.get('filename', '?')}] {doc.page_content}"
            for doc in docs
        )

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_code(retriever.invoke(x["question"]))
        )
        | code_prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"question": question})


def get_code_summary(repo_path: str) -> dict:
    """AT05 — génère un résumé structuré du repo Python.

    Analyse les fichiers .py et retourne un dictionnaire avec :
    - nombre de fichiers
    - liste des fichiers
    - classes et fonctions détectées par fichier

    Args:
        repo_path: chemin vers le repo Python.

    Returns:
        Dictionnaire avec le résumé du repo.
    """
    import ast

    repo = Path(repo_path)
    py_files = sorted(repo.glob("*.py"))

    summary = {
        "total_files": len(py_files),
        "files": [],
    }

    for py_file in py_files:
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            summary["files"].append({
                "filename": py_file.name,
                "classes": classes,
                "functions": functions,
                "num_classes": len(classes),
                "num_functions": len(functions),
            })
        except SyntaxError:
            summary["files"].append({
                "filename": py_file.name,
                "classes": [],
                "functions": [],
                "error": "Syntax error",
            })

    return summary