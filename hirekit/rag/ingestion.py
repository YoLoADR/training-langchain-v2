"""Document Loaders — chargement des CVs, offres et skills.

AT03 — Document Loaders : PyMuPDFLoader, JSONLoader, CSVLoader.

Ce module charge les documents simulés générés par scripts/generate_*.py
et les convertit en objets langchain_core.documents.Document avec métadonnées.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from langchain_core.documents import Document


def load_cv_pdf(path: str) -> list[Document]:
    """AT03 — charge un CV PDF avec métadonnées (source, page).

    Utilise PyMuPDFLoader (fitz) qui est rapide et supporte le texte
    extractible. Les métadonnées incluent 'source' (chemin du fichier)
    et 'page' (numéro de page, 0-indexé).

    Args:
        path: chemin vers le fichier PDF d'un CV.

    Returns:
        Liste de Document (un par page du PDF).
    """
    from langchain_community.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(path)
    documents = loader.load()

    # Enrichir les métadonnées avec le nom du fichier (utile pour le RAG)
    filename = Path(path).stem
    for doc in documents:
        doc.metadata["source"] = path
        doc.metadata["filename"] = filename
        doc.metadata["type"] = "cv"

    return documents


def load_all_cvs(cvs_dir: str = "data/cvs") -> list[Document]:
    """AT03 — charge tous les CVs PDF d'un dossier.

    Args:
        cvs_dir: dossier contenant les CVs PDF (défaut: data/cvs).

    Returns:
        Liste de Document (toutes les pages de tous les CVs).
    """
    cvs_path = Path(cvs_dir)
    pdf_files = sorted(cvs_path.glob("cv_*.pdf"))
    all_docs = []
    for pdf_file in pdf_files:
        docs = load_cv_pdf(str(pdf_file))
        all_docs.extend(docs)
    return all_docs


def load_offers_json(path: str) -> list[Document]:
    """AT03 — charge les offres d'emploi depuis un fichier JSON.

    Chaque offre devient un Document avec le contenu textuel de l'offre
    (titre, entreprise, description, compétences) et des métadonnées
    (id, categorie, localisation).

    Args:
        path: chemin vers le fichier JSON d'une offre.

    Returns:
        Liste contenant un seul Document pour cette offre.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    # Construire le contenu textuel de l'offre
    content_parts = [
        f"Titre: {data.get('titre', '')}",
        f"Entreprise: {data.get('entreprise', '')}",
        f"Description: {data.get('description', '')}",
        f"Compétences requises: {', '.join(data.get('competences', []))}",
        f"Localisation: {data.get('localisation', '')}",
        f"Expérience requise: {data.get('experience_requise', '')}",
        f"Télétravail: {data.get('teletravail', '')}",
    ]
    content = "\n".join(content_parts)

    metadata = {
        "source": path,
        "id": data.get("id", ""),
        "type": "offer",
        "categorie": data.get("categorie", ""),
        "localisation": data.get("localisation", ""),
        "titre": data.get("titre", ""),
    }

    return [Document(page_content=content, metadata=metadata)]


def load_all_offers(offers_dir: str = "data/offers") -> list[Document]:
    """AT03 — charge toutes les offres JSON d'un dossier.

    Args:
        offers_dir: dossier contenant les offres JSON (défaut: data/offers).

    Returns:
        Liste de Document (un par offre).
    """
    offers_path = Path(offers_dir)
    json_files = sorted(offers_path.glob("offer_*.json"))
    all_docs = []
    for json_file in json_files:
        docs = load_offers_json(str(json_file))
        all_docs.extend(docs)
    return all_docs


def load_skills_csv(path: str) -> list[Document]:
    """AT03 — charge la taxonomie de compétences depuis un CSV.

    Chaque compétence devient un Document avec le nom de la compétence
    et ses mots-clés comme contenu, et la catégorie comme métadonnée.

    Args:
        path: chemin vers le fichier CSV des compétences.

    Returns:
        Liste de Document (un par compétence).
    """
    documents = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            content = f"{row['nom']} ({row['categorie']}): {row['mots_cles']}"
            metadata = {
                "source": path,
                "type": "skill",
                "categorie": row["categorie"],
                "id": row["id"],
            }
            documents.append(Document(page_content=content, metadata=metadata))
    return documents


def load_cv_text_from_json(cv_id: str, cvs_data_path: str = "data/cvs/cvs_data.json") -> str:
    """AT03 — extrait le texte d'un CV depuis cvs_data.json (plus rapide que le PDF).

    Utile pour les tests et les chaînes LCEL qui n'ont pas besoin du PDF parsing.

    Args:
        cv_id: identifiant du CV (ex: "cv_001").
        cvs_data_path: chemin vers cvs_data.json.

    Returns:
        Texte du CV formaté.
    """
    data = json.loads(Path(cvs_data_path).read_text(encoding="utf-8"))
    for cv in data:
        if cv["id"] == cv_id:
            parts = [
                cv["nom"],
                cv["titre"],
                cv["email"],
                f"Téléphone: {cv['telephone']}",
                "",
                "Compétences:",
            ]
            for skill in cv["competences"]:
                parts.append(f"  - {skill['nom']} ({skill['niveau']}, {skill['annees']} ans)")
            parts.append("")
            parts.append("Expériences:")
            for exp in cv["experiences"]:
                parts.append(f"  - {exp['poste']} chez {exp['entreprise']} ({exp['duree']}): {exp['description']}")
            parts.append("")
            parts.append(f"Anglais: {cv['anglais']}")
            return "\n".join(parts)
    raise ValueError(f"CV {cv_id} non trouvé dans {cvs_data_path}")