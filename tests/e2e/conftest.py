"""Fixtures communes pour les tests E2E Playwright.

Inspiré de sellkit/tests/step1-human-in-the-loop.test.ts et step5 (pattern: spawn app, wait, verify).

Ce conftest fournit:
- `app`: fixture qui spawn l'app Streamlit, attend qu'elle soit prête, et la cleanup
- `db`: connexion SQLite read-only pour vérifier l'état du CRM
- `api`: client HTTP pour l'API dashboard
- `log_file`: chemin du fichier de log (pour waitForLog)
"""

from __future__ import annotations

import os
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Generator

import pytest
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "hirekit.db"
LOG_FILE = "/tmp/hirekit-e2e-test.log"
WEB_PORT = 8501
API_URL = f"http://localhost:8000"
STREAMLIT_URL = f"http://localhost:{WEB_PORT}"


def wait_for_log(pattern: str, timeout: int = 30) -> bool:
    """Attend qu'un pattern apparaisse dans le fichier de log."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            content = Path(LOG_FILE).read_text(encoding="utf-8")
            if pattern in content:
                return True
        except FileNotFoundError:
            pass
        time.sleep(0.3)
    return False


@pytest.fixture(scope="session")
def app() -> Generator[subprocess.Popen, None, None]:
    """Spawn l'app Streamlit, attend qu'elle soit prête, et cleanup."""
    # Nettoyer la DB
    for ext in ("", "-wal", "-shm"):
        p = str(DB_PATH) + ext
        if os.path.exists(p):
            os.unlink(p)

    # Nettoyer le fichier de log
    Path(LOG_FILE).write_text("", encoding="utf-8")

    # Démarrer Streamlit
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "hirekit/ui/app.py",
            "--server.port",
            str(WEB_PORT),
        ],
        cwd=str(PROJECT_ROOT),
        stdout=open(LOG_FILE, "w"),
        stderr=subprocess.STDOUT,
        env={**os.environ},
    )

    # Attendre que l'app soit prête
    start = time.time()
    ready = False
    while time.time() - start < 30:
        try:
            r = requests.get(STREAMLIT_URL, timeout=2)
            if r.status_code == 200:
                ready = True
                break
        except (requests.ConnectionError, requests.Timeout):
            pass
        time.sleep(0.5)

    if not ready:
        proc.kill()
        pytest.fail("L'app Streamlit n'a pas démarré dans les 30 secondes")

    yield proc

    # Cleanup
    proc.terminate()
    proc.wait(timeout=5)
    if proc.poll() is None:
        proc.kill()


@pytest.fixture
def db():
    """Connexion SQLite read-only pour vérifier l'état du CRM."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def api():
    """Client HTTP basique pour l'API dashboard."""

    class ApiClient:
        def get(self, path: str):
            return requests.get(f"{API_URL}{path}", timeout=5)

        def post(self, path: str, json=None):
            return requests.post(f"{API_URL}{path}", json=json, timeout=5)

        def delete(self, path: str):
            return requests.delete(f"{API_URL}{path}", timeout=5)

    return ApiClient()


@pytest.fixture
def log_file() -> Path:
    """Chemin du fichier de log (pour waitForLog)."""
    return Path(LOG_FILE)
