"""Types CRM — stages et candidat.

Inspiration: sellkit/src/crm/types.ts

Pipeline: new → contacted → interested → qualified → closed_won/closed_lost
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Any


class Stage(str, Enum):
    """CRM pipeline stages (funnel)."""

    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    QUALIFIED = "qualified"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


STAGES = [s.value for s in Stage]

STAGE_LABELS: dict[str, str] = {
    "new": "New",
    "contacted": "Contacted",
    "interested": "Interested",
    "qualified": "Qualified",
    "closed_won": "Closed Won",
    "closed_lost": "Closed Lost",
}


@dataclass
class Candidate:
    """Un candidat dans le CRM (pipeline de recrutement)."""

    id: str
    phone: str
    first_name: str | None = None
    username: str | None = None
    stage: str = "new"
    last_message: str | None = None
    last_direction: str | None = None
    last_timestamp: int | None = None
    message_count: int = 0
    created_at: int = 0
    updated_at: int = 0
    tg_user_id: int | None = None
    followup_count: int = 0
    followup_last_sent: int | None = None
    followup_next_due: int | None = None
    conversion_link: str | None = None
    qual_json: str | None = None

    @classmethod
    def from_row(cls, row: dict) -> "Candidate":
        """Crée un Candidate depuis une ligne SQLite (dict)."""
        return cls(
            id=row["id"],
            phone=row["phone"],
            first_name=row.get("first_name"),
            username=row.get("username"),
            stage=row.get("stage", "new"),
            last_message=row.get("last_message"),
            last_direction=row.get("last_direction"),
            last_timestamp=row.get("last_timestamp"),
            message_count=row.get("message_count", 0),
            created_at=row.get("created_at", 0),
            updated_at=row.get("updated_at", 0),
            tg_user_id=row.get("tg_user_id"),
            followup_count=row.get("followup_count", 0),
            followup_last_sent=row.get("followup_last_sent"),
            followup_next_due=row.get("followup_next_due"),
            conversion_link=row.get("conversion_link"),
            qual_json=row.get("qual_json"),
        )


@dataclass
class Message:
    """Un message de conversation (pour l'historique)."""

    id: str
    prospect_id: str
    direction: str  # "in" ou "out"
    text: str
    timestamp: int
    objection: str | None = None
