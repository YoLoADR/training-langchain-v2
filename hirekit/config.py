"""Configuration centrale du package hirekit.

Lit les variables d'environnement depuis .env et expose des constantes.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ─── LLM Provider ───────────────────────────────────────────────────────────
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic")
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

# ─── Embeddings ─────────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)

# ─── LangSmith ──────────────────────────────────────────────────────────────
LANGSMITH_API_KEY: str | None = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "ai-hirekit")
LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"

# ─── Telegram ───────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")

# ─── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / os.getenv("DATA_DIR", "data")
CVS_DIR: Path = PROJECT_ROOT / os.getenv("CVS_DIR", "data/cvs")
OFFERS_DIR: Path = PROJECT_ROOT / os.getenv("OFFERS_DIR", "data/offers")
FAISS_INDEX_DIR: Path = PROJECT_ROOT / os.getenv("FAISS_INDEX_DIR", "data/faiss_index")
CHROMA_DB_DIR: Path = PROJECT_ROOT / os.getenv("CHROMA_DB_DIR", "data/chroma_db")
QA_DATASET_PATH: Path = DATA_DIR / "qa_dataset.jsonl"
SKILLS_CSV_PATH: Path = DATA_DIR / "skills.csv"
AVAILABILITY_PATH: Path = DATA_DIR / "availability.json"
