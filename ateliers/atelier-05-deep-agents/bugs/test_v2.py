"""Test bug v2 — AGENTS.md manquant."""

import pytest
from pathlib import Path


def test_agents_md_loaded():
    """AGENTS.md doit être chargé depuis .agent/memory/recruiter/AGENTS.md."""
    from hirekit.deep_agent.recruiter_agent import AGENTS_MD

    assert len(AGENTS_MD) > 50, f"AGENTS.md est vide ou manquant: '{AGENTS_MD[:50]}...'"
    assert "Langue" in AGENTS_MD or "FRANÇAIS" in AGENTS_MD, (
        "AGENTS.md ne contient pas les règles globales"
    )
    assert "Recadrage" in AGENTS_MD, "AGENTS.md ne contient pas la règle de recadrage"
    assert "URLs" in AGENTS_MD or "liens" in AGENTS_MD, (
        "AGENTS.md ne contient pas la règle des URLs"
    )
