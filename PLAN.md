# PLAN.md — Fil rouge ai-hirekit : développement des 6 ateliers LangChain

> Issue GitHub #1 — YoLoADR/training-langchain-v2
> Équipe 🇨🇺 Cuba (Fix + Continue) — Lot: `hirekit/llm/` + `hirekit/services/`
> Ateliers: AT01 + AT02 (priorité), puis continuation AT03-AT06

---

## Vue d'ensemble

Le repo contient déjà le squelette : package `hirekit/` avec stubs `NotImplementedError`,
6 dossiers d'ateliers, 14 fichiers de tests TDD, branches git par atelier. AT01 a un
GUIDE-ELEVE.md complet + exercice.py + solution.py.

Ce plan découpe le travail restant en User Stories, priorisées selon l'approche suggérée
par l'issue : données simulées d'abord, puis ateliers AT02→AT06.

---

## Phase 5 — Données simulées (scripts/generate_*.py)

Les ateliers dépendent de ces données. C'est le prérequis de tout le reste.

### US-DATA-01 : Générateur de CVs PDF fictifs

**Fichier** : `scripts/generate_cvs.py`
**Description** : Génère 30 CVs PDF (1-2 pages) avec profils variés :
dev React, dev Python, DevOps, designer, marketing, alternant, junior fullstack,
senior backend, data engineer, PO, etc.
**Format de sortie** : `data/cvs/cv_001.pdf` à `data/cvs/cv_030.pdf`
**Données par CV** : nom, email, téléphone, compétences (nom + niveau + années),
expériences (poste, entreprise, durée, description), formations, niveau d'anglais.
**Critères d'acceptation** :
- 30 fichiers PDF créés dans `data/cvs/`
- Noms français diversifiés (incluant les personas : Marie Dubois, Karim Benali, etc.)
- Au moins 10 profils différents représentés
- Le script est idempotent (relance = écrase)
- Tests : `pytest tests/test_data/` vérifie le count et la diversité

### US-DATA-02 : Générateur d'offres d'emploi JSON

**Fichier** : `scripts/generate_offers.py`
**Description** : Génère 15 offres d'emploi au format JSON.
**Format de sortie** : `data/offers/offer_001.json` à `data/offers/offer_015.json`
**Données par offre** : id, titre, entreprise, description, compétences requises (liste),
localisation, salaire (min/max), type de contrat, expérience requise, télétravail.
**Critères d'acceptation** :
- 15 fichiers JSON valides dans `data/offers/`
- Offres alignées avec les profils CV (React, Python, DevOps, design, etc.)
- Schéma cohérent pour le matching AT02

### US-DATA-03 : Taxonomie de compétences CSV

**Fichier** : `scripts/generate_skills.py`
**Description** : Génère `data/skills.csv` avec 100 compétences catégorisées.
**Format de sortie** : `data/skills.csv` (colonnes: id, nom, categorie, mots_cles)
**Catégories** : frontend, backend, devops, data, mobile, design, soft_skills, languages
**Critères d'acceptation** :
- 100 lignes dans skills.csv
- Au moins 8 catégories représentées
- Chaque compétence a des mots-clés pour le matching sémantique

### US-DATA-04 : Dataset QA JSONL

**Fichier** : `scripts/generate_qa_dataset.py`
**Description** : Génère 150 paires question/réponse au format JSONL pour l'évaluation (AT06).
**Format de sortie** : `data/qa_dataset.jsonl`
**Structure par ligne** : `{"id", "question", "reponse_attendue", "sources": [cv_ids], "type": "screening|matching|availability|general"}`
**Critères d'acceptation** :
- 150 lignes dans qa_dataset.jsonl
- Questions référencent les vrais CVs générés (ids correspondants)
- Types variés : screening (50), matching (50), availability (25), general (25)

### US-DATA-05 : Calendrier de disponibilité JSON

**Fichier** : `scripts/generate_availability.py`
**Description** : Génère un calendrier JSON de 30 jours de créneaux pour l'outil de planning (AT04).
**Format de sortie** : `data/availability.json`
**Structure** : `{"candidates": [{"candidate_id", "name", "slots": [{"date", "start", "end", "available": true/false}]}]}`
**Critères d'acceptation** :
- 30 candidats avec disponibilités sur 30 jours
- Créneaux de 1h entre 9h-18h
- ~60% des créneaux disponibles, 40% occupés (aléatoire reproductible avec seed)

### US-DATA-06 : Mini-repo Python pour Code-Reviewer

**Fichier** : `scripts/generate_code_repo.py`
**Description** : Génère 10 fichiers Python formant un mini-repo pour le Code-Reviewer (AT05).
**Format de sortie** : `data/code_repo/*.py` (10 fichiers)
**Contenu** : mini app Flask/FastAPI avec auth, models, routes, services, utils, tests
**Critères d'acceptation** :
- 10 fichiers .py créés
- Code réaliste et lisible (pas de lorem ipsum)
- Inclut: auth.py, models.py, routes.py, services.py, utils.py, config.py,
  database.py, middleware.py, errors.py, main.py

---

## Phase 14 — Scripts utilitaires

### US-UTIL-01 : Script de vérification d'atelier

**Fichier** : `scripts/check_atelier_ready.sh`
**Description** : Vérifie qu'un atelier est prêt (deps installées, .env configuré, données présentes).
**Critères d'acceptation** :
- `bash scripts/check_atelier_ready.sh 01` vérifie: venv, .env, data/cvs, data/offers
- Code sortie 0 si OK, 1 si manquant
- Messages clairs indiquant ce qui manque

### US-UTIL-02 : Script de vérification des scope guards

**Fichier** : `scripts/verify_branch_scope.sh`
**Description** : Vérifie que les `.claude/CLAUDE.md` scope guards sont en place sur chaque branche.
**Critères d'acceptation** :
- Vérifie les 6 ateliers ont un `.claude/CLAUDE.md`
- Rapporte les scope guards manquants

---

## Phase 7 — Atelier AT02 (LCEL + Mémoire)

> Lot équipe Cuba — `hirekit/services/matching.py`

### US-AT02-01 : Implémenter hirekit/services/matching.py

**Modules concernés** : `hirekit/services/matching.py`, `hirekit/llm/prompts.py` (get_matching_prompt)
**Description** : Chaîne LCEL de matching CV↔offre avec mémoire recruteur persistée.
**Concepts couverts** : LCEL pipe, RunnablePassthrough, RunnableLambda, RunnableParallel,
RunnablePassthrough.assign(), RunnableBranch, RunnableWithFallbacks,
ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory,
Persistence (save/load JSON), .batch()
**Critères d'acceptation** :
- `get_matching_chain()` retourne une chaîne LCEL fonctionnelle
- `pytest tests/test_services/test_matching.py` passe (xfail retiré)
- La chaîne accepte cv + offer et retourne un MatchResult

### US-AT02-02 : GUIDE-ELEVE.md complet pour AT02

**Fichier** : `ateliers/atelier-02-lcel-memoire/GUIDE-ELEVE.md`
**Description** : Guide complet (~400-600 lignes) suivant le pattern AT01.
**Structure** : Mission, Périmètre, Carnet de bord, Tronc commun, Mini-lab, Bug Hunt,
Sprint, Bonus, Wrap-up (quiz 10 questions)

### US-AT02-03 : exercice.py + solution.py pour AT02

**Fichiers** : `ateliers/atelier-02-lcel-memoire/exercice.py`, `solution.py`
**Description** : Exercice avec TODOs commentés + solution de référence.

### US-AT02-04 : Bugs + Checkpoints pour AT02

**Fichiers** : `ateliers/atelier-02-lcel-memoire/bugs/` (3 patches + 3 tests + 3 explications),
`ateliers/atelier-02-lcel-memoire/checkpoints/` (check_1.py + check_final.py)

---

## Phase 8 — Ateliers AT03 à AT06

Chaque atelier suit le même pattern qu'AT02 :
1. Implémentation du module hirekit/
2. GUIDE-ELEVE.md complet
3. exercice.py + solution.py
4. bugs/ (3 bugs) + checkpoints/ (2 QCM)
5. GUIDE-FORMATEUR.md

### US-AT03 : RAG (AT03) — hirekit/rag/
### US-AT04 : Agents + Tools (AT04) — hirekit/agent/
### US-AT05 : Chatbot + Code Review (AT05) — hirekit/ui/
### US-AT06 : Éval + Déploiement (AT06) — hirekit/eval/

(Détails à préciser au démarrage de chaque atelier)

---

## Ordre d'exécution

1. **US-DATA-01 à US-DATA-06** (en parallèle où possible) — prérequis de tout
2. **US-UTIL-01 + US-UTIL-02** — scripts utilitaires
3. **US-AT02-01 à US-AT02-04** — atelier LCEL + Mémoire
4. **US-AT03** — RAG
5. **US-AT04** — Agents
6. **US-AT05** — Chatbot
7. **US-AT06** — Éval + Déploiement

Commit après chaque US ou groupe cohérent. Push vers origin/main.