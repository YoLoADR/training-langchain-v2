# Atelier 06 — Chatbots + Telegram + CRM (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/ui/` et `hirekit/crm/` et lis les modules.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé
- [ ] `.env` contient une clé API valide
- [ ] `python -c "import hirekit.crm; print('OK')"` affiche OK
- [ ] `python -c "import hirekit.telemetry; print('OK')"` affiche OK
- [ ] `python -c "import hirekit.pipeline; print('OK')"` affiche OK
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Le Deep Agent (AT05) fonctionne en CLI. Maintenant,
connecte-le à Telegram pour qu'il parle aux candidats automatiquement. Et construis
un dashboard CRM pour que le recruteur suive le pipeline en temps réel."**

Le flux complet à implémenter (inspiré de sellkit/src/telegram/handler.ts) :

```
Candidat envoie un message Telegram
  ↓
1. Détection d'objection (LLM → fallback keyword)
  ↓
2. Détection de closing (LLM → fallback keyword → stage CRM)
  ↓
3. Extraction mémoire (LLM → 6 champs → merge → stockage DB)
  ↓
4. CRM: get_or_create, update_stage, add_message
  ↓
5. Deep Agent V3 (beforeModel injecte SKILL.md + contexte)
  ↓
6. Reply sur Telegram + log structuré
```

**Livrable** :
1. `hirekit/ui/telegram_bot.py` — handler complet (objection→closing→memory→CRM→agent→reply)
2. `hirekit/ui/app.py` — dashboard Streamlit (pipeline kanban, stats, messages)
3. `hirekit/telemetry/log.py` — 14 fonctions de log structuré

**Critères de succès** :
- Le handler Telegram suit le flux complet (6 étapes)
- Le CRM SQLite persiste les candidats, messages, stages
- Le dashboard Streamlit affiche le pipeline kanban
- Les logs structurés contiennent les 14 préfixes verbatim
- `pytest tests/unit/test_crm.py` passe
- `pytest tests/unit/test_telemetry.py` passe

---

## 🚧 Périmètre

- ✅ **Dans le scope** : Streamlit, python-telegram-bot (simulé), CRM SQLite (WAL),
  pipeline CRM (6 stages), follow-up sweep, dashboard API, logs structurés (14 préfixes),
  handler Telegram (objection→closing→memory→CRM→agent→reply)
- ❌ **Hors scope** : Deep Agents (AT05), RAG (AT03), LCEL (AT02), LangSmith (AT07),
  Docker Compose (AT07), tests E2E Playwright (AT07)

---

## 🧠 Carnet de bord (concepts à mobiliser)

### Pipeline CRM

Un tunnel de recrutement où chaque candidat avance d'étape en étape.

**Analogie** : un entonnoir de vente. Les candidats entrent en haut (new) et descendent
vers la conversion (closed_won) ou la sortie (closed_lost).

**Dans le projet** : `hirekit/crm/types.py` — `STAGES = [new, contacted, interested, qualified, closed_won, closed_lost]`

### SQLite + WAL

Un fichier de base de données avec des onglets, où plusieurs processus peuvent lire
en même temps qu'un autre écrit.

**Analogie** : un classeur avec des onglets. Le dashboard Streamlit lit pendant que
le bot Telegram écrit, sans conflit.

**Dans le projet** : `hirekit/crm/store.py` — `self.db.execute("PRAGMA journal_mode = WAL")`

### Logs structurés (14 préfixes)

Un journal de bord avec des icônes pour retrouver l'info vite. Chaque fonction de log
émet un préfixe exact (verbatim) parsé par les tests E2E.

**Analogie** : les pictogrammes d'un tableau de bord — 📥 pour les entrées, 📤 pour
les sorties, 🟡 pour les objections, 🟣 pour le closing.

**Dans le projet** : `hirekit/telemetry/log.py` — 14 fonctions : `msg_in()`, `objection()`,
`refusal()`, `closing()`, `memory()`, `llm_calling()`, `msg_out()`, `llm_error()`,
`conversion_link()`, `stage_update()`, etc.

### Handler Telegram (flux complet)

Le handler orchestre le flux complet à chaque message entrant : détection → CRM → agent → reply.

**Analogie** : un standardiste qui suit une procédure : 1. identifier l'appelant,
2. détecter le motif, 3. chercher le dossier, 4. transférer à l'expert, 5. répondre.

**Dans le projet** : `hirekit/ui/telegram_bot.py` — suit le flux :
`objection → closing → memory → CRM → Deep Agent → reply + log`

### Streamlit dashboard

Un tableau de bord visuel que le recruteur ouvre dans son navigateur. Affiche le pipeline
kanban, les stats globales, et l'historique des messages par candidat.

**Dans le projet** : `hirekit/ui/app.py` — colonnes kanban par stage, stats, messages.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — CRM Store SQLite (25 min)

**Objectif** : implémenter le CRM store avec SQLite WAL.

**Indices** :
- `hirekit/crm/store.py` — `CrmStore` avec `get_or_create()`, `update_stage()`, `add_message()`, `get_messages()`
- `hirekit/crm/types.py` — `Stage` (Enum), `Candidate` (dataclass)
- Inspire-toi de sellkit/src/crm/store.ts

### 🔬 Mini-lab — Pipeline stages (15 min)

Crée un candidat, ajoute des messages, change son stage. Observe le pipeline.

### Étape 2 — Handler Telegram (30 min)

**Objectif** : implémenter le handler complet.

**Indices** :
- `hirekit/ui/telegram_bot.py` — `handle_message(text, phone)` suit le flux
- `hirekit/pipeline/objections.py` — `detect_objection()`
- `hirekit/pipeline/closing.py` — `detect_closing()`
- `hirekit/pipeline/memory.py` — `extract_memory()`, `merge_memory()`
- `hirekit/crm/store.py` — `crm.get_or_create()`, `crm.add_message()`
- `hirekit/telemetry/log.py` — logs structurés

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer.

### 📊 Mesure-toi (15 min)

| Métrique | Valeur | Cible |
|---|---|---|
| **CRM store fonctionne** | Oui/Non | Oui |
| **Handler flux complet (6 étapes)** | ___/6 | 6 |
| **14 préfixes de log** | ___/14 | 14 |
| **Dashboard Streamlit affiche pipeline** | Oui/Non | Oui |

✋ **Checkpoint final**

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions** :
1. Quels sont les 6 stages du pipeline CRM ?
2. Qu'est-ce que WAL et pourquoi l'utilise-t-on ?
3. Quel est le flux complet du handler Telegram (6 étapes) ?
4. Combien de préfixes de log structuré existe-t-il ?
5. À quoi sert `get_or_create()` dans le CRM ?
6. Comment le handler détecte-t-il une objection ?
7. Comment le handler détecte-t-il un signal de closing ?
8. Comment la mémoire est-elle extraite et stockée ?
9. Qu'affiche le dashboard Streamlit ?
10. Comment le follow-up sweep fonctionne-t-il ?

---

## 🔗 Pour aller plus loin

**Pont avec AT07** : Le bot Telegram et le CRM fonctionnent. Au prochain atelier,
on évaluera les performances (LangSmith, Recall@k, MRR), on déploiera avec Docker
Compose, et on écrira les tests E2E human-in-the-loop avec Playwright.