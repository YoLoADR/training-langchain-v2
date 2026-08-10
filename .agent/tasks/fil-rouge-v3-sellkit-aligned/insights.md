# Insights — Fil Rouge v3 (aligné sellkit)

> Journal de progression du fil rouge LangChain, aligné sur l'architecture sellkit.

## 2026-08-10 — Phase 0 : Sauvegarder le plan

### Décisions prises

1. **Alignement sellkit** : training-langchain-v2 doit ressembler à sellkit sur le plan
   architectural (Deep Agents 4 couches, CRM pipeline, pipeline détection, tests E2E).
   sellkit est TypeScript — training-langchain-v2 est Python. On traduit les concepts,
   on ne copie pas le code.

2. **Nouvel ordre des ateliers** : AT04 ReAct → AT05 Deep Agents → AT06 Chatbots+CRM →
   AT07 Eval+E2E. Le Deep Agents arrive après ReAct.

3. **Nouveaux modules** : hirekit/pipeline/ (objections, closing, memory, qualification),
   hirekit/deep_agent/ (recruiter_agent, middleware, harness_profile),
   hirekit/crm/ (types, store SQLite), hirekit/telemetry/ (log structuré),
   .agent/ (AGENTS.md + 5 SKILL.md).

4. **Tests restructurés** : tests/unit/ (purs, pas LLM), tests/integration/ (avec LLM),
   tests/e2e/ (Playwright human-in-the-loop).

## 2026-08-10 — Phase 1-4 : Modules sellkit-aligned

### Phase 1 — hirekit/pipeline/ (commit 074b3d0)
- `qualification.py` : FIELD_QUESTIONS (6 champs), STAGE_LABELS, CLOSING_STAGES
- `objections.py` : OBJECTION_CATALOG (8 types), detect_objection() LLM + fallback keyword
- `closing.py` : ClosingType (5 signaux), STAGE_MAP, detect_closing() LLM + fallback keyword
- `memory.py` : ProspectMemory, extract_memory() LLM, merge, count, next_missing, format, serialize/parse

### Phase 2 — hirekit/deep_agent/ (commit 9c2cd64)
- `recruiter_agent.py` : create_deep_agent() 4 couches (systemPrompt + memory + skills + contextSchema)
- `middleware.py` : beforeModel + build_context_prompt() 9 combinaisons + read_skill_for_context()
- `harness_profile.py` : register_recruiter_harness_profile() excludedTools + excludedMiddleware

### Phase 3 — hirekit/crm/ + hirekit/telemetry/ (commit f266fe9)
- `crm/types.py` : STAGES (6 stages), Stage (Enum), Candidate (dataclass), Message (dataclass)
- `crm/store.py` : CrmStore SQLite WAL (get_or_create, update_stage, add_message, set_qual_json, set_conversion_link, get_followup_due, stats)
- `telemetry/log.py` : 14 fonctions de log structuré (📥, 🟡, 🔴, 🟣, 🧠, 🤖, 📤, ❌, 🔗, 📊)

### Phase 4 — .agent/ (commit d33b12d)
- `memory/recruiter/AGENTS.md` : règles globales (langue, recadrage, URLs, rôle)
- `skills/recruiter/phase-first-contact/SKILL.md` : premier contact (recadrage + démarrage)
- `skills/recruiter/phase-qualification/SKILL.md` : qualification (1 question à la fois)
- `skills/recruiter/phase-reformulation/SKILL.md` : reformulation + présentation test
- `skills/recruiter/phase-closing/SKILL.md` : closing (engagement, lien, appel, fin)
- `skills/recruiter/phase-test-technique/SKILL.md` : test technique (2 semaines, 150€, zones grises)

## 2026-08-10 — Phase 5-7 : Ateliers

### Phase 5 — AT05 Deep Agents (commit 7247d73)
- GUIDE-ELEVE.md complet (mission, carnet de bord 7 concepts, mini-lab, bug hunt 3 bugs, checkpoints, sprint/bonus, wrap-up)
- exercice.py (5 TODOs) + solution.py
- bugs/ (3 patches + 3 tests + 3 explications)
- checkpoints/ (check_1.py 3 QCM + check_final.py 5 QCM)
- .claude/CLAUDE.md scope guard

### Phase 6+7 — AT06 + AT07 (commit 86bf5e5)
- AT06 GUIDE-ELEVE.md restructuré (Chatbots + Telegram + CRM aligné sellkit)
- AT07 GUIDE-ELEVE.md créé (Eval + Deploy + E2E Playwright)
- AT07 .claude/CLAUDE.md scope guard

## 2026-08-10 — Phase 8-10 : Tests

### Phase 8 — tests/unit/ (commit 996638a)
- `test_memory.py` : merge, count, nextMissingField (CRITICAL tests), format, serialize/parse round-trip, 3 scénarios paramétrés (Nathan, Francis, Sarah)
- `test_middleware.py` : build_context_prompt 9 combinaisons + read_skill_for_context 6 tests (5 phases + refusal)
- `test_skills.py` : AGENTS.md règles globales, 5 skills frontmatter valide, pas de conflit skills/AGENTS.md, test technique key info
- `test_telemetry.py` : 14 préfixes verbatim (capture stdout/stderr)
- `test_crm.py` : 6 stages, get_or_create idempotent, update_stage, add_message, get_messages, set_conversion_link idempotent, stats, clear, delete

### Phase 9+10 — tests/integration/ + tests/e2e/ (commit d7fee50)
- `tests/integration/test_deep_agent.py` : create_deep_agent + invoke (skip si pas de clé API)
- `tests/e2e/conftest.py` : fixtures (app, db, api, log_file) — spawn Streamlit, wait, cleanup
- `tests/e2e/test_step1_conversation.py` : DB vide, app accessible, CRM store, 14 préfixes telemetry
- `tests/e2e/test_step5_full_pipeline.py` : 3 scénarios paramétrés (13 étapes), stage transitions, CRM pipeline new→closed_won
- `tests/e2e/test_telegram_screening.py` : screening complet 0→6 champs, objection detection 8 types, closing detection 5 types, CRM pipeline screening→closed_won

## 2026-08-10 — Correction alignement énoncés/code

### Écarts trouvés et corrigés (commit c7372c9)

1. **hirekit/eval/metrics.py** : stubs `NotImplementedError` → implémenté `compute_recall_at_k()`,
   `compute_mrr()`, `compute_cost()`, `evaluate_qa_dataset()` avec pricing par modèle
2. **hirekit/eval/tracing.py** : stub `NotImplementedError` → implémenté `get_langsmith_callback()`,
   `is_tracing_enabled()`, `enable_tracing()`, `get_run_tags()`
3. **hirekit/ui/telegram_bot.py** : ancien code Cuba (commandes /search, /match) → remplacé par
   le flux sellkit complet (objection→closing→memory→CRM→Deep Agent→reply) avec `handle_message()`
4. **hirekit/ui/app.py** : ajouté page "Pipeline CRM" kanban (colonnes par stage, stats, messages récents)
5. **atelier-06-eval-benchmark-deploy/** : dossier doublon supprimé (remplacé par atelier-07-eval-deploy)
6. **.gitignore** : ajouté .playwright-mcp/, .serena/, *.png, .opencode-edits.log

### Vérification finale

- 0 stub `NotImplementedError` dans hirekit/ (vérifié avec rg)
- Tous les tests (unit, integration, e2e) importent depuis les bons modules qui existent
- AT01-AT07 : chaque GUIDE-ELEVE référence des modules qui existent et sont implémentés
- AT05 Deep Agents : GUIDE-ELEVE référence hirekit/deep_agent/, .agent/ — tous présents
- AT06 Chatbots+CRM : GUIDE-ELEVE référence hirekit/ui/, hirekit/crm/, hirekit/telemetry/, hirekit/pipeline/ — tous présents et implémentés
- AT07 Eval+Deploy : GUIDE-ELEVE référence hirekit/eval/ — implémenté (plus de stubs)

```
hirekit/
├── config.py                    # Configuration (.env)
├── llm/                         # AT01 — LLMs, Prompts, Parsers
│   ├── provider.py
│   ├── prompts.py
│   └── parsers.py
├── services/                    # AT02 — LCEL, Mémoire
│   └── matching.py
├── rag/                         # AT03 — RAG
│   ├── ingestion.py
│   ├── chunking.py
│   ├── vectorstore_faiss.py
│   ├── vectorstore_chroma.py
│   └── retriever.py
├── agent/                       # AT04 — Agents ReAct + Tools
│   ├── react_agent.py
│   └── tools.py
├── pipeline/                    # NOUVEAU — Pipeline détection (inspiré sellkit)
│   ├── qualification.py
│   ├── objections.py
│   ├── closing.py
│   └── memory.py
├── deep_agent/                  # AT05 — Deep Agents 4 couches (inspiré sellkit)
│   ├── recruiter_agent.py
│   ├── middleware.py
│   └── harness_profile.py
├── crm/                         # NOUVEAU — CRM SQLite (inspiré sellkit)
│   ├── types.py
│   └── store.py
├── telemetry/                   # NOUVEAU — Logs structurés (inspiré sellkit)
│   └── log.py
├── ui/                          # AT06 — Chatbots, Telegram, CRM
│   ├── app.py
│   ├── telegram_bot.py
│   └── code_reviewer.py
└── eval/                        # AT07 — Évaluation, Déploiement
    ├── metrics.py
    └── tracing.py

.agent/                          # NOUVEAU — Memory + Skills (inspiré sellkit)
├── memory/recruiter/AGENTS.md
└── skills/recruiter/
    ├── phase-first-contact/SKILL.md
    ├── phase-qualification/SKILL.md
    ├── phase-reformulation/SKILL.md
    ├── phase-closing/SKILL.md
    └── phase-test-technique/SKILL.md

ateliers/
├── atelier-01-llm-prompts-parsers/
├── atelier-02-lcel-memoire/
├── atelier-03-rag/
├── atelier-04-agents-tools/
├── atelier-05-deep-agents/      # NOUVEAU
├── atelier-05-chatbot-code-review/ # → devient AT06
├── atelier-06-eval-benchmark-deploy/ # → devient AT07
└── atelier-07-eval-deploy/      # NOUVEAU

tests/
├── unit/                        # Tests purs (pas LLM, pas réseau)
│   ├── test_memory.py
│   ├── test_middleware.py
│   ├── test_skills.py
│   ├── test_telemetry.py
│   └── test_crm.py
├── integration/                 # Tests avec LLM
│   └── test_deep_agent.py
├── e2e/                         # Tests Playwright human-in-the-loop
│   ├── conftest.py
│   ├── test_step1_conversation.py
│   ├── test_step5_full_pipeline.py
│   └── test_telegram_screening.py
└── (tests existants Cuba: test_llm/, test_rag/, test_agent/, test_services/, test_eval/, test_ui/)
```