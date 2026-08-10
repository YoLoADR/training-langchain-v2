"""Tests pour hirekit.services.availability — AT04."""

import pytest
from pathlib import Path


class TestCheckAvailability:
    """AT04 — check_availability() vérifie les créneaux."""

    def test_check_availability(self, project_root: Path):
        from hirekit.services.availability import check_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        # 2025-09-01 est un lundi dans le calendrier généré
        result = check_availability("2025-09-01")
        assert isinstance(result, dict)
        assert "date" in result
        assert "available_candidates" in result
        assert "total_checked" in result
        assert result["date"] == "2025-09-01"

    def test_check_availability_returns_candidates(self, project_root: Path):
        from hirekit.services.availability import check_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        result = check_availability("2025-09-01")
        # Au moins un candidat devrait être disponible (60% de dispo)
        assert result["total_checked"] == 30
        for c in result["available_candidates"]:
            assert "candidate_id" in c
            assert "name" in c
            assert "total_available_hours" in c
            assert c["total_available_hours"] > 0

    def test_check_availability_weekend(self, project_root: Path):
        from hirekit.services.availability import check_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        # 2025-09-06 est un samedi → pas de créneaux
        result = check_availability("2025-09-06")
        assert result["total_available"] == 0


class TestCheckCandidateAvailability:
    """AT04 — check_candidate_availability() vérifie un candidat."""

    def test_check_candidate_availability(self, project_root: Path):
        from hirekit.services.availability import check_candidate_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        result = check_candidate_availability("cv_001", date="2025-09-01")
        assert isinstance(result, dict)
        assert result["candidate_id"] == "cv_001"
        assert "available_slots" in result

    def test_check_candidate_not_found(self, project_root: Path):
        from hirekit.services.availability import check_candidate_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        result = check_candidate_availability("cv_invalid", date="2025-09-01")
        assert result["name"] == "Non trouvé"
        assert result["total_available"] == 0


class TestFindBestSlots:
    """AT04 — find_best_slots() trouve les créneaux communs."""

    def test_find_best_slots(self, project_root: Path):
        from hirekit.services.availability import find_best_slots

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        result = find_best_slots(["cv_001", "cv_002"], date="2025-09-01")
        assert isinstance(result, dict)
        assert "common_slots" in result
        assert result["date"] == "2025-09-01"


class TestLoadAvailability:
    """AT04 — load_availability() charge le calendrier."""

    def test_load_availability(self, project_root: Path):
        from hirekit.services.availability import load_availability

        avail_path = project_root / "data" / "availability.json"
        if not avail_path.exists():
            pytest.skip("availability.json non généré")

        data = load_availability(str(avail_path))
        assert "candidates" in data
        assert data["num_candidates"] == 30

    def test_load_availability_not_found(self, tmp_path: Path):
        from hirekit.services.availability import load_availability

        with pytest.raises(FileNotFoundError, match="non trouvé"):
            load_availability(tmp_path / "nonexistent.json")