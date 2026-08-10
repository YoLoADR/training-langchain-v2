# Insights — Fil Rouge v3 (aligné sellkit)

> Journal de progression du fil rouge LangChain, aligné sur l'architecture sellkit.
> Ce document trace le raisonnement qui a mené aux choix, pas juste le "quoi" mais le "pourquoi".

---

## Session 2026-08-10 — Analyse et planification

### 1. Problème initial

L'utilisateur a exprimé trois griefs sur la session précédente :

1. **"A aucun moment je n'ai vu les tests Playwright sur mon ordi"** — Les tests
   E2E Playwright n'existaient pas dans le projet. Le dossier `.playwright-mcp/`
   ne contenait que des artefacts MCP, pas des tests.

2. **"Tu as mal analysé ai-hirekit"** — L'analyse initiale décrivait ai-hirekit
   comme un "kit de publication d'offres sur sites africains via Hermes". L'utilisateur
   a corrigé : ai-hirekit est un **recruteur dans un cube** qui filtre les candidats
   via **Telegram** et met à jour un **CRM**.

3. **"Le dossier tâche devait être dans ce projet"** — `ai-teams-benchmark/.agent/tasks/training-langchain-v2-fil-rouge/`
   aurait dû être dans `training-langchain-v2/.agent/tasks/`.

### 2. Erreurs d'analyse identifiées et corrigées

#### Erreur A — ai-hirekit et Hermes

**Erreur commise** : J'ai mappé des concepts LangChain (`create_deep_agent()`,
`FilesystemBackend`, `TodoListMiddleware`) vers des implémentations Hermes
(`hermes-agent --profile`, `RECON.md`, `GitHub Issues`).

**Pourquoi c'était faux** :
1. ai-hirekit est **conçu pour** Hermes (README l.3, l.51-53) mais les profils Hermes
   pour ai-hirekit **ne sont pas déployés** (README l.132, l.204-206). Les bots Hermes
   actifs sur VM 102 travaillent sur ai-team, pas sur ai-hirekit.
2. Même si ai-hirekit utilisait Hermes, la formation `training-langchain-v2` est une
   formation **LangChain** — elle doit utiliser les librairies LangChain
   (`deepagents`, `langgraph`, `langchain`), pas Hermes.
3. Présenter un mapping Deep Agents → Hermes comme "inspiration" est absurde : ce
   sont deux frameworks concurrents avec des APIs différentes.

**Leçon retenue** : Ne pas mapper des concepts d'un framework vers un autre framework
différent. Vérifier si une technologie est réellement déployée avant de dire qu'elle
est utilisée. La formation doit utiliser les outils qu'elle enseigne.

#### Erreur B — Plan superficiel

**Erreur commise** : Le plan initial était une liste à puces avec des noms d'ateliers
mais sans contenu réel : pas de carnet de bord, pas d'exemples du fil rouge, pas de
spécification des fichiers à créer.

**Pourquoi c'était insuffisant** : Un plan de délégation à une équipe IA doit être
suffisamment détaillé pour que l'équipe puisse exécuter sans ambiguïté. Un plan
"AT01: LLM + Prompts" ne dit pas quels concepts LangChain couvrir, quels fichiers
créer, quels tests écrire.

**Leçon retenue** : Chaque atelier doit spécifier : les concepts LangChain couverts,
le module hirekit/ construit, le carnet de bord (définition + analogie + exemple
fil rouge), les tests, et l'inspiration sellkit exacte (fichier + ligne).

#### Erreur C — Manque de profondeur dans l'analyse des sources

**Erreur commise** : J'ai survolé le pattern pédagogique `pre-training-rag` sans
lire les GUIDE-ELEVE.md en détail. J'ai survolé la doc Deep Agents sans vérifier
l'API réelle.

**Pourquoi c'était problématique** : Le pattern pédagogique de pre-training-rag
(contenu structuré : mission → carnet de bord → mini-lab → bug hunt → checkpoints →
sprint/bonus → wrap-up) est essentiel pour la qualité de la formation. Sans l'avoir
lu en détail, on ne peut pas le reproduire.

**Leçon retenue** : Lire les fichiers sources soi-même (pas via sous-agent) avant
de produire un plan. Vérifier chaque claim avec le fichier source.

### 3. Découverte de sellkit

L'utilisateur a pointé vers `/Users/yohannravino/Factory/sellkit` en disant :
"ce projet est plus avancé sur les concepts Langchain et est donc mieux comme
inspiration".

**Analyse approfondie de sellkit** (lecture de tous les fichiers source moi-même) :

- **Langage** : TypeScript/Node.js (pas Python)
- **Librairies** : `@langchain/core`, `@langchain/langgraph`, `@langchain/ollama`, `deepagents`
- **Architecture** : Deep Agents V3 avec 4 couches
  1. systemPrompt — Identité statique + AGENTS.md
  2. memory — AGENTS.md injecté dans systemPrompt
  3. skills — SKILL.md injecté par middleware beforeModel
  4. contextSchema — RecruitmentContextSchema (Zod) + contexte dynamique
- **CRM** : SQLite WAL, 6 stages (new→contacted→interested→qualified→closed_won/closed_lost)
- **Pipeline** : objection detection (8 types) → closing detection (5 signaux) →
  memory extraction (6 champs) → CRM → Deep Agent → reply
- **Skills** : 5 SKILL.md chargés dynamiquement selon la phase
  (first-contact, qualification, reformulation, closing, test-technique)
- **Tests** : 3 niveaux
  - `tests/unit/` — tests purs (pas de LLM, pas de réseau)
  - `tests/integration/` — tests avec LLM
  - `tests/step*-human-in-the-loop.test.ts` — tests qui spawn l'app, guident un humain,
    vérifient DB/API/logs à chaque étape
- **Telemetry** : 14 préfixes de log verbatim (📥, 🟡, 🔴, 🟣, 🧠, 🤖, 📤, ❌, 🔗, 📊)

**Décision** : training-langchain-v2 doit être un **miroir Python de sellkit**.
On traduit les concepts TypeScript → Python (Zod → Pydantic, better-sqlite3 → sqlite3,
vitest → pytest, etc.), on ne copie pas le code.

**Pourquoi sellkit plutôt que ai-hirekit comme inspiration** :
- sellkit implémente Deep Agents en production → ai-hirekit non
- sellkit a un CRM SQLite avec pipeline → ai-hirekit non
- sellkit a des tests human-in-the-loop → ai-hirekit non
- sellkit a des skills dynamiques → ai-hirekit non
- sellkit a un handler Telegram complet → ai-hirekit non
- ai-hirekit garde son rôle : thème métier (recrutement, cube, Telegram, CRM)

### 4. Décisions architecturales (avec raisonnement)

#### 4.1 Pourquoi 7 ateliers et pas 6 ?

Le programme officiel Ambient IT fait 3 jours (6 demi-journées). L'utilisateur a
demandé d'ajouter un atelier Deep Agents.

**Raisonnement de l'ordre** :
- AT05 Deep Agents arrive **après** AT04 ReAct : l'élève doit connaître les agents
  avant de découvrir le harness Deep Agents (qui est une abstraction au-dessus)
- AT06 Chatbots+Telegram+CRM arrive **après** AT05 : le handler Telegram utilise
  le Deep Agent (flux : objection→closing→memory→CRM→**Deep Agent**→reply)
- AT07 Eval+Deploy+E2E arrive en dernier : les tests E2E vérifient le système complet

#### 4.2 Pourquoi une architecture 4 couches ?

**Raisonnement** (inspiré de sellkit `src/agent/deep-agent.ts`) :
1. **Couche 1 (systemPrompt)** — Identité statique. Ne change jamais.
2. **Couche 2 (memory)** — AGENTS.md. Règles globales qui s'appliquent à toutes les
   phases (langue, recadrage, URLs). Lu au démarrage, injecté dans systemPrompt.
3. **Couche 3 (skills)** — SKILL.md. Règles par phase. Changent à chaque message
   selon où en est le candidat. Injectés par middleware beforeModel.
4. **Couche 4 (contextSchema)** — RecruitmentContext. Contexte dynamique du candidat
   (nom, expérience, stage, objection détectée, prochaine question). Pydantic schema.

**Pourquoi pas un systemPrompt unique ?**
- Un systemPrompt de 2000 tokens serait (a) coûteux, (b) difficile à maintenir,
  (c) non-cachable par Anthropic prompt caching.
- La séparation permet de cacher les couches 1+2 (stables) et de n'envoyer que les
  couches 3+4 (dynamiques) à chaque appel.

#### 4.3 Pourquoi LLM + fallback keyword pour les détections ?

**Raisonnement** (inspiré de sellkit `src/pipeline/objections.ts`) :
- Le LLM comprend le contexte ("c'est trop cher pour moi" = objection trop_cher
  même sans le mot exact "cher")
- Le keyword matching est un filet de sécurité si le LLM timeout ou rate
- Les deux coexistent : on essaie le LLM d'abord (gpt-4o-mini, rapide et pas cher),
  fallback keyword si erreur

#### 4.4 Pourquoi SQLite + WAL pour le CRM ?

**Raisonnement** (inspiré de sellkit `src/crm/store.ts`) :
- Le bot Telegram écrit pendant que le dashboard Streamlit lit → accès concurrent
- WAL (Write-Ahead Logging) permet des lectures concurrentes sans bloquer les écritures
- SQLite est simple (un fichier), pas besoin d'un serveur DB
- La migration est automatique (ajout de colonnes si manquantes)

#### 4.5 Pourquoi 14 préfixes de log verbatim ?

**Raisonnement** (inspiré de sellkit `src/telemetry/log.ts`) :
- Les tests E2E (step1, step5) parsent les logs pour vérifier que le système a
  bien exécuté chaque étape
- Si un préfixe change, le test échoue → les préfixes sont une **interface contractuelle**
- Chaque préfixe a une icône pour retrouver l'info visuellement (📥 entrant, 📤 sortant,
  🟡 objection, 🟣 closing, 🧠 mémoire, etc.)

#### 4.6 Pourquoi des skills dynamiques plutôt qu'un systemPrompt fixe ?

**Raisonnement** (inspiré de sellkit `.agent/skills/recruiter/`) :
- Un recruteur humain ne suit pas le même script du début à la fin. Il s'adapte.
- Les skills dynamiques reproduisent cette adaptation :
  - `phase-first-contact` : recadrage + démarrage qualification
  - `phase-qualification` : 1 question à la fois
  - `phase-reformulation` : résumé des 6 infos + présentation test
  - `phase-closing` : engagement, lien, appel
  - `phase-test-technique` : détails du test (2 semaines, 150€, zones grises)
- Le middleware `beforeModel` choisit le bon skill selon `qual_count` et `stage`

### 5. Décision de délégation à Cuba

**Raisonnement** : Cuba est la meilleure équipe du benchmark (77/100, 3 PRs merged,
12+ tests, 10h44m). PO glm-5.2:cloud, Dev mistral-large-3, Lead deepseek-v4-pro.

**Cuba a déjà implémenté** AT01-AT05 (6 ateliers originaux) avec 4 commits :
- c790bc7 : données simulées + PLAN.md + scripts (70 fichiers, 42k lignes)
- 3561ff7 : AT01+AT02 implémentation LCEL, Mémoire, Prompts, Parsers
- 9235e0b : AT03 RAG complet (Document Loaders, Splitters, FAISS+ChromaDB, Retriever MMR)
- 1d6801e : AT04 Agents ReAct + Tools (4 outils, AgentExecutor)
- 8afb329 : AT05 Chatbots + Code Analysis + Multimodal (Streamlit, Telegram, Code-Reviewer)

**Manque identifié** : Deep Agents, CRM sellkit-style, pipeline détection, tests E2E.
Cette session a comblé ces manques.

---

## Session 2026-08-10 — Implémentation (12 phases)

### Phase 0 — Sauvegarder le plan (commit 074b3d0)

Création de `.agent/tasks/fil-rouge-v3-sellkit-aligned/` avec PLAN.md, todos.md, insights.md.
Copie de l'ancien dossier tâche depuis `ai-teams-benchmark/.agent/tasks/`.

**Raisonnement** : Le pattern `ai-teams-benchmark/.agent/tasks/` (PLAN.md + todos.md +
insights.md + SCORECARD.md) est éprouvé pour le suivi de progression. On le reproduit
dans le projet lui-même plutôt que dans le benchmark externe.

### Phase 1 — hirekit/pipeline/ (commit 074b3d0)

Création de 4 fichiers inspirés de `sellkit/src/pipeline/` :

- `qualification.py` : FIELD_QUESTIONS (6 champs dans l'ordre name→experience→
  availability→location→revenueGoal→riskAppetite), STAGE_LABELS, CLOSING_STAGES
- `objections.py` : OBJECTION_CATALOG (8 types : trop_cher, arnaque, reflechir,
  pas_interesse, fixe, legalite, famille, temps), detect_sync() LLM + fallback keyword
- `closing.py` : ClosingType (5 signaux : closing_cue, commitment_signal, call_request,
  job_interest, refusal), STAGE_MAP (signal → stage CRM), detect_closing_sync() LLM + fallback
- `memory.py` : ProspectMemory (Pydantic), extract_memory_sync() LLM avec
  with_structured_output(MemorySchema), merge_memory(), count_qualification_fields(),
  next_missing_field() (ordre strict), format_memory_for_prompt(), serialize/parse

**Raisonnement de l'ordre des champs** : sellkit utilise l'ordre
name → experience → availability → location → revenueGoal → riskAppetite.
Cet ordre correspond au déroulé naturel d'un entretien de recrutement :
1. Comment vous appelez-vous ? (name)
2. Quelle est votre expérience ? (experience)
3. Quand êtes-vous disponible ? (availability)
4. Où êtes-vous situé ? (location)
5. Quel est votre objectif de revenu ? (revenueGoal)
6. Êtes-vous à l'aise avec le risque ? (riskAppetite)

### Phase 2 — hirekit/deep_agent/ (commit 9c2cd64)

Création de 3 fichiers inspirés de `sellkit/src/agent/` :

- `recruiter_agent.py` : `get_deep_agent()` avec create_deep_agent() 4 couches.
  Lit AGENTS.md au démarrage et l'injecte dans IDENTITY_PROMPT.
  `run_deep_turn()` exécute un tour de conversation avec contexte dynamique.
- `middleware.py` : `RecruitmentContext` (Pydantic avec 11 champs),
  `read_skill_for_context()` (charge le bon SKILL.md selon qual_count/stage/isClosing),
  `build_context_prompt()` (9 combinaisons : vide, memory, question, lien, objection,
  combo, refusal), `create_recruitment_context_middleware()` (beforeModel hook)
- `harness_profile.py` : `register_recruiter_harness_profile()` exclut
  write_todos, task, SummarizationMiddleware, todoListMiddleware

**Raisonnement du HarnessProfile** : L'agent recruteur fait de la conversation, pas
de la planification de tâches ni de l'écriture de fichiers. On exclut donc les tools
et middleware non nécessaires pour (a) réduire la latence, (b) éviter les hallucinations
où l'agent essaierait d'écrire des fichiers au lieu de répondre au candidat.

### Phase 3 — hirekit/crm/ + hirekit/telemetry/ (commit f266fe9)

- `crm/types.py` : STAGES (6 stages), Stage (Enum), Candidate (dataclass avec 15 champs),
  Message (dataclass)
- `crm/store.py` : CrmStore SQLite WAL avec 15 méthodes (get_or_create, get, get_all,
  update_stage, update_info, add_message, get_messages, get_recent_messages,
  get_followup_due, mark_followup_sent, set_conversion_link, get_conversion_link,
  get_qual_json, set_qual_json, clear_messages, delete_candidate, stats)
- `telemetry/log.py` : 17 fonctions de log (msg_in, objection, refusal, closing,
  closing_first_interest, closing_ignored, memory, llm_calling, msg_out, llm_error,
  llm_error_empty, conversion_link, stage_update, closing_fallback, memory_fallback,
  objection_fallback)

**Raisonnement du pattern `crm` dict** : sellkit exporte un objet `crm` avec des
méthodes. En Python, j'ai d'abord utilisé un dict de lambdas (`crm = {"get_or_create": lambda...}`)
mais le LSP ne comprenait pas les types. J'ai remplacé par un pattern `_crm()` qui
retourne un singleton `CrmStore`, ce qui est plus propre typage-wise.

### Phase 4 — .agent/ (commit d33b12d)

- `memory/recruiter/AGENTS.md` : 4 règles globales (Langue, Recadrage, URLs, Rôle)
- `skills/recruiter/phase-first-contact/SKILL.md` : recadrage hors sujet + démarrage
- `skills/recruiter/phase-qualification/SKILL.md` : 1 question à la fois, pas de test
- `skills/recruiter/phase-reformulation/SKILL.md` : résumé 6 infos + présentation test
- `skills/recruiter/phase-closing/SKILL.md` : engagement, lien, appel, fin
- `skills/recruiter/phase-test-technique/SKILL.md` : 2 semaines, 150€, zones grises

**Raisonnement du contenu des SKILL.md** : sellkit utilise le contexte de l'immobilier
commercial (Express Immo). J'ai adapté au contexte du recrutement tech (HireKit) :
- "fiches de poste" au lieu de "fiches de poste Express Immo"
- "test technique" (2 semaines, 150€) au lieu de "test de vente"
- "zones grises" (startup) au lieu de "zones grises immobilier"
- Les règles globales (langue FR, recadrage, URLs, rôle) sont identiques

### Phase 5 — AT05 Deep Agents (commit 7247d73)

Création complète de l'atelier avec le pattern pre-training-rag :
- GUIDE-ELEVE.md (329 lignes) : mission, carnet de bord 7 concepts (create_deep_agent,
  contextSchema, beforeModel, skills dynamiques, HarnessProfile, Memory, buildContextPrompt),
  mini-lab (changer qual_count 0→3→6), bug hunt 3 bugs, checkpoints (3+5 QCM),
  sprint/bonus, wrap-up 10 questions
- exercice.py (5 TODOs) + solution.py
- bugs/ : 3 patches (skills inversés, AGENTS.md manquant, opt-out non géré) + 3 tests + 3 explications
- checkpoints/ : check_1.py (3 QCM mi-atelier) + check_final.py (5 QCM fin)
- .claude/CLAUDE.md scope guard

**Raisonnement des bugs** : chaque bug illustre un concept clé :
- v1 (skills inversés) → l'ordre des conditions dans `read_skill_for_context()` matters
- v2 (AGENTS.md manquant) → le chemin vers AGENTS.md doit être correct
- v3 (opt-out non géré) → le refusal doit être traité en priorité absolue

### Phase 6+7 — AT06 + AT07 (commit 86bf5e5)

- AT06 GUIDE-ELEVE.md restructuré : mission "connecte le Deep Agent à Telegram +
  dashboard CRM", carnet de bord (Pipeline CRM, SQLite+WAL, logs structurés, handler
  Telegram, Streamlit dashboard), flux complet (objection→closing→memory→CRM→agent→reply)
- AT07 GUIDE-ELEVE.md créé : mission "prouve que ça marche avec tests E2E Playwright +
  LangSmith + Docker", carnet de bord (LangSmith, Recall@k, tests E2E, Docker Compose)
- AT07 .claude/CLAUDE.md scope guard

### Phase 8 — tests/unit/ (commit 996638a)

5 fichiers de tests purs (pas de LLM, pas de réseau) :

- `test_memory.py` : 5 classes de test (TestMergeMemory, TestCountQualificationFields,
  TestNextMissingField avec CRITICAL tests, TestSerializeParseRoundTrip,
  TestFormatMemoryForPrompt, TestScenarios avec 3 scénarios paramétrés Nathan/Francis/Sarah)
- `test_middleware.py` : TestBuildContextPrompt (9 combinaisons) + TestReadSkillForContext (6 tests)
- `test_skills.py` : TestAgentsMd (3 tests) + TestSkillsStructure (5 skills frontmatter,
  pas de conflit, test technique key info)
- `test_telemetry.py` : 17 tests (un par fonction de log, capture stdout/stderr)
- `test_crm.py` : TestStages (3 tests) + TestCrmStore (14 tests : get_or_create,
  idempotent, update_stage, add_message, get_messages, conversion_link idempotent,
  qual_json, stats, clear, delete)

**Raisonnement des 3 scénarios paramétrés** : sellkit utilise 3 scénarios aléatoires
(Nathan débutant, Francis expérimenté, Sarah reconversion) pour éviter les biais de
test. Chaque scénario suit le même parcours 0→6 champs mais avec des réponses
différentes, ce qui vérifie que la logique de qualification est robuste.

### Phase 9+10 — tests/integration/ + tests/e2e/ (commit d7fee50)

- `tests/integration/test_deep_agent.py` : 3 tests (agent créé, tour minimal,
  tour avec qualification) — skip si pas de clé API
- `tests/e2e/conftest.py` : fixtures (app, db, api, log_file) — spawn Streamlit,
  attendre ready, cleanup
- `tests/e2e/test_step1_conversation.py` : 5 tests (DB vide, app accessible,
  CRM store, logs, 14 préfixes telemetry)
- `tests/e2e/test_step5_full_pipeline.py` : 3 scénarios paramétrés (13 étapes),
  stage transitions, CRM pipeline new→closed_won
- `tests/e2e/test_telegram_screening.py` : screening 0→6 champs, objection 8 types,
  closing 5 types, CRM pipeline screening→closed_won

**Raisonnement des tests E2E** : sellkit utilise un pattern "human-in-the-loop" où
le test guide un humain à travers les étapes. En Python avec Playwright, on automatise
ce pattern : le test spawn l'app, simule les interactions, et vérifie DB/API/logs à
chaque étape. Les tests sont marqués `@pytest.mark.e2e` et skip si Playwright non installé.

### Phase 11 — Documentation (commit fe5fd0f)

Mise à jour de insights.md et todos.md avec l'architecture finale.

### Phase 12 — Correction alignement énoncés/code (commit c7372c9)

**Problème** : Après implémentation, vérification systématique de l'alignement entre
les GUIDE-ELEVE.md (énoncés) et le code réel dans `hirekit/`.

**Écarts trouvés** :

1. `hirekit/eval/metrics.py` = 3 stubs `NotImplementedError` mais AT07 dit de les utiliser
2. `hirekit/eval/tracing.py` = 1 stub `NotImplementedError` mais AT07 dit de brancher LangSmith
3. `hirekit/ui/telegram_bot.py` = ancien code Cuba (commandes /search, /match) mais AT06
   décrit le flux sellkit (objection→closing→memory→CRM→agent→reply)
4. `hirekit/ui/app.py` = 4 pages mais AT06 mentionne un dashboard CRM kanban
5. `atelier-06-eval-benchmark-deploy/` = doublon obsolète avec `atelier-07-eval-deploy/`

**Corrections apportées** :

1. `metrics.py` → implémenté `compute_recall_at_k()`, `compute_mrr()`, `compute_cost()`,
   `evaluate_qa_dataset()` avec MODEL_PRICING dict
2. `tracing.py` → implémenté `get_langsmith_callback()`, `is_tracing_enabled()`,
   `enable_tracing()`, `get_run_tags()`
3. `telegram_bot.py` → remplacé par `handle_message()` avec flux sellkit complet
   (objection→closing→memory→CRM→Deep Agent→reply), `process_command()` pour admin,
   `start_telegram_bot_simulated()` et `start_telegram_bot_real()`
4. `app.py` → ajouté `render_crm_pipeline()` (kanban par stage, stats, messages récents)
5. `atelier-06-eval-benchmark-deploy/` → supprimé

**Raisonnement** : Un énoncé qui dit "utilise Recall@k" mais le code lève
`NotImplementedError` est un mensonge pédagogique. L'élève ne peut pas tester son code.
Le code de référence doit toujours être implémenté et fonctionnel.

### Vérification finale

- **0 stub `NotImplementedError`** dans `hirekit/` (vérifié avec `rg "NotImplementedError" hirekit/`)
- **Tous les tests** (unit, integration, e2e) importent depuis des modules qui existent
- **Chaque GUIDE-ELEVE** référence des modules implémentés et fonctionnels
- **AT05 Deep Agents** : GUIDE-ELEVE référence `hirekit/deep_agent/`, `.agent/` — tous présents
- **AT06 Chatbots+CRM** : GUIDE-ELEVE référence `hirekit/ui/`, `hirekit/crm/`,
  `hirekit/telemetry/`, `hirekit/pipeline/` — tous présents et implémentés
- **AT07 Eval+Deploy** : GUIDE-ELEVE référence `hirekit/eval/` — implémenté (plus de stubs)

---

## Architecture finale (miroir sellkit)

```
hirekit/
├── config.py                    # Configuration (.env)
├── llm/                         # AT01 — LLMs, Prompts, Parsers
│   ├── provider.py              # get_llm(), get_chat_model() — abstraction provider
│   ├── prompts.py               # SYSTEM_PROMPT_RECRUITER, PromptTemplate, ChatPromptTemplate
│   └── parsers.py               # CVInfo, MatchResult, InterviewGuide (Pydantic)
├── services/                    # AT02 — LCEL, Mémoire
│   ├── matching.py              # get_matching_chain() LCEL, get_recruiter_memory(), save/load
│   └── availability.py          # check_availability() calendrier fictif
├── rag/                         # AT03 — RAG
│   ├── ingestion.py             # PyMuPDFLoader, JSONLoader, CSVLoader
│   ├── chunking.py              # CharacterTextSplitter, RecursiveCharacterTextSplitter
│   ├── vectorstore_faiss.py     # FAISS.from_documents(), FastEmbedEmbeddings
│   ├── vectorstore_chroma.py    # Chroma.from_documents()
│   └── retriever.py             # as_retriever(MMR), EnsembleRetriever
├── agent/                       # AT04 — Agents ReAct + Tools
│   ├── react_agent.py           # create_react_agent, AgentExecutor(max_iterations=8)
│   └── tools.py                 # search_cvs, match_candidate, web_search, python_repl
├── pipeline/                    # NOUVEAU — Pipeline détection (inspiré sellkit/src/pipeline/)
│   ├── qualification.py         # FIELD_QUESTIONS (6 champs), STAGE_LABELS, CLOSING_STAGES
│   ├── objections.py            # OBJECTION_CATALOG (8 types), detect_sync() LLM+fallback
│   ├── closing.py               # ClosingType (5 signaux), STAGE_MAP, detect_closing_sync()
│   └── memory.py                # ProspectMemory, extract_memory_sync(), merge, count, next, format
├── deep_agent/                  # AT05 — Deep Agents 4 couches (inspiré sellkit/src/agent/)
│   ├── recruiter_agent.py       # create_deep_agent() 4 couches, run_deep_turn()
│   ├── middleware.py            # beforeModel + build_context_prompt() + read_skill_for_context()
│   └── harness_profile.py       # register_recruiter_harness_profile() excludedTools
├── crm/                         # NOUVEAU — CRM SQLite (inspiré sellkit/src/crm/)
│   ├── types.py                 # STAGES (6 stages), Stage, Candidate, Message
│   └── store.py                 # CrmStore SQLite WAL (15 méthodes)
├── telemetry/                   # NOUVEAU — Logs structurés (inspiré sellkit/src/telemetry/)
│   └── log.py                   # 17 fonctions de log (14 préfixes verbatim)
├── ui/                          # AT06 — Chatbots, Telegram, CRM
│   ├── app.py                   # Streamlit 5 pages (Chat, Matching, CVs, CRM kanban, Multimodal)
│   ├── telegram_bot.py          # handle_message() flux sellkit + process_command() admin
│   └── code_reviewer.py         # index_code_repo() + ask_code_question()
└── eval/                        # AT07 — Évaluation, Déploiement
    ├── metrics.py               # compute_recall_at_k(), compute_mrr(), compute_cost(), evaluate_qa_dataset()
    └── tracing.py               # get_langsmith_callback(), is_tracing_enabled(), enable_tracing()

.agent/                          # NOUVEAU — Memory + Skills (inspiré sellkit/.agent/)
├── memory/recruiter/AGENTS.md   # Règles globales (langue, recadrage, URLs, rôle)
└── skills/recruiter/
    ├── phase-first-contact/SKILL.md     # qual_count=0 : recadrage + démarrage
    ├── phase-qualification/SKILL.md     # qual_count 1-5 : 1 question à la fois
    ├── phase-reformulation/SKILL.md     # qual_count=6 : résumé + présentation test
    ├── phase-closing/SKILL.md           # is_closing : engagement, lien, appel
    └── phase-test-technique/SKILL.md    # show_test_and_link : 2 semaines, 150€, zones grises

ateliers/
├── atelier-01-llm-prompts-parsers/      # Cuba ✅
├── atelier-02-lcel-memoire/             # Cuba ✅
├── atelier-03-rag/                      # Cuba ✅
├── atelier-04-agents-tools/             # Cuba ✅
├── atelier-05-deep-agents/              # NOUVEAU (cette session)
├── atelier-05-chatbot-code-review/      # Cuba ✅ → devient AT06
└── atelier-07-eval-deploy/              # NOUVEAU (cette session)

tests/
├── unit/                        # Tests purs (pas LLM, pas réseau)
│   ├── test_memory.py           # merge, count, nextMissingField, 3 scénarios paramétrés
│   ├── test_middleware.py       # buildContextPrompt 9 combinaisons + read_skill 6 tests
│   ├── test_skills.py           # 5 skills frontmatter, AGENTS.md, pas de conflit
│   ├── test_telemetry.py        # 14 préfixes verbatim
│   └── test_crm.py              # 6 stages, get_or_create, conversion_link idempotent, stats
├── integration/                 # Tests avec LLM
│   └── test_deep_agent.py       # create_deep_agent + invoke (skip si pas de clé API)
├── e2e/                         # Tests Playwright human-in-the-loop
│   ├── conftest.py              # fixtures: app (spawn Streamlit), db, api, log_file
│   ├── test_step1_conversation.py    # DB vide, app, CRM, 14 préfixes
│   ├── test_step5_full_pipeline.py   # 3 scénarios, 13 étapes, stage transitions
│   └── test_telegram_screening.py     # screening 0→6, objection 8 types, closing 5 types
└── (tests existants Cuba: test_llm/, test_rag/, test_agent/, test_services/, test_eval/, test_ui/)
```

---

## Leçons apprises

1. **Ne pas mapper un framework vers un autre** — Deep Agents ≠ Hermes. La formation
   LangChain doit utiliser les librairies LangChain.

2. **Lire les sources soi-même** — Les sous-agents (explore) peuvent survoler et
   mal interpréter. Pour les décisions architecturales, lire les fichiers source
   directement.

3. **Vérifier si une technologie est déployée** — ai-hirekit est "conçu pour" Hermes
   mais les profils ne sont pas déployés. Dire "ai-hirekit utilise Hermes" sans
   vérifier est une erreur.

4. **Le code de référence doit être implémenté** — Un énoncé qui dit "utilise Recall@k"
   mais le code lève `NotImplementedError` est un mensonge pédagogique.

5. **L'inspiration architecturale vient du projet le plus avancé** — sellkit (production-ready,
   Deep Agents V3) est une meilleure inspiration que ai-hirekit (planning, non déployé).

6. **Le pattern pédagogique doit être lu en détail** — pre-training-rag a un format
   spécifique (mission → carnet de bord → mini-lab → bug hunt → checkpoints → sprint/bonus
   → wrap-up) qu'on ne peut pas reproduire sans l'avoir lu.

7. **Les tests E2E doivent être visualisables** — L'utilisateur veut voir les tests
   Playwright tourner sur son ordi. Les tests doivent spawner l'app, interagir via
   Streamlit/Telegram, et vérifier DB/API/logs.

8. **Documenter le raisonnement, pas juste le résultat** — Les docc doivent expliquer
   *pourquoi* chaque décision a été prise, pas juste *quoi* a été fait.