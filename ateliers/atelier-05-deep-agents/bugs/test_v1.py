"""Test bug v1 — Skills inversés."""

import pytest
from hirekit.deep_agent.middleware import RecruitmentContext, read_skill_for_context


def test_first_contact_skill_when_qual_count_0():
    """quand qual_count=0, le skill phase-first-contact doit être chargé."""
    ctx = RecruitmentContext(qual_count=0, stage="new")
    skill = read_skill_for_context(ctx)
    assert "phase-first-contact" in skill or "Premier Contact" in skill, (
        f"Expected phase-first-contact, got: {skill[:100]}"
    )


def test_qualification_skill_when_qual_count_3():
    """quand qual_count=3, le skill phase-qualification doit être chargé."""
    ctx = RecruitmentContext(qual_count=3, stage="contacted")
    skill = read_skill_for_context(ctx)
    assert "phase-qualification" in skill or "Qualification" in skill, (
        f"Expected phase-qualification, got: {skill[:100]}"
    )
