# Atelier 01 — LLM + Prompts + Output Parsers (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/llm/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] Les CVs sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Avant d'investir dans le RAG, prouve-moi qu'un LLM seul
ne peut pas matcher des CVs. Et montre-moi qu'on peut au moins extraire les infos
structurées d'un CV avec un Output Parser."**

**Livrable** : une démo CLI (`python ateliers/atelier-01-llm-prompts-parsers/exercice.py`)
qui :
1. Pose 5 questions privées sur des CVs à un LLM nu → constate les hallucinations
2. Compare LLMs (completion API) vs Chat Models (messages API)
3. Extrait les infos d'un CV en JSON structuré via PydanticOutputParser
4. Utilise un ExampleSelector pour du few-shot prompting (Bonus)

**Critères de succès auto-vérifiables** :
- Hallucination rate ≥ 80% sur les 5 questions privées (le LLM invente les réponses)
- Extraction CV→JSON valide (l'objet CVInfo est correctement rempli)
- `pytest tests/test_llm/test_provider.py` passe
- `pytest tests/test_llm/test_parsers.py` passe

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : LLMs vs Chat Models, PromptTemplate, ChatPromptTemplate,
  ExampleSelector (sélecteurs d'exemples), PydanticOutputParser,
  CommaSeparatedListOutputParser, temperature, max_tokens, system prompt, few-shot
- ❌ **Hors scope** (ateliers suivants) : LCEL, Conversation Memory, RAG, FAISS,
  ChromaDB, agents, tools, Streamlit, Telegram, Docker
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local
  (si tu utilises Claude/Cursor : demander "ajoute du RAG" ou "utilise LCEL" déclenchera
  un refus automatique — c'est intentionnel)

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/llm/provider.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer LLM vs Chat Model en 3 phrases | (b) Modifier `temperature` de 0.1 à 0.9, prédire l'effet sur les hallucinations |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### LLMs vs Chat Models

**LLM** (completion API) : tu envoies un texte, tu reçois un texte. Interface simple,
style `llm.invoke("Bonjour")` → `"Bonjour, comment puis-je vous aider ?"`.

**Chat Model** (messages API) : tu envoies une liste de messages avec des rôles
(`system`, `human`, `ai`), tu reçois un message. Interface structurée, style
`chat.invoke([SystemMessage("Tu es un recruteur"), HumanMessage("Analyse ce CV")])`.

**Analogie** : le LLM, c'est un walkie-talkie (un message à la fois). Le Chat Model,
c'est une messagerie instantanée avec profils (qui dit quoi, dans quel rôle).

**Dans le projet** : `get_llm()` retourne un LLM, `get_chat_model()` retourne un Chat
Model. Les deux lisent `LLM_PROVIDER` dans `.env`.

### Prompt Template

Un template de prompt avec des variables (`{variable}`) qui sont remplies à l'exécution.

**Analogie** : un formulaire type lettre de motivation avec des champs à remplir :
`"Je postule pour le poste de {poste} chez {entreprise}."`

**Dans le projet** : `PromptTemplate.from_template("Analyse ce CV : {cv}")` →
`prompt.format(cv="...")`.

### ChatPromptTemplate

Un template pour Chat Model avec des messages structurés (system, human, ai).

**Dans le projet** : `ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT),
("human", "{question}")])`.

### Sélecteurs d'exemples (ExampleSelector)

Choisit dynamiquement les exemples à inclure dans un prompt few-shot, en fonction de
la question. Contrairement au few-shot statique (mêmes exemples pour toutes les
questions), l'ExampleSelector adapte les exemples.

**Analogie** : un prof qui choisit ses exemples d'exercices selon le niveau de l'élève
qui pose la question, plutôt que de toujours donner les mêmes.

**Types** : `SemanticSimilarityExampleSelector` (choisit les exemples sémantiquement
proches), `LengthBasedExampleSelector` (limite la longueur).

### Output Parser

Extrait une structure de données depuis la sortie texte du LLM.

**PydanticOutputParser** : définit un schéma Pydantic, le parser valide la sortie du
LLM et retourne un objet Python typé.

**Analogie** : un formulaire administratif qui doit être rempli selon un format précis.
Le parser vérifie que les champs sont présents et correctement typés.

**Dans le projet** : `PydanticOutputParser(pydantic_object=CVInfo)` → le LLM doit
retourner un JSON conforme au schéma `CVInfo`. Le parser injecte
`{format_instructions}` dans le prompt.

### Temperature

Contrôle le degré d'aléatoire. À `temperature=0`, le modèle choisit toujours le token
le plus probable (déterministe). À `temperature=0.9`, il puise dans des tokens moins
probables (créatif).

**Analogie** : temperature 0 = robot qui répond toujours pareil. temperature 0.9 =
artiste qui improvise. Pour un assistant recruteur qui doit donner des faits fiables,
on veut temperature basse (0.1).

### Hallucination

Réponse plausible mais fausse produite par le LLM faute d'informations réelles. Le
modèle prédit le token le plus probable statistiquement, sans vérification factuelle.

**Dans cet atelier** : on pose "Quelle est l'expérience de Marie Dubois en React ?" sur
un CV que le LLM n'a jamais vu. Il invente une réponse plausible.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — LLMs vs Chat Models et hallucinations (25 min)

**Objectif** : instancier un LLM et un Chat Model, poser 5 questions privées sur des CVs,
constater les hallucinations.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-01-llm-prompts-parsers/exercice.py`
- Importer `get_llm` et `get_chat_model` depuis `hirekit.llm.provider`
- Les 5 questions privées sont dans `exercice.py` :
  ```python
  QUESTIONS_CV = [
      "Quelle est l'expérience de Marie Dubois en React ?",
      "Combien d'années d'expérience en Python a Karim Benali ?",
      "Quel est le dernier poste de Sophie Martin ?",
      "Quelles compétences DevOps a Léa Chen ?",
      "Quel est le niveau d'anglais de Thomas Petit ?",
  ]
  ```
- Poser les questions aux deux modèles (LLM et Chat Model) et comparer les réponses

**Observation attendue** : le modèle répond avec confiance à chaque question. Il propose
des années d'expérience, des noms d'entreprises, des niveaux de compétence — tout est
inventé. Personne dans la salle ne sait quelle est la vraie expérience de Marie Dubois
— et le modèle non plus.

**C'est le moment de dire** : "Ce que vous voyez là, c'est une hallucination. Le modèle
prédit des tokens statistiquement plausibles. Ce n'est pas un bug, c'est le
fonctionnement normal d'un LLM sans accès aux données."

✋ **Checkpoint 1** — Lance `python ateliers/atelier-01-llm-prompts-parsers/checkpoints/check_1.py`

---

### Mini-lab — Temperature et déterminisme (15 min)

Crée un second LLM avec `temperature=0.9` et repose la même question 2 fois.
Observe si la réponse change. Puis passe à `temperature=0` et relance.

| Temperature | Run 1 vs Run 2 | Déterminisme |
|---|---|---|
| 0.1 | identiques ? | Oui/Non |
| 0.9 | identiques ? | Oui/Non |

---

### Étape 2 — Extraction structurée avec Output Parsers (30 min)

**Objectif** : utiliser `PydanticOutputParser` pour extraire un CV en JSON structuré.

**Indices (Build)** :
- Importer `CVInfo` et `get_cv_parser` depuis `hirekit.llm.parsers`
- Le parser génère des `format_instructions` à injecter dans le prompt :
  ```python
  parser = get_cv_parser()
  prompt = PromptTemplate(
      template="Extrais les informations de ce CV:\n{cv}\n\n{format_instructions}",
      input_variables=["cv"],
      partial_variables={"format_instructions": parser.get_format_instructions()},
  )
  chain = prompt | get_chat_model() | parser
  result = chain.invoke({"cv": cv_text})  # → CVInfo
  ```
- Vérifier que `result.nom`, `result.competences`, `result.experiences` sont remplis

**Observation attendue** : le LLM retourne un JSON valide. Le parser le convertit en
objet `CVInfo`. On a maintenant des données structurées — mais elles sont toujours
inventées si le CV n'est pas fourni en contexte.

**C'est le pont vers AT03 (RAG)** : l'Output Parser structure la sortie, mais le LLM
a toujours besoin du contenu du CV pour répondre correctement. Au prochain atelier,
on injectera les vrais CVs dans le contexte.

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — Temperature trop haute**
```bash
git apply ateliers/atelier-01-llm-prompts-parsers/bugs/v1.patch
pytest ateliers/atelier-01-llm-prompts-parsers/bugs/test_v1.py -v
```
Observe : les réponses changent entre deux runs. Répare : remettre temperature=0.1.

**Bug v2 — max_tokens=50 (réponse tronquée)**
```bash
git apply ateliers/atelier-01-llm-prompts-parsers/bugs/v2.patch
pytest ateliers/atelier-01-llm-prompts-parsers/bugs/test_v2.py -v
```
Observe : la réponse s'arrête en plein milieu. Répare : max_tokens=1024.

**Bug v3 — Pas de system prompt (HumanMessage au lieu de SystemMessage)**
```bash
git apply ateliers/atelier-01-llm-prompts-parsers/bugs/v3.patch
pytest ateliers/atelier-01-llm-prompts-parsers/bugs/test_v3.py -v
```
Observe : le modèle répond hors sujet. Répare : remettre SystemMessage.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Hallucination rate** (5 questions privées) | ___% | ≥ 80% |
| **Déterminisme** (T=0, 2 runs identiques ?) | Oui/Non | Oui |
| **Extraction CV→JSON valide** | Oui/Non | Oui |
| **Latence moyenne** (s) | ___s | < 5s |
| **Tokens consommés** (total) | ___ | observable |

✋ **Checkpoint final** — `python ateliers/atelier-01-llm-prompts-parsers/checkpoints/check_final.py`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 2 concepts fondamentaux.

**Sprint 1 — LLMs vs Chat Models** : ouvre `hirekit/llm/provider.py`, lis comment
`get_llm()` et `get_chat_model()` fonctionnent. Écris 2 lignes qui instancient chacun
et pose la même question aux deux.

**Sprint 2 — Output Parser** : ouvre `hirekit/llm/parsers.py`, lis le modèle `CVInfo`.
Instancie le parser, affiche `parser.get_format_instructions()`.

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — ExampleSelector dynamique

Ajoute un `SemanticSimilarityExampleSelector` qui choisit 3 exemples de bonnes
extractions de CV parmi 10, en fonction du CV à analyser. Observe si l'extraction
est meilleure qu'avec des exemples statiques.

### Défi Bonus 2 — Comparaison de modèles

Compare Claude Sonnet vs Claude Haiku (ou GPT-4o vs GPT-4o-mini) sur les 5 questions
privées. Mesure latence, tokens, qualité perçue. Quel est l'arbitrage coût/latence/qualité ?

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Quelle est la différence entre un LLM et un Chat Model ?
2. Qu'est-ce qu'une hallucination LLM ?
3. Que fait `temperature=0` vs `temperature=0.9` ?
4. Qu'est-ce qu'un PromptTemplate ?
5. Qu'est-ce qu'un ExampleSelector et en quoi diffère-t-il du few-shot statique ?
6. Que fait un PydanticOutputParser ?
7. Pourquoi le system prompt est-il important ?
8. Que se passe-t-il si `max_tokens=50` ?
9. Cite 2 limites d'un LLM sans RAG pour le recrutement.
10. Dans ai-hirekit, quand aura-t-on besoin du RAG (AT03) pour résoudre quel problème ?

→ Score ≥ 8/10 : prêt pour AT02 (LCEL + Mémoire).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT02** : l'Output Parser structure la sortie, mais le LLM hallucine toujours
sur les données privées. Au prochain atelier, on construira une chaîne LCEL déclarative
pour le matching CV↔offre, avec une mémoire conversationnelle qui se souvient des
critères du recruteur entre les sessions. Le RAG (AT03) résoudra enfin le problème
d'hallucination en injectant les vrais CVs.