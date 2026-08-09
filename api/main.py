"""FastAPI — API REST pour ai-hirekit.

AT05/AT06 — Déploiement : FastAPI + Docker Compose.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="AI-HireKit API",
    description="Assistant IA pour recruteurs — Fil rouge formation LangChain",
    version="2.0.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "2.0.0"}


@app.post("/chat")
async def chat(message: str, mode: str = "llm_only") -> dict:
    """AT05 — endpoint de chat (llm_only, rag_only, agent)."""
    raise NotImplementedError("AT05 — implémentez /chat dans api/main.py")


@app.post("/match")
async def match(cv: str, offer: str) -> dict:
    """AT02 — endpoint de matching CV↔offre."""
    raise NotImplementedError("AT02 — implémentez /match dans api/main.py")
