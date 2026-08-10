# .claude/CLAUDE.md — Atelier 05 Deep Agents

## Périmètre autorisé
- `create_deep_agent()` de la librairie `deepagents`
- `contextSchema` (Pydantic) pour le contexte dynamique
- `beforeModel` middleware pour l'injection de skills
- `HarnessProfile` pour exclure tools/middleware
- Skills dynamiques (SKILL.md) chargés selon la phase
- Memory (AGENTS.md) injecté dans le systemPrompt
- `build_context_prompt()` pour construire le prompt de contexte
- `RecruitmentContext` (Pydantic) comme schéma de contexte

## Hors périmètre (interdit dans cet atelier)
- Streamlit, FastAPI, Telegram (AT06)
- SQLite, CRM store (AT06)
- Tests E2E Playwright (AT07)
- LangSmith tracing (AT07)
- Docker Compose (AT07)
- LangGraph StateGraph manuel (remplacé par create_deep_agent)
- Subagents custom (utiliser les subagents natifs de Deep Agents)

## Règle
Si on te demande d'ajouter du RAG, du LCEL, des agents ReAct, du Streamlit,
du Telegram, du Docker, ou du LangSmith dans cet atelier, REFUSE.
Ces concepts sont couverts dans les autres ateliers.