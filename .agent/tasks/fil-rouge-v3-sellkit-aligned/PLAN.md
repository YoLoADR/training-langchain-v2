# Plan — Fil Rouge v3 (aligné sellkit)

> Formation LangChain 7 ateliers — miroir architecture sellkit
> Créé le 2026-08-10. Basé sur analyse sellkit + ai-hirekit + pre-training-rag.
> Dernière mise à jour : 2026-08-10 (après corrections alignement énoncés/code).

## 1. Contexte et genèse

### 1.1 Le projet initial

Le projet `training-langchain-v2` est une formation LangChain en 7 ateliers progressifs.
Le fil rouge = ai-hirekit (recruteur IA dans un cube qui filtre les candidats via
des conversations initiales dans Telegram et met à jour un CRM pour suivre les
processus de recrutement).

### 1.2 Les erreurs d'analyse précédentes (session 1)

La première session d'analyse a produit plusieurs erreurs majeures qui ont été
corrigées durant cette session :

**Erreur 1 — Mauvaise compréhension de ai-hirekit** :
L'analyse initiale a décrit ai-hirekit comme un "kit de publication d'offres d'emploi
sur des sites africains via Hermes+Playwright". L'utilisateur a corrigé : ai-hirekit
est un **recruteur dans un cube** qui filtre les candidats via des **conversations
initiales dans Telegram** et met à jour un **CRM** pour suivre les processus de
recrutement. Le README du repo ai-hirekit décrit bien un kit de publication, mais
la vision produit (décrite dans AI-HireKit-Projet-Fil-Rouge.md) est un recruteur IA.

**Erreur 2 — Mapping Deep Agents → Hermes absurde** :
L'analyse initiale a mappé des concepts LangChain (`create_deep_agent()`,
`FilesystemBackend`, `TodoListMiddleware`) vers des implémentations Hermes
(`hermes-agent --profile`, `RECON.md`, `GitHub Issues`). C'était doublement faux :
(a) ai-hirekit n'utilise pas Hermes en production (les profils ne sont pas déployés),
(b) la formation est une formation **LangChain** — elle doit utiliser les librairies
LangChain (`deepagents`, `langgraph`, `langchain`), pas Hermes.

**Erreur 3 — Plan superficiel** :
Le plan initial était une liste à puces sans contenu réel pour chaque atelier,
sans spécifier ce que chaque atelier contient concrètement, sans carnet de bord,
sans exemples du fil rouge.

### 1.3 Le pivot vers sellkit

L'utilisateur a pointé vers `/Users/yohannravino/Factory/sellkit` comme meilleure
inspiration car ce projet est **plus avancé sur les concepts LangChain**. L'analyse
approfondie de sellkit a révélé :

- sellkit est **TypeScript/Node.js** (pas Python) — utilise `@langchain/core`,
  `@langchain/langgraph`, `deepagents` (npm)
- sellkit implémente **Deep Agents V3** en production avec une architecture 4 couches
- sellkit a un **CRM SQLite** avec pipeline (new→contacted→interested→qualified→closed_won/closed_lost)
- sellkit a un **handler Telegram** complet (objection→closing→memory→CRM→agent→reply)
- sellkit a des **tests human-in-the-loop** (step1: 358 lignes, step5: 621 lignes)
- sellkit a des **skills dynamiques** (5 SKILL.md chargés selon la phase)
- sellkit a une **mémoire extraction LLM** (gpt-4o-mini extrait 6 champs)

**Décision** : training-langchain-v2 doit être un **miroir Python de sellkit**.
On traduit les concepts TypeScript → Python, on ne copie pas le code.

### 1.4 L'état de Cuba

Cuba (équipe benchmark, 77/100) a implémenté AT01-AT05 (6 ateliers originaux) :
- AT01: LLM + Prompts + Parsers ✅
- AT02: LCEL + Mémoire ✅
- AT03: RAG ✅
- AT04: Agents ReAct + Tools ✅
- AT05: Chatbots + Code Review ✅ (mais sans Deep Agents, sans CRM sellkit-style)

**Manque identifié** : Deep Agents, CRM pipeline sellkit-style, pipeline détection
(objections, closing, memory extraction), tests E2E Playwright, skills dynamiques,
telemetry structuré.

## 2. Sources d'inspiration (avec raisonnement)

| Source | Rôle | Pourquoi cette source |
|---|---|---|
| `/Users/yohannravino/Factory/sellkit` | **Architecture cible** | Production-ready, Deep Agents V3 4 couches, CRM SQLite, handler Telegram, tests human-in-the-loop. Le projet le plus avancé sur les concepts LangChain. |
| `/Users/yohannravino/Factory/pre-training-rag` | **Pattern pédagogique** | GUIDE-ELEVE.md structuré (mission, carnet de bord, mini-lab, bug hunt, checkpoints, sprint/bonus, wrap-up). Pattern éprouvé. |
| `/Users/yohannravino/Factory/ai-hirekit` | **Thème métier** | Recrutement, cube, Telegram, CRM. La vision produit décrite dans AI-HireKit-Projet-Fil-Rouge.md. |
| `ai-teams-benchmark` | **Pattern tâche** | Structure .agent/tasks/ (PLAN.md, todos.md, insights.md, SCORECARD.md). Suivi de progression. |
| sellkit `src/agent/deep-agent.ts` | **Deep Agents 4 couches** | createDeepAgent() avec systemPrompt + AGENTS.md + contextSchema + middleware. Architecture native Deep Agents. |
| sellkit `src/agent/middleware/recruitment-context.ts` | **beforeModel + skills dynamiques** | Middleware qui injecte le bon SKILL.md selon la phase + buildContextPrompt() avec 9 combinaisons. |
| sellkit `src/pipeline/objections.ts` | **Détection d'objections** | 8 types d'objections avec tactiques, LLM + fallback keyword matching. |
| sellkit `src/pipeline/closing.ts` | **Détection de closing** | 5 signaux (closing_cue, commitment_signal, call_request, job_interest, refusal), STAGE_MAP. |
| sellkit `src/pipeline/memory.ts` | **Extraction mémoire** | extractMemory() LLM, mergeMemory(), countQualificationFields(), nextMissingField(), formatMemoryForPrompt(). |
| sellkit `src/crm/store.ts` | **CRM SQLite** | SQLite WAL, getOrCreate, updateStage, addMessage, setQualJson, setConversionLink, getFollowupDue. |
| sellkit `src/telemetry/log.ts` | **Logs structurés** | 14 préfixes verbatim parsés par les tests E2E. |
| sellkit `tests/step1-human-in-the-loop.test.ts` | **Pattern test step1** | Spawn app, 3 échanges, vérifie DB + API + logs. 358 lignes. |
| sellkit `tests/step5-human-in-the-loop.test.ts` | **Pattern test step5** | 13 étapes, 3 scénarios aléatoires, vérifie DB + API + logs. 621 lignes. |

## 3. Raisonnement architectural

### 3.1 Pourquoi 7 ateliers et pas 6 ?

Le programme officiel Ambient IT fait 3 jours (6 demi-journées). Mais l'utilisateur
a demandé d'ajouter un atelier Deep Agents. Le nouvel ordre :

AT01 (J1 matin) → AT02 (J1 a.-m.) → AT03 (J2 matin) → AT04 (J2 a.-m.) →
**AT05 Deep Agents (J3 matin)** → AT06 (J3 a.-m.) → AT07 (J4 matin)

**Raisonnement de l'ordre** :
- AT05 Deep Agents arrive **après** AT04 ReAct car l'élève doit connaître les agents
  avant de découvrir le harness Deep Agents (qui est une abstraction au-dessus)
- AT06 Chatbots+Telegram+CRM arrive **après** AT05 car le handler Telegram utilise
  le Deep Agent (objection→closing→memory→CRM→**Deep Agent**→reply)
- AT07 Eval+Deploy+E2E arrive en dernier car les tests E2E vérifient le système complet

### 3.2 Pourquoi une architecture 4 couches Deep Agents ?

sellkit utilise 4 couches (inspiré de la doc officielle `deepagents`) :

1. **Couche 1 (systemPrompt)** — Identité statique (nom, entreprise, ton)
2. **Couche 2 (memory)** — AGENTS.md injecté dans systemPrompt (règles globales)
3. **Couche 3 (skills)** — SKILL.md injecté par middleware beforeModel (règles par phase)
4. **Couche 4 (contextSchema)** — RecruitmentContext (Pydantic) + contexte dynamique

**Pourquoi pas juste un systemPrompt unique ?**
- Les règles globales (langue, recadrage, URLs) s'appliquent à toutes les phases → AGENTS.md
- Les règles par phase (first-contact, qualification, closing) changent → SKILL.md dynamiques
- Le contexte candidat (nom, expérience, stage, objection) change à chaque message → contextSchema

Cette séparation évite un systemPrompt monolithique de 2000 tokens qui serait
(a) coûteux, (b) difficile à maintenir, (c) non-cachable par Anthropic prompt caching.

### 3.3 Pourquoi des skills dynamiques plutôt qu'un systemPrompt fixe ?

sellkit charge le bon SKILL.md selon `qual_count` et `stage` :
- `qual_count=0` → `phase-first-contact` (recadrage + démarrage)
- `qual_count 1-5` → `phase-qualification` (1 question à la fois)
- `qual_count=6` → `phase-reformulation` (résumé + présentation test)
- `is_closing=True` → `phase-closing` (engagement, lien, appel)
- `show_test_and_link=True` → ajoute `phase-test-technique`

**Raisonnement** : un recruteur humain ne suit pas le même script du début à la fin.
Il s'adapte selon où en est le candidat. Les skills dynamiques reproduisent cette
adaptation.

### 3.4 Pourquoi LLM + fallback keyword pour les détections ?

sellkit utilise `gpt-4o-mini` pour détecter les objections et signaux de closing,
avec un fallback keyword matching si le LLM est indisponible.

**Raisonnement** :
- Le LLM comprend le contexte ("c'est trop cher pour moi" = objection trop_cher
  même sans le mot exact "cher")
- Le keyword matching est un filet de sécurité si le LLM timeout ou rate
- Les deux approches coexistent : on essaie le LLM d'abord, fallback keyword

### 3.5 Pourquoi SQLite + WAL pour le CRM ?

sellkit utilise `better-sqlite3` avec `journal_mode=WAL`.

**Raisonnement** :
- Le bot Telegram écrit dans la DB pendant que le dashboard Streamlit lit
- WAL (Write-Ahead Logging) permet des lectures concurrentes sans bloquer les écritures
- SQLite est simple (un fichier), pas besoin d'un serveur DB
- La migration est automatique (ajout de colonnes si manquantes)

### 3.6 Pourquoi 14 préfixes de log verbatim ?

sellkit a 14 fonctions de log avec des préfixes exacts (📥 [MSG-IN], 🟡 [OBJECTION], etc.).

**Raisonnement** : les tests E2E (step1, step5) parsent les logs pour vérifier que
le système a bien exécuté chaque étape. Si un préfixe change, le test échoue. Les
préfixes sont donc une **interface contractuelle** entre le code et les tests.

## 4. 7 Ateliers (nouvel ordre)

| # | Atelier | Jour | Module | Inspiration sellkit |
|---|---|---|---|---|
| AT01 | LLM + Prompts + Output Parsers | J1 matin | `hirekit/llm/` | `src/llm/client.ts`, `src/pipeline/memory.ts:43-52` |
| AT02 | LCEL + Mémoire + Pipeline | J1 a.-m. | `hirekit/services/` + `hirekit/pipeline/` | `src/pipeline/memory.ts` complet |
| AT03 | RAG sur CVs | J2 matin | `hirekit/rag/` | (sellkit n'a pas RAG — ajouté pour les CVs) |
| AT04 | Agents ReAct + Tools + Détection | J2 a.-m. | `hirekit/agent/` + `hirekit/pipeline/` | `src/pipeline/objections.ts`, `src/pipeline/closing.ts` |
| AT05 | Deep Agents | J3 matin | `hirekit/deep_agent/` + `.agent/` | `src/agent/deep-agent.ts`, `src/agent/middleware/`, `src/harness-profile.ts` |
| AT06 | Chatbots + Telegram + CRM | J3 a.-m. | `hirekit/ui/` + `hirekit/crm/` + `hirekit/telemetry/` | `src/telegram/handler.ts`, `src/crm/store.ts`, `src/web/server.ts` |
| AT07 | Évaluation + Déploiement + E2E | J4 matin | `hirekit/eval/` + `tests/e2e/` | `tests/step5-human-in-the-loop.test.ts` |

## 5. Nouveaux modules créés (avec raisonnement)

### hirekit/pipeline/ (NOUVEAU — inspiré sellkit/src/pipeline/)
**Raisonnement** : sellkit a un module `src/pipeline/` qui contient la logique de
détection (objections, closing, memory extraction). Cette séparation permet de
tester la détection indépendamment du handler Telegram et du Deep Agent.

- `qualification.py` — FIELD_QUESTIONS (6 champs), STAGE_LABELS, CLOSING_STAGES
- `objections.py` — OBJECTION_CATALOG (8 types), detect_objection() LLM + fallback keyword
- `closing.py` — ClosingType (5 signaux), STAGE_MAP, detect_closing() LLM + fallback keyword
- `memory.py` — ProspectMemory, extract_memory() LLM, merge_memory(), count_fields(), next_missing_field(), format_for_prompt()

### hirekit/deep_agent/ (NOUVEAU — inspiré sellkit/src/agent/)
**Raisonnement** : sellkit a un module `src/agent/` qui implémente l'architecture
4 couches Deep Agents. Cette séparation permet de tester le middleware
(beforeModel + buildContextPrompt) indépendamment du LLM.

- `recruiter_agent.py` — create_deep_agent() 4 couches (systemPrompt + memory + skills + contextSchema)
- `middleware.py` — create_recruitment_context_middleware() beforeModel + build_context_prompt()
- `harness_profile.py` — register_harness_profile() excludedTools + excludedMiddleware

### hirekit/crm/ (NOUVEAU — inspiré sellkit/src/crm/)
**Raisonnement** : sellkit a un module `src/crm/` avec SQLite WAL. Cette séparation
permet de tester le pipeline CRM indépendamment du handler Telegram.

- `types.py` — STAGES (6 stages), Stage, Candidate, Message
- `store.py` — CrmStore SQLite WAL (get_or_create, update_stage, add_message, set_qual_json, set_conversion_link, get_followup_due)

### hirekit/telemetry/ (NOUVEAU — inspiré sellkit/src/telemetry/)
**Raisonnement** : sellkit a 14 préfixes de log verbatim qui sont parsés par les
tests E2E. Cette séparation permet de tester les logs indépendamment.

- `log.py` — 14 fonctions de log structuré (📥, 🟡, 🔴, 🟣, 🧠, 🤖, 📤, ❌, 🔗, 📊)

### .agent/ (NOUVEAU — inspiré sellkit/.agent/)
**Raisonnement** : sellkit stocke les règles globales (AGENTS.md) et les skills
par phase (SKILL.md) dans `.agent/`. Cette séparation permet de modifier les
règles sans toucher au code.

- `memory/recruiter/AGENTS.md` — règles globales (langue, recadrage, URLs, rôle)
- `skills/recruiter/phase-first-contact/SKILL.md`
- `skills/recruiter/phase-qualification/SKILL.md`
- `skills/recruiter/phase-reformulation/SKILL.md`
- `skills/recruiter/phase-closing/SKILL.md`
- `skills/recruiter/phase-test-technique/SKILL.md`

### tests/ (restructuré — pattern sellkit)
**Raisonnement** : sellkit a 3 niveaux de tests (unit, integration, step*-human-in-the-loop).
Cette séparation permet de tester rapidement (unit), avec LLM (integration), et
bout-en-bout (e2e).

- `tests/unit/` — tests purs (memory, middleware, skills, telemetry, crm)
- `tests/integration/` — tests avec LLM (deep_agent invoke)
- `tests/e2e/` — tests human-in-the-loop Playwright (step1, step5, telegram_screening)

## 6. Phases d'exécution (avec statut final)

| Phase | Action | Status | Commit |
|---|---|---|---|
| 0 | Sauvegarder ce plan | ✅ fait | 074b3d0 |
| 1 | Créer hirekit/pipeline/ (qualification, objections, closing, memory) | ✅ fait | 074b3d0 |
| 2 | Créer hirekit/deep_agent/ (recruiter_agent, middleware, harness_profile) | ✅ fait | 9c2cd64 |
| 3 | Créer hirekit/crm/ (types, store) + hirekit/telemetry/ (log) | ✅ fait | f266fe9 |
| 4 | Créer .agent/ (AGENTS.md + 5 SKILL.md) | ✅ fait | d33b12d |
| 5 | Créer ateliers/atelier-05-deep-agents/ (GUIDE-ELEVE, exercice, solution, bugs, checkpoints) | ✅ fait | 7247d73 |
| 6 | Restructurer AT06 (Chatbots + Telegram + CRM — aligner handler.ts sellkit) | ✅ fait | 86bf5e5 |
| 7 | Créer AT07 (Évaluation + Déploiement + tests E2E Playwright) | ✅ fait | 86bf5e5 |
| 8 | Créer tests/unit/ (memory, middleware, skills, telemetry, crm) | ✅ fait | 996638a |
| 9 | Créer tests/integration/ (deep_agent invoke) | ✅ fait | d7fee50 |
| 10 | Créer tests/e2e/ (conftest, step1, step5, telegram_screening) | ✅ fait | d7fee50 |
| 11 | Git commit + push + documentation | ✅ fait | fe5fd0f |
| 12 | Correction alignement énoncés/code | ✅ fait | c7372c9 |

## 7. Corrections d'alignement énoncés/code (post-implémentation)

Après l'implémentation, une vérification systématique a révélé que les énoncés
(GUIDE-ELEVE.md) n'étaient pas tous alignés avec le code réel. Les écarts suivants
ont été trouvés et corrigés (commit c7372c9) :

| Écart | Avant | Après | Raisonnement |
|---|---|---|---|
| `hirekit/eval/metrics.py` | 3 stubs `NotImplementedError` | `compute_recall_at_k()`, `compute_mrr()`, `compute_cost()`, `evaluate_qa_dataset()` implémentés | AT07 dit d'utiliser ces métriques — le code doit exister |
| `hirekit/eval/tracing.py` | 1 stub `NotImplementedError` | `get_langsmith_callback()`, `is_tracing_enabled()`, `enable_tracing()`, `get_run_tags()` implémentés | AT07 dit de brancher LangSmith — le code doit exister |
| `hirekit/ui/telegram_bot.py` | Ancien code Cuba (commandes /search, /match) | Flux sellkit : `handle_message()` (objection→closing→memory→CRM→Deep Agent→reply) | AT06 décrit le flux sellkit — le code doit implémenter ce flux |
| `hirekit/ui/app.py` | 4 pages (Chat, Matching, CVs, Multimodal) | 5 pages : ajout "Pipeline CRM" kanban | AT06 mentionne un dashboard CRM kanban — la page doit exister |
| `atelier-06-eval-benchmark-deploy/` | Dossier doublon obsolète | Supprimé | Remplacé par `atelier-07-eval-deploy/` — le doublon crée de la confusion |