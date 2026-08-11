# Atelier 05 — Chatbots + Code Analysis + Multimodal (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/ui/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] L'index FAISS existe (`data/faiss_index/`) — sinon : `python ateliers/atelier-03-rag/solution.py`
- [ ] Le repo `data/code_repo/` contient des fichiers `.py` (sinon : `python scripts/generate_code_repo.py`)
- [ ] J'ai relu les GUIDE-ELEVE d'AT03 (RAG) et AT04 (Agents)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Le RAG (AT03) et l'Agent (AT04) fonctionnent en CLI.
Maintenant expose-les dans deux interfaces utilisateur : (1) un bot Telegram simulé
pour les recruteurs en mobilité, et (2) un Code Reviewer RAG qui indexe un repo Python
et répond aux questions des développeurs sur le code."**

**Livrable** : une démo CLI (`python ateliers/atelier-05-chatbot-code-review/exercice.py`) qui :

1. Teste le bot Telegram simulé (`process_command`) — commandes `/start`, `/help`,
   `/search`, `/web`, `/match`, `/code`
2. Indexe le repo `data/code_repo/` avec `GenericLoader` + `LanguageParser`
3. Pose des questions sur le code (où est l'auth, que fait `hash_password`…) et obtient
   des **réponses générées par le LLM** (pas de simples extraits bruts)
4. Génère un résumé structuré du repo (`get_code_summary`)
5. (Bonus) Lance le dashboard Streamlit : `streamlit run hirekit/ui/app.py`

**Critères de succès auto-vérifiables** :

- `process_command` répond aux 6 commandes (`start`, `help`, `status`, `search`, `web`, `code`)
- `index_code_repo` retourne un `BaseRetriever` fonctionnel
- `ask_code_question_with_llm` produit une réponse en langage naturel citant les fichiers
- `get_code_summary` liste les fichiers avec leurs classes et fonctions
- Le Q&A sur le code cite au moins un fichier source par réponse

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : `process_command` (bot Telegram simulé), `GenericLoader` +
  `LanguageParser`, chunking du code (séparateurs `class`/`def`), FAISS sur le code,
  Q&A sourcé sur le code via LLM, `get_code_summary` (AST), Streamlit (bonus)
- ❌ **Hors scope** (ateliers suivants) : CRM SQLite, pipeline complet Telegram
  (objection→closing→memory→CRM→agent→reply), Docker, LangSmith, tests E2E
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/ui/telegram_bot.py` et `code_reviewer.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer pourquoi `LanguageParser` est mieux qu'un loader texte pour le code | (b) Changer `chunk_size` de 500 à 200, prédire l'effet sur le Q&A code |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### Bot Telegram simulé

Le bot Telegram est simulé en local via `process_command(command, args)` — aucune
configuration API Telegram n'est requise. En production, `start_telegram_bot_real()`
branche le même handler sur `python-telegram-bot`.

**Analogie** : un standardiste qui suit une procédure simple (commandes) avant de
passer à des conversations complexes (AT06).

### GenericLoader + LanguageParser

`GenericLoader` charge les fichiers d'un dossier selon un pattern (`**/*.py`).
`LanguageParser` parse le code en préservant la structure (classes, fonctions, imports)
plutôt qu'en découpant naïvement au caractère.

**Analogie** : `LanguageParser`, c'est lire un livre chapitre par chapitre. Un loader
texte brut, c'est lire page par page sans tenir compte des sections.

### Chunking du code

Le code se chunk différemment du texte naturel : on utilise des séparateurs
`["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]` pour préserver les blocs logiques.
Couper au milieu d'une fonction détruit le contexte sémantique.

### ask_code_question_with_llm

Contrairement à `ask_code_question` (qui retourne des extraits bruts sans LLM),
`ask_code_question_with_llm` construit une chaîne RAG complète
(`retriever | prompt | llm | parser`) pour produire une réponse en langage naturel.

> ⚠️ **Important** : `ask_code_question` (sans LLM) est utile pour les tests et le
> debugging, mais **ne réalise pas la mission** de cet atelier — l'élève doit voir
> une vraie réponse générée par le LLM, pas juste des extraits de code.

**Dans le projet** : `hirekit/ui/code_reviewer.py:162` — `ask_code_question_with_llm`
construit la chaîne LCEL et invoque le LLM avec le contexte récupéré.

### get_code_summary

Analyse les fichiers `.py` via le module `ast` de Python et retourne un dictionnaire
avec le nombre de fichiers, les classes et les fonctions détectées par fichier.

### Streamlit (bonus)

Framework Python pour construire des dashboards web sans HTML/CSS.
`hirekit/ui/app.py` expose les pages : Chat, Dashboard Matching, Bibliothèque CVs,
Multimodal.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Bot Telegram simulé (25 min)

**Objectif** : tester les commandes du bot Telegram simulé.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-05-chatbot-code-review/exercice.py` (TODO 1)
- Importer `process_command` depuis `hirekit.ui.telegram_bot`
- Tester les commandes :
  ```python
  from hirekit.ui.telegram_bot import process_command

  print(process_command("start"))
  print(process_command("help"))
  print(process_command("search", "qui a de l'expérience en React ?"))
  print(process_command("web", "Marie Dubois développeur React"))
  ```

**Observation attendue** : `start` affiche le message de bienvenue, `help` liste les
commandes, `search` utilise le RAG FAISS (AT03), `web` utilise l'outil `web_search`
(AT04), `code` utilise le Code Reviewer.

**C'est le moment de dire** : "Le bot Telegram n'est qu'une fine couche de présentation
au-dessus des outils qu'on a construits aux ateliers précédents. `process_command`
délègue à `search_cvs_tool`, `web_search_tool`, etc."

✋ **Checkpoint 1** — `python ateliers/atelier-05-chatbot-code-review/checkpoints/check_1.py`

---

### Mini-lab — GenericLoader vs loader texte (15 min)

Compare les deux stratégies de chargement sur `data/code_repo/` :

```python
from hirekit.ui.code_reviewer import load_python_files
from langchain_community.document_loaders import TextLoader

# Avec GenericLoader + LanguageParser
docs = load_python_files("data/code_repo")
print(f"GenericLoader: {len(docs)} documents")
for d in docs[:3]:
    print(f"  [{d.metadata.get('source')}] {len(d.page_content)} chars")
```

| Stratégie | Nb documents | Taille moy | Structure préservée ? |
|---|---|---|---|
| `GenericLoader` + `LanguageParser` | ___ | ___ | ___ |
| `TextLoader` brut | ___ | ___ | ___ |

**Question** : pourquoi `LanguageParser` produit-il des chunks plus cohérents pour
le Q&A sur le code ?

---

### Étape 2 — Indexer le repo Python (30 min)

**Objectif** : indexer `data/code_repo/` comme corpus RAG pour le Q&A sur le code.

**Indices (Build)** :
- Fichier à compléter : `exercice.py` (TODO 2)
- Importer `index_code_repo` depuis `hirekit.ui.code_reviewer`
- Indexer le repo :
  ```python
  from hirekit.ui.code_reviewer import index_code_repo

  retriever = index_code_repo("data/code_repo")
  print(f"Repo indexé: retriever prêt ({type(retriever).__name__})")
  ```
- Tester la recherche :
  ```python
  docs = retriever.invoke("hash_password")
  for d in docs:
      print(f"  [{d.metadata.get('filename')}] {d.page_content[:100]}...")
  ```

**Observation attendue** : le retriever retourne les chunks de code les plus pertinents.
Pour la question `hash_password`, les chunks contenant la définition de la fonction
doivent apparaître dans le top 3.

✋ **Checkpoint 2** — `python ateliers/atelier-05-chatbot-code-review/checkpoints/check_2.py`

---

### Étape 3 — Q&A sur le code avec LLM (20 min)

**Objectif** : poser des questions sur le code et obtenir des **réponses générées par
le LLM** (pas des extraits bruts).

**Indices (Build)** :
- Fichier à compléter : `exercice.py` (TODO 3)
- Importer `ask_code_question_with_llm` depuis `hirekit.ui.code_reviewer`
  (et **non** `ask_code_question` qui ne fait que retourner des extraits sans LLM)
- Poser les questions :
  ```python
  from hirekit.ui.code_reviewer import ask_code_question_with_llm

  questions = [
      "Où est gérée l'authentification ?",
      "Que fait la fonction hash_password ?",
      "Quels sont les modèles de la base de données ?",
      "Comment fonctionne le rate limiting ?",
  ]
  for question in questions:
      answer = ask_code_question_with_llm(question, retriever)
      print(f"Q: {question}\nA: {answer[:300]}...")
  ```

**Observation attendue** : le LLM répond en langage naturel en citant les fichiers et
fonctions concernés. Chaque réponse est sourcée (`[auth.py]`, `[models.py]`, etc.).

**C'est le moment de dire** : "Si tu affiches juste les extraits bruts sans LLM, tu ne
fais pas du RAG — tu fais de la recherche plein texte. Le RAG, c'est récupérer ET
générer une réponse contextualisée."

✋ **Checkpoint 3** — `python ateliers/atelier-05-chatbot-code-review/checkpoints/check_3.py`

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — `chunk_size=10` (chunks trop petits pour le code)**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v1.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v1.py -v
```
Observe : les chunks sont si petits qu'une fonction est éparpillée sur plusieurs
chunks. Le retriever ne retrouve pas la définition complète. Répare : remettre
`chunk_size=500`.

**Bug v2 — `ask_code_question` au lieu de `ask_code_question_with_llm`**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v2.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v2.py -v
```
Observe : les réponses sont des extraits bruts, pas des phrases en langage naturel.
L'élève croit voir du RAG, mais il n'y a pas de génération LLM. Répare : utiliser
`ask_code_question_with_llm`.

**Bug v3 — `LanguageParser` retiré (perte de structure)**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v3.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v3.py -v
```
Observe : le loader texte brut coupe au milieu des classes/fonctions. Le Q&A devient
incohérent. Répare : restaurer `GenericLoader` + `LanguageParser`.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Commandes bot fonctionnelles** | ___/6 | 6 |
| **Documents chargés** (`load_python_files`) | ___ | ≥ 3 |
| **Retriever code fonctionnel** | Oui/Non | Oui |
| **Q&A généré par le LLM** (`ask_code_question_with_llm`) | Oui/Non | Oui |
| **Réponse cite un fichier source** | Oui/Non | Oui |
| **`get_code_summary` liste les classes/fonctions** | Oui/Non | Oui |
| **Latence moyenne** Q&A code (s) | ___s | < 8s |

✋ **Checkpoint final** — `python ateliers/atelier-05-chatbot-code-review/checkpoints/check_final.py`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 2 concepts fondamentaux.

**Sprint 1 — GenericLoader + LanguageParser** : ouvre `hirekit/ui/code_reviewer.py`,
lis `load_python_files`. Charge un fichier `.py` avec et sans `LanguageParser` et
compare les documents produits.

**Sprint 2 — Q&A code** : ouvre `code_reviewer.py`, lis `ask_code_question_with_llm`.
Identifie la chaîne LCEL (`retriever | prompt | llm | parser`). Remarque la différence
avec `ask_code_question` (sans LLM) — pourquoi la version LLM répond-elle mieux ?

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — Streamlit dashboard

Lance le dashboard Streamlit :
```bash
streamlit run hirekit/ui/app.py
```

Explore les pages : Chat, Dashboard Matching, Bibliothèque CVs, Multimodal.
Ajoute une page "Code Reviewer" qui expose `ask_code_question_with_llm`.

### Défi Bonus 2 — Bot Telegram interactif

Lance le bot Telegram simulé :
```python
from hirekit.ui.telegram_bot import start_telegram_bot_simulated

start_telegram_bot_simulated()
```

Teste des conversations : `/search React`, `/code Où est l'authentification ?`,
`/match Marie Dubois | Dev React senior`.

### Défi Bonus 3 — Indexer un vrai repo

Indexe un vrai projet Python (par exemple `hirekit/` lui-même) et pose des questions
sur son architecture. Observe les limites du RAG sur un codebase plus complexe.

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Pourquoi utiliser `GenericLoader` + `LanguageParser` plutôt qu'un `TextLoader` brut ?
2. Quels séparateurs utilise-t-on pour le chunking du code Python ?
3. Quelle est la différence entre `ask_code_question` et `ask_code_question_with_llm` ?
4. Pourquoi la version LLM est-elle nécessaire pour la mission de cet atelier ?
5. Que fait `process_command` et quelles commandes sont disponibles ?
6. Comment le bot Telegram simulé délègue-t-il aux outils des ateliers précédents ?
7. Que retourne `get_code_summary` et comment utilise-t-il le module `ast` ?
8. Pourquoi le Q&A code doit-il citer les fichiers source ?
9. Comment passer du bot simulé au vrai bot Telegram en production ?
10. Quelles sont les limites du RAG sur un codebase complexe ?

→ Score >= 8/10 : prêt pour AT06 (CRM + Telegram + Pipeline complet).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT06** : le bot Telegram simulé de cet atelier expose des commandes
simples (`/search`, `/code`). Au prochain atelier, on construira le **handler
complet** (objection→closing→memory→CRM→agent→reply) qui transforme le bot en
copilote recruteur conversationnel, avec un CRM SQLite pour suivre le pipeline de
candidature en temps réel.

**Lien direct avec AT03/AT04** : le Code Reviewer réutilise le RAG FAISS d'AT03
(indexation, chunking, retriever) et le bot Telegram réutilise les tools d'AT04
(`search_cvs`, `web_search`). C'est la boucle : on assemble les briques des
ateliers précédents dans une interface utilisateur.