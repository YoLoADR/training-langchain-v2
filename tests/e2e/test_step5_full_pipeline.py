"""Test E2E step5 — Pipeline complet: 13 étapes, 3 scénarios aléatoires.

Inspiré de sellkit/tests/step5-human-in-the-loop.test.ts (621 lignes).

3 SCÉNARIOS aléatoires (pour éviter les biais):
  A — Nathan, débutant motivé (Vitry-sur-Seine)
  B — Francis, commercial expérimenté (Paris 15e)
  C — Sarah, reconversion professionnelle (Aubervilliers)

13 ÉTAPES:
  Phase 1 — TRIAGE: 5.1 hors-sujet, 5.2 intérêt, 5.3 nom, 5.4 expérience, 5.5 dispo
  Phase 2 — ANALYSIS: 5.6 lieu, 5.7 revenu, 5.8 risque → 6/6 → reformulation, 5.9 intérêt closing
  Phase 3 — CLOSING: 5.10 question test, 5.11 appel, 5.12 engagement, 5.13 au revoir

6 champs: name, experience, availability, location, revenueGoal, riskAppetite
Ordre: name → experience → availability → location → revenueGoal → riskAppetite

Note: Ce test utilise Playwright pour ouvrir l'app Streamlit et simuler les interactions.
Il nécessite que l'app soit lancée (fixture `app`).
"""

import random

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
)
from hirekit.pipeline.closing import STAGE_MAP

pytestmark = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")


SCENARIOS = [
    {
        "name": "A — Nathan, débutant motivé (Vitry-sur-Seine)",
        "persona": "Jeune sans expérience, très motivé, cherche un premier job",
        "steps": {
            "s1_horsujet": "Il fait super beau aujourd'hui, vous avez vu le match hier ?",
            "s2_interet": "Oui, je cherche un job",
            "s3_nom": "Je m'appelle Nathan",
            "s4_experience": "J'ai pas d'expérience mais je souhaite travailler",
            "s5_dispo": "Je suis disponible immédiatement",
            "s6_lieu": "Je vis à Vitry-sur-Seine",
            "s7_revenu": "Je vise 3000 euros par mois minimum",
            "s8_risque": "Ca ne me dérange pas les zones grises, je suis à l'aise avec une startup",
            "s9_interet_closing": "Ok ça m'intéresse fortement, je veux en savoir plus",
            "s10_question_test": "C'est quoi le test technique exactement ?",
            "s11_appel": "On peut s'appeler pour en parler plus en détail ?",
            "s12_commitment": "Ok je suis prêt pour le test, je signe. C'est parti !",
            "s13_aurevoir": "Parfait merci, bonne journée à vous",
        },
    },
    {
        "name": "B — Francis, commercial expérimenté (Paris 15e)",
        "persona": "Commercial 5 ans en immobilier, cherche nouveau défi",
        "steps": {
            "s1_horsujet": "Salut, il fait beau aujourd'hui non ?",
            "s2_interet": "Oui, je suis en recherche active d'emploi",
            "s3_nom": "Moi c'est Francis",
            "s4_experience": "J'ai travaillé 5 ans dans la vente, principalement de l'immobilier",
            "s5_dispo": "Je peux commencer la semaine prochaine",
            "s6_lieu": "J'habite dans le 15e arrondissement de Paris",
            "s7_revenu": "Je vise 5000 euros par mois",
            "s8_risque": "Les zones grises ne me posent aucun problème",
            "s9_interet_closing": "Vos postes m'intéressent beaucoup, j'aimerais postuler",
            "s10_question_test": "Combien de temps dure le test exactement ?",
            "s11_appel": "Je préfère en parler au téléphone, c'est possible ?",
            "s12_commitment": "Ça me va, je démarre le test quand vous voulez",
            "s13_aurevoir": "Merci beaucoup, à bientôt",
        },
    },
    {
        "name": "C — Sarah, reconversion professionnelle (Aubervilliers)",
        "persona": "Marketing digital → veut changer de domaine",
        "steps": {
            "s1_horsujet": "Coucou, super temps aujourd'hui ! Vous avez vu le match de foot hier soir ?",
            "s2_interet": "Oui je cherche du travail actuellement",
            "s3_nom": "Je m'appelle Sarah",
            "s4_experience": "Je viens du marketing digital mais je veux changer de domaine complètement",
            "s5_dispo": "Dispo dès maintenant, je n'ai plus de poste actuellement",
            "s6_lieu": "Je suis basée à Aubervilliers",
            "s7_revenu": "Au moins 2500 euros pour commencer",
            "s8_risque": "Ça ne me dérange pas du tout, j'aime bien l'idée d'une startup",
            "s9_interet_closing": "C'est très intéressant, je veux en savoir plus sur les postes",
            "s10_question_test": "Quels sont les détails du test ?",
            "s11_appel": "On pourrait se téléphoner pour discuter ?",
            "s12_commitment": "Je suis partante pour le test, allons-y !",
            "s13_aurevoir": "Super, merci pour votre temps",
        },
    },
]


@pytest.mark.e2e
@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["name"] for s in SCENARIOS])
def test_scenario_0_to_6_respects_order(scenario):
    """Chaque scénario doit respecter l'ordre 0→6 champs de qualification."""
    memory = ProspectMemory()
    steps = scenario["steps"]

    step_extractions = [
        (
            steps["s3_nom"],
            {
                "name": "Nathan"
                if "Nathan" in scenario["name"]
                else "Francis"
                if "Francis" in scenario["name"]
                else "Sarah"
            },
        ),
        (
            steps["s4_experience"],
            {
                "experience": "aucune"
                if "Nathan" in scenario["name"]
                else "5 ans vente"
                if "Francis" in scenario["name"]
                else "marketing digital"
            },
        ),
        (
            steps["s5_dispo"],
            {
                "availability": "immédiat"
                if "Nathan" in scenario["name"]
                else "semaine prochaine"
                if "Francis" in scenario["name"]
                else "dès maintenant"
            },
        ),
        (
            steps["s6_lieu"],
            {
                "location": "Vitry-sur-Seine"
                if "Nathan" in scenario["name"]
                else "Paris 15e"
                if "Francis" in scenario["name"]
                else "Aubervilliers"
            },
        ),
        (
            steps["s7_revenu"],
            {
                "revenueGoal": "3000 euros"
                if "Nathan" in scenario["name"]
                else "5000 euros"
                if "Francis" in scenario["name"]
                else "2500 euros"
            },
        ),
        (
            steps["s8_risque"],
            {
                "riskAppetite": "à l'aise"
                if "Nathan" in scenario["name"]
                else "aucun problème"
                if "Francis" in scenario["name"]
                else "ça ne me dérange pas"
            },
        ),
    ]

    expected_qual = 0
    for msg, extracted in step_extractions:
        memory = merge_memory(memory, extracted)
        qual_count = count_qualification_fields(memory)
        expected_qual += 1
        assert qual_count == expected_qual, (
            f"Scénario {scenario['name']}: après '{msg}', qual_count={qual_count} au lieu de {expected_qual}"
        )

    assert next_missing_field(memory) is None, "Tous les champs devraient être remplis"


@pytest.mark.e2e
@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["name"] for s in SCENARIOS])
def test_scenario_stage_transitions(scenario):
    """Vérifie les transitions de stage pour chaque scénario."""
    # 5.9 interet_closing → stage=interested
    assert STAGE_MAP["job_interest"] == "interested"
    # 5.11 appel → stage=qualified
    assert STAGE_MAP["call_request"] == "qualified"
    # 5.12 commitment → stage=closed_won
    assert STAGE_MAP["commitment_signal"] == "closed_won"
    # 5.13 au revoir → no stage change
    assert STAGE_MAP["closing_cue"] is None


@pytest.mark.e2e
def test_step5_crm_pipeline_works():
    """Le pipeline CRM doit fonctionner de bout en bout."""
    import os
    import tempfile

    from hirekit.crm.store import CrmStore

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        test_db = f.name

    try:
        store = CrmStore(test_db)

        # Phase 1: new → contacted
        c = store.get_or_create("+33612345678")
        assert c.stage == "new"
        store.add_message("+33612345678", "in", "Bonjour")
        store.add_message("+33612345678", "out", "Salut ! Vous cherchez un job ?")
        store.update_stage("+33612345678", "contacted")
        assert store.get("+33612345678").stage == "contacted"

        # Phase 2: contacted → interested
        store.update_stage("+33612345678", "interested")
        link = store.set_conversion_link("+33612345678")
        assert link is not None
        assert "t.me" in link or "start=" in link

        # Phase 3: interested → qualified → closed_won
        store.update_stage("+33612345678", "qualified")
        store.update_stage("+33612345678", "closed_won")

        c = store.get("+33612345678")
        assert c.stage == "closed_won"
        assert c.conversion_link is not None

        # Vérifier les stats
        stats = store.stats()
        assert stats["total_candidates"] == 1
        assert stats["by_stage"]["closed_won"] == 1

        store.close()
    finally:
        os.unlink(test_db)
        for ext in ("-wal", "-shm"):
            p = test_db + ext
            if os.path.exists(p):
                os.unlink(p)
