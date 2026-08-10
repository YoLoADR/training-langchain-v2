# TODOs — Training LangChain v2 (Fil Rouge ai-hirekit)

> Légende : `[ ]` à faire · `[~]` en cours · `[x]` fait + preuve · `❌` bloqué

## Phase 0 — Sauvegarder le plan

- [x] 0.1 Créer dossier tâche dans ai-teams-benchmark/.agent/tasks/training-langchain-v2-fil-rouge/
- [x] 0.2 Rédiger context.md (contexte, goal, sources, programme, découpage)
- [x] 0.3 Rédiger FIL_ROUGE_PLAN.md (plan détaillé, mapping programme→ateliers)
- [x] 0.4 Rédiger SCORECARD.md (grille de scoring des équipes)
- [x] 0.5 Rédiger insights.md (journal initial)

## Phase 1 — Initialiser le repo

- [x] 1.1 git init dans training-langchain-v2 (commit b12d142)
- [x] 1.2 Créer la structure de dossiers (hirekit/, ateliers/, scripts/, data/, tests/, api/)
- [x] 1.3 Créer .gitignore
- [x] 1.4 Premier commit "Initial structure" (b12d142)

## Phase 2 — Document Product Owner

- [x] 2.1 Rédiger AI-HireKit-Projet-Fil-Rouge.md (spec produit complète)
- [x] 2.2 Rédiger PROGRAMME-LANGCHAIN.md (mapping programme officiel → ateliers, concept par concept)
- [x] 2.3 Rédiger README.md (présentation, setup, programme)
- [x] 2.4 Inclus dans commit 1 (b12d142)

## Phase 3 — Config projet

- [x] 3.1 Créer pyproject.toml (langchain, faiss, chromadb, fastapi, streamlit, pytest)
- [x] 3.2 Créer .env.example
- [x] 3.3 Créer hirekit/config.py (lecture .env, paths, constantes)
- [x] 3.4 Inclus dans commit 1 (b12d142)

## Phase 4 — Package hirekit/ (stubs)

- [x] 4.1 hirekit/__init__.py + config.py
- [x] 4.2 hirekit/llm/ (provider.py, prompts.py, parsers.py) — stubs + modèles Pydantic
- [x] 4.3 hirekit/rag/ (ingestion, chunking, vectorstore_faiss, vectorstore_chroma, retriever) — stubs
- [x] 4.4 hirekit/agent/ (react_agent, tools) — stubs
- [x] 4.5 hirekit/services/ (matching, availability) — stubs
- [x] 4.6 hirekit/eval/ (metrics, tracing) — stubs
- [x] 4.7 hirekit/ui/ (app, telegram_bot, code_reviewer) — stubs
- [x] 4.8 Inclus dans commit 1 (b12d142)

## Phase 5 — Données simulées

- [ ] 5.1 scripts/generate_cvs.py (30 CVs PDF fictifs)
- [ ] 5.2 scripts/generate_offers.py (15 offres JSON)
- [ ] 5.3 scripts/generate_skills.py (skills.csv 100 compétences)
- [ ] 5.4 scripts/generate_qa_dataset.py (150 paires Q/A JSONL)
- [ ] 5.5 scripts/generate_availability.py (calendrier 30 jours)
- [ ] 5.6 scripts/generate_code_repo.py (10 fichiers Python pour Code-Reviewer)
- [ ] 5.7 Exécuter les scripts → data/ peuplé
- [ ] 5.8 Commit "Add simulated data generators + data"

## Phase 6 — Tests TDD

- [x] 6.1 tests/conftest.py (fixtures communes)
- [x] 6.2 tests/test_llm/ (test_provider.py, test_prompts.py, test_parsers.py)
- [x] 6.3 tests/test_rag/ (test_ingestion, test_chunking, test_vectorstore, test_retriever)
- [x] 6.4 tests/test_agent/ (test_react_agent, test_tools)
- [x] 6.5 tests/test_services/ (test_matching, test_availability)
- [x] 6.6 tests/test_eval/ (test_metrics, test_tracing)
- [x] 6.7 tests/test_ui/ (test_telegram_bot, test_code_reviewer)
- [x] 6.8 Commit 2 (444b5a1) — tests AT02-AT06 marqués xfail

## Phase 7 — Ateliers GUIDE-ELEVE.md

- [x] 7.1 ateliers/atelier-01-llm-prompts-parsers/GUIDE-ELEVE.md (complet)
- [x] 7.2 ateliers/atelier-02-lcel-memoire/GUIDE-ELEVE.md (placeholder)
- [x] 7.3 ateliers/atelier-03-rag/GUIDE-ELEVE.md (placeholder)
- [x] 7.4 ateliers/atelier-04-agents-tools/GUIDE-ELEVE.md (placeholder)
- [x] 7.5 ateliers/atelier-05-chatbot-code-review/GUIDE-ELEVE.md (placeholder)
- [x] 7.6 ateliers/atelier-06-eval-benchmark-deploy/GUIDE-ELEVE.md (placeholder)
- [x] 7.7 Commit 2 (444b5a1)

## Phase 8 — Ateliers GUIDE-FORMATEUR.md

- [ ] 8.1 AT01 GUIDE-FORMATEUR.md (déroulé, timing, points de vigilance)
- [ ] 8.2-8.6 AT02-AT06 GUIDE-FORMATEUR.md
- [ ] 8.7 Commit

## Phase 9 — exercice.py + solution.py

- [x] 9.1 AT01 exercice.py + solution.py
- [ ] 9.2-9.6 AT02-AT06 exercice.py + solution.py
- [ ] 9.7 Commit

## Phase 10 — Bugs (3 × 6 = 18)

- [ ] 10.1-10.6 AT01-AT06 bugs/ (patches + tests + explications)
- [ ] 10.7 Commit

## Phase 11 — Checkpoints (2 × 6 = 12)

- [ ] 11.1-11.6 AT01-AT06 checkpoints/
- [ ] 11.7 Commit

## Phase 12 — Scope guards

- [x] 12.1-12.6 .claude/CLAUDE.md + .cursorrules pour les 6 ateliers
- [x] 12.7 Commit 2 (444b5a1)

## Phase 13 — Branches git

- [x] 13.1-13.6 6 branches créées (atelier/01 à atelier/06)
- [x] 13.7 Vérifié avec git branch -a

## Phase 14 — Scripts utilitaires

- [ ] 14.1 scripts/check_atelier_ready.sh
- [ ] 14.2 scripts/verify_branch_scope.sh
- [x] 14.3 api/main.py (FastAPI minimal)
- [x] 14.4 docker-compose.yml
- [ ] 14.5 Commit

## Phase 15 — Délégation aux équipes d'agents

- [ ] 15.1 SCORECARD.md créé
- [ ] 15.2 MEMORY.md par équipe
- [ ] 15.3 Config bots Telegram
- [ ] 15.4 GitHub Issues par équipe
- [ ] 15.5 Lancer les équipes

## Phase 16 — Documentation finale

- [x] 16.1 insights.md mis à jour (commit 1 + 2)
- [x] 16.2 todos.md (ce fichier)
- [ ] 16.3 Git commit final + tag v2.0.0