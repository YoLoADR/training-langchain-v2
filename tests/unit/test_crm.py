"""Tests unitaires pour hirekit.crm.store — CRM SQLite pipeline.

Inspiré de sellkit/tests/verify-flow.test.ts (section 8: Store).
Tests purs: utilise une DB temporaire.
"""

import os
import tempfile
from pathlib import Path

import pytest

from hirekit.crm.store import CrmStore
from hirekit.crm.types import STAGES, STAGE_LABELS


@pytest.fixture
def store():
    """Crée un CRM store avec une DB temporaire."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    s = CrmStore(db_path)
    yield s
    s.close()
    os.unlink(db_path)
    for ext in ("-wal", "-shm"):
        p = db_path + ext
        if os.path.exists(p):
            os.unlink(p)


class TestStages:
    """Vérifie les 6 stages du pipeline CRM."""

    def test_stages_count(self):
        assert len(STAGES) == 6

    def test_stages_order(self):
        expected = ["new", "contacted", "interested", "qualified", "closed_won", "closed_lost"]
        assert STAGES == expected

    def test_stage_labels_exist(self):
        for stage in STAGES:
            assert stage in STAGE_LABELS, f"Label manquant pour stage: {stage}"


class TestCrmStore:
    """Tests du CRM store SQLite."""

    def test_get_or_create_new_candidate(self, store):
        c = store.get_or_create("+33612345678")
        assert c is not None
        assert c.phone == "+33612345678"
        assert c.stage == "new"
        assert c.message_count == 0

    def test_get_or_create_idempotent(self, store):
        c1 = store.get_or_create("+33612345678")
        c2 = store.get_or_create("+33612345678")
        assert c1.id == c2.id
        assert c1.phone == c2.phone

    def test_get_returns_none_for_unknown(self, store):
        assert store.get("+33000000000") is None

    def test_get_all_returns_list(self, store):
        store.get_or_create("+33611111111")
        store.get_or_create("+33622222222")
        all_candidates = store.get_all()
        assert len(all_candidates) == 2

    def test_update_stage(self, store):
        store.get_or_create("+33612345678")
        store.update_stage("+33612345678", "interested")
        c = store.get("+33612345678")
        assert c is not None
        assert c.stage == "interested"

    def test_add_message_in(self, store):
        store.get_or_create("+33612345678")
        store.add_message("+33612345678", "in", "Bonjour")
        c = store.get("+33612345678")
        assert c is not None
        assert c.message_count == 1
        assert c.last_message == "Bonjour"
        assert c.last_direction == "in"

    def test_add_message_out(self, store):
        store.get_or_create("+33612345678")
        store.add_message("+33612345678", "out", "Bonjour, comment puis-je vous aider ?")
        c = store.get("+33612345678")
        assert c is not None
        assert c.message_count == 1
        assert c.last_direction == "out"

    def test_get_messages(self, store):
        store.get_or_create("+33612345678")
        store.add_message("+33612345678", "in", "Bonjour")
        store.add_message("+33612345678", "out", "Salut !")
        msgs = store.get_messages("+33612345678")
        assert len(msgs) == 2
        assert msgs[0].direction == "in"
        assert msgs[1].direction == "out"

    def test_set_conversion_link_idempotent(self, store):
        phone = "+33612345678"
        store.get_or_create(phone)
        link1 = store.set_conversion_link(phone)
        assert link1 is not None
        assert "t.me" in link1 or "start=" in link1
        link2 = store.set_conversion_link(phone)
        assert link2 == link1, "set_conversion_link doit être idempotent"

    def test_get_conversion_link_none_if_not_set(self, store):
        assert store.get_conversion_link("+33699999999") is None

    def test_set_qual_json(self, store):
        store.get_or_create("+33612345678")
        store.set_qual_json("+33612345678", '{"name": "Nathan"}')
        assert store.get_qual_json("+33612345678") == '{"name": "Nathan"}'

    def test_get_qual_json_none_if_not_set(self, store):
        assert store.get_qual_json("+33699999999") is None

    def test_stats(self, store):
        store.get_or_create("+33611111111")
        store.get_or_create("+33622222222")
        store.update_stage("+33611111111", "contacted")
        stats = store.stats()
        assert stats["total_candidates"] == 2
        assert stats["by_stage"]["contacted"] == 1
        assert stats["by_stage"]["new"] == 1

    def test_clear_messages(self, store):
        store.get_or_create("+33612345678")
        store.add_message("+33612345678", "in", "Bonjour")
        store.add_message("+33612345678", "out", "Salut !")
        store.clear_messages("+33612345678")
        msgs = store.get_messages("+33612345678")
        assert len(msgs) == 0
        c = store.get("+33612345678")
        assert c is not None
        assert c.message_count == 0

    def test_delete_candidate(self, store):
        store.get_or_create("+33612345678")
        store.add_message("+33612345678", "in", "Bonjour")
        store.delete_candidate("+33612345678")
        assert store.get("+33612345678") is None
        assert len(store.get_messages("+33612345678")) == 0
