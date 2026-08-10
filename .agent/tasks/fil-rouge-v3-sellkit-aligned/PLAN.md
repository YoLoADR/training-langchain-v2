# Plan — Fil Rouge v3 (aligné sellkit)

> Formation LangChain 7 ateliers — miroir architecture sellkit
> Créé le 2026-08-10. Basé sur analyse sellkit + ai-hirekit + pre-training-rag.

## Contexte

Le projet training-langchain-v2 est une formation LangChain en 7 ateliers progressifs.
Le fil rouge = ai-hirekit (recruteur IA qui filtre les candidats via Telegram + CRM).

**Inspiration architecture** : `/Users/yohannravino/Factory/sellkit` (TypeScript, production-ready)
**Pattern pédagogique** : `/Users/yohannravino/Factory/pre-training-rag` (GUIDE-ELEVE.md structuré)
**Thème métier** : `/Users/yohannravino/Factory/ai-hirekit` (recrutement, cube, Telegram)

## État au 2026-08-10

Cuba (équipe benchmark, 77/100) a implémenté AT01-AT05 (6 ateliers originaux) :
- AT01: LLM + Prompts + Parsers ✅
- AT02: LCEL + Mémoire ✅
- AT03: RAG ✅
- AT04: Agents ReAct + Tools ✅
- AT05: Chatbots + Code Review ✅ (mais sans Deep Agents, sans CRM sellkit-style)

**Manque** : Deep Agents (AT05 nouveau), CRM pipeline, pipeline détection, tests E2E Playwright.

## 7 Ateliers (nouvel ordre)

| # | Atelier | Jour | Module | Inspiration sellkit |
|---|---|---|---|---|
| AT01 | LLM + Prompts + Output Parsers | J1 matin | `hirekit/llm/` | `src/llm/client.ts`, `src/pipeline/memory.ts:43-52` |
| AT02 | LCEL + Mémoire + Pipeline | J1 a.-m. | `hirekit/services/` + `hirekit/pipeline/` | `src/pipeline/memory.ts` complet |
| AT03 | RAG sur CVs | J2 matin | `hirekit/rag/` | (sellkit n'a pas RAG) |
| AT04 | Agents ReAct + Tools + Détection | J2 a.-m. | `hirekit/agent/` + `hirekit/pipeline/` | `src/pipeline/objections.ts`, `src/pipeline/closing.ts` |
| AT05 | Deep Agents | J3 matin | `hirekit/deep_agent/` + `.agent/` | `src/agent/deep-agent.ts`, `src/agent/middleware/`, `src/harness-profile.ts` |
| AT06 | Chatbots + Telegram + CRM | J3 a.-m. | `hirekit/ui/` + `hirekit/crm/` + `hirekit/telemetry/` | `src/telegram/handler.ts`, `src/crm/store.ts`, `src/web/server.ts` |
| AT07 | Évaluation + Déploiement + E2E | J4 matin | `hirekit/eval/` + `tests/e2e/` | `tests/step5-human-in-the-loop.test.ts` |

## Nouveaux modules à créer

### hirekit/pipeline/ (NOUVEAU — inspiré sellkit/src/pipeline/)
- `qualification.py` — FIELD_QUESTIONS (6 champs), STAGE_LABELS, CLOSING_STAGES
- `objections.py` — OBJECTION_CATALOG (8 types), detect_objection() LLM + fallback keyword
- `closing.py` — ClosingType (5 signaux), STAGE_MAP, detect_closing() LLM + fallback keyword
- `memory.py` — ProspectMemory, extract_memory() LLM, merge_memory(), count_fields(), next_missing_field(), format_for_prompt()

### hirekit/deep_agent/ (NOUVEAU — inspiré sellkit/src/agent/)
- `recruiter_agent.py` — create_deep_agent() 4 couches (systemPrompt + memory + skills + contextSchema)
- `middleware.py` — create_recruitment_context_middleware() beforeModel + build_context_prompt()
- `harness_profile.py` — register_harness_profile() excludedTools + excludedMiddleware

### hirekit/crm/ (NOUVEAU — inspiré sellkit/src/crm/)
- `types.py` — STAGES (6 stages), Stage, Candidate
- `store.py` — CrmStore SQLite (get_or_create, update_stage, add_message, set_qual_json, set_conversion_link, get_followup_due)

### hirekit/telemetry/ (NOUVEAU — inspiré sellkit/src/telemetry/)
- `log.py` — 14 fonctions de log structuré (📥, 🟡, 🔴, 🟣, 🧠, 🤖, 📤, ❌, 🔗, 📊)

### .agent/ (NOUVEAU — inspiré sellkit/.agent/)
- `memory/recruiter/AGENTS.md` — règles globales (langue, recadrage, URLs, rôle)
- `skills/recruiter/phase-first-contact/SKILL.md`
- `skills/recruiter/phase-qualification/SKILL.md`
- `skills/recruiter/phase-reformulation/SKILL.md`
- `skills/recruiter/phase-closing/SKILL.md`
- `skills/recruiter/phase-test-technique/SKILL.md`

### tests/ (restructuré — pattern sellkit)
- `tests/unit/` — tests purs (memory, middleware, skills, telemetry, crm)
- `tests/integration/` — tests avec LLM (deep_agent invoke)
- `tests/e2e/` — tests human-in-the-loop Playwright (step1, step5, telegram_screening)

## Phases d'exécution

| Phase | Action | Status |
|---|---|---|
| 0 | Sauvegarder ce plan | en cours |
| 1 | Créer hirekit/pipeline/ (qualification, objections, closing, memory) | à faire |
| 2 | Créer hirekit/deep_agent/ (recruiter_agent, middleware, harness_profile) | à faire |
| 3 | Créer hirekit/crm/ (types, store) + hirekit/telemetry/ (log) | à faire |
| 4 | Créer .agent/ (AGENTS.md + 5 SKILL.md) | à faire |
| 5 | Créer ateliers/atelier-05-deep-agents/ (GUIDE-ELEVE, exercice, solution, bugs, checkpoints) | à faire |
| 6 | Restructurer AT06 (Chatbots + Telegram + CRM — aligner handler.ts sellkit) | à faire |
| 7 | Créer AT07 (Évaluation + Déploiement + tests E2E Playwright) | à faire |
| 8 | Créer tests/unit/ (memory, middleware, skills, telemetry, crm) | à faire |
| 9 | Créer tests/integration/ (deep_agent invoke) | à faire |
| 10 | Créer tests/e2e/ (conftest, step1, step5, telegram_screening) | à faire |
| 11 | Git commit + push à chaque phase | continu |
| 12 | Documenter progression dans insights.md + todos.md | continu |