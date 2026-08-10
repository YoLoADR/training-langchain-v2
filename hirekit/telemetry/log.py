"""Logs structurés — 14 préfixes verbatim pour les tests E2E.

Inspiration: sellkit/src/telemetry/log.ts

Chaque fonction émet un préfixe spécifique parsé par les tests E2E
(step1, step5). Les préfixes sont EXACTS (verbatim) — ne pas les modifier.
"""

from __future__ import annotations

from typing import Any


def msg_in(name: str, phone: str, text: str) -> None:
    print(f"📥 [MSG-IN] {name} ({phone}): {text[:80]}")


def objection(key: str, source: str, tactic: str) -> None:
    print(f"  🟡 [OBJECTION] {key} ({source}) → {tactic[:60]}...")


def refusal(source: str) -> None:
    print(f"  🔴 [REFUSAL] Candidat demande opt-out ({source})")


def closing(
    closing_type: str, source: str, target_stage: str | None, should_send_link: bool
) -> None:
    link = " + lien" if should_send_link else ""
    print(f"  🟣 [CLOSING] {closing_type} ({source}) → stage: {target_stage or 'no change'}{link}")


def closing_first_interest() -> None:
    print("  🟣 [CLOSING] First interest — sending link but keeping stage")


def closing_ignored(closing_type: str, qual_count: int) -> None:
    print(
        f"  🟣 [CLOSING] Ignored {closing_type} (qualCount={qual_count}/6 < 6) — candidate not fully qualified"
    )


def memory(extracted: dict) -> None:
    if not extracted:
        return
    fields = ", ".join(f"{k}={v}" for k, v in extracted.items())
    print(f"  🧠 [MEMORY] Extracted: {fields}")


def llm_calling(model: str, phone: str) -> None:
    print(f"🤖 [LLM] Calling {model} for {phone}...")


def msg_out(name: str, text: str) -> None:
    print(f"📤 [MSG-OUT] → {name}: {text[:100]}")


def llm_error(phone: str, error: Exception) -> None:
    print(f"❌ [LLM-ERROR] {phone}: All retries + fallbacks failed: {error}")


def llm_error_empty() -> None:
    print("❌ [LLM-ERROR] Reply was empty — not sending to Telegram")


def conversion_link(phone: str, link: str | None) -> None:
    if link:
        print(f"  🔗 [CONVERSION] Lien généré pour {phone}: {link[:60]}...")
    else:
        print(f"  🔗 [CONVERSION] Lien déjà envoyé pour {phone}")


def stage_update(phone: str, stage: str) -> None:
    print(f"  📊 [STAGE] {phone} → {stage}")


def closing_fallback(error_msg: str) -> None:
    print(f"  🟡 [CLOSING] LLM detection failed, fallback: {error_msg[:60]}")


def memory_fallback(error_msg: str) -> None:
    print(f"  🟡 [MEMORY] Extraction failed: {error_msg[:60]}")


def objection_fallback(error_msg: str) -> None:
    print(f"  🟡 [OBJECTION] LLM detection failed, falling back to keywords: {error_msg[:80]}")
