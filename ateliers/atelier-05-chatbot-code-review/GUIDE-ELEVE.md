# Atelier 05 — Chatbots + Code Analysis + Multimodal (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/ui/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `pip install streamlit` a été lancé (interface web Streamlit)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] `python -c "import streamlit; print('OK')"` affiche OK
- [ ] Les CVs sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] Le repo de code est présent dans `data/code_repo/` (10 fichiers `.py`) — sinon : `python scripts/generate_code_repo.py`
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"On a un agent qui matche des CVs (AT04).
Maintenant je veux trois interfaces : un bot Telegram pour les recruteurs mobiles,
un Code-Reviewer qui indexe notre repo Python et répond aux questions des développeurs,
et une app Streamlit type ChatGPT pour le bureau."**

**Livrable** : une démo CLI (`python ateliers/atelier-05-chatbot-code-review/exercice.py`)
qui :

1. Lance le bot Telegram simulé et teste les commandes (`/start`, `/help`, `/search`, `/web`, `/code`)
2. Indexe le repo `data/code_repo/` (10 fichiers `.py`) avec GenericLoader + LanguageParser
3. Pose des questions sur le code ("Où est l'authentification ?", "Que fait `hash_password` ?")
4. (Bonus) Démarre Streamlit avec `streamlit run hirekit/ui/app.py` (4 pages : Chat, Dashboard, Bibliothèque, Multimodal)

**Critères de succès auto-vérifiables** :
- `pytest tests/test_ui/test_telegram_bot.py` passe (bot simulé + `process_command`)
- `pytest tests/test_ui/test_code_reviewer.py` passe (GenericLoader, indexation, Q&A)
- `pytest tests/test_ui/test_app.py` passe (fonctions Streamlit)
- Le code reviewer répond aux questions ("Où est l'auth ?" → extrait de `auth.py`)
- `format_response` respecte la limite Telegram (4096 caractères)

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : Streamlit UX (`st.chat_message`, `st.chat_input`, multi-pages),
  bot Telegram simulé (`process_command`, commandes `/search` `/web` `/code`),
  GenericLoader + LanguageParser (parsing `.py`), Code RAG (indexation FAISS + Q&A sur code),
  multimodal mock (transcription vocale simulée + TTS mock), `format_response` (limite 4096)
- ❌ **Hors scope** (ateliers suivants) : LangSmith, tracing, évaluation automatisée,
  Docker, déploiement, CI/CD, benchmarking, FastAPI REST API en production
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local
  (si tu utilises Claude/Cursor : demander "ajoute LangSmith" ou "dockerise tout"
  déclenchera un refus automatique — c'est intentionnel)

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/ui/telegram_bot.py` et `hirekit/ui/code_reviewer.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer `process_command` vs agent AT04 en 3 phrases | (b) Modifier `format_response` pour tronquer à 1000 chars, prédire l'effet sur les longues réponses |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### Streamlit

Framework Python pour créer des applications web interactives sans écrire de HTML/CSS/JS.
Tu écris du Python séquentiel (`st.title()`, `st.write()`) et Streamlit génère l'UI.

**Analogie** : c'est un notebook Jupyter qui se transforme automatiquement en site web
avec navigation, boutons, formulaires — sans toucher au frontend.

**Dans le projet** : `hirekit/ui/app.py` contient 4 pages — Chat, Dashboard Matching,
Bibliothèque CVs, Multimodal — lancées via `streamlit run hirekit/ui/app.py`.

### st.chat_message / st.chat_input

Composants Streamlit dédiés au chat. `st.chat_message("user")` crée une bulle de message
avec avatar, `st.chat_input()` affiche une barre de saisie en bas de page.

**Analogie** : ce sont les briques qui transforment une page web en interface type
ChatGPT — bulles avec avatars, historique défilant, saisie persistante.

**Dans le projet** : `render_chat_page()` utilise `st.chat_message` pour afficher
l'historique et `st.chat_input` pour capturer le message utilisateur. L'historique
est stocké dans `st.session_state["chat_messages"]`.

### ChatGPT UX

Le pattern d'interface conversationnelle popularisé par ChatGPT : bulles de messages
alternées (user/assistant), historique persistant dans la session, indicateur de
"typing" pendant la génération. L'utilisateur tape en langage naturel, l'assistant
répond en streaming ou avec un spinner.

**Dans le projet** : `render_chat_page()` réplique ce pattern avec `st.spinner("Réflexion...")`
pendant que `_process_chat_message()` génère la réponse.

### GenericLoader

Loader LangChain générique qui peut charger des fichiers depuis un système de fichiers
avec différents parsers. On le configure avec un `glob` (ex: `**/*.py`) et un parser
spécifique au langage.

**Analogie** : un chef de chantier qui ramasse tous les fichiers d'un type donné dans
un dossier et les confie au spécialiste approprié (LanguageParser pour Python).

**Dans le projet** : `load_python_files()` utilise `GenericLoader.from_filesystem()`
avec `glob="**/*.py"` et `LanguageParser(parser_threshold=50)`.

### LanguageParser

Parser LangChain qui structure le code source en préservant les éléments logiques :
classes, fonctions, imports. Au lieu de traiter un fichier `.py` comme du texte brut,
il sépare les blocs de code en documents distincts.

**Analogie** : un éditeur de code qui comprend la syntaxe — il ne découpe pas au
milieu d'une fonction mais respecte les blocs `class` et `def`.

**Dans le projet** : `LanguageParser(parser_threshold=50)` ignore les fichiers de
moins de 50 lignes (évite le bruit des `__init__.py` vides).

### Code RAG

Application du pattern RAG (Retrieval-Augmented Generation) à du code source au lieu
de documents textuels. On indexe les fichiers `.py` dans un vectorstore (FAISS), puis
on récupère les chunks pertinents pour répondre à des questions sur le code.

**Analogie** : au lieu d'un chatbot qui lit des PDFs, c'est un assistant développeur
qui "connaît" ton codebase et peut dire où se trouve l'auth ou ce que fait une fonction.

**Dans le projet** : `index_code_repo()` construit le pipeline complet —
`load_python_files` → `chunk_code_documents` → `FAISS.from_documents` → retriever MMR.
`ask_code_question()` interroge le retriever et retourne les extraits de code pertinents.

### Multimodal (STT / TTS)

**STT** (Speech-to-Text) : convertit un signal audio en texte (transcription vocale).
**TTS** (Text-to-Speech) : convertit du texte en signal audio (synthèse vocale).

Dans un assistant multimodal, l'utilisateur peut parler au lieu d'écrire (STT), et
l'assistant peut répondre à voix (TTS).

**Analogie** : STT = dictée vocale sur ton téléphone. TTS = Siri/Léa qui te parle.

**Dans le projet** : `render_multimodal_page()` mock ces deux modalités — l'utilisateur
tape un texte censé simuler une transcription STT, et le TTS affiche le texte au lieu
de générer un vrai audio. Les vrais modèles (Whisper, OpenAI TTS) seraient branchés
en production.

### Bot Telegram

Bot automatisé sur la messagerie Telegram. L'utilisateur envoie des commandes
(`/search React`, `/code Où est l'auth ?`) et le bot répond via l'API Telegram.

**Analogie** : un assistant recruteur qu'un consultant peut utiliser depuis son
téléphone, dans les transports, sans ouvrir un laptop.

**Dans le projet** : `telegram_bot.py` fournit deux modes — `start_telegram_bot_simulated()`
(mock local via stdin, pas de config API) et `start_telegram_bot_real()` (vrai bot
via `python-telegram-bot`, nécessite `TELEGRAM_BOT_TOKEN`).

### process_command

Fonction centrale du bot Telegram qui route une commande vers la bonne action.
Prend une commande (`"search"`, `"help"`, `"code"`) et des arguments, retourne
une réponse formatée.

**Analogie** : un standardiste qui reçoit un appel, identifie le service demandé
et transfère au bon département.

**Dans le projet** : `process_command("search", "React")` → invoque `search_cvs_tool`.
`process_command("code", "Où est l'auth ?")` → invoque `index_code_repo` + `ask_code_question`.
Les commandes inconnues retournent un message d'aide.

### format_response (4096 chars)

Telegram impose une limite de 4096 caractères par message. `format_response` tronque
le texte si nécessaire et ajoute `[...tronqué]` pour indiquer la coupure.

**Analogie** : un compte Twitter qui coupe les messages trop longs — sauf qu'ici
on ajoute un marqueur au lieu de couper brutalement.

**Dans le projet** : `format_response(text, max_length=4096)` — si `len(text) > 4096`,
retourne `text[:4076] + "\n\n[...tronqué]"`. Tous les résultats du bot passent
par cette fonction avant d'être envoyés.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Bot Telegram simulé (25 min)

**Objectif** : tester `process_command` sur toutes les commandes du bot, comprendre
le routing commande → outil.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-05-chatbot-code-review/exercice.py`
- Importer `process_command` depuis `hirekit.ui.telegram_bot`
- Tester les commandes dans cet ordre :
  ```python
  # Commande de bienvenue
  print(process_command("start"))
  # → 🤖 HireKit Bot — Assistant recruteur

  # Aide
  print(process_command("help"))
  # → 📋 Commandes disponibles: /start, /help, /search, /match, /web, /code, /quit

  # Recherche de candidats
  print(process_command("search", "qui a de l'expérience en React ?"))
  # → resultat de search_cvs_tool

  # Recherche web (réputation)
  print(process_command("web", "Marie Dubois développeur React"))
  # → resultat de web_search_tool

  # Question sur le code
  print(process_command("code", "Où est gérée l'authentification ?"))
  # → extrait de auth.py
  ```
- Comprendre le routing : `/search` → `search_cvs_tool`, `/web` → `web_search_tool`,
  `/code` → `index_code_repo` + `ask_code_question`
- Tester le mode simulé interactif : `start_telegram_bot_simulated()` (lit stdin)

**Observation attendue** : chaque commande route vers un tool différent. Les commandes
sans args (`/search` sans query) retournent un message "Usage". Les commandes inconnues
retournent "Commande inconnue, tape /help". La fonction `format_response` tronque
les réponses > 4096 caractères.

✋ **Checkpoint 1** — Lance `pytest tests/test_ui/test_telegram_bot.py -v`

---

### Mini-lab — Bot vs Agent AT04 (15 min)

Compare la réponse du bot Telegram (`process_command("search", "React")`) avec la
réponse de l'agent AT04 (`run_agent("Qui a de l'expérience en React ?")`).

| Critère | Bot Telegram (`process_command`) | Agent AT04 (`run_agent`) |
|---|---|---|
| **Routing** | Routage statique (if/elif) | Routage dynamique (LLM décide) |
| **Latence** | Rapide (pas de LLM pour router) | Plus lent (LLM réfléchit) |
| **Flexibilité** | Commandes fixes uniquement | Langage naturel |
| **Contrôle** | 100% prévisible | Le LLM peut choisir le mauvais tool |

**Question** : quand préférer un bot à commandes fixes vs un agent LLM ?
→ Réponse : pour les workflows critiques et répétitifs (recruteur mobile), le bot
garde un contrôle total. Pour l'exploration libre (dashboard au bureau), l'agent
est plus flexible.

---

### Étape 2 — Code Reviewer (30 min)

**Objectif** : indexer le repo `data/code_repo/` (10 fichiers `.py`) et poser des
questions sur le code via RAG.

**Indices (Build)** :
- Importer `index_code_repo`, `ask_code_question`, `get_code_summary` depuis
  `hirekit.ui.code_reviewer`
- Indexer le repo et poser des questions :
  ```python
  # Indexer le repo
  retriever = index_code_repo("data/code_repo")
  print(f"Repo indexé: {type(retriever).__name__}")

  # Poser des questions sur le code
  questions = [
      "Où est gérée l'authentification ?",
      "Que fait la fonction hash_password ?",
      "Quels sont les modèles de la base de données ?",
      "Comment fonctionne le rate limiting ?",
  ]
  for question in questions:
      print(f"Q: {question}")
      answer = ask_code_question(question, retriever)
      print(f"A: {answer[:300]}...\n")
  ```
- Générer un résumé du repo :
  ```python
  summary = get_code_summary("data/code_repo")
  print(f"Total fichiers: {summary['total_files']}")  # → 10
  for f in summary["files"]:
      print(f"  {f['filename']}: {f['num_classes']} classes, {f['num_functions']} fonctions")
  ```

**Observation attendue** : `index_code_repo` charge les 10 fichiers `.py` via
GenericLoader + LanguageParser, les chunk avec des séparateurs adaptés au code
(`\nclass `, `\ndef `, `\n\n`, `\n`), construit un index FAISS et retourne un
retriever MMR. Les questions "Où est l'auth ?" retournent des extraits de `auth.py`.
"Que fait `hash_password` ?" retourne la fonction de hash SHA-256.

**C'est le pont avec le RAG AT03** : le pattern est identique (loader → chunker →
vectorstore → retriever), mais appliqué à du code au lieu de CVs. Le LanguageParser
remplace le text splitter générique pour préserver la structure du code.

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — format_response ne tronque pas (limite absente)**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v1.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v1.py -v
```
Observe : les réponses > 4096 caractères passent telles quelles → Telegram rejette
le message. Répare : remettre la troncature avec `text[:max_length - 20] + "\n\n[...tronqué]"`.

**Bug v2 — LanguageParser désactivé (loader générique au lieu de code)**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v2.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v2.py -v
```
Observe : les fichiers `.py` sont chargés comme du texte brut, les fonctions sont
découpées au milieu. Les réponses aux questions sur le code sont moins précises.
Répare : remettre `LanguageParser(parser_threshold=50)` dans le GenericLoader.

**Bug v3 — process_command ne route pas /code (commande manquante)**
```bash
git apply ateliers/atelier-05-chatbot-code-review/bugs/v3.patch
pytest ateliers/atelier-05-chatbot-code-review/bugs/test_v3.py -v
```
Observe : `/code Où est l'auth ?` retourne "Commande inconnue" au lieu d'invoquer
le code reviewer. Répare : remettre le bloc `if command == "code":` avec l'appel
à `index_code_repo` + `ask_code_question`.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Commandes bot testées** | ___ / 6 | ≥ 6 |
| **Fichiers `.py` indexés** | ___ | 10 |
| **Questions code répondues** | ___ / 4 | ≥ 3 |
| **`format_response` respecte 4096** | Oui/Non | Oui |
| **`pytest tests/test_ui/` passe** | ___ tests OK | 100% |
| **Latence indexation repo** (s) | ___s | < 10s |
| **Latence Q&A code** (s) | ___s | < 3s |

✋ **Checkpoint final** — `pytest tests/test_ui/ -v`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 2 concepts fondamentaux.

**Sprint 1 — Bot Telegram simulé** : ouvre `hirekit/ui/telegram_bot.py`, lis comment
`process_command` route les commandes. Teste `process_command("start")`,
`process_command("help")`, `process_command("search", "React")` dans un terminal.
Vérifie que `format_response` tronque bien à 4096 caractères.

**Sprint 2 — Code Reviewer** : ouvre `hirekit/ui/code_reviewer.py`, lis le pipeline
`load_python_files` → `chunk_code_documents` → `index_code_repo`. Indexe le repo
`data/code_repo/` et pose la question "Où est l'authentification ?". Vérifie que
la réponse contient un extrait de `auth.py`.

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — Streamlit multi-pages (30 min)

Lance l'application Streamlit et explore les 4 pages :
```bash
streamlit run hirekit/ui/app.py
```

Pages disponibles :
1. **💬 Chat** — interface type ChatGPT avec `st.chat_message` et `st.chat_input`
2. **📊 Dashboard Matching** — matcher un CV avec une offre, visualiser le score
3. **📚 Bibliothèque CVs** — liste et recherche de CVs par mot-clé
4. **🎙️ Multimodal** — transcription vocale mock + TTS mock

**Défi** : ajoute une 5ème page "💻 Code Reviewer" dans `hirekit/ui/app.py` qui
permet de poser des questions sur le code via l'interface Streamlit (input texte →
`index_code_repo` + `ask_code_question` → réponse affichée).

### Défi Bonus 2 — Vrai bot Telegram (15 min)

Configure un vrai bot Telegram via BotFather :
1. Crée un bot sur Telegram via @BotFather → récupère le token
2. Ajoute `TELEGRAM_BOT_TOKEN=...` dans `.env`
3. `pip install python-telegram-bot`
4. Lance `start_telegram_bot_real()` depuis `hirekit/ui/telegram_bot.py`
5. Teste les commandes depuis ton téléphone : `/search React`, `/code Où est l'auth ?`

### Défi Bonus 3 — Multimodal STT/TTS (20 min)

Remplace les mocks par de vrais modèles :
1. **STT** : branche OpenAI Whisper (`openai.Audio.transcribe`) sur un fichier audio
2. **TTS** : branche OpenAI TTS (`openai.Audio.speech`) pour vocaliser la réponse
3. Modifie `render_multimodal_page()` dans `hirekit/ui/app.py` pour utiliser les vrais modèles
4. Teste : parle → transcription → réponse LLM → vocalisation

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Qu'est-ce que Streamlit et pourquoi l'utiliser pour un chatbot ?
2. Que font `st.chat_message` et `st.chat_input` ?
3. Quelle est la différence entre le bot Telegram (`process_command`) et l'agent AT04 ?
4. Qu'est-ce que GenericLoader et pourquoi l'utiliser pour du code ?
5. Que fait LanguageParser et pourquoi ne pas utiliser un text splitter générique ?
6. Explique le pipeline du Code RAG (3 étapes) ?
7. Quelle est la limite Telegram et comment `format_response` la gère-t-elle ?
8. Que sont STT et TTS dans un assistant multimodal ?
9. Cite 2 différences entre le bot Telegram simulé et le vrai bot.
10. Dans ai-hirekit, quand aura-t-on besoin de LangSmith (AT06) et pourquoi ?

→ Score ≥ 8/10 : prêt pour AT06 (LangSmith + Évaluation + Déploiement).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT06** : le bot Telegram et le Code Reviewer fonctionnent, mais on n'a
aucune visibilité sur ce qui se passe — pas de traces, pas de métriques, pas
d'évaluation automatisée. Au prochain atelier, on instrumente tout avec LangSmith
(traces des chaînes, scoring des réponses, A/B testing des prompts), on conteneurise
l'application avec Docker, et on déploie en production. Le bot Telegram simulé
deviendra un vrai service persistant.