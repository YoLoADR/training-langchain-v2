"""Tests unitaires pour hirekit.pipeline.memory — tests purs, pas de LLM.

Inspiré de sellkit/tests/verify-flow.test.ts (sections 1-3).
Tests: merge, count, nextMissingField, format, serialize/parse round-trip, 3 scénarios.
"""

import pytest
from hirekit.pipeline.memory import (
    ProspectMemory,
    EMPTY_MEMORY,
    merge_memory,
    count_qualification_fields,
    next_missing_field,
    format_memory_for_prompt,
    parse_memory,
    serialize_memory,
)


class TestMergeMemory:
    """merge_memory doit garder les nouvelles infos sans écraser les anciennes."""

    def test_merge_keeps_new_info_without_overwriting(self):
        existing = ProspectMemory(name="Nathan")
        new_info = {"experience": "aucune"}
        merged = merge_memory(existing, new_info)
        assert merged.name == "Nathan"
        assert merged.experience == "aucune"

    def test_merge_keeps_all_existing_info(self):
        existing = ProspectMemory(
            name="Francis", experience="5 ans vente", availability="semaine prochaine"
        )
        new_info = {"location": "Paris 15e"}
        merged = merge_memory(existing, new_info)
        assert merged.name == "Francis"
        assert merged.experience == "5 ans vente"
        assert merged.availability == "semaine prochaine"
        assert merged.location == "Paris 15e"

    def test_merge_empty_new_info_keeps_everything(self):
        existing = ProspectMemory(name="Sarah", location="Aubervilliers")
        merged = merge_memory(existing, {})
        assert merged.name == "Sarah"
        assert merged.location == "Aubervilliers"


class TestCountQualificationFields:
    """count_qualification_fields doit compter les 6 champs non-null."""

    def test_empty_memory_is_0(self):
        assert count_qualification_fields(EMPTY_MEMORY) == 0

    def test_one_field_is_1(self):
        assert count_qualification_fields(ProspectMemory(name="Nathan")) == 1

    def test_six_fields_is_6(self):
        full = ProspectMemory(
            name="Nathan",
            experience="aucune",
            availability="immédiat",
            location="Vitry-sur-Seine",
            revenueGoal="3000 euros",
            riskAppetite="à l'aise",
        )
        assert count_qualification_fields(full) == 6

    def test_motivation_and_notes_dont_count(self):
        m = ProspectMemory(motivation="cherche un job", notes="a un véhicule")
        assert count_qualification_fields(m) == 0


class TestNextMissingField:
    """next_missing_field doit respecter l'ordre: name→experience→availability→location→revenueGoal→riskAppetite."""

    def test_empty_memory_returns_name(self):
        assert next_missing_field(EMPTY_MEMORY) == "name"

    def test_name_only_returns_experience(self):
        m = ProspectMemory(name="Nathan")
        assert next_missing_field(m) == "experience"

    def test_name_experience_returns_availability(self):
        m = ProspectMemory(name="Nathan", experience="aucune")
        assert next_missing_field(m) == "availability"

    def test_name_experience_availability_returns_location(self):
        m = ProspectMemory(name="Nathan", experience="aucune", availability="immédiat")
        assert next_missing_field(m) == "location"

    def test_five_fields_returns_riskAppetite(self):
        m = ProspectMemory(
            name="Nathan",
            experience="aucune",
            availability="immédiat",
            location="Vitry",
            revenueGoal="3000",
        )
        assert next_missing_field(m) == "riskAppetite"

    def test_six_fields_returns_none(self):
        m = ProspectMemory(
            name="Nathan",
            experience="aucune",
            availability="immédiat",
            location="Vitry",
            revenueGoal="3000",
            riskAppetite="ok",
        )
        assert next_missing_field(m) is None

    def test_critical_name_availability_without_experience_returns_experience(self):
        m = ProspectMemory(name="Nathan", availability="immédiat")
        assert next_missing_field(m) == "experience"

    def test_critical_name_location_without_experience_returns_experience(self):
        m = ProspectMemory(name="Nathan", location="Paris")
        assert next_missing_field(m) == "experience"


class TestSerializeParseRoundTrip:
    """serialize_memory puis parse_memory doit retrouver les mêmes valeurs."""

    def test_round_trip(self):
        m = ProspectMemory(name="Francis", experience="5 ans vente", location="Paris 15e")
        json_str = serialize_memory(m)
        parsed = parse_memory(json_str)
        assert parsed.name == "Francis"
        assert parsed.experience == "5 ans vente"
        assert parsed.location == "Paris 15e"
        assert parsed.availability is None

    def test_parse_null_returns_empty(self):
        parsed = parse_memory(None)
        assert parsed.name is None
        assert parsed.experience is None

    def test_parse_invalid_json_returns_empty(self):
        parsed = parse_memory("not valid json")
        assert parsed.name is None


class TestFormatMemoryForPrompt:
    """format_memory_for_prompt doit formater les infos pour injection dans le prompt."""

    def test_empty_memory_returns_none(self):
        assert format_memory_for_prompt(EMPTY_MEMORY) is None

    def test_name_only_produces_one_line(self):
        m = ProspectMemory(name="Nathan")
        formatted = format_memory_for_prompt(m)
        assert "Nom: Nathan" in formatted

    def test_full_memory_produces_six_lines(self):
        m = ProspectMemory(
            name="Nathan",
            experience="aucune",
            availability="immédiat",
            location="Vitry-sur-Seine",
            revenueGoal="3000 euros",
            riskAppetite="à l'aise",
        )
        formatted = format_memory_for_prompt(m)
        assert "Nom: Nathan" in formatted
        assert "Expérience: aucune" in formatted
        assert "Disponibilité: immédiat" in formatted
        assert "Localisation: Vitry-sur-Seine" in formatted
        assert "Objectif revenu: 3000 euros" in formatted
        assert "Appétence aux risques: à l'aise" in formatted


class TestScenarios:
    """3 scénarios complets (Nathan, Francis, Sarah) — 0→6 champs dans l'ordre."""

    @pytest.mark.parametrize(
        "name,messages,expected",
        [
            (
                "Nathan (Vitry)",
                [
                    ("Il fait super beau aujourd'hui", {}, 0, "name"),
                    ("Oui, je cherche un job", {}, 0, "name"),
                    ("Je m'appelle Nathan", {"name": "Nathan"}, 1, "experience"),
                    (
                        "J'ai pas d'expérience mais je souhaite travailler",
                        {"experience": "aucune"},
                        2,
                        "availability",
                    ),
                    (
                        "Je suis disponible immédiatement",
                        {"availability": "immédiat"},
                        3,
                        "location",
                    ),
                    ("Je vis à Vitry-sur-Seine", {"location": "Vitry-sur-Seine"}, 4, "revenueGoal"),
                    (
                        "Je vise 3000 euros par mois minimum",
                        {"revenueGoal": "3000 euros"},
                        5,
                        "riskAppetite",
                    ),
                    (
                        "Ca ne me dérange pas les zones grises",
                        {"riskAppetite": "à l'aise"},
                        6,
                        None,
                    ),
                ],
                "Nathan",
            ),
            (
                "Francis (Paris 15e)",
                [
                    ("Salut, il fait beau aujourd'hui non ?", {}, 0, "name"),
                    ("Oui, je suis en recherche active d'emploi", {}, 0, "name"),
                    ("Moi c'est Francis", {"name": "Francis"}, 1, "experience"),
                    (
                        "J'ai travaillé 5 ans dans la vente",
                        {"experience": "5 ans, vente"},
                        2,
                        "availability",
                    ),
                    (
                        "Je peux commencer la semaine prochaine",
                        {"availability": "la semaine prochaine"},
                        3,
                        "location",
                    ),
                    (
                        "J'habite dans le 15e arrondissement de Paris",
                        {"location": "15e arrondissement de Paris"},
                        4,
                        "revenueGoal",
                    ),
                    (
                        "Je vise 5000 euros par mois",
                        {"revenueGoal": "5000 euros"},
                        5,
                        "riskAppetite",
                    ),
                    (
                        "Les zones grises ne me posent aucun problème",
                        {"riskAppetite": "aucun problème"},
                        6,
                        None,
                    ),
                ],
                "Francis",
            ),
            (
                "Sarah (Aubervilliers)",
                [
                    ("Coucou, super temps aujourd'hui !", {}, 0, "name"),
                    ("Oui je cherche du travail actuellement", {}, 0, "name"),
                    ("Je m'appelle Sarah", {"name": "Sarah"}, 1, "experience"),
                    (
                        "Je viens du marketing digital mais je veux changer",
                        {"experience": "marketing digital"},
                        2,
                        "availability",
                    ),
                    ("Dispo dès maintenant", {"availability": "dès maintenant"}, 3, "location"),
                    (
                        "Je suis basée à Aubervilliers",
                        {"location": "Aubervilliers"},
                        4,
                        "revenueGoal",
                    ),
                    (
                        "Au moins 2500 euros pour commencer",
                        {"revenueGoal": "2500 euros"},
                        5,
                        "riskAppetite",
                    ),
                    (
                        "Ça ne me dérange pas du tout",
                        {"riskAppetite": "ça ne me dérange pas"},
                        6,
                        None,
                    ),
                ],
                "Sarah",
            ),
        ],
    )
    def test_scenario_0_to_6_respects_order(self, name, messages, expected, scenario_name):
        """Chaque scénario doit respecter l'ordre 0→6 champs."""
        memory = ProspectMemory()
        for msg, extracted, expected_qual, expected_next in messages:
            if extracted:
                memory = merge_memory(memory, extracted)
            qual_count = count_qualification_fields(memory)
            next_field = next_missing_field(memory)
            assert qual_count == expected_qual, (
                f"Scénario {scenario_name}: après '{msg}', qual_count={qual_count} au lieu de {expected_qual}"
            )
            assert next_field == expected_next, (
                f"Scénario {scenario_name}: après '{msg}', next_field={next_field} au lieu de {expected_next}"
            )
