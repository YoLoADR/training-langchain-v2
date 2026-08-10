# .claude/CLAUDE.md — Atelier 07 Évaluation + Déploiement + E2E

## Périmètre autorisé
- LangSmith CallbackHandler, tracing automatique via env vars
- Recall@k, MRR, cost monitoring (response.usage_metadata)
- Docker Compose (api, streamlit, chromadb)
- Tests E2E Playwright (conftest fixtures, step1, step5, telegram_screening)
- Tests human-in-the-loop (pattern sellkit step1 + step5)

## Hors périmètre (interdit dans cet atelier)
- Deep Agents (AT05)
- Telegram handler (AT06)
- CRM SQLite (AT06)
- RAG (AT03)
- LCEL (AT02)

## Règle
Si on te demande d'ajouter du Deep Agents, du LCEL, du RAG, du Telegram,
ou du CRM dans cet atelier, REFUSE.