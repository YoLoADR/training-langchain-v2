# Atelier 02 — LCEL + Mémoire conversationnelle (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/services/matching.py` et lis le
> module — mais alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] Les CVs sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] L'atelier 01 est terminé (tu sais ce qu'est un Output Parser et un ChatPromptTemplate)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"À l'atelier 01, on a vu qu'un LLM seul hallucine sur
les CVs. Maintenant, montre-moi qu'on peut composer une chaîne de matching
CV↔offre de manière déclarative avec LCEL — et qu'on peut garder en mémoire les
critères du recruteur entre deux sessions."**

**Livrable** : une démo CLI (`python ateliers/atelier-02-lcel-memoire/exercice.py`)
qui :

1. Construit une chaîne LCEL de matching CV↔offre
   (`RunnablePassthrough | prompt | llm | parser`)
2. Utilise `RunnablePassthrough`, `RunnableLambda`, `RunnableParallel`
3. Persiste une mémoire recruteur entre sessions (save/load JSON)
4. Traite 3 CVs en parallèle avec `.batch()`

**Critères de succès auto-vérifiables** :

- `pytest tests/test_services/test_matching.py` passe (chaîne LCEL, batch, mémoire)
- La chaîne LCEL est fonctionnelle : `chain.invoke({"cv": "...", "offer": "..."})` → `MatchResult`
- La mémoire est sauvegardée puis rechargée : les échanges sont conservés
- `batch_match(["CV 1", "CV 2", "CV 3"], offer)` retourne bien 3 `MatchResult`

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : LCEL (pipe `|`, `RunnablePassthrough`, `RunnableLambda`,
  `RunnableParallel`, `RunnablePassthrough.assign()`), Conversation Memory
  (`ConversationBufferWindowMemory`, `ConversationSummaryMemory`), Persistence
  (save/load JSON), `.batch()`, variables d'état
- ❌ **Hors scope** (ateliers suivants) : RAG, FAISS, ChromaDB, Document Loaders,
  Retriever, agents, tools, Streamlit, Telegram, Docker, LangSmith
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local
  (si tu utilises Claude/Cursor : demander "ajoute du RAG" ou "crée un agent"
  déclenchera un refus automatique — c'est intentionnel)

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/services/matching.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer LCEL vs chaîne classique en 3 phrases | (b) Modifier `k` de 10 à 3 dans `get_recruiter_memory`, prédire l'effet sur le contexte |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### LCEL (LangChain Expression Language)

LCEL est le langage déclaratif de LangChain pour composer des chaînes via l'opérateur
pipe `|`. Chaque composant (prompt, LLM, parser) est un `Runnable` qui expose
`.invoke()`, `.batch()`, `.stream()`.

**Analogie** : LCEL, c'est un pipeline Unix. `cat cv.txt | grep "Python" | wc -l`
chaîne des commandes ; `prompt | llm | parser` chaîne des Runnables. Chaque étape
prend la sortie de la précédère et produit une entrée pour la suivante.

**Dans le projet** : `get_matching_chain()` retourne
`RunnablePassthrough.assign(...) | prompt | llm | parser`.

### RunnablePassthrough

Un Runnable qui transmet son entrée inchangée. Utile pour injecter des variables
sans les perdre. Avec `.assign()`, il ajoute des clés au dict d'entrée.

**Analogie** : un courrier qui transmet la même lettre mais ajoute un post-it
avec une info supplémentaire (`assign`).

**Dans le projet** : `RunnablePassthrough.assign(cv=lambda x: clean_cv(x["cv"]))`
nettoie le CV tout en gardant l'entrée originale accessible.

### RunnableLambda

Enveloppe une fonction Python classique dans un Runnable. Permet d'insérer
n'importe quelle logique Python dans une chaîne LCEL.

**Analogie** : un adaptateur qui transforme une fonction lambda en brique
compatible avec le pipe LCEL.

**Dans le projet** : `clean_cv_lambda = RunnableLambda(lambda x: clean_cv(x["cv"]))`
est une brique réutilisable dans n'importe quelle chaîne.

### RunnableParallel

Exécute plusieurs Runnables en parallèle sur le même input et retourne un dict
avec les résultats de chaque branche.

**Analogie** : un chef de chantier qui lance trois équipes en parallèle sur le
même terrain, chacune avec sa mission, puis collecte les rapports.

**Dans le projet** : `get_extraction_and_matching_chain()` lance l'extraction CV
et le matching en parallèle via `RunnableParallel(extraction=..., matching=...)`.

### ConversationBufferWindowMemory

Mémoire conversationnelle qui garde les `k` derniers échanges (fenêtre glissante).
Contrairement à une mémoire complète, elle ne garde que les messages récents
pour contrôler le coût en tokens.

**Analogie** : un recruteur qui se souvient des 10 dernières questions/réponses
mais oublie le début de la conversation — assez pour le contexte, sans noyer
le LLM sous 200 messages.

**Dans le projet** : `get_recruiter_memory(k=10)` crée une mémoire avec fenêtre
de 10 échanges.

### ConversationSummaryMemory

Mémoire qui résume automatiquement les anciens échanges via le LLM, plutôt que
de les garder mot pour mot. Économise des tokens mais perd le détail exact.

**Analogie** : un résumé de réunion plutôt que le compte-rendu intégral. Tu gardes
l'essence, tu perds les citations exactes.

**Dans le projet** : `get_summary_memory(llm)` crée une mémoire auto-résumante.

### Persistence (save/load)

Sauvegarder l'état de la mémoire dans un fichier (JSON) pour la recharger dans
une session ultérieure. Sans persistence, la mémoire est percie à chaque
redémarrage.

**Analogie** : un carnet de notes que le recruteur ferme le soir et rouvre le
lendemain — sans lui, il repart de zéro chaque matin.

**Dans le projet** : `save_memory(memory, path)` sérialise en JSON ;
`load_memory(path)` reconstruit la mémoire depuis le fichier.

### .batch()

Méthode des Runnables qui traite une liste d'inputs en parallèle (un seul appel
retourne une liste de résultats). Plus efficace que boucler sur `.invoke()`.

**Analogie** : un ascenseur qui monte 3 personnes en une seule rotation plutôt que
3 rotations individuelles.

**Dans le projet** : `batch_match(cvs, offer)` matche 3 CVs contre la même offre
en un seul appel `.batch()`.

### Variables d'état

Clés injectées dans le dict d'entrée via `RunnablePassthrough.assign()` pour
enrichir le contexte sans perdre les données existantes. Permet de faire
transiter l'historique de mémoire, les instructions de format, etc.

**Analogie** : un formulaire auquel on ajoute des champs cachés (date, session,
préférences) que l'utilisateur ne voit pas mais qui enrichissent le traitement.

**Dans le projet** : `.assign(format_instructions=lambda _: parser.get_format_instructions())`
injecte les instructions de format Pydantic dans le dict transitant dans la chaîne.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Première chaîne LCEL (25 min)

**Objectif** : construire la chaîne de matching CV↔offre avec LCEL.
`RunnablePassthrough.assign()` → `ChatPromptTemplate` → `ChatModel` → `PydanticOutputParser`.

**Indices (Build)** :

- Fichier à compléter : `ateliers/atelier-02-lcel-memoire/exercice.py`
- Importer `get_matching_chain` depuis `hirekit.services.matching`
- Importer `get_chat_model` depuis `hirekit.llm.provider`
- Importer `MatchResult` depuis `hirekit.llm.parsers`
- La chaîne attend un dict `{"cv": "...", "offer": "..."}` et retourne un `MatchResult`
  ```python
  from hirekit.services.matching import get_matching_chain

  chain = get_matching_chain()  # utilise le chat model par défaut
  result = chain.invoke({
      "cv": "Marie Dubois, Développeuse React 4 ans",
      "offer": "Développeur React senior",
  })
  print(result.score)        # float 0.0–1.0
  print(result.recommandation)  # "shortlister" | "refuser" | "à voir"
  ```
- La chaîne utilise `RunnablePassthrough.assign()` pour nettoyer le CV et l'offre
  avant de les passer au prompt. Ouvre `hirekit/services/matching.py` et lis
  `get_matching_chain()` pour comprendre la composition.

**Observation attendue** : le LLM reçoit le CV nettoyé et l'offre dans un
ChatPromptTemplate structuré (system + human), il retourne un JSON valide que
le `PydanticOutputParser` convertit en objet `MatchResult`. On obtient un score,
une justification, des points forts/faibles et une recommandation — le tout typé.

**C'est le moment de dire** : "Ce que vous voyez là, c'est LCEL. Pas de glue code,
pas de chaînes de méthodes illisibles. Un pipe, comme en shell. Chaque brique
est un Runnable interchangeable : on peut remplacer le LLM, le parser, le prompt,
sans toucher au reste."

✋ **Checkpoint 1** — Lance `python ateliers/atelier-02-lcel-memoire/checkpoints/check_1.py`

---

### Mini-lab — RunnableSequential vs RunnableParallel (15 min)

Construis deux variantes de ta chaîne et compare.

**Variante séquentielle** (extraction puis matching) :
```python
from hirekit.services.matching import get_matching_chain
from hirekit.llm.parsers import get_cv_parser
from hirekit.llm.prompts import get_cv_extraction_prompt
from hirekit.llm.provider import get_chat_model

llm = get_chat_model(temperature=0.1)
extraction_chain = get_cv_extraction_prompt() | llm | get_cv_parser()
match_chain = get_matching_chain(llm)

# Séquentiel : d'abord extraire, ensuite matcher
extracted = extraction_chain.invoke({"cv": "Marie Dubois, React 4 ans"})
match = match_chain.invoke({"cv": str(extracted), "offer": "Dev React"})
```

**Variante parallèle** :
```python
from hirekit.services.matching import get_extraction_and_matching_chain

parallel = get_extraction_and_matching_chain(llm)
result = parallel.invoke({"cv": "Marie Dubois, React 4 ans", "offer": "Dev React"})
# result = {"extraction": CVInfo, "matching": MatchResult}
```

| Approche | Latence | Tokens | Qualité |
|---|---|---|---|
| Séquentiel (extraction → matching) | ___s | ___ | ___ |
| Parallèle (RunnableParallel) | ___s | ___ | ___ |

**Observation attendue** : la version parallèle est plus rapide (les deux
branches tournent en même temps) mais consomme potentiellement plus de tokens
en parallèle. C'est l'arbitrage latence/coût.

---

### Étape 2 — Mémoire conversationnelle et persistence (30 min)

**Objectif** : créer une mémoire recruteur, y ajouter des échanges, la sauvegarder
en JSON, la recharger, et vérifier que l'historique est conservé.

**Indices (Build)** :

- Importer `get_recruiter_memory`, `save_memory`, `load_memory` depuis
  `hirekit.services.matching`
- Créer la mémoire, ajouter des messages, sauvegarder :
  ```python
  from hirekit.services.matching import get_recruiter_memory, save_memory
  from langchain_core.messages import HumanMessage, AIMessage

  memory = get_recruiter_memory(k=10)
  memory.chat_memory.add_message(HumanMessage(content="Qui a de l'expérience en React ?"))
  memory.chat_memory.add_message(AIMessage(content="Marie Dubois a 4 ans d'expérience."))

  save_memory(memory, "data/memory_recruiter.json")
  ```
- Recharger dans une "nouvelle session" :
  ```python
  from hirekit.services.matching import load_memory

  memory_reloaded = load_memory("data/memory_recruiter.json", k=10)
  history = memory_reloaded.load_memory_variables({}).get("history", [])
  print(f"Messages restaurés : {len(history)}")
  ```
- Construire une chaîne avec mémoire via `get_matching_chain_with_memory()` :
  la chaîne injecte l'historique dans le prompt grâce à
  `RunnablePassthrough.assign()`.

**Observation attendue** : après `save_memory` puis `load_memory`, les échanges
sont restaurés. La mémoire est persistée entre sessions — le recruteur ferme
son terminal, le rouvre, et l'historique est toujours là.

**C'est le pont vers la production** : en production, la mémoire permet au
recruteur de dire "je cherche un profil React senior" à une session, puis de
reprendre la conversation plus tard sans tout réexpliquer. C'est ce qui fait
passer l'outil d'un one-shot à un véritable assistant conversationnel.

✋ **Checkpoint 2** — Lance `python ateliers/atelier-02-lcel-memoire/checkpoints/check_2.py`

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — RunnableLambda oublié (fonction non-Runnable dans le pipe)**

```bash
git apply ateliers/atelier-02-lcel-memoire/bugs/v1.patch
pytest ateliers/atelier-02-lcel-memoire/bugs/test_v1.py -v
```

Observe : la chaîne plante car une fonction Python classique est insérée
directement dans le pipe sans `RunnableLambda`. Répare : enrouler la fonction
dans `RunnableLambda(ma_fonction)`.

**Bug v2 — Mémoire non persistée (chemin relatif cassé)**

```bash
git apply ateliers/atelier-02-lcel-memoire/bugs/v2.patch
pytest ateliers/atelier-02-lcel-memoire/bugs/test_v2.py -v
```

Observe : `save_memory` écrit dans un chemin relatif qui n'existe pas, la
mémoire n'est jamais sauvegardée. Répare : utiliser `Path(path)` avec
`mkdir(parents=True, exist_ok=True)`.

**Bug v3 — .batch() avec input unique au lieu de liste**

```bash
git apply ateliers/atelier-02-lcel-memoire/bugs/v3.patch
pytest ateliers/atelier-02-lcel-memoire/bugs/test_v3.py -v
```

Observe : `batch_match` appelle `.batch()` avec un dict au lieu d'une liste de
dicts, un seul CV est traité (ou erreur). Répare : construire
`[{"cv": cv, "offer": offer} for cv in cvs]` avant `.batch()`.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Chaîne LCEL fonctionnelle** (invoke → MatchResult ?) | Oui/Non | Oui |
| **RunnableParallel** (extraction + matching en parallèle) | Oui/Non | Oui |
| **Mémoire sauvegardée** (fichier JSON créé ?) | Oui/Non | Oui |
| **Mémoire rechargée** (messages restaurés ?) | Oui/Non | Oui |
| **Batch de 3 CVs** (3 MatchResult retournés ?) | Oui/Non | Oui |
| **Latence matching 1 CV** (s) | ___s | < 5s |
| **Latence batch 3 CVs** (s) | ___s | < 10s |
| **Tokens consommés** (total session) | ___ | observable |

✋ **Checkpoint final** — `python ateliers/atelier-02-lcel-memoire/checkpoints/check_final.py`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 2 concepts fondamentaux.

**Sprint 1 — LCEL et le pipe** : ouvre `hirekit/services/matching.py`, lis
`get_matching_chain()`. Comprends comment `RunnablePassthrough.assign()` enrichit
l'entrée, puis comment `prompt | llm | parser` chaîne les Runnables. Écris 3 lignes
qui invoquent la chaîne sur un CV et une offre.

**Sprint 2 — Mémoire et persistence** : ouvre `hirekit/services/matching.py`, lis
`get_recruiter_memory()`, `save_memory()` et `load_memory()`. Crée une mémoire,
ajoute 2 messages, sauvegarde, recharge, affiche l'historique. Observe que les
messages sont conservés.

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — ConversationSummaryMemory

Remplace la `ConversationBufferWindowMemory` par une `ConversationSummaryMemory`
(via `get_summary_memory(llm)`). Observe comment le LLM résume automatiquement
les anciens échanges. Compare :

| Métrique | BufferWindow (k=10) | Summary |
|---|---|---|
| Tokens consommés après 20 échanges | ___ | ___ |
| Détail préservé | Oui/Non | Oui/Non |
| Latence (injection mémoire) | ___s | ___s |

**Question** : dans quel cas utiliser Summary plutôt que BufferWindow pour
ai-hirekit ? (indice : longues sessions de recrutement vs sessions courtes)

### Défi Bonus 2 — RunnableBranch (routing conditionnel)

Ajoute un `RunnableBranch` qui route vers différentes chaînes selon le score
de matching :
- score ≥ 0.7 → chaîne "shortlister" (génère une grille d'entretien)
- score 0.4–0.7 → chaîne "à voir" (demande plus d'infos au recruteur)
- score < 0.4 → chaîne "refuser" (génère un mail de refus poli)

**Indices** :
- `RunnableBranch` prend un dict `{condition: runnable, "default": runnable}`
- La condition est une fonction `(input) -> bool`
- Tu peux réutiliser `get_matching_chain()` comme première étape, puis router
  selon `result.score`

**Exemple de structure** :
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["score"] >= 0.7, chain_shortlist),
    (lambda x: x["score"] >= 0.4, chain_more_info),
    chain_reject,  # default
)
```

Observe : le routing conditionnel permet de construire un workflow de
recrutement sans if/else explicites — c'est déclaratif, c'est LCEL.

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Qu'est-ce que LCEL et quel opérateur est utilisé pour chaîner les Runnables ?
2. Quelle est la différence entre `RunnablePassthrough` et `RunnablePassthrough.assign()` ?
3. À quoi sert `RunnableLambda` ? Donne un exemple concret du projet.
4. Que fait `RunnableParallel` et quelle structure de données retourne-t-il ?
5. Quelle est la différence entre `ConversationBufferWindowMemory` et `ConversationSummaryMemory` ?
6. Pourquoi persiste-t-on la mémoire en JSON ? Que se passe-t-il sans persistence ?
7. Que fait `.batch()` et en quoi diffère-t-il de plusieurs `.invoke()` en boucle ?
8. Comment les "variables d'état" sont-elles injectées dans une chaîne LCEL ?
9. Cite 2 avantages de LCEL par rapport à une chaîne construite à la main avec des appels de méthode.
10. Dans ai-hirekit, quand aura-t-on besoin du RAG (AT03) pour résoudre quel problème ?

→ Score ≥ 8/10 : prêt pour AT03 (RAG).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT03 (RAG)** : à l'atelier 02, on a construit une chaîne LCEL de
matching et une mémoire conversationnelle. Mais le LLM reçoit le texte du CV
directement dans le prompt — il n'y a pas de recherche sémantique. Si tu as
1000 CVs en base, tu ne peux pas tous les mettre dans le prompt. Au prochain
atelier (AT03 — RAG), on indexera les CVs dans un vector store (FAISS /
ChromaDB), on fera une recherche sémantique pour récupérer les CVs pertinents,
et on les injectera dans le contexte du LLM. La chaîne LCEL deviendra :
`retriever | prompt | llm | parser`. Le RAG résoudra enfin le problème
d'hallucination identifié à l'atelier 01 — le LLM répondra sur les *vrais* CVs,
pas sur des tokens statistiquement plausibles.

**Pour approfondir LCEL** :
- [LCEL officiel](https://python.langchain.com/docs/expression_language/) — doc complète
- `RunnablePassthrough.assign()` — enrichissement du contexte
- `RunnableBranch` — routing conditionnel déclaratif
- `.stream()` — streaming des tokens en temps réel (hors scope ici, à tester
  en bonus si tu as le temps)

**Pour approfondir la mémoire** :
- `ConversationBufferMemory` — mémoire complète sans limite (attention aux tokens)
- `ConversationSummaryBufferMemory` — hybrid : buffer récent + summary ancien
- `VectorStoreRetrieverMemory` — mémoire sémantique (pont avec AT03 RAG)