# Insights — Training LangChain v2 (Fil Rouge ai-hirekit)

> Journal de progression du reverse-engineering de ai-hirekit en fil rouge LangChain.

## 2026-08-09 — Phase 0 : Sauvegarder le plan

### Décisions prises

1. **Thème** : ai-hirekit = assistant IA recruteur (recrutement/hiring). Le projet
   original (publication d'offres sur sites africains via Hermes+Playwright) n'est pas
   un projet LangChain. On garde le thème métier (recrutement) mais on réimplémente
   en LangChain pour la formation.

2. **Reverse-engineering** : on part du projet final (assistant recruteur LangChain
   complet) et on le découpe à l'envers en 6 ateliers progressifs. Chaque atelier
   correspond à une demi-journée du programme Ambient IT.

3. **Mapping programme** : vérifié concept par concept contre le programme officiel
   (https://www.ambient-it.net/formation/langchain/). Corrections apportées :
   - AT01 : ajouté ExampleSelector (sélecteurs d'exemples) + distinction LLMs vs Chat Models
   - AT02 : ajouté Persistence et variables d'état (RunnablePassthrough.assign)
   - AT03 : repositionné le Retriever comme outil anti-hallucination (pas juste métrique)
   - AT04 : ajouté code execution (PythonREPLTool) + recherches web comme atelier principal
   - AT05 : changé OCR → audio/vocal (le programme dit "multimodal audio/vocal")
   - AT06 : ajouté benchmarking des agents (pas seulement VectorDB) + monitoring coûts

4. **TDD** : chaque module a ses tests écrits avant l'implémentation. Sur les branches
   précoces, les tests des modules non implémentés sont skip/xfail.

5. **Délégation** : 3 équipes d'agents IA (pattern ai-teams-benchmark v3.1). Cuba s'occupe
   de hirekit/llm/ + services/ (AT01-02), Haiti de hirekit/rag/ + agent/ (AT03-04),
   Guyane de hirekit/ui/ + eval/ + api/ (AT05-06).

### Leçons apprises du premier plan (à éviter)

- Ne pas calquer la structure RAFT de HomeButler (fine-tuning, RAFT) — le programme
  LangChain est différent (LCEL, Output Parsers, Code Analysis, pas de fine-tuning)
- Ne pas survoler le programme officiel — vérifier chaque concept mot à mot
- Ne pas inventer un projet de zéro — reverse-engineer le projet existant
- Ne pas oublier le TDD — c'est une demande explicite de l'utilisateur

## 2026-08-09 — Phase 1-4 : Repo + spec + stubs + tests

### Commit 1 (b12d142) — Initial structure
- git init dans training-langchain-v2
- AI-HireKit-Projet-Fil-Rouge.md : spec produit complète (personas, US, archi, stack)
- PROGRAMME-LANGCHAIN.md : mapping concept par concept du programme Ambient IT
- hirekit/ package avec stubs NotImplementedError (llm/, rag/, agent/, services/, eval/, ui/)
- pyproject.toml (langchain, faiss, chromadb, fastapi, streamlit, pytest)
- .env.example, .gitignore, docker-compose.yml, api/main.py (FastAPI minimal)

### Commit 2 (444b5a1) — Ateliers + tests TDD
- 6 dossiers d'ateliers créés (bugs/, checkpoints/, .claude/)
- AT01 GUIDE-ELEVE.md complet (mission, carnet de bord, bug hunt, sprint/bonus, quiz 10Q)
- AT01 exercice.py (squelette à TODOs) + solution.py (référence)
- AT01 .claude/CLAUDE.md scope guard (bloquent LCEL, RAG, agents...)
- AT02-AT06 GUIDE-ELEVE.md placeholders + scope guards
- tests/ TDD scaffolding (14 fichiers de tests)
  - test_llm/test_provider.py, test_parsers.py, test_prompts.py (AT01)
  - test_rag/test_ingestion.py, test_chunking.py, test_vectorstore.py, test_retriever.py (AT03)
  - test_agent/test_tools.py, test_react_agent.py (AT04)
  - test_services/test_matching.py, test_availability.py (AT02/AT04)
  - test_eval/test_metrics.py, test_tracing.py (AT06)
  - test_ui/test_telegram_bot.py, test_code_reviewer.py (AT05)
  - Tests AT02-AT06 marqués xfail (non implémentés sur cette branche)

### Décisions techniques
- Stubs lèvent NotImplementedError (pas de faux retour) → l'élève doit implémenter
- Tests AT01 (test_provider, test_parsers) sont les seuls non-xfail (AT01 = branche courante)
- Pydantic models (CVInfo, MatchResult, InterviewGuide) sont déjà définis dans parsers.py
  car ils servent de schéma de référence pour les Output Parsers
- SYSTEM_PROMPT_RECRUITER déjà défini dans prompts.py (constante)
- docker-compose.yml avec 3 services (api, streamlit, chromadb)

## 2026-08-09 — Phase 15 : Lancement de l'équipe Cuba

### Sélection de l'équipe

Cuba a été sélectionnée comme meilleure équipe du benchmark :
- Score v3.1 : 77/100 (meilleur des 3 équipes)
- 3 PRs merged, 12+ tests, 16+ fichiers source
- Stratégie Fix + Continue (PO orchestre Dev/Lead via terminal)
- Modèles : PO glm-5.2:cloud, Dev mistral-large-3, Lead deepseek-v4-pro
- Temps : 10h44m (le plus rapide)

### Infrastructure déployée

1. Repo GitHub créé : https://github.com/YoLoADR/training-langchain-v2
2. 7 branches pushées (main + 6 ateliers)
3. 11 labels créés (atelier, hirekit/*, data, tests, docs, bug-hunt, checkpoint)
4. Issue #1 créée avec brief complet
5. Repo cloné sur VM 102 : /home/hermes/projects/hirekit-cuba
6. 3 profils Hermes créés : cuba-hirekit-po-bot, -dev-bot, -lead-bot
7. 3 wrappers créés dans /home/hermes/.local/bin/
8. 3 config.yaml créés (models, max_turns=500, cwd=hirekit-cuba)
9. 3 MEMORY.md créés (PO: brief complet, Dev: TDD, Lead: review)
10. Bot Telegram mis à jour sur Contabo (ajout team "hirekit" dans TEAMS)

### Lancement du PO

Le PO Cuba (Yanet, glm-5.2:cloud) a été lancé sur VM 102 en nohup.
Premiers résultats après ~2 minutes :
- PLAN.md créé (7890 octets, découpage en US détaillé)
- scripts/generate_cvs.py créé (20134 octets)
- Le PO travaille en autonomie

### Suivi

Le PO est autonome. Il suit l'ordre : données → AT02 → AT03 → ... → AT06.
Les PRs apparaîtront sur GitHub. Le suivi se fait via :
- `gh pr list --repo YoLoADR/training-langchain-v2`
- `cat /tmp/hirekit-po.log` sur VM 102
- Bot Telegram @cuba_team_ai_bot (commande /check)

### Phase 5 complétée par Cuba

Le PO a terminé la Phase 5 en autonomie :
- PLAN.md créé (184 lignes, découpage en US détaillé)
- 6 scripts generate_*.py créés (cvs, offers, skills, qa, availability, code_repo)
- 2 scripts utilitaires (check_atelier_ready.sh, verify_branch_scope.sh)
- Données générées : 30 CVs PDF, 15 offres JSON, 100 skills CSV, 150 QA JSONL, calendrier, 10 fichiers Python
- 21 tests TDD pour valider les données → tous passent
- Commit c790bc7 pushé sur GitHub (70 fichiers, 42608 lignes)

### AT02 en cours

Le PO passe à AT02 (LCEL + Mémoire) — il installe LangChain pour implémenter hirekit/services/matching.py