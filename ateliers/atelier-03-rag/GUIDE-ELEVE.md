# Atelier 03 — RAG sur CVs et offres (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/rag/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e \".[dev]\"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] Les 30 CVs PDF sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] Les 15 offres JSON sont présentes dans `data/offers/` (sinon : `python scripts/generate_offers.py`)
- [ ] `data/skills.csv` existe (sinon : `python scripts/generate_skills.py`)
- [ ] J'ai relu le GUIDE-ELEVE d'AT01 — notamment les 5 questions privées qui hallucinaient
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"À l'atelier 01, on a prouvé qu'un LLM nu hallucine
sur les CVs. Maintenant,索引-les et fais-lui retrouver les vraies réponses. Je veux
un Q&A sourcé : chaque réponse cite le CV source. Et le hallucination rate doit
tomber à 0%."**

**Livrable** : une démo CLI (`python ateliers/atelier-03-rag/exercice.py`) qui :

1. Charge 30 CVs PDF + 15 offres JSON + `skills.csv`
2. Chunk les documents avec `RecursiveCharacterTextSplitter`
3. Construit un index FAISS pour les CVs + ChromaDB pour les offres
4. Repose les 5 questions privées d'AT01 avec le RAG → hallucination rate chute à 0%
5. Fait du Q&A sourcé (chaque réponse cite son CV source)

**Critères de succès auto-vérifiables** :

- `pytest tests/test_rag/` passe (ingestion, chunking, vectorstore, retriever)
- Recall@5 >= 0.80 (le retriever trouve le bon CV dans le top 5 pour les 5 questions)
- 0 hallucination sur les 5 questions privées (Marie Dubois, Karim Benali, Sophie Martin, Léa Chen, Thomas Petit)
- Chaque réponse RAG cite sa source (`[cv_001]`, `[cv_007]`, etc.)

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : Document Loaders (`PyMuPDFLoader`, `JSONLoader`, `CSVLoader`),
  Text Splitters (`RecursiveCharacterTextSplitter`, `CharacterTextSplitter`),
  Vector Stores (FAISS, ChromaDB), Embeddings (FastEmbed / Fake),
  Retriever (MMR, similarity), anti-hallucination, Recall@k, Q&A sourcé
- ❌ **Hors scope** (ateliers suivants) : Agents, Tools, Streamlit, Telegram, Docker,
  LCEL avancé, LangSmith, Benchmarking
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local
  (si tu utilises Claude/Cursor : demander "ajoute un agent" ou "déploie en Docker"
  déclenchera un refus automatique — c'est intentionnel)

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/rag/ingestion.py` et `hirekit/rag/chunking.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer RAG en 3 phrases (récupération + génération) | (b) Modifier `chunk_size` de 200 à 800, prédire l'effet sur le Recall@5 |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### RAG (Retrieval-Augmented Generation)

Le RAG est un pattern en deux étapes : **récupérer** les documents pertinents depuis
un index, puis **générer** une réponse en injectant ces documents dans le contexte du
LLM. Le modèle ne hallucine plus car il répond depuis des sources réelles.

**Analogie** : un examen à livre ouvert. Sans RAG, l'étudiant répond de mémoire (il
invente). Avec RAG, on lui donne les bonnes pages du manuel avant qu'il rédige sa
réponse — il cite ses sources.

**Dans le projet** : `build_rag_chain()` construit la chaîne LCEL
`RunnablePassthrough.assign(context=retriever) | prompt | llm | StrOutputParser`.

### Document Loader

Un loader convertit un fichier (PDF, JSON, CSV) en objets `Document` LangChain avec
du contenu (`page_content`) et des métadonnées (`metadata`).

**Types dans le projet** :
- `PyMuPDFLoader` — PDF → un Document par page (CVs)
- `JSONLoader` / parsing manuel — JSON → un Document par offre
- `CSVLoader` / parsing manuel — CSV → un Document par compétence

**Analogie** : un traducteur qui transforme des formats fichiers en un format unique
que la suite de la pipeline comprend (le `Document` LangChain).

### Text Splitter

Découpe un document long en chunks plus petits pour l'indexation vectorielle. Un
chunk trop grand dilue la pertinence ; trop petit perd le contexte.

**`CharacterTextSplitter`** — découpe à taille fixe sur un séparateur unique (`\n`).
Simple mais peut couper au milieu d'une phrase.

**`RecursiveCharacterTextSplitter`** — essaie d'abord `\n\n` (paragraphes), puis
`\n` (lignes), puis ` ` (mots), puis `""` (caractères). Préserve la structure
sémantique. **Recommandé par LangChain.**

**Analogie** : le splitter récursif, c'est couper un gâteau d'abord aux lignes
naturelles, puis au milieu si besoin. Le splitter fixe, c'est couper tous les 5 cm
même à travers une cerise.

### Embeddings

Convertit du texte en vecteur numérique (ex: 384 dimensions). Deux textes
sémantiquement proches produisent des vecteurs proches dans l'espace vectoriel.

**Dans le projet** : `get_default_embeddings()` retourne `FastEmbedEmbeddings`
(modèle multilingue 384d sur CPU) en production, ou `FakeEmbeddings` (384d
déterministe) en test/CI.

**Analogie** : les embeddings, c'est le GPS sémantique. "Développeur React" et
"Ingénieur frontend React" atterrissent au même endroit du GPS, même si les mots
diffèrent.

### Vector Store

Stocke les vecteurs d'embeddings et permet la recherche de similarité (cosinus).
Étant donnée une query, il retourne les k documents dont les vecteurs sont les plus
proches.

**FAISS** — optimisé pour la recherche en mémoire, rapide, sérialisable sur disque.
Utilisé pour les CVs (recherche purement sémantique).

**ChromaDB** — optimisé pour les requêtes avec filtrage de métadonnées
(catégorie, localisation). Persistant. Utilisé pour les offres (le recruteur filtre
par catégorie ou localisation).

**Analogie** : FAISS, c'est l'index à l'arrière d'un livre (très rapide pour
chercher par mot-clé). ChromaDB, c'est une bibliothèque avec des étiquettes par
rayon et par éditeur (on filtre avant de chercher).

### Retriever

Interface unifiée pour récupérer des documents pertinents depuis un Vector Store.
`vectorstore.as_retriever()` transforme un Vector Store en `BaseRetriever` avec
une méthode `.invoke(query)`.

**`search_type="similarity"`** — cosinus simple, retourne les k plus proches.

**`search_type="mmr"`** — Maximal Marginal Relevance, équilibre pertinence et
diversité (évite les doublons de CVs).

### MMR (Maximal Marginal Relevance)

Algorithme de sélection qui maximise la pertinence **et** la diversité des résultats.
À chaque étape, il sélectionne le document le plus pertinent qui est aussi le plus
différent des documents déjà sélectionnés.

**`lambda_mult`** (0 à 1) contrôle l'arbitrage :
- `0` = max diversité (résultats très variés)
- `1` = max pertinence (résultats les plus proches de la query)
- `0.5` = équilibre (défaut)

**Analogie** : un recruteur qui selection des candidats. Sans MMR, il prend les 5
candidats qui se ressemblent le plus (tous backend Python). Avec MMR, il prend les
plus pertinents mais s'assure qu'ils ne sont pas tous identiques (un backend, un
fullstack, un DevOps...).

### Recall@k

Métrique de retrieval : sur les k documents retournés, est-ce que le document
pertinent (ground truth) est présent ? Recall@5 = 1.0 si le bon CV est dans le top 5.

**Dans cet atelier** : pour chaque question privée, le CV correspondant
(ex: `cv_001` pour Marie Dubois) doit apparaître dans les 5 résultats du retriever.

### Anti-hallucination

Stratégie pour empêcher le LLM d'inventer des réponses. Dans le RAG, on injecte le
system prompt : *"Réponds UNIQUEMENT sur le contexte fourni. Si la réponse n'est pas
dans le contexte, dis 'Je n'ai pas cette information.'"* Le LLM n'invente plus car
il est contraint par les sources.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Document Loaders (25 min)

**Objectif** : charger 30 CVs PDF, 15 offres JSON et `skills.csv` en objets
`Document` LangChain.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-03-rag/exercice.py`
- Importer les loaders depuis `hirekit.rag.ingestion` :
  ```python
  from hirekit.rag.ingestion import load_all_cvs, load_all_offers, load_skills_csv

  cvs_docs = load_all_cvs("data/cvs")          # → 30+ pages de CV
  offers_docs = load_all_offers("data/offers")  # → 15 offres
  skills_docs = load_skills_csv("data/skills.csv")  # → 100 compétences
  ```
- Vérifier les métadonnées : chaque `Document` a `metadata["type"]` ("cv", "offer",
  "skill"), `metadata["source"]` (chemin), et `metadata["filename"]` (pour les CVs)

**Observation attendue** : `load_all_cvs` retourne ≥ 30 documents (1 page par CV
minimum). `load_all_offers` retourne exactement 15 documents. `load_skills_csv`
retourne 100 documents (un par compétence du CSV). Toutes les métadonnées sont
présentes et typées.

**C'est le moment de dire** : "Chaque Document LangChain porte son contenu texte
ET ses métadonnées. Ces métadonnées feront toute la différence au moment du Q&A
sourcé : on pourra citer `[cv_001]` comme source parce qu'on a conservé le
`filename`."

✋ **Checkpoint 1** — `python ateliers/atelier-03-rag/checkpoints/check_1.py`

---

### Mini-lab — RecursiveCharacterTextSplitter vs CharacterTextSplitter (15 min)

Compare les deux stratégies de chunking sur les 30 CVs et remplis ce tableau :

```python
from hirekit.rag.chunking import compare_chunking_strategies

stats = compare_chunking_strategies(cvs_docs, chunk_size=400)
print(stats)
# {'fixed_size': {'count': ..., 'avg_size': ..., 'min_size': ..., 'max_size': ...},
#  'recursive':  {'count': ..., 'avg_size': ..., 'min_size': ..., 'max_size': ...}}
```

| Stratégie | Nb chunks | Taille moy | Taille min | Taille max | Qualité perçue |
|---|---|---|---|---|---|
| `CharacterTextSplitter` (fixe) | ___ | ___ | ___ | ___ | ___ |
| `RecursiveCharacterTextSplitter` (récursif) | ___ | ___ | ___ | ___ | ___ |

**Question** : pourquoi le chunking récursif produit-il des chunks plus cohérents
(découpe aux paragraphes plutôt qu'au caractère près) ?

**Réponse attendue** : le splitter récursif essaie `\n\n` → `\n` → ` ` → ``, donc
il découpe aux frontières naturelles du texte. Le splitter fixe coupe tous les N
caractères sur `\n` uniquement, ce qui peut tronquer une phrase ou une liste de
compétences au milieu.

---

### Étape 2 — Vector Stores + Embeddings (30 min)

**Objectif** : construire un index FAISS pour les CVs et un index ChromaDB pour les
offres, puis tester la recherche de similarité.

**Indices (Build)** :
- Importer les vector stores :
  ```python
  from hirekit.rag.vectorstore_faiss import build_faiss_index, search_cvs
  from hirekit.rag.vectorstore_chroma import build_chroma_index, search_offers

  # Index FAISS pour les CVs (chunks de 400 caractères)
  cv_chunks = chunk_cvs(cvs_docs, chunk_size=400, chunk_overlap=50)
  faiss_store = build_faiss_index(cv_chunks, force_rebuild=True)
  print(f"Index FAISS construit : {len(cv_chunks)} chunks indexés")

  # Index ChromaDB pour les offres (chunks de 600 caractères)
  offer_chunks = chunk_offers(offers_docs, chunk_size=600, chunk_overlap=100)
  chroma_store = build_chroma_index(offer_chunks)
  print(f"Index ChromaDB construit : {len(offer_chunks)} chunks indexés")
  ```
- Tester la recherche :
  ```python
  results = search_cvs("React Python", vectorstore=faiss_store, k=5)
  for r in results:
      print(f"  [{r.metadata.get('filename')}] {r.page_content[:80]}...")
  ```

**Observation attendue** : FAISS retourne les chunks de CVs les plus similaires à la
query. `search_cvs("Marie Dubois React")` doit retourner des chunks de `cv_001`
dans le top 5. ChromaDB fait de même pour les offres, avec en plus la possibilité de
filtrer par métadonnées (`filter={"categorie": "frontend"}`).

**C'est le pont vers le Q&A sourcé** : les métadonnées `filename` des résultats
permettront de citer la source dans la réponse finale. Sans métadonnées, on a des
chunks mais on ne sait pas de quel CV ils proviennent.

✋ **Checkpoint 2** — `python ateliers/atelier-03-rag/checkpoints/check_2.py`

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — Chunk size trop petit (chunks de 50 caractères)**
```bash
git apply ateliers/atelier-03-rag/bugs/v1.patch
pytest ateliers/atelier-03-rag/bugs/test_v1.py -v
```
Observe : les chunks sont si petits que les compétences et expériences sont
éparpillées sur plusieurs chunks. Le retriever ne retrouve pas le bon CV.
Répare : remettre `chunk_size=400`.

**Bug v2 — Pas de métadonnées de source (filename manquant)**
```bash
git apply ateliers/atelier-03-rag/bugs/v2.patch
pytest ateliers/atelier-03-rag/bugs/test_v2.py -v
```
Observe : les résultats de recherche n'ont plus `metadata["filename"]`. Impossible
de citer la source dans le Q&A sourcé. Répare : remettre l'enrichissement des
métadonnées dans `load_cv_pdf`.

**Bug v3 — Retriever `search_type="invalid"` (ValueError)**
```bash
git apply ateliers/atelier-03-rag/bugs/v3.patch
pytest ateliers/atelier-03-rag/bugs/test_v3.py -v
```
Observe : `get_cv_retriever(search_type="invalid")` lève une `ValueError`. La chaîne
RAG ne se construit pas. Répare : utiliser `search_type="similarity"` ou `"mmr"`.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats après avoir construit le RAG :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Hallucination rate** (5 questions privées sans RAG, AT01) | ___% | ≥ 80% |
| **Hallucination rate** (5 questions privées avec RAG) | ___% | 0% |
| **Recall@5** — Marie Dubois (`cv_001` dans le top 5 ?) | Oui/Non | Oui |
| **Recall@5** — Karim Benali (`cv_007` dans le top 5 ?) | Oui/Non | Oui |
| **Recall@5** — Sophie Martin (`cv_010` dans le top 5 ?) | Oui/Non | Oui |
| **Recall@5** — Léa Chen (`cv_015` dans le top 5 ?) | Oui/Non | Oui |
| **Recall@5** — Thomas Petit (`cv_020` dans le top 5 ?) | Oui/Non | Oui |
| **Recall@5 global** | ___/5 → ___% | >= 80% (4/5) |
| **Q&A sourcé** (réponse + source `[cv_xxx]`) | Oui/Non | Oui |
| **Latence moyenne** retrieve + generate (s) | ___s | < 10s |

✋ **Checkpoint final** — `python ateliers/atelier-03-rag/checkpoints/check_final.py`

**Rappel des 5 questions privées et réponses attendues** :

| Question | CV source | Réponse attendue |
|---|---|---|
| Quelle est l'expérience de Marie Dubois en React ? | `cv_001` | 4 ans, niveau avancé |
| Combien d'années d'expérience en Python a Karim Benali ? | `cv_007` | 6 ans, niveau expert |
| Quel est le dernier poste de Sophie Martin ? | `cv_010` | Senior Product Owner chez ProductCorp, 3 ans |
| Quelles compétences DevOps a Léa Chen ? | `cv_015` | Kubernetes, Docker, Terraform, AWS, GitLab CI, Ansible, Prometheus, Linux |
| Quel est le niveau d'anglais de Thomas Petit ? | `cv_020` | Technique (B2) |

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 3 concepts fondamentaux.

**Sprint 1 — Document Loaders** : ouvre `hirekit/rag/ingestion.py`, lis comment
`load_cv_pdf` utilise `PyMuPDFLoader` et enrichit les métadonnées. Écris 2 lignes
qui chargent un CV et affichent `metadata["filename"]`.

**Sprint 2 — Chunking** : ouvre `hirekit/rag/chunking.py`, lis la différence entre
`chunk_fixed_size` et `chunk_recursive`. Chunk un CV de test avec les deux et
compare visuellement les chunks produits.

**Sprint 3 — Vector Store + Retriever** : ouvre `hirekit/rag/vectorstore_faiss.py`
et `hirekit/rag/retriever.py`. Construis un mini-index FAISS avec 3 documents de
test et fais une recherche `similarity_search`. Puis convertis-le en retriever
avec `as_retriever()` et invoque-le.

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — MMR tuning (`lambda_mult`)

Compare `lambda_mult` à 0.0, 0.5 et 1.0 sur les 5 questions privées. Pour chaque
valeur, mesure :
- Le nombre de CVs uniques dans le top 5 (diversité)
- Le Recall@5 (est-ce que le bon CV est toujours retrouvé ?)

```python
from hirekit.rag.retriever import get_cv_retriever

for lam in [0.0, 0.5, 1.0]:
    retriever = get_cv_retriever(search_type="mmr", k=5, lambda_mult=lam)
    docs = retriever.invoke("Quelle est l'expérience de Marie Dubois en React ?")
    sources = set(d.metadata.get("filename") for d in docs)
    print(f"lambda_mult={lam}: {len(sources)} CVs uniques, cv_001 présent: {'cv_001' in sources}")
```

**Question** : quelle valeur de `lambda_mult` donne le meilleur équilibre
pertinence/diversité pour les CVs de ce projet ?

### Défi Bonus 2 — EnsembleRetriever (CVs + Offres)

Combine le retriever FAISS (CVs) et ChromaDB (offres) avec un `EnsembleRetriever`
pour répondre à des questions croisées comme *"Quels candidats matchent l'offre
DevOps Kubernetes ?"*.

```python
from hirekit.rag.retriever import get_ensemble_retriever

ensemble = get_ensemble_retriever(faiss_k=8, chroma_k=4, weights=[0.7, 0.3])
docs = ensemble.invoke("Kubernetes Docker Terraform")
for d in docs:
    print(f"  [{d.metadata.get('type')}] {d.metadata.get('filename', d.metadata.get('id', '?'))}")
```

**Observation** : l'EnsembleRetriever retourne à la fois des CVs (DevOps) et des
offres (requérant DevOps). Les `weights` contrôlent l'importance de chaque source.

### Défi Bonus 3 — ChromaDB filter par métadonnées

Utilise le filtre de ChromaDB pour chercher des offres par catégorie uniquement :

```python
from hirekit.rag.vectorstore_chroma import search_offers, load_chroma_index

store = load_chroma_index()
results = search_offers(
    "React frontend",
    vectorstore=store,
    k=5,
    filter={"categorie": "frontend"},
)
for r in results:
    print(f"  [{r.metadata.get('categorie')}] {r.metadata.get('titre')}")
```

**Question** : pourquoi ChromaDB est-il plus adapté que FAISS pour ce cas d'usage
de filtrage par métadonnées ?

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Qu'est-ce que le RAG et en quoi résout-il le problème d'hallucination d'AT01 ?
2. Quelle est la différence entre un Document Loader et un Text Splitter ?
3. Pourquoi `RecursiveCharacterTextSplitter` est-il recommandé vs `CharacterTextSplitter` ?
4. Que fait un modèle d'embeddings ? Quelle dimension utilise `get_default_embeddings()` ?
5. Quelle est la différence entre FAISS et ChromaDB, et pourquoi cette distinction dans le projet ?
6. Qu'est-ce qu'un Retriever et comment l'obtient-on depuis un Vector Store ?
7. Qu'est-ce que le MMR (Maximal Marginal Relevance) et que contrôle `lambda_mult` ?
8. Comment mesure-t-on le Recall@5 ? Pourquoi cette métrique pour le RAG ?
9. Comment le system prompt de la chaîne RAG empêche-t-il les hallucinations ?
10. Pourquoi les métadonnées (`filename`, `type`) sont-elles cruciales pour le Q&A sourcé ?

→ Score >= 8/10 : prêt pour AT04 (Agents).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT04 (Agents)** : le RAG a résolu l'hallucination — le LLM répond
maintenant depuis les vrais CVs indexés. Mais il ne peut pas encore *agir* : il
ne peut pas décider seul de matcher un CV contre une offre, enchaîner une recherche
CV puis une recherche offre, ou filtrer par localisation sans qu'on le lui demande
explicitement. Au prochain atelier, on construira des **Agents ReAct** qui
utilisent le retriever FAISS et ChromaDB comme *tools* et décident eux-mêmes
quand chercher un CV, quand chercher une offre, et quand combiner les deux via
l'EnsembleRetriever.

**Lien direct avec AT01** : les 5 questions privées (Marie Dubois → React, Karim
Benali → Python, Sophie Martin → dernier poste, Léa Chen → DevOps, Thomas Petit →
anglais) qui hallucinaient à ≥ 80% sans RAG doivent maintenant trouver leurs vraies
réponses dans les CVs indexés — avec 0% d'hallucination et une source citée pour
chaque réponse. C'est la boucle : AT01 prouve le problème, AT03 le résout.