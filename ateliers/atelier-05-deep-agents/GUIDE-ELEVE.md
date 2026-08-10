# Atelier 05 — Deep Agents (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/deep_agent/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit.deep_agent; print('OK')"` affiche OK
- [ ] `python -c "from deepagents import create_deep_agent; print('OK')"` affiche OK
- [ ] Les CVs sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Le recruteur actuel est un simple chatbot. Transforme-le
en un agent autonome capable de planifier, de charger des compétences selon la phase de
conversation, et de persister sa mémoire entre sessions. Utilise la librairie Deep Agents
de LangChain."**

Tu as 4 couches à assembler :

1. **Couche 1 (systemPrompt)** : Identité statique + AGENTS.md (règles globales)
2. **Couche 2 (memory)** : AGENTS.md injecté dans le systemPrompt
3. **Couche 3 (skills)** : SKILL.md injecté dynamiquement par middleware beforeModel
4. **Couche 4 (contextSchema)** : RecruitmentContext (Pydantic) + contexte dynamique

**Livrable** : une démo CLI (`python ateliers/atelier-05-deep-agents/exercice.py`)
qui :
1. Crée un Deep Agent avec `create_deep_agent()` et 4 couches
2. Simule une conversation de recrutement avec un candidat
3. Charge dynamiquement le bon SKILL.md selon la phase (first-contact → qualification → reformulation → closing)
4. Persiste le contexte candidat (mémoire, stage, qualification fields)
5. Détecte les objections et signaux de closing via le middleware

**Critères de succès auto-vérifiables** :
- `create_deep_agent()` retourne un agent compilé avec `.invoke()`
- Le middleware `beforeModel` injecte le bon SKILL.md selon `qual_count`
- `build_context_prompt()` produit les bonnes sections (infos candidat, prochaine question, objection)
- `pytest tests/unit/test_middleware.py` passe
- `pytest tests/unit/test_skills.py` passe

**Budget temps** : 1h40 Core (+30 min Sprint OU 60 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : `create_deep_agent()`, `contextSchema` (Pydantic), `beforeModel` middleware,
  `HarnessProfile`, Skills (SKILL.md dynamiques), Memory (AGENTS.md), `build_context_prompt()`,
  `read_skill_for_context()`, `RecruitmentContext`
- ❌ **Hors scope** (ateliers suivants) : Streamlit, Telegram, CRM SQLite, follow-up sweep,
  Docker Compose, LangSmith tracing, tests E2E Playwright
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/deep_agent/middleware.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer les 4 couches Deep Agents en 3 phrases | (b) Modifier `qual_count` de 0 à 6, prédire quel SKILL.md sera chargé |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### create_deep_agent()

Un "harness" (cadre d'agent) batteries-inclu qui fournit des capacités built-in :
planning, filesystem, subagents, context management — sans avoir à les coder manuellement.

**Analogie** : une usine qui assemble un robot complet avec tous ses accessoires
(outils, mémoire, planning, skills). Au lieu de monter chaque pièce toi-même, tu donnes
une spec et l'usine assemble.

**Dans le projet** : `hirekit/deep_agent/recruiter_agent.py` appelle `create_deep_agent()`
avec `model`, `system_prompt`, `context_schema`, `middleware`, `checkpointer=False`.

### contextSchema (Pydantic)

Un schéma Pydantic qui décrit le contexte dynamique injecté avant chaque appel LLM.
Le middleware `beforeModel` reçoit ce contexte et peut l'utiliser pour personnaliser le prompt.

**Analogie** : une fiche de suivi que le manager remplit avant chaque entretien :
"Le candidat s'appelle Nathan, il a rempli 3/6 champs, il est au stage 'contacted',
la prochaine question à poser est sa disponibilité."

**Dans le projet** : `RecruitmentContext` (Pydantic) avec `qual_count`, `stage`,
`memory_prompt`, `next_field`, `objection_key`, `link_being_sent`, etc.

### beforeModel middleware

Un hook exécuté AVANT chaque appel au modèle LLM. Il peut modifier l'état
(messages) en injectant un SystemMessage avec du contenu dynamique.

**Analogie** : un secrétaire qui prépare le dossier du candidat avant chaque entretien.
Il lit la fiche de suivi, sort le bon manuel de procédure (SKILL.md), et prépare
le briefing (contexte dynamique). Le recruteur n'a plus qu'à conduire l'entretien.

**Dans le projet** : `hirekit/deep_agent/middleware.py` — `before_model()` injecte
le bon SKILL.md + le contexte dynamique (infos candidat, prochaine question,
objection détectée) avant chaque appel LLM.

### Skills dynamiques (SKILL.md)

Des fichiers markdown qui décrivent le comportement attendu selon la phase de
conversation. Le middleware charge le bon skill selon le contexte (qual_count, stage).

**Analogie** : des fiches réflexes que l'agent sort du tiroir selon la situation.
"Premier contact" pour le premier message, "Qualification" pour les questions,
"Reformulation" pour le résumé, "Closing" pour la conclusion.

**Dans le projet** : `.agent/skills/recruiter/phase-first-contact/SKILL.md`,
`phase-qualification/SKILL.md`, `phase-reformulation/SKILL.md`,
`phase-closing/SKILL.md`, `phase-test-technique/SKILL.md`.

La fonction `read_skill_for_context()` dans `middleware.py` choisit le bon skill :
- `qual_count=0` → `phase-first-contact`
- `qual_count 1-5` → `phase-qualification`
- `qual_count=6` → `phase-reformulation`
- `is_closing=True` → `phase-closing`
- `show_test_and_link=True` → ajoute `phase-test-technique`

### Memory (AGENTS.md)

Un fichier markdown lu au démarrage et injecté dans le systemPrompt.
Il contient les règles globales qui s'appliquent à toutes les phases.

**Analogie** : un post-it collé sur l'écran que l'agent relit à chaque démarrage.
"Tu parles français, tu recadres le hors sujet, tu ne donnes jamais d'URL,
tu es un recruteur pas un assistant."

**Dans le projet** : `.agent/memory/recruiter/AGENTS.md` — lu dans
`recruiter_agent.py` et injecté dans `IDENTITY_PROMPT`.

### HarnessProfile

Une configuration qui permet d'exclure certains tools et middleware du harness
Deep Agents. Utile quand on n'a pas besoin de toutes les fonctionnalités.

**Analogie** : des réglages usine — "je ne veux pas de planning automatique,
pas de subagents, pas de filesystem. Mon agent fait juste de la conversation."

**Dans le projet** : `hirekit/deep_agent/harness_profile.py` —
`register_recruiter_harness_profile()` exclut `write_todos`, `task`,
`SummarizationMiddleware`, `todoListMiddleware`.

### build_context_prompt()

Fonction qui construit le prompt de contexte dynamique à partir du
`RecruitmentContext`. Elle assemble les sections : infos candidat,
prochaine question, lien, objection, opt-out.

**Analogie** : le briefing que le manager donne avant chaque appel :
"Infos candidat: Nathan, débutant. Prochaine question: disponibilité.
Objection: trop_cher → tactique: reformuler la valeur."

**Dans le projet** : `hirekit/deep_agent/middleware.py` — `build_context_prompt()`
produit les sections en fonction des champs non-null de `RecruitmentContext`.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Lire l'architecture 4 couches (15 min)

**Objectif** : comprendre l'architecture Deep Agents avant de coder.

Ouvre ces fichiers et lis-les :
- `hirekit/deep_agent/recruiter_agent.py` — `create_deep_agent()` avec 4 couches
- `hirekit/deep_agent/middleware.py` — `beforeModel` + `build_context_prompt()`
- `.agent/memory/recruiter/AGENTS.md` — règles globales
- `.agent/skills/recruiter/phase-first-contact/SKILL.md` — skill de premier contact

Identifie chaque couche :
1. Couche 1 (systemPrompt) → `IDENTITY_PROMPT` dans `recruiter_agent.py`
2. Couche 2 (memory) → `AGENTS_MD` lu et injecté dans `IDENTITY_PROMPT`
3. Couche 3 (skills) → `read_skill_for_context()` dans `middleware.py`
4. Couche 4 (contextSchema) → `RecruitmentContext` (Pydantic) + `build_context_prompt()`

✋ **Checkpoint 1** — Lance `python ateliers/atelier-05-deep-agents/checkpoints/check_1.py`

---

### 🔬 Mini-lab — Changer de phase (15 min)

**Variable** : `qual_count` dans `RecruitmentContext`
**Plage** : tester qual_count=0, 3, 6

**Protocole** :
1. Crée un `RecruitmentContext(qual_count=0, stage="new")`
2. Appelle `read_skill_for_context(ctx)` → quel SKILL.md est retourné ?
3. Crée un `RecruitmentContext(qual_count=3, stage="contacted")`
4. Appelle `read_skill_for_context(ctx)` → quel SKILL.md est retourné ?
5. Crée un `RecruitmentContext(qual_count=6, stage="contacted")`
6. Appelle `read_skill_for_context(ctx)` → quel SKILL.md est retourné ?

| qual_count | stage | SKILL.md attendu |
|---|---|---|
| 0 | new | phase-first-contact |
| 3 | contacted | phase-qualification |
| 6 | contacted | phase-reformulation |
| 6 | interested | phase-closing (isClosing=True) |

---

### Étape 2 — Construire l'agent et simuler une conversation (30 min)

**Objectif** : créer un Deep Agent et simuler un tour de conversation.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-05-deep-agents/exercice.py`
- Importer `get_deep_agent` et `run_deep_turn` depuis `hirekit.deep_agent.recruiter_agent`
- Importer `RecruitmentContext` depuis `hirekit.deep_agent.middleware`
- Créer un contexte minimal : `RecruitmentContext(qual_count=0, stage="new")`
- Appeler `run_deep_turn(phone, messages, context)` → réponse texte

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — Skills inversés (qualification au lieu de first-contact)**
```bash
git apply ateliers/atelier-05-deep-agents/bugs/v1.patch
pytest ateliers/atelier-05-deep-agents/bugs/test_v1.py -v
```

**Bug v2 — AGENTS.md manquant (règles globales non injectées)**
```bash
git apply ateliers/atelier-05-deep-agents/bugs/v2.patch
pytest ateliers/atelier-05-deep-agents/bugs/test_v2.py -v
```

**Bug v3 — contextSchema vide (pas de contexte dynamique)**
```bash
git apply ateliers/atelier-05-deep-agents/bugs/v3.patch
pytest ateliers/atelier-05-deep-agents/bugs/test_v3.py -v
```

---

### 📊 Mesure-toi (15 min)

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Agent créé** | Oui/Non | Oui |
| **beforeModel injecte SKILL.md** | Oui/Non | Oui |
| **build_context_prompt produit sections** | ___/5 | 5 |
| **Latence create_deep_agent** | ___s | < 5s |
| **Skills chargés correctement** | ___/4 | 4 |

✋ **Checkpoint final** — `python ateliers/atelier-05-deep-agents/checkpoints/check_final.py`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les concepts fondamentaux.

**Sprint 1 — create_deep_agent()** : ouvre `hirekit/deep_agent/recruiter_agent.py`,
lis comment `create_deep_agent()` est appelé. Identifie les 4 paramètres principaux.

**Sprint 2 — beforeModel** : ouvre `hirekit/deep_agent/middleware.py`, lis la fonction
`before_model()`. Comprends comment elle injecte le SKILL.md + le contexte.

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — Subagents

Ajoute un subagent `screener` qui délègue le screening initial à un agent spécialisé.
Le recruteur principal délègue, le screener fait le travail, puis renvoie le résultat.

### Défi Bonus 2 — SummarizationMiddleware

Active `SummarizationMiddleware` dans le harness profile et observe comment l'agent
résume automatiquement l'historique après 50 messages.

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Qu'est-ce que `create_deep_agent()` ?
2. Quelles sont les 4 couches de l'architecture Deep Agents ?
3. À quoi sert le `contextSchema` ?
4. Que fait le middleware `beforeModel` ?
5. Comment sont chargés les SKILL.md dynamiquement ?
6. Quelle est la différence entre AGENTS.md et SKILL.md ?
7. À quoi sert le `HarnessProfile` ?
8. Que fait `build_context_prompt()` ?
9. Comment le middleware choisit-il quel skill charger ?
10. Pourquoi `checkpointer=False` dans notre configuration ?

---

## 🔗 Pour aller plus loin

**Pont avec AT06** : Le Deep Agent est créé, mais il ne sait pas encore parler à Telegram
ni mettre à jour un CRM. Au prochain atelier, on connectera l'agent à Telegram (handler
objection→closing→memory→CRM→agent→reply) et on construira le dashboard CRM Streamlit.

**Documentation Deep Agents** :
- https://docs.langchain.com/oss/python/deepagents/overview
- https://reference.langchain.com/python/deepagents/