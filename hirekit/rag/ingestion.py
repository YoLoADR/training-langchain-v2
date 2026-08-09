"""Document Loaders — chargement des CVs, offres et skills.

AT03 — Document Loaders : PyMuPDFLoader, JSONLoader, CSVLoader.
"""

from __future__ import annotations

from langchain_core.documents import Document


def load_cv_pdf(path: str) -> list[Document]:
    """AT03 — charge un CV PDF avec métadonnées (source, page)."""
    raise NotImplementedError("AT03 — implémentez load_cv_pdf() dans hirekit/rag/ingestion.py")


def load_offers_json(path: str) -> list[Document]:
    """AT03 — charge les offres d'emploi depuis un JSON."""
    raise NotImplementedError("AT03 — implémentez load_offers_json() dans hirekit/rag/ingestion.py")


def load_skills_csv(path: str) -> list[Document]:
    """AT03 — charge la taxonomie de compétences depuis un CSV."""
    raise NotImplementedError("AT03 — implémentez load_skills_csv() dans hirekit/rag/ingestion.py")
