"""Tests pour hirekit.rag.ingestion — AT03."""

import json
import pytest
from pathlib import Path


class TestLoadCVPdf:
    """AT03 — load_cv_pdf() charge un CV PDF en Document."""

    def test_load_cv_pdf(self, project_root: Path):
        from hirekit.rag.ingestion import load_cv_pdf

        cv_path = project_root / "data" / "cvs" / "cv_001.pdf"
        if not cv_path.exists():
            pytest.skip("CVs non générés")

        docs = load_cv_pdf(str(cv_path))
        assert len(docs) > 0
        assert all(hasattr(d, "page_content") for d in docs)
        assert all(hasattr(d, "metadata") for d in docs)

    def test_load_cv_pdf_has_metadata(self, project_root: Path):
        from hirekit.rag.ingestion import load_cv_pdf

        cv_path = project_root / "data" / "cvs" / "cv_001.pdf"
        if not cv_path.exists():
            pytest.skip("CVs non générés")

        docs = load_cv_pdf(str(cv_path))
        assert len(docs) > 0
        assert docs[0].metadata["type"] == "cv"
        assert "source" in docs[0].metadata
        assert "filename" in docs[0].metadata

    def test_load_cv_pdf_contains_name(self, project_root: Path):
        from hirekit.rag.ingestion import load_cv_pdf

        cv_path = project_root / "data" / "cvs" / "cv_001.pdf"
        if not cv_path.exists():
            pytest.skip("CVs non générés")

        docs = load_cv_pdf(str(cv_path))
        full_text = " ".join(d.page_content for d in docs)
        assert "Marie Dubois" in full_text or "Dubois" in full_text


class TestLoadAllCvs:
    """AT03 — load_all_cvs() charge tous les CVs d'un dossier."""

    def test_load_all_cvs(self, project_root: Path):
        from hirekit.rag.ingestion import load_all_cvs

        cvs_dir = project_root / "data" / "cvs"
        if not cvs_dir.exists():
            pytest.skip("CVs non générés")

        docs = load_all_cvs(str(cvs_dir))
        assert len(docs) >= 30  # au moins 30 CVs (au moins 1 page chacun)

    def test_load_all_cvs_metadata(self, project_root: Path):
        from hirekit.rag.ingestion import load_all_cvs

        cvs_dir = project_root / "data" / "cvs"
        if not cvs_dir.exists():
            pytest.skip("CVs non générés")

        docs = load_all_cvs(str(cvs_dir))
        for doc in docs:
            assert doc.metadata["type"] == "cv"


class TestLoadOffersJson:
    """AT03 — load_offers_json() charge une offre JSON en Document."""

    def test_load_offers_json(self, project_root: Path):
        from hirekit.rag.ingestion import load_offers_json

        offer_path = project_root / "data" / "offers" / "offer_001.json"
        if not offer_path.exists():
            pytest.skip("Offres non générées")

        docs = load_offers_json(str(offer_path))
        assert len(docs) == 1
        assert hasattr(docs[0], "page_content")
        assert hasattr(docs[0], "metadata")

    def test_load_offers_json_metadata(self, project_root: Path):
        from hirekit.rag.ingestion import load_offers_json

        offer_path = project_root / "data" / "offers" / "offer_001.json"
        if not offer_path.exists():
            pytest.skip("Offres non générées")

        docs = load_offers_json(str(offer_path))
        assert docs[0].metadata["type"] == "offer"
        assert "id" in docs[0].metadata
        assert "categorie" in docs[0].metadata

    def test_load_all_offers(self, project_root: Path):
        from hirekit.rag.ingestion import load_all_offers

        offers_dir = project_root / "data" / "offers"
        if not offers_dir.exists():
            pytest.skip("Offres non générées")

        docs = load_all_offers(str(offers_dir))
        assert len(docs) == 15


class TestLoadSkillsCsv:
    """AT03 — load_skills_csv() charge les compétences en Documents."""

    def test_load_skills_csv(self, project_root: Path):
        from hirekit.rag.ingestion import load_skills_csv

        csv_path = project_root / "data" / "skills.csv"
        if not csv_path.exists():
            pytest.skip("skills.csv non généré")

        docs = load_skills_csv(str(csv_path))
        assert len(docs) == 100

    def test_load_skills_csv_metadata(self, project_root: Path):
        from hirekit.rag.ingestion import load_skills_csv

        csv_path = project_root / "data" / "skills.csv"
        if not csv_path.exists():
            pytest.skip("skills.csv non généré")

        docs = load_skills_csv(str(csv_path))
        assert all(d.metadata["type"] == "skill" for d in docs)
        assert "categorie" in docs[0].metadata


class TestLoadCvTextFromJson:
    """AT03 — load_cv_text_from_json() extrait le texte d'un CV depuis le JSON."""

    def test_load_cv_text_from_json(self, project_root: Path):
        from hirekit.rag.ingestion import load_cv_text_from_json

        data_path = project_root / "data" / "cvs" / "cvs_data.json"
        if not data_path.exists():
            pytest.skip("cvs_data.json non généré")

        text = load_cv_text_from_json("cv_001", str(data_path))
        assert "Marie Dubois" in text or "Dubois" in text
        assert "React" in text

    def test_load_cv_text_from_json_invalid_id(self, project_root: Path):
        from hirekit.rag.ingestion import load_cv_text_from_json

        data_path = project_root / "data" / "cvs" / "cvs_data.json"
        if not data_path.exists():
            pytest.skip("cvs_data.json non généré")

        with pytest.raises(ValueError, match="non trouvé"):
            load_cv_text_from_json("cv_invalid", str(data_path))