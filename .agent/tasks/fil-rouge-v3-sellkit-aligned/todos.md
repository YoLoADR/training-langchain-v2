# TODOs — Fil Rouge v3 (aligné sellkit)

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` fait + preuve · `❌` bloqué
> Dernière mise à jour : 2026-08-10 (après corrections alignement + documentation raisonnement)

## Phase 0 — Sauvegarder le plan
- [x] 0.1 Créer .agent/tasks/fil-rouge-v3-sellkit-aligned/PLAN.md
- [x] 0.2 Copier l'ancien dossier tâche depuis ai-teams-benchmark
- [x] 0.3 Rédiger todos.md (ce fichier)
- [x] 0.4 Rédiger insights.md (journal initial avec raisonnement)

## Phase 1 — hirekit/pipeline/ (NOUVEAU)
- [x] 1.1 hirekit/pipeline/__init__.py
- [x] 1.2 hirekit/pipeline/qualification.py (FIELD_QUESTIONS 6 champs, STAGE_LABELS, CLOSING_STAGES)
- [x] 1.3 hirekit/pipeline/objections.py (OBJECTION_CATALOG 8 types, detect_sync LLM+fallback keyword)
- [x] 1.4 hirekit/pipeline/closing.py (ClosingType 5 signaux, STAGE_MAP, detect_closing_sync LLM+fallback)
- [x] 1.5 hirekit/pipeline/memory.py (ProspectMemory, extract_memory_sync, merge, count, next_missing, format, serialize/parse)
- [x] 1.6 Commit 074b3d0

## Phase 2 — hirekit/deep_agent/ (NOUVEAU)
- [x] 2.1 hirekit/deep_agent/__init__.py
- [x] 2.2 hirekit/deep_agent/recruiter_agent.py (create_deep_agent 4 couches, run_deep_turn)
- [x] 2.3 hirekit/deep_agent/middleware.py (RecruitmentContext, beforeModel, build_context_prompt 9 combos, read_skill_for_context)
- [x] 2.4 hirekit/deep_agent/harness_profile.py (register_recruiter_harness_profile excludedTools)
- [x] 2.5 Commit 9c2cd64

## Phase 3 — hirekit/crm/ + hirekit/telemetry/ (NOUVEAU)
- [x] 3.1 hirekit/crm/__init__.py
- [x] 3.2 hirekit/crm/types.py (STAGES 6 stages, Stage Enum, Candidate dataclass, Message dataclass)
- [x] 3.3 hirekit/crm/store.py (CrmStore SQLite WAL, 15 méthodes, migrations auto)
- [x] 3.4 hirekit/telemetry/__init__.py
- [x] 3.5 hirekit/telemetry/log.py (17 fonctions de log, 14 préfixes verbatim)
- [x] 3.6 Commit f266fe9

## Phase 4 — .agent/ (NOUVEAU)
- [x] 4.1 .agent/memory/recruiter/AGENTS.md (4 règles globales: langue, recadrage, URLs, rôle)
- [x] 4.2 .agent/skills/recruiter/phase-first-contact/SKILL.md (recadrage + démarrage)
- [x] 4.3 .agent/skills/recruiter/phase-qualification/SKILL.md (1 question à la fois, pas de test)
- [x] 4.4 .agent/skills/recruiter/phase-reformulation/SKILL.md (résumé 6 infos + présentation test)
- [x] 4.5 .agent/skills/recruiter/phase-closing/SKILL.md (engagement, lien, appel, fin)
- [x] 4.6 .agent/skills/recruiter/phase-test-technique/SKILL.md (2 semaines, 150€, zones grises)
- [x] 4.7 Commit d33b12d

## Phase 5 — Atelier AT05 Deep Agents (NOUVEAU)
- [x] 5.1 Créer ateliers/atelier-05-deep-agents/ (dossier + bugs/ + checkpoints/ + .claude/)
- [x] 5.2 GUIDE-ELEVE.md complet (mission, carnet de bord 7 concepts, mini-lab, bug hunt 3 bugs, checkpoints 3+5 QCM, sprint/bonus, wrap-up 10 questions)
- [x] 5.3 exercice.py (5 TODOs) + solution.py (import depuis hirekit/)
- [x] 5.4 bugs/ (v1 skills inversés, v2 AGENTS.md manquant, v3 opt-out non géré + 3 tests + 3 explications)
- [x] 5.5 checkpoints/ (check_1.py 3 QCM mi-atelier + check_final.py 5 QCM fin)
- [x] 5.6 .claude/CLAUDE.md scope guard (Deep Agents autorisé, Streamlit/Telegram/Docker interdit)
- [x] 5.7 Commit 7247d73

## Phase 6 — Restructurer AT06 (Chatbots + Telegram + CRM)
- [x] 6.1 Mettre à jour ateliers/atelier-05-chatbot-code-review/GUIDE-ELEVE.md (aligné sellkit: flux objection→closing→memory→CRM→agent→reply)
- [x] 6.2 Commit 86bf5e5

## Phase 7 — Atelier AT07 (Évaluation + Déploiement + E2E)
- [x] 7.1 Créer ateliers/atelier-07-eval-deploy/ (dossier + .claude/)
- [x] 7.2 GUIDE-ELEVE.md (LangSmith, Recall@k, MRR, Docker, tests E2E Playwright)
- [x] 7.3 .claude/CLAUDE.md scope guard (Eval/Docker/E2E autorisé, Deep Agents/Telegram/CRM interdit)
- [x] 7.4 Commit 86bf5e5

## Phase 8 — tests/unit/ (pattern sellkit)
- [x] 8.1 tests/unit/__init__.py
- [x] 8.2 tests/unit/test_memory.py (5 classes: merge, count, nextMissingField CRITICAL, serialize/parse, format, 3 scénarios paramétrés Nathan/Francis/Sarah)
- [x] 8.3 tests/unit/test_middleware.py (buildContextPrompt 9 combinaisons + read_skill_for_context 6 tests)
- [x] 8.4 tests/unit/test_skills.py (AGENTS.md règles, 5 skills frontmatter, pas de conflit, test technique key info)
- [x] 8.5 tests/unit/test_telemetry.py (17 tests, capture stdout/stderr, 14 préfixes verbatim)
- [x] 8.6 tests/unit/test_crm.py (TestStages 3 tests + TestCrmStore 14 tests: get_or_create, idempotent, update_stage, add_message, conversion_link, qual_json, stats, clear, delete)
- [x] 8.7 Commit 996638a

## Phase 9 — tests/integration/ (pattern sellkit)
- [x] 9.1 tests/integration/__init__.py
- [x] 9.2 tests/integration/test_deep_agent.py (3 tests: agent créé, tour minimal, tour qualification — skip si pas de clé API)
- [x] 9.3 Commit d7fee50

## Phase 10 — tests/e2e/ (Playwright, pattern sellkit)
- [x] 10.1 tests/e2e/__init__.py
- [x] 10.2 tests/e2e/conftest.py (fixtures: app spawn Streamlit + wait + cleanup, db SQLite read-only, api HTTP, log_file)
- [x] 10.3 tests/e2e/test_step1_conversation.py (5 tests: DB vide, app accessible, CRM store, logs, 14 préfixes telemetry)
- [x] 10.4 tests/e2e/test_step5_full_pipeline.py (3 scénarios paramétrés 13 étapes, stage transitions, CRM pipeline new→closed_won)
- [x] 10.5 tests/e2e/test_telegram_screening.py (screening 0→6 champs, objection 8 types, closing 5 types, CRM pipeline)
- [x] 10.6 Commit d7fee50

## Phase 11 — Git + documentation
- [x] 11.1 Git commit à chaque phase (12 commits au total)
- [x] 11.2 insights.md mis à jour avec raisonnement complet (pas juste le "quoi" mais le "pourquoi")
- [x] 11.3 todos.md mis à jour (ce fichier)
- [x] 11.4 Git push final (fe5fd0f)
- [ ] 11.5 Tag v3.0.0 (à faire quand l'utilisateur valide)

## Phase 12 — Correction alignement énoncés/code (post-implémentation)
- [x] 12.1 hirekit/eval/metrics.py: stubs → implémenté (compute_recall_at_k, compute_mrr, compute_cost, evaluate_qa_dataset + MODEL_PRICING)
- [x] 12.2 hirekit/eval/tracing.py: stub → implémenté (get_langsmith_callback, is_tracing_enabled, enable_tracing, get_run_tags)
- [x] 12.3 hirekit/ui/telegram_bot.py: ancien code Cuba → flux sellkit (handle_message objection→closing→memory→CRM→Deep Agent→reply)
- [x] 12.4 hirekit/ui/app.py: ajout page "Pipeline CRM" kanban (colonnes par stage, stats, messages récents)
- [x] 12.5 atelier-06-eval-benchmark-deploy/: doublon supprimé
- [x] 12.6 .gitignore: ajouté .playwright-mcp/, .serena/, *.png, .opencode-edits.log
- [x] 12.7 Commit c7372c9

## Phase 13 — Documentation du raisonnement
- [x] 13.1 PLAN.md réécrit avec sections 1-7 (contexte, erreurs, sources, raisonnement architectural, modules, phases, corrections)
- [x] 13.2 insights.md réécrit avec raisonnement complet (erreurs, découverte sellkit, décisions architecturales, leçons apprises)
- [x] 13.3 todos.md mis à jour avec descriptions détaillées et commit hashes

## Reste à faire

- [ ] Tag v3.0.0 (quand l'utilisateur valide)
- [ ] Délégation à Cuba pour les ateliers AT06 et AT07 (exercice.py, solution.py, bugs, checkpoints)
- [ ] Tests Playwright visualisables sur l'ordi de l'utilisateur (nécessite pip install pytest-playwright + playwright install)