"""Tests unitaires pour hirekit.telemetry.log — 14 préfixes verbatim.

Inspiré de sellkit/tests/unit/telemetry/log.test.ts (156 lignes).
Tests purs: capture la sortie console et vérifie que chaque préfixe est présent.
"""

import io
from contextlib import redirect_stdout, redirect_stderr

import pytest

from hirekit.telemetry import log


def capture_stdout(fn):
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn()
    return buf.getvalue()


def capture_stderr(fn):
    buf = io.StringIO()
    with redirect_stderr(buf):
        fn()
    return buf.getvalue()


class TestTelemetryPrefixes:
    """14 préfixes verbatim — chaque fonction doit émettre son préfixe exact."""

    def test_1_msg_in_emits_msg_in(self):
        out = capture_stdout(lambda: log.msg_in("Nathan", "+33712345678", "Bonjour"))
        assert "📥 [MSG-IN]" in out
        assert "Nathan" in out
        assert "+33712345678" in out

    def test_2_objection_emits_objection(self):
        out = capture_stdout(
            lambda: log.objection("trop_cher", "llm", "Reformuler la valeur perçue.")
        )
        assert "🟡 [OBJECTION]" in out
        assert "trop_cher" in out
        assert "llm" in out

    def test_3_refusal_emits_refusal(self):
        out = capture_stdout(lambda: log.refusal("llm"))
        assert "🔴 [REFUSAL]" in out

    def test_4_closing_emits_closing(self):
        out = capture_stdout(lambda: log.closing("commitment_signal", "llm", "closed_won", True))
        assert "🟣 [CLOSING]" in out
        assert "commitment_signal" in out
        assert "closed_won" in out

    def test_4b_closing_first_interest(self):
        out = capture_stdout(lambda: log.closing_first_interest())
        assert "🟣 [CLOSING]" in out
        assert "First interest" in out

    def test_4c_closing_ignored(self):
        out = capture_stdout(lambda: log.closing_ignored("job_interest", 3))
        assert "🟣 [CLOSING]" in out
        assert "Ignored" in out

    def test_5_memory_emits_memory(self):
        out = capture_stdout(lambda: log.memory({"name": "Nathan", "experience": "aucune"}))
        assert "🧠 [MEMORY]" in out
        assert "name=Nathan" in out
        assert "experience=aucune" in out

    def test_5b_memory_empty_does_not_emit(self):
        out = capture_stdout(lambda: log.memory({}))
        assert out == ""

    def test_6_llm_calling_emits_llm(self):
        out = capture_stdout(lambda: log.llm_calling("gpt-4o", "+33712345678"))
        assert "🤖 [LLM]" in out
        assert "gpt-4o" in out

    def test_7_msg_out_emits_msg_out(self):
        out = capture_stdout(lambda: log.msg_out("Nathan", "Bonjour, comment allez-vous ?"))
        assert "📤 [MSG-OUT]" in out
        assert "Nathan" in out

    def test_8_llm_error_emits_error(self):
        out = capture_stderr(lambda: log.llm_error("+33712345678", Exception("timeout")))
        assert "❌ [LLM-ERROR]" in out
        assert "+33712345678" in out

    def test_8b_llm_error_empty(self):
        out = capture_stderr(lambda: log.llm_error_empty())
        assert "❌ [LLM-ERROR]" in out

    def test_9_conversion_link_new(self):
        out = capture_stdout(
            lambda: log.conversion_link("+33712345678", "https://t.me/app?start=abc123")
        )
        assert "🔗 [CONVERSION]" in out

    def test_9b_conversion_link_existing(self):
        out = capture_stdout(lambda: log.conversion_link("+33712345678", None))
        assert "🔗 [CONVERSION]" in out
        assert "déjà" in out.lower()

    def test_10_stage_update(self):
        out = capture_stdout(lambda: log.stage_update("+33712345678", "interested"))
        assert "📊 [STAGE]" in out
        assert "interested" in out

    def test_11_closing_fallback(self):
        out = capture_stdout(lambda: log.closing_fallback("Connection timeout"))
        assert "🟡 [CLOSING]" in out

    def test_12_memory_fallback(self):
        out = capture_stdout(lambda: log.memory_fallback("Connection timeout"))
        assert "🟡 [MEMORY]" in out

    def test_13_objection_fallback(self):
        out = capture_stdout(lambda: log.objection_fallback("Connection timeout"))
        assert "🟡 [OBJECTION]" in out
