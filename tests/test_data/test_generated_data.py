"""Tests pour les données simulées (scripts/generate_*.py).

Vérifie que les données générées sont complètes et cohérentes.
Ces tests supposent que les scripts de génération ont été lancés.
"""

import json
import csv
from pathlib import Path

import pytest


class TestCVData:
    """Vérifie les CVs PDF générés par generate_cvs.py."""

    @pytest.fixture
    def cvs_data(self, project_root: Path) -> list[dict]:
        json_path = project_root / "data" / "cvs" / "cvs_data.json"
        if not json_path.exists():
            pytest.skip("CVs non générés — lancez: python scripts/generate_cvs.py")
        return json.loads(json_path.read_text(encoding="utf-8"))

    @pytest.fixture
    def cv_pdfs(self, cvs_dir: Path) -> list[Path]:
        pdfs = list(cvs_dir.glob("cv_*.pdf"))
        if not pdfs:
            pytest.skip("CVs PDF non générés — lancez: python scripts/generate_cvs.py")
        return pdfs

    def test_30_cvs_pdf_exist(self, cv_pdfs: list[Path]):
        assert len(cv_pdfs) == 30

    def test_30_cvs_in_json(self, cvs_data: list[dict]):
        assert len(cvs_data) == 30

    def test_cv_has_required_fields(self, cvs_data: list[dict]):
        required = {"id", "nom", "email", "telephone", "titre", "competences", "experiences"}
        for cv in cvs_data:
            missing = required - set(cv.keys())
            assert not missing, f"CV {cv.get('id')} missing: {missing}"

    def test_cv_diverse_categories(self, cvs_data: list[dict]):
        categories = {cv["categorie"] for cv in cvs_data}
        assert len(categories) >= 8, f"Only {len(categories)} categories: {categories}"

    def test_personas_present(self, cvs_data: list[dict]):
        names = {cv["nom"] for cv in cvs_data}
        expected = {"Marie Dubois", "Karim Benali", "Sophie Martin", "Léa Chen", "Thomas Petit"}
        assert expected.issubset(names), f"Missing personas: {expected - names}"

    def test_cv_pdf_is_valid_pdf(self, cv_pdfs: list[Path]):
        for pdf in cv_pdfs[:3]:  # vérifie les 3 premiers
            header = pdf.read_bytes()[:5]
            assert header.startswith(b"%PDF"), f"{pdf.name} is not a valid PDF"


class TestOffersData:
    """Vérifie les offres JSON générées par generate_offers.py."""

    @pytest.fixture
    def offers(self, offers_dir: Path) -> list[dict]:
        files = sorted(offers_dir.glob("offer_*.json"))
        if not files:
            pytest.skip("Offres non générées — lancez: python scripts/generate_offers.py")
        return [json.loads(f.read_text(encoding="utf-8")) for f in files]

    def test_15_offers_exist(self, offers: list[dict]):
        assert len(offers) == 15

    def test_offer_has_required_fields(self, offers: list[dict]):
        required = {"id", "titre", "entreprise", "competences", "localisation", "salaire_min"}
        for offer in offers:
            missing = required - set(offer.keys())
            assert not missing, f"Offer {offer.get('id')} missing: {missing}"

    def test_offers_diverse_categories(self, offers: list[dict]):
        categories = {o["categorie"] for o in offers}
        assert len(categories) >= 7


class TestSkillsCSV:
    """Vérifie skills.csv généré par generate_skills.py."""

    @pytest.fixture
    def skills_csv(self, project_root: Path) -> list[dict]:
        path = project_root / "data" / "skills.csv"
        if not path.exists():
            pytest.skip("skills.csv non généré — lancez: python scripts/generate_skills.py")
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_100_skills(self, skills_csv: list[dict]):
        assert len(skills_csv) == 100

    def test_8_categories(self, skills_csv: list[dict]):
        categories = {row["categorie"] for row in skills_csv}
        assert len(categories) >= 8

    def test_skills_have_mots_cles(self, skills_csv: list[dict]):
        for row in skills_csv:
            assert len(row["mots_cles"]) > 0, f"Skill {row['nom']} has no mots_cles"


class TestQADataset:
    """Vérifie qa_dataset.jsonl généré par generate_qa_dataset.py."""

    @pytest.fixture
    def qa_pairs(self, project_root: Path) -> list[dict]:
        path = project_root / "data" / "qa_dataset.jsonl"
        if not path.exists():
            pytest.skip("qa_dataset.jsonl non généré — lancez: python scripts/generate_qa_dataset.py")
        lines = path.read_text(encoding="utf-8").strip().split("\n")
        return [json.loads(line) for line in lines]

    def test_150_pairs(self, qa_pairs: list[dict]):
        assert len(qa_pairs) == 150

    def test_types_distribution(self, qa_pairs: list[dict]):
        types = {}
        for q in qa_pairs:
            types[q["type"]] = types.get(q["type"], 0) + 1
        assert types.get("screening", 0) == 50
        assert types.get("matching", 0) == 50
        assert types.get("availability", 0) == 25
        assert types.get("general", 0) == 25

    def test_qa_has_sources(self, qa_pairs: list[dict]):
        for q in qa_pairs:
            assert len(q["sources"]) > 0, f"QA {q['id']} has no sources"

    def test_persona_questions_present(self, qa_pairs: list[dict]):
        questions = [q["question"] for q in qa_pairs]
        assert "Quelle est l'expérience de Marie Dubois en React ?" in questions


class TestAvailability:
    """Vérifie availability.json généré par generate_availability.py."""

    @pytest.fixture
    def availability(self, project_root: Path) -> dict:
        path = project_root / "data" / "availability.json"
        if not path.exists():
            pytest.skip("availability.json non généré — lancez: python scripts/generate_availability.py")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_30_candidates(self, availability: dict):
        assert availability["num_candidates"] == 30

    def test_candidates_have_slots(self, availability: dict):
        for c in availability["candidates"]:
            assert c["total_slots"] > 0
            assert c["available_slots"] >= 0
            assert c["available_slots"] <= c["total_slots"]


class TestCodeRepo:
    """Vérifie le mini-repo Python généré par generate_code_repo.py."""

    @pytest.fixture
    def code_repo_files(self, project_root: Path) -> list[Path]:
        code_dir = project_root / "data" / "code_repo"
        if not code_dir.exists():
            pytest.skip("code_repo non généré — lancez: python scripts/generate_code_repo.py")
        return sorted(code_dir.glob("*.py"))

    def test_10_python_files(self, code_repo_files: list[Path]):
        assert len(code_repo_files) == 10

    def test_expected_files_present(self, code_repo_files: list[Path]):
        names = {f.name for f in code_repo_files}
        expected = {
            "config.py", "database.py", "models.py", "auth.py", "routes.py",
            "services.py", "middleware.py", "errors.py", "utils.py", "main.py",
        }
        assert expected == names

    def test_files_are_valid_python(self, code_repo_files: list[Path]):
        import ast
        for py_file in code_repo_files:
            try:
                ast.parse(py_file.read_text(encoding="utf-8"))
            except SyntaxError as e:
                pytest.fail(f"{py_file.name} has syntax error: {e}")