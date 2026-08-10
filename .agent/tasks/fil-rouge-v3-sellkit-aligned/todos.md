# TODOs — Fil Rouge v3 (aligné sellkit)

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` fait + preuve · `❌` bloqué

## Phase 0 — Sauvegarder le plan
- [x] 0.1 Créer .agent/tasks/fil-rouge-v3-sellkit-aligned/PLAN.md
- [x] 0.2 Copier l'ancien dossier tâche depuis ai-teams-benchmark
- [x] 0.3 Rédiger todos.md (ce fichier)
- [x] 0.4 Rédiger insights.md (journal initial)

## Phase 1 — hirekit/pipeline/ (NOUVEAU)
- [x] 1.1 hirekit/pipeline/__init__.py
- [x] 1.2 hirekit/pipeline/qualification.py (FIELD_QUESTIONS, STAGE_LABELS, CLOSING_STAGES)
- [x] 1.3 hirekit/pipeline/objections.py (OBJECTION_CATALOG 8 types, detect_objection LLM+fallback)
- [x] 1.4 hirekit/pipeline/closing.py (ClosingType 5 signaux, STAGE_MAP, detect_closing LLM+fallback)
- [x] 1.5 hirekit/pipeline/memory.py (ProspectMemory, extract_memory, merge, count, next_missing, format)
- [x] 1.6 Commit 074b3d0

## Phase 2 — hirekit/deep_agent/ (NOUVEAU)
- [x] 2.1 hirekit/deep_agent/__init__.py
- [x] 2.2 hirekit/deep_agent/recruiter_agent.py (create_deep_agent 4 couches)
- [x] 2.3 hirekit/deep_agent/middleware.py (beforeModel + build_context_prompt)
- [x] 2.4 hirekit/deep_agent/harness_profile.py (register_harness_profile)
- [x] 2.5 Commit 9c2cd64

## Phase 3 — hirekit/crm/ + hirekit/telemetry/ (NOUVEAU)
- [x] 3.1 hirekit/crm/__init__.py
- [x] 3.2 hirekit/crm/types.py (STAGES, Stage, Candidate, Message)
- [x] 3.3 hirekit/crm/store.py (CrmStore SQLite WAL)
- [x] 3.4 hirekit/telemetry/__init__.py
- [x] 3.5 hirekit/telemetry/log.py (14 fonctions de log structuré)
- [x] 3.6 Commit f266fe9

## Phase 4 — .agent/ (NOUVEAU)
- [x] 4.1 .agent/memory/recruiter/AGENTS.md (règles globales)
- [x] 4.2 .agent/skills/recruiter/phase-first-contact/SKILL.md
- [x] 4.3 .agent/skills/recruiter/phase-qualification/SKILL.md
- [x] 4.4 .agent/skills/recruiter/phase-reformulation/SKILL.md
- [x] 4.5 .agent/skills/recruiter/phase-closing/SKILL.md
- [x] 4.6 .agent/skills/recruiter/phase-test-technique/SKILL.md
- [x] 4.7 Commit d33b12d

## Phase 5 — Atelier AT05 Deep Agents (NOUVEAU)
- [x] 5.1 Créer ateliers/atelier-05-deep-agents/ (dossier)
- [x] 5.2 GUIDE-ELEVE.md complet (mission, carnet de bord 7 concepts, mini-lab, bug hunt, checkpoints)
- [x] 5.3 exercice.py + solution.py
- [x] 5.4 bugs/ (3 patches + 3 tests + 3 explications)
- [x] 5.5 checkpoints/ (check_1.py + check_final.py)
- [x] 5.6 .claude/CLAUDE.md scope guard
- [x] 5.7 Commit 7247d73

## Phase 6 — Restructurer AT06 (Chatbots + Telegram + CRM)
- [x] 6.1 Mettre à jour ateliers/atelier-05-chatbot-code-review/GUIDE-ELEVE.md (aligné sellkit)
- [x] 6.2 Commit 86bf5e5

## Phase 7 — Atelier AT07 (Évaluation + Déploiement + E2E)
- [x] 7.1 Créer ateliers/atelier-07-eval-deploy/ (dossier)
- [x] 7.2 GUIDE-ELEVE.md (LangSmith, Recall@k, MRR, Docker, tests E2E)
- [x] 7.3 .claude/CLAUDE.md scope guard
- [x] 7.4 Commit 86bf5e5

## Phase 8 — tests/unit/ (pattern sellkit)
- [x] 8.1 tests/unit/__init__.py
- [x] 8.2 tests/unit/test_memory.py (merge, count, nextMissingField, 3 scénarios paramétrés)
- [x] 8.3 tests/unit/test_middleware.py (buildContextPrompt 9 combinaisons + read_skill 6 tests)
- [x] 8.4 tests/unit/test_skills.py (5 skills frontmatter, AGENTS.md, pas de conflit)
- [x] 8.5 tests/unit/test_telemetry.py (14 préfixes verbatim)
- [x] 8.6 tests/unit/test_crm.py (6 stages, get_or_create, update_stage, conversion_link idempotent, stats)
- [x] 8.7 Commit 996638a

## Phase 9 — tests/integration/ (pattern sellkit)
- [x] 9.1 tests/integration/__init__.py
- [x] 9.2 tests/integration/test_deep_agent.py (create_deep_agent + invoke, skip si pas de clé API)
- [x] 9.3 Commit d7fee50

## Phase 10 — tests/e2e/ (Playwright, pattern sellkit)
- [x] 10.1 tests/e2e/__init__.py
- [x] 10.2 tests/e2e/conftest.py (fixtures: app, db, api, log_file)
- [x] 10.3 tests/e2e/test_step1_conversation.py (DB vide, app accessible, CRM store, 14 préfixes)
- [x] 10.4 tests/e2e/test_step5_full_pipeline.py (3 scénarios, 13 étapes, stage transitions, CRM pipeline)
- [x] 10.5 tests/e2e/test_telegram_screening.py (screening 0→6, objection 8 types, closing 5 types, CRM)
- [x] 10.6 Commit d7fee50

## Phase 11 — Git + documentation
- [x] 11.1 Git commit à chaque phase (7 commits)
- [x] 11.2 insights.md mis à jour avec architecture finale
- [x] 11.3 todos.md mis à jour (ce fichier)
- [ ] 11.4 Git push final
- [ ] 11.5 Tag v3.0.0