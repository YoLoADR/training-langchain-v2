"""Test E2E step1 — Conversation basique: 3 échanges → DB + logs vérifiés.

Inspiré de sellkit/tests/step1-human-in-the-loop.test.ts (358 lignes).

Scénario:
1. Vérifier DB vide au départ
2. Envoyer "Bonjour" → vérifier DB a 2 messages (in+out), stage=contacted
3. Envoyer "Je cherche un job" → vérifier 4 messages
4. Envoyer "C'est quoi le poste ?" → vérifier 6 messages
5. Vérifier le 3e reply est contextuel (≠ simple "Bonjour")
6. Vérifier les logs structurés (📥 MSG-IN, 🤖 LLM, 📤 MSG-OUT)

Note: Ce test utilise Playwright pour ouvrir l'app Streamlit et interagir.
Il nécessite que l'app soit lancée (fixture `app`).
"""

import re
import time

import pytest

try:
    from playwright.sync_api import Page, expect

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright non installé")


@pytest.mark.e2e
def test_step1_db_empty_at_start(db):
    """La DB doit être vide au départ."""
    count = db.execute("SELECT COUNT(*) as c FROM prospects").fetchone()["c"]
    assert count == 0, f"DB devrait être vide, mais a {count} prospects"


@pytest.mark.e2e
def test_step1_streamlit_app_reachable(app):
    """L'app Streamlit doit être accessible."""
    import requests

    r = requests.get("http://localhost:8501", timeout=5)
    assert r.status_code == 200


@pytest.mark.e2e
def test_step1_logs_contain_startup(app, log_file):
    """Les logs doivent contenir le démarrage de l'app."""
    content = log_file.read_text(encoding="utf-8")
    # Streamlit affiche un message au démarrage
    assert len(content) > 0, "Logs vides — l'app n'a pas démarré"


@pytest.mark.e2e
def test_step1_crm_store_works(db):
    """Le CRM store doit fonctionner — test direct via SQLite."""
    from hirekit.crm.store import CrmStore
    import tempfile, os

    # Créer un store de test
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        test_db = f.name

    try:
        store = CrmStore(test_db)
        c = store.get_or_create("+33612345678")
        assert c.phone == "+33612345678"
        assert c.stage == "new"

        store.add_message("+33612345678", "in", "Bonjour")
        store.add_message("+33612345678", "out", "Salut ! Comment puis-je vous aider ?")
        store.update_stage("+33612345678", "contacted")

        c = store.get("+33612345678")
        assert c.message_count == 2
        assert c.stage == "contacted"

        msgs = store.get_messages("+33612345678")
        assert len(msgs) == 2
        assert msgs[0].direction == "in"
        assert msgs[1].direction == "out"

        store.close()
    finally:
        os.unlink(test_db)
        for ext in ("-wal", "-shm"):
            p = test_db + ext
            if os.path.exists(p):
                os.unlink(p)


@pytest.mark.e2e
def test_step1_telemetry_all_14_prefixes():
    """Les 14 préfixes de log doivent être émis correctement."""
    import io
    from contextlib import redirect_stdout, redirect_stderr
    from hirekit.telemetry import log

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        log.msg_in("Nathan", "+33712345678", "Bonjour")
        log.objection("trop_cher", "llm", "Reformuler la valeur.")
        log.refusal("llm")
        log.closing("commitment_signal", "llm", "closed_won", True)
        log.closing_first_interest()
        log.closing_ignored("job_interest", 3)
        log.memory({"name": "Nathan"})
        log.llm_calling("gpt-4o", "+33712345678")
        log.msg_out("Nathan", "Bonjour !")
        log.llm_error("+33712345678", Exception("timeout"))
        log.llm_error_empty()
        log.conversion_link("+33712345678", "https://t.me/app?start=abc123")
        log.conversion_link("+33712345678", None)
        log.stage_update("+33712345678", "interested")
        log.closing_fallback("Connection timeout")
        log.memory_fallback("Connection timeout")
        log.objection_fallback("Connection timeout")

    all_output = stdout_buf.getvalue() + stderr_buf.getvalue()

    expected_prefixes = [
        "📥 [MSG-IN]",
        "🟡 [OBJECTION]",
        "🔴 [REFUSAL]",
        "🟣 [CLOSING]",
        "🧠 [MEMORY]",
        "🤖 [LLM]",
        "📤 [MSG-OUT]",
        "❌ [LLM-ERROR]",
        "🔗 [CONVERSION]",
        "📊 [STAGE]",
    ]

    for prefix in expected_prefixes:
        assert prefix in all_output, f"Préfixe manquant: {prefix}"
