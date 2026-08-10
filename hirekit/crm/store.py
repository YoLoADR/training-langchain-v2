"""CRM Store — SQLite-backed candidate store.

Inspiration: sellkit/src/crm/store.ts

SQLite avec WAL pour accès concurrent (dashboard lit pendant que le bot écrit).
Pipeline: new → contacted → interested → qualified → closed_won/closed_lost
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any

from hirekit.crm.types import Candidate, Message, Stage
from hirekit.config import DATA_DIR

DB_PATH = DATA_DIR / "hirekit.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS prospects (
    id            TEXT PRIMARY KEY,
    phone         TEXT UNIQUE NOT NULL,
    first_name    TEXT,
    username      TEXT,
    stage         TEXT NOT NULL DEFAULT 'new',
    last_message  TEXT,
    last_direction TEXT,
    last_timestamp INTEGER,
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     INTEGER NOT NULL,
    updated_at     INTEGER NOT NULL,
    tg_user_id     INTEGER,
    followup_count  INTEGER NOT NULL DEFAULT 0,
    followup_last_sent INTEGER,
    followup_next_due   INTEGER,
    conversion_link    TEXT,
    qual_json          TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id           TEXT PRIMARY KEY,
    prospect_id  TEXT NOT NULL REFERENCES prospects(id),
    direction    TEXT NOT NULL CHECK(direction IN ('in','out')),
    text         TEXT NOT NULL,
    timestamp    INTEGER NOT NULL,
    objection    TEXT
);

CREATE INDEX IF NOT EXISTS idx_prospects_stage ON prospects(stage);
CREATE INDEX IF NOT EXISTS idx_messages_prospect ON messages(prospect_id);
CREATE INDEX IF NOT EXISTS idx_prospects_followup ON prospects(followup_next_due);
"""


class CrmStore:
    """SQLite-backed CRM store with WAL mode."""

    def __init__(self, db_path: str | Path | None = None):
        path = str(db_path or DB_PATH)
        path = path.replace("file:", "").lstrip("./")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db: sqlite3.Connection = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode = WAL")
        self.db.executescript(SCHEMA_SQL)
        self._migrate()

    def _migrate(self) -> None:
        """Add missing columns to existing DBs."""
        cols = {row["name"] for row in self.db.execute("PRAGMA table_info(prospects)")}
        additions = {
            "tg_user_id": "INTEGER",
            "followup_count": "INTEGER NOT NULL DEFAULT 0",
            "followup_last_sent": "INTEGER",
            "followup_next_due": "INTEGER",
            "conversion_link": "TEXT",
            "qual_json": "TEXT",
        }
        for col, type_ in additions.items():
            if col not in cols:
                self.db.execute(f"ALTER TABLE prospects ADD COLUMN {col} {type_}")

        msg_cols = {row["name"] for row in self.db.execute("PRAGMA table_info(messages)")}
        if "objection" not in msg_cols:
            self.db.execute("ALTER TABLE messages ADD COLUMN objection TEXT")

    def get_or_create(
        self,
        phone: str,
        opts: dict | None = None,
    ) -> Candidate:
        """Get existing candidate or create new one."""
        existing = self.db.execute("SELECT * FROM prospects WHERE phone = ?", (phone,)).fetchone()
        if existing:
            return Candidate.from_row(dict(existing))

        now = int(time.time() * 1000)
        cid = str(uuid.uuid4())
        self.db.execute(
            "INSERT INTO prospects (id, phone, first_name, username, stage, created_at, updated_at, tg_user_id) "
            "VALUES (?, ?, ?, ?, 'new', ?, ?, ?)",
            (
                cid,
                phone,
                (opts or {}).get("first_name"),
                (opts or {}).get("username"),
                now,
                now,
                (opts or {}).get("tg_user_id"),
            ),
        )
        self.db.commit()
        result = self.get(phone)
        assert result is not None, "Candidate should exist after insert"
        return result

    def get(self, phone: str) -> Candidate | None:
        row = self.db.execute("SELECT * FROM prospects WHERE phone = ?", (phone,)).fetchone()
        return Candidate.from_row(dict(row)) if row else None

    def get_all(self) -> list[Candidate]:
        rows = self.db.execute("SELECT * FROM prospects ORDER BY updated_at DESC").fetchall()
        return [Candidate.from_row(dict(r)) for r in rows]

    def update_stage(self, phone: str, stage: str) -> None:
        self.db.execute(
            "UPDATE prospects SET stage = ?, updated_at = ? WHERE phone = ?",
            (stage, int(time.time() * 1000), phone),
        )
        self.db.commit()

    def update_info(self, phone: str, opts: dict) -> None:
        sets, args = [], []
        for key in ("first_name", "username", "tg_user_id"):
            if key in opts:
                sets.append(f"{key} = ?")
                args.append(opts[key])
        if not sets:
            return
        sets.append("updated_at = ?")
        args.append(int(time.time() * 1000))
        args.append(phone)
        self.db.execute(f"UPDATE prospects SET {', '.join(sets)} WHERE phone = ?", args)
        self.db.commit()

    def add_message(
        self, phone: str, direction: str, text: str, objection: str | None = None
    ) -> None:
        candidate = self.get_or_create(phone)
        mid = str(uuid.uuid4())
        ts = int(time.time() * 1000)
        self.db.execute(
            "INSERT INTO messages (id, prospect_id, direction, text, timestamp, objection) VALUES (?, ?, ?, ?, ?, ?)",
            (mid, candidate.id, direction, text, ts, objection),
        )
        if direction == "in":
            self.db.execute(
                "UPDATE prospects SET last_message = ?, last_direction = ?, last_timestamp = ?, "
                "message_count = message_count + 1, updated_at = ?, "
                "followup_count = 0, followup_last_sent = NULL, followup_next_due = NULL WHERE phone = ?",
                (text, direction, ts, ts, phone),
            )
        else:
            self.db.execute(
                "UPDATE prospects SET last_message = ?, last_direction = ?, last_timestamp = ?, "
                "message_count = message_count + 1, updated_at = ? WHERE phone = ?",
                (text, direction, ts, ts, phone),
            )
        self.db.commit()

    def get_messages(self, phone: str) -> list[Message]:
        candidate = self.get(phone)
        if not candidate:
            return []
        rows = self.db.execute(
            "SELECT * FROM messages WHERE prospect_id = ? ORDER BY timestamp ASC",
            (candidate.id,),
        ).fetchall()
        return [Message(**dict(r)) for r in rows]

    def get_recent_messages(self, limit: int = 50) -> list[dict]:
        rows = self.db.execute(
            "SELECT p.phone, p.first_name, m.direction, m.text, m.timestamp "
            "FROM messages m JOIN prospects p ON p.id = m.prospect_id "
            "ORDER BY m.timestamp DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_followup_due(self, max_relances: int = 2) -> list[Candidate]:
        now = int(time.time() * 1000)
        rows = self.db.execute(
            "SELECT * FROM prospects WHERE last_direction = 'out' "
            "AND followup_next_due IS NOT NULL AND followup_next_due <= ? "
            "AND followup_count < ? AND stage NOT IN ('closed_won', 'closed_lost') "
            "ORDER BY followup_next_due ASC",
            (now, max_relances),
        ).fetchall()
        return [Candidate.from_row(dict(r)) for r in rows]

    def mark_followup_sent(self, phone: str) -> None:
        candidate = self.get(phone)
        if not candidate:
            return
        new_count = candidate.followup_count + 1
        now = int(time.time() * 1000)
        self.db.execute(
            "UPDATE prospects SET followup_count = ?, followup_last_sent = ?, updated_at = ? WHERE phone = ?",
            (new_count, now, now, phone),
        )
        self.db.commit()

    def set_conversion_link(self, phone: str, base_url: str = "https://t.me/hirekit") -> str:
        """Generate and store a conversion link (idempotent)."""
        existing = self.get_conversion_link(phone)
        if existing:
            return existing

        hash_str = hashlib.sha256(f"{phone}{time.time()}".encode()).hexdigest()[:16]
        link = f"{base_url}?start={hash_str}"
        self.db.execute(
            "UPDATE prospects SET conversion_link = ?, updated_at = ? WHERE phone = ?",
            (link, int(time.time() * 1000), phone),
        )
        self.db.commit()
        return link

    def get_conversion_link(self, phone: str) -> str | None:
        candidate = self.get(phone)
        return candidate.conversion_link if candidate else None

    def get_qual_json(self, phone: str) -> str | None:
        candidate = self.get(phone)
        return candidate.qual_json if candidate else None

    def set_qual_json(self, phone: str, json_str: str) -> None:
        self.db.execute(
            "UPDATE prospects SET qual_json = ?, updated_at = ? WHERE phone = ?",
            (json_str, int(time.time() * 1000), phone),
        )
        self.db.commit()

    def clear_messages(self, phone: str) -> None:
        candidate = self.get(phone)
        if not candidate:
            return
        self.db.execute("DELETE FROM messages WHERE prospect_id = ?", (candidate.id,))
        self.db.execute(
            "UPDATE prospects SET last_message = NULL, last_direction = NULL, "
            "last_timestamp = NULL, message_count = 0, updated_at = ?, "
            "followup_count = 0, followup_last_sent = NULL, followup_next_due = NULL WHERE phone = ?",
            (int(time.time() * 1000), phone),
        )
        self.db.commit()

    def delete_candidate(self, phone: str) -> None:
        candidate = self.get(phone)
        if not candidate:
            return
        self.db.execute("DELETE FROM messages WHERE prospect_id = ?", (candidate.id,))
        self.db.execute("DELETE FROM prospects WHERE id = ?", (candidate.id,))
        self.db.commit()

    def stats(self) -> dict:
        total = self.db.execute("SELECT COUNT(*) as c FROM prospects").fetchone()["c"]
        total_msgs = self.db.execute("SELECT COUNT(*) as c FROM messages").fetchone()["c"]
        by_stage_rows = self.db.execute(
            "SELECT stage, COUNT(*) as c FROM prospects GROUP BY stage"
        ).fetchall()
        by_stage = {r["stage"]: r["c"] for r in by_stage_rows}
        return {"total_candidates": total, "total_messages": total_msgs, "by_stage": by_stage}

    def close(self) -> None:
        self.db.close()


_store: CrmStore | None = None


def get_store() -> CrmStore:
    global _store
    if _store is None:
        _store = CrmStore()
    return _store


crm = {
    "get_or_create": lambda phone, opts=None: get_store().get_or_create(phone, opts),
    "get": lambda phone: get_store().get(phone),
    "get_all": lambda: get_store().get_all(),
    "update_stage": lambda phone, stage: get_store().update_stage(phone, stage),
    "update_info": lambda phone, opts: get_store().update_info(phone, opts),
    "add_message": lambda phone, direction, text, objection=None: get_store().add_message(
        phone, direction, text, objection
    ),
    "get_messages": lambda phone: get_store().get_messages(phone),
    "get_recent_messages": lambda limit=50: get_store().get_recent_messages(limit),
    "clear_messages": lambda phone: get_store().clear_messages(phone),
    "delete_candidate": lambda phone: get_store().delete_candidate(phone),
    "get_followup_due": lambda max_relances=2: get_store().get_followup_due(max_relances),
    "mark_followup_sent": lambda phone: get_store().mark_followup_sent(phone),
    "set_conversion_link": lambda phone, base_url="https://t.me/hirekit": (
        get_store().set_conversion_link(phone, base_url)
    ),
    "get_conversion_link": lambda phone: get_store().get_conversion_link(phone),
    "get_qual_json": lambda phone: get_store().get_qual_json(phone),
    "set_qual_json": lambda phone, json_str: get_store().set_qual_json(phone, json_str),
    "stats": lambda: get_store().stats(),
    "close": lambda: (get_store().close(), None)[1],
}
