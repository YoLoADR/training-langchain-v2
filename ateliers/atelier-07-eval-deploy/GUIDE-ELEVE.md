# Atelier 07 — Évaluation + Déploiement + Tests E2E (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/eval/` et `tests/e2e/` et lis les modules.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé
- [ ] `pip install pytest-playwright` et `playwright install` ont été lancés
- [ ] `.env` contient `LANGSMITH_API_KEY=lsv2_...` et `LANGSMITH_TRACING=true`
- [ ] `python -c "import hirekit.eval; print('OK')"` affiche OK
- [ ] Docker est installé (`docker --version`)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Le bot Telegram et le CRM fonctionnent. Maintenant,
prouve-moi que ça marche bout en bout avec des tests E2E Playwright. Branche LangSmith
pour observer les traces. Déploie tout avec Docker Compose."**

**Livrable** :
1. `hirekit/eval/metrics.py` — `compute_recall_at_k()`, `compute_mrr()`, `compute_cost()`
2. `hirekit/eval/tracing.py` — `get_langsmith_callback()`
3. `tests/e2e/conftest.py` — fixtures Playwright (spawn app, wait, db, api)
4. `tests/e2e/test_step1_conversation.py` — 3 échanges → DB + API + logs
5. `tests/e2e/test_step5_full_pipeline.py` — 13 étapes, 3 scénarios aléatoires
6. `docker-compose.yml` — services api + streamlit + chromadb

**Critères de succès** :
- `pytest tests/e2e/ -v` passe (tests Playwright visibles)
- LangSmith trace automatiquement les appels LLM
- `docker compose up` lance tous les services
- Recall@5 ≥ 0.80 sur le dataset QA

---

## 🚧 Périmètre

- ✅ **Dans le scope** : LangSmith CallbackHandler, Recall@k, MRR, cost monitoring,
  Docker Compose, tests E2E Playwright (human-in-the-loop), conftest fixtures
- ❌ **Hors scope** : Deep Agents (AT05), Telegram handler (AT06), CRM (AT06),
  RAG (AT03), LCEL (AT02)

---

## 🧠 Carnet de bord

### LangSmith tracing

La boîte noire de l'avion : chaque appel LLM est enregistré automatiquement.

**Analogie** : un tableau de vol qui enregistre chaque action du pilote (LLM).

**Dans le projet** : auto-tracing via `LANGSMITH_TRACING=true` dans `.env`.

### Recall@k

Sur 10 questions, combien de fois la bonne réponse était dans le top k ?

**Analogie** : "sur 10 recrutements, combien de fois le bon candidat était dans
les 5 premiers ?"

**Dans le projet** : `compute_recall_at_k(results, k=5)` → ratio ≥ 0.80.

### Tests E2E human-in-the-loop (Playwright)

Des tests qui guident un humain à travers un scénario et vérifient l'état du système
(DB, API, logs) à chaque étape.

**Analogie** : un inspecteur qui suit une checklist de 13 points et coche chaque vérification.

**Dans le projet** : `tests/e2e/test_step5_full_pipeline.py` — 13 étapes, 3 scénarios
aléatoires (Nathan, Francis, Sarah), vérifie DB stage, msg_count, logs à chaque étape.

### Docker Compose

Un orchestre qui lance tous les services d'un coup.

**Analogie** : un chef d'orchestre qui dit "1, 2, 3, partez" et tous les musiciens
commencent en même temps.

**Dans le projet** : `docker-compose.yml` — api:8000, streamlit:8501, chromadb:8001.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Métriques d'évaluation (25 min)

**Indices** :
- `hirekit/eval/metrics.py` — `compute_recall_at_k()`, `compute_mrr()`, `compute_cost()`

### Étape 2 — Tests E2E Playwright (40 min)

**Indices** :
- `tests/e2e/conftest.py` — fixtures: `app` (spawn), `db` (SQLite read-only), `api` (HTTP client)
- `tests/e2e/test_step1_conversation.py` — 3 échanges, vérifie DB + API + logs
- Inspire-toi de sellkit/tests/step1-human-in-the-loop.test.ts (358 lignes)

### 🐛 Bug Hunt (20 min)

### 📊 Mesure-toi (15 min)

✋ **Checkpoint final**

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions** :
1. Qu'est-ce que LangSmith tracing ?
2. Comment active-t-on le tracing automatique ?
3. Qu'est-ce que Recall@k ?
4. Qu'est-ce que MRR ?
5. Comment les tests E2E Playwright vérifient-ils le système ?
6. Combien d'étapes a le test step5 ?
7. Combien de scénarios aléatoires ?
8. Que fait le conftest.py ?
9. Quels services lance docker-compose.yml ?
10. Pourquoi les tests E2E sont-ils importants ?

---

## 🔗 Pour aller plus loin

Le projet fil rouge est maintenant complet : 7 ateliers, de LLM nu à Deep Agents
autonome avec Telegram, CRM, et tests E2E. Tu as construit un équivalent Python
de sellkit (TypeScript), avec une architecture 4 couches Deep Agents.