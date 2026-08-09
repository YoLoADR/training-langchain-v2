"""Fixtures communes pour les tests hirekit."""

import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def cvs_dir(project_root: Path) -> Path:
    return project_root / "data" / "cvs"


@pytest.fixture
def offers_dir(project_root: Path) -> Path:
    return project_root / "data" / "offers"


@pytest.fixture
def sample_cv_text() -> str:
    return """
    Marie Dubois
    Développeuse Fullstack — 5 ans d'expérience
    marie.dubois@email.fr

    Compétences : React (4 ans), Python (2 ans), Docker (1 an)
    Expérience : TechCorp (2022-2024), StartupXYZ (2020-2022)
    """


@pytest.fixture
def sample_offer_text() -> str:
    return """
    Poste : Développeur React Senior
    Compétences requises : React, TypeScript, Node.js
    Localisation : Paris
    """
