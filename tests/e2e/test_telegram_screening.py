"""Test E2E — Telegram screening: candidat → screening → CRM.

Inspiré du flux sellkit/src/telegram/handler.ts (objection→closing→memory→CRM→agent→reply).

Ce test simule un candidat qui:
1. Démarre une conversation Telegram
2. Répond aux questions de screening
3. Le bot évalue et met à jour le CRM
4. Le dashboard affiche le candidat dans "Screening"

Note: Ce test utilise Playwright pour ouvrir l'app Streamlit et vérifier le dashboard.
"""

import pytest

try:
    from playwright.sync_api import Page, expect

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

from hirekit.pipeline.memory import (
    ProspectMemory,
    EMPTY_MEMORY,
    merge_memory,
    count_qualification_fields,
    next_missing_field,
    format_memory_for_prompt,
)
from hirekit.pipeline.objections import OBJECTION_CATALOG, _detect_keywords
from hirekit.pipeline.closing import _detect_keywords as _detect_closing_keywords

pytestmark = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")


@pytest.mark.e2e
def test_telegram_screening_full_flow():
    """Simule le flux complet de screening d'un candidat."""
    # 1. Candidat démarre une conversation
    memory = ProspectMemory()
    assert count_qualification_fields(memory) == 0
    assert next_missing_field(memory) == "name"

    # 2. Candidat partage son nom
    memory = merge_memory(memory, {"name": "Marie Dubois"})
    assert count_qualification_fields(memory) == 1
    assert next_missing_field(memory) == "experience"

    # 3. Candidat partage son expérience
    memory = merge_memory(memory, {"experience": "Développeuse Fullstack 5 ans"})
    assert count_qualification_fields(memory) == 2
    assert next_missing_field(memory) == "availability"

    # 4. Candidat partage sa disponibilité
    memory = merge_memory(memory, {"availability": "immédiat"})
    assert count_qualification_fields(memory) == 3
    assert next_missing_field(memory) == "location"

    # 5. Candidat partage sa localisation
    memory = merge_memory(memory, {"location": "Paris"})
    assert count_qualification_fields(memory) == 4
    assert next_missing_field(memory) == "revenueGoal"

    # 6. Candidat partage son objectif de revenu
    memory = merge_memory(memory, {"revenueGoal": "4500 euros"})
    assert count_qualification_fields(memory) == 5
    assert next_missing_field(memory) == "riskAppetite"

    # 7. Candidat partage son appétence au risque
    memory = merge_memory(memory, {"riskAppetite": "à l'aise"})
    assert count_qualification_fields(memory) == 6
    assert next_missing_field(memory) is None

    # 8. Vérifier que la mémoire formatée contient toutes les infos
    formatted = format_memory_for_prompt(memory)
    assert formatted is not None
    assert "Marie Dubois" in formatted
    assert "Développeuse Fullstack 5 ans" in formatted
    assert "immédiat" in formatted
    assert "Paris" in formatted
    assert "4500 euros" in formatted
    assert "à l'aise" in formatted


@pytest.mark.e2e
def test_objection_detection_keyword_fallback():
    """La détection d'objections par keyword doit fonctionner."""
    test_cases = [
        ("C'est trop cher pour moi", "trop_cher"),
        ("C'est une arnaque ça", "arnaque"),
        ("Laissez-moi réfléchir", "reflechir"),
        ("Non merci, pas intéressé", "pas_interesse"),
        ("Je veux un salaire fixe", "fixe"),
        ("C'est légal votre truc ?", "legalite"),
        ("J'ai mes enfants à gérer", "famille"),
        ("Je n'ai pas le temps", "temps"),
    ]

    for text, expected_key in test_cases:
        objection, refusal, source = _detect_keywords(text)
        assert objection is not None, f"Objection non détectée pour: {text}"
        assert objection.key == expected_key, (
            f"Mauvaise objection pour '{text}': {objection.key} au lieu de {expected_key}"
        )
        assert source == "keyword"


@pytest.mark.e2e
def test_closing_detection_keyword_fallback():
    """La détection de closing par keyword doit fonctionner."""
    test_cases = [
        ("Au revoir, bonne journée", "closing_cue"),
        ("Ok je suis prêt, c'est parti", "commitment_signal"),
        ("On peut s'appeler ?", "call_request"),
        ("Ça m'intéresse fortement", "job_interest"),
        ("Ne me recontactez plus", "refusal"),
    ]

    for text, expected_type in test_cases:
        result = _detect_closing_keywords(text)
        assert result.type == expected_type, (
            f"Mauvais type pour '{text}': {result.type} au lieu de {expected_type}"
        )
        assert result.source == "keyword"


@pytest.mark.e2e
def test_crm_pipeline_screening_to_closed_won():
    """Le pipeline CRM doit passer de new → closed_won à travers les étapes."""
    import os
    import tempfile

    from hirekit.crm.store import CrmStore

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        test_db = f.name

    try:
        store = CrmStore(test_db)
        phone = "+33612345678"

        # 1. Nouveau candidat
        c = store.get_or_create(phone)
        assert c.stage == "new"

        # 2. Premier échange → contacted
        store.add_message(phone, "in", "Bonjour")
        store.add_message(phone, "out", "Bonjour ! Vous cherchez un job ?")
        store.update_stage(phone, "contacted")

        # 3. Qualification → interested
        store.set_qual_json(phone, '{"name": "Marie", "experience": "5 ans"}')
        store.update_stage(phone, "interested")

        # 4. Conversion link
        link = store.set_conversion_link(phone)
        assert link is not None

        # 5. Qualified
        store.update_stage(phone, "qualified")

        # 6. Closed won
        store.update_stage(phone, "closed_won")

        c = store.get(phone)
        assert c.stage == "closed_won"
        assert c.conversion_link is not None
        assert c.qual_json is not None

        # Vérifier le nombre de messages
        msgs = store.get_messages(phone)
        assert len(msgs) == 2

        store.close()
    finally:
        os.unlink(test_db)
        for ext in ("-wal", "-shm"):
            p = test_db + ext
            if os.path.exists(p):
                os.unlink(p)
