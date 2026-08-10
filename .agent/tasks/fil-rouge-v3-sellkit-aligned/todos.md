# TODOs — Fil Rouge v3 (aligné sellkit)

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` fait + preuve · `❌` bloqué

## Phase 0 — Sauvegarder le plan

- [x] 0.1 Créer .agent/tasks/fil-rouge-v3-sellkit-aligned/PLAN.md
- [x] 0.2 Copier l'ancien dossier tâche depuis ai-teams-benchmark
- [x] 0.3 Rédiger todos.md (ce fichier)
- [x] 0.4 Rédiger insights.md (journal initial)

## Phase 1 — hirekit/pipeline/ (NOUVEAU)

- [ ] 1.1 hirekit/pipeline/__init__.py
- [ ] 1.2 hirekit/pipeline/qualification.py (FIELD_QUESTIONS, STAGE_LABELS, CLOSING_STAGES)
- [ ] 1.3 hirekit/pipeline/objections.py (OBJECTION_CATALOG 8 types, detect_objection LLM+fallback)
- [ ] 1.4 hirekit/pipeline/closing.py (ClosingType 5 signaux, STAGE_MAP, detect_closing LLM+fallback)
- [ ] 1.5 hirekit/pipeline/memory.py (ProspectMemory, extract_memory, merge, count, next_missing, format)
- [ ] 1.6 Commit "AT: pipeline (qualification, objections, closing, memory)"

## Phase 2 — hirekit/deep_agent/ (NOUVEAU)

- [ ] 2.1 hirekit/deep_agent/__init__.py
- [ ] 2.2 hirekit/deep_agent/recruiter_agent.py (create_deep_agent 4 couches)
- [ ] 2.3 hirekit/deep_agent/middleware.py (beforeModel + build_context_prompt)
- [ ] 2.4 hirekit/deep_agent/harness_profile.py (register_harness_profile)
- [ ] 2.5 Commit "AT: deep_agent (recruiter_agent, middleware, harness_profile)"

## Phase 3 — hirekit/crm/ + hirekit/telemetry/ (NOUVEAU)

- [ ] 3.1 hirekit/crm/__init__.py
- [ ] 3.2 hirekit/crm/types.py (STAGES, Stage, Candidate)
- [ ] 3.3 hirekit/crm/store.py (CrmStore SQLite WAL)
- [ ] 3.4 hirekit/telemetry/__init__.py
- [ ] 3.5 hirekit/telemetry/log.py (14 fonctions de log structuré)
- [ ] 3.6 Commit "AT: crm + telemetry (SQLite pipeline, logs structurés)"

## Phase 4 — .agent/ (NOUVEAU)

- [ ] 4.1 .agent/memory/recruiter/AGENTS.md (règles globales)
- [ ] 4.2 .agent/skills/recruiter/phase-first-contact/SKILL.md
- [ ] 4.3 .agent/skills/recruiter/phase-qualification/SKILL.md
- [ ] 4.4 .agent/skills/recruiter/phase-reformulation/SKILL.md
- [ ] 4.5 .agent/skills/recruiter/phase-closing/SKILL.md
- [ ] 4.6 .agent/skills/recruiter/phase-test-technique/SKILL.md
- [ ] 4.7 Commit "AT: .agent (AGENTS.md + 5 SKILL.md)"

## Phase 5 — Atelier AT05 Deep Agents (NOUVEAU)

- [ ] 5.1 Créer ateliers/atelier-05-deep-agents/ (dossier)
- [ ] 5.2 GUIDE-ELEVE.md complet (mission, carnet de bord, mini-lab, bug hunt, checkpoints)
- [ ] 5.3 exercice.py + solution.py
- [ ] 5.4 bugs/ (3 patches + 3 tests + 3 explications)
- [ ] 5.5 checkpoints/ (check_1.py + check_final.py)
- [ ] 5.6 .claude/CLAUDE.md scope guard
- [ ] 5.7 Commit "AT05: Deep Agents atelier complet"

## Phase 6 — Restructurer AT06 (Chatbots + Telegram + CRM)

- [ ] 6.1 Mettre à jour hirekit/ui/telegram_bot.py (handler pattern sellkit: objection→closing→memory→CRM→agent→reply)
- [ ] 6.2 Mettre à jour hirekit/ui/app.py (dashboard CRM kanban)
- [ ] 6.3 Mettre à jour ateliers/atelier-06-*/GUIDE-ELEVE.md
- [ ] 6.4 Commit "AT06: Chatbots + Telegram + CRM aligné sellkit"

## Phase 7 — Atelier AT07 (Évaluation + Déploiement + E2E)

- [ ] 7.1 Créer ateliers/atelier-07-eval-deploy/ (dossier)
- [ ] 7.2 GUIDE-ELEVE.md (LangSmith, Recall@k, MRR, Docker, tests E2E)
- [ ] 7.3 exercice.py + solution.py
- [ ] 7.4 bugs/ + checkpoints/
- [ ] 7.5 Commit "AT07: Évaluation + Déploiement atelier"

## Phase 8 — tests/unit/ (pattern sellkit)

- [ ] 8.1 tests/unit/__init__.py
- [ ] 8.2 tests/unit/test_memory.py (merge, count, nextMissingField, 3 scénarios)
- [ ] 8.3 tests/unit/test_middleware.py (buildContextPrompt 9 combinaisons)
- [ ] 8.4 tests/unit/test_skills.py (5 skills frontmatter, AGENTS.md)
- [ ] 8.5 tests/unit/test_telemetry.py (14 préfixes verbatim)
- [ ] 8.6 tests/unit/test_crm.py (get_or_create, update_stage, conversion_link idempotent)
- [ ] 8.7 Commit "tests: unit (memory, middleware, skills, telemetry, crm)"

## Phase 9 — tests/integration/ (pattern sellkit)

- [ ] 9.1 tests/integration/__init__.py
- [ ] 9.2 tests/integration/test_deep_agent.py (create_deep_agent + invoke)
- [ ] 9.3 Commit "tests: integration (deep_agent)"

## Phase 10 — tests/e2e/ (Playwright, pattern sellkit)

- [ ] 10.1 tests/e2e/__init__.py
- [ ] 10.2 tests/e2e/conftest.py (fixtures: app, db, api, playwright)
- [ ] 10.3 tests/e2e/test_step1_conversation.py (3 échanges → DB + API + logs)
- [ ] 10.4 tests/e2e/test_step5_full_pipeline.py (13 étapes, 3 scénarios aléatoires)
- [ ] 10.5 tests/e2e/test_telegram_screening.py (candidat → screening → CRM)
- [ ] 10.6 Commit "tests: e2e Playwright (step1, step5, telegram_screening)"

## Phase 11 — Git + documentation

- [ ] 11.1 Git commit + push à chaque phase
- [ ] 11.2 insights.md mis à jour à chaque phase
- [ ] 11.3 todos.md mis à jour (ce fichier)
- [ ] 11.4 Tag v3.0.0 quand tout est fait