# Atelier 04 — Agents ReAct + Tools (demi-journée, ~3h30)

> **Comment ce guide fonctionne** : tu reçois une mission, des contraintes, des indices ;
> tu construis. Si tu cherches le tuto, ouvre `hirekit/agent/` et lis les modules — mais
> alors tu n'apprends pas.

---

## 🚦 Pré-vol (avant de commencer) — 20 min

- [ ] `pip install -e ".[dev]"` a été lancé (package hirekit installé)
- [ ] `.env` contient une clé API valide (`ANTHROPIC_API_KEY=sk-ant-...` ou `OPENAI_API_KEY=sk-...`)
- [ ] `python -c "import hirekit; print('OK')"` affiche OK
- [ ] L'index FAISS existe (`data/faiss_index/`) — sinon : `python ateliers/atelier-03-rag/solution.py`
- [ ] Les CVs sont présents dans `data/cvs/` (sinon : `python scripts/generate_cvs.py`)
- [ ] J'ai lu la section "Périmètre" ci-dessous

---

## 🎯 La mission

Le PM ai-hirekit te demande : **"Construis-moi un agent intelligent qui orchestre
plusieurs outils pour trouver des candidats, vérifier leur réputation en ligne, et
calculer un score composite — le tout en autonomie, sans intervention humaine."**

**Livrable** : une démo CLI (`python ateliers/atelier-04-agents-tools/exercice.py`)
qui :
1. Construit un agent ReAct avec 4 outils (`search_cvs`, `match_candidate`,
   `web_search`, `python_repl`)
2. Pose la requête : *"Trouve les 3 meilleurs profils DevOps, vérifie leur réputation
   en ligne, et calcule un score composite (exp × 0.5 + reputation × 0.3 + dispo × 0.2)"*
3. L'agent choisit intelligemment `search_cvs` → `web_search` → `python_repl` (cycle
   Thought/Action/Observation)
4. Affiche la trace ReAct complète (`intermediate_steps`)

**Critères de succès auto-vérifiables** :
- `pytest tests/test_agent/test_tools.py` passe (4 outils décorés avec `@tool`)
- `pytest tests/test_agent/test_react_agent.py` passe (AgentExecutor assemblé)
- L'agent sélectionne les bons outils dans le bon ordre pour la requête complexe
- La trace ReAct contient ≥ 2 `intermediate_steps` (l'agent a vraiment réfléchi)

**Budget temps** : 1h40 Core (+30 min Sprint OU 60-70 min Bonus)

---

## 🚧 Périmètre de cet atelier

- ✅ **Dans le scope** : Agent ReAct (Thought/Action/Observation), `create_react_agent`,
  `AgentExecutor`, décorateur `@tool`, `PythonREPLTool`, `web_search` (simulé),
  `return_intermediate_steps`, `handle_parsing_errors`, `max_iterations`,
  agents autonomes, mémoire `ConversationBufferWindowMemory`
- ❌ **Hors scope** (ateliers suivants) : Streamlit, Telegram, Docker, LangSmith,
  benchmarking, évaluation systematic, code review, RAG avancé
- 🛡️ **Garde-fou activé** : `.claude/CLAUDE.md` local
  (si tu utilises Claude/Cursor : demander "ajoute Streamlit" ou "utilise Docker"
  déclenchera un refus automatique — c'est intentionnel)

---

## 🛠️ vs 🎮 — Choisis ta piste

| Critère | 🛠️ Piste Build | 🎮 Piste Vibe |
|---|---|---|
| **Outil** | Code à la main ; Claude Code en mode `plan` ou fermé | Délégation OK à Claude/Cursor |
| **Liberté** | Tu décides tout | Tu valides ce que l'IA produit |
| **Obligation Build** | Lire `hirekit/agent/tools.py` et `react_agent.py` avant de coder | — |
| **Obligation Vibe** | (a) Expliquer ReAct (Thought/Action/Observation) en 3 phrases | (b) Changer `max_iterations` de 8 à 3, prédire l'effet sur la trace |
| **Bug Hunt** | Tu trouves le bug toi-même | Tu prédis l'effet du bug avant de regarder le test |

---

## 🧠 Carnet de bord (concepts à mobiliser)

> Lis ce lexique avant de commencer à coder. Il sera testé dans les checkpoints.

### Agent

Un **agent** est un LLM augmenté de la capacité de décider et d'appeler des outils.
Contrairement à une chaîne LCEL (pipeline fixe, exécution déterministe), l'agent
**choisit** dynamiquement la prochaine action en fonction du résultat précédent.

**Analogie** : une chaîne LCEL, c'est un bulletin de commande (étapes fixes). Un agent,
c'est un détective qui examine chaque indice et décide de la prochaine enquête.

### ReAct (Reasoning + Acting)

**ReAct** est un pattern où le LLM alterne raisonnement et actions dans une boucle :

```
Thought: je dois d'abord trouver des candidats DevOps
Action: search_cvs
Action Input: "profil DevOps"
Observation: Found 4 candidates: Marie Dubois, Karim Benali...
Thought: maintenant je vérifie leur réputation en ligne
Action: web_search
Action Input: "Marie Dubois développeur React"
Observation: GitHub: profil trouvé, 3 repos publics...
Thought: I now know the final answer
Final Answer: ...
```

Le LLM écrit littéralement `Thought:`, `Action:`, `Action Input:` dans sa sortie.
Le framework parse ces lignes, appelle l'outil, injecte l'`Observation`, et relance
le LLM jusqu'à `Final Answer`.

**Analogie** : un cuisinier qui goûte à chaque étape et décide d'ajouter du sel ou
non avant de continuer — pas une recette exécutée en aveugle.

### AgentExecutor

L'**AgentExecutor** est la boucle qui orchestre l'agent : elle appelle l'agent,
parse sa sortie, exécute l'outil demandé, réinjecte l'observation, et recommence.

Paramètres clés :
- `max_iterations` — nombre max de cycles Thought→Action→Observation (défaut : 8)
- `handle_parsing_errors` — si le LLM produit un format invalide, on relance au lieu
  de crasher
- `return_intermediate_steps` — conserve la trace complète (audit trail)
- `verbose` — affiche chaque étape dans la console

### Décorateur @tool

Le décorateur `@tool` transforme une fonction Python en `BaseTool` LangChain.
LangChain inspecte la signature et la docstring pour générer le nom, la description
et le schéma d'entrée que le LLM voit.

```python
from langchain_core.tools import tool

@tool("search_cvs")
def search_cvs_tool(query: str) -> str:
    """Recherche de candidats dans la base de CVs (RAG).
    Args:
        query: requête en langage naturel.
    Returns:
        Liste des candidats trouvés.
    """
    ...
```

**Important** : la **docstring** est ce que le LLM lit pour décider d'utiliser
l'outil. Une docstring floue = mauvaise sélection d'outils.

### Tool

Un **Tool** est l'unité d'action de l'agent. Il expose un `name`, une
`description`, et une méthode `invoke()`. Le LLM ne voit que le name + description ;
il ne connaît pas le code interne.

### PythonREPLTool

Outil qui permet à l'agent d'exécuter du code Python pour faire des calculs,
des statistiques ou manipuler des données. Dans ai-hirekit, on l'utilise pour
calculer le score composite : `exp × 0.5 + reputation × 0.3 + dispo × 0.2`.

**Analogie** : l'agent a une calculatrice scientifique sous la main. Au lieu
d'essayer de calculer de tête, il écrit le calcul et obtient le résultat exact.

### web_search

Outil de recherche web (simulé en local dans cet atelier pour éviter les appels
API externes). En production, on remplace par DuckDuckGoSearchRun ou SerpAPI.
Ici, les réponses sont mockées dans `_WEB_SEARCH_MOCK` pour rester reproductible.

### Thought / Action / Observation

Les trois phases du cycle ReAct :
- **Thought** — le LLM raisonne sur l'état courant et décide de la prochaine action
- **Action** — le nom de l'outil à appeler + son input
- **Observation** — le résultat retourné par l'outil, injecté dans le contexte

Le cycle se répète jusqu'à ce que le LLM décide `Final Answer`.

### intermediate_steps

Liste des tuples `(AgentAction, observation)` accumulés pendant l'exécution.
Chaque tuple contient : le tool appelé, l'input passé, et le résultat observé.
Avec `return_intermediate_steps=True`, on peut inspecter a posteriori le
raisonnement complet de l'agent — c'est l'**audit trail**.

### handle_parsing_errors

Quand le LLM produit une sortie qui ne respecte pas le format ReAct (par exemple
il oublie `Action Input:`), le parser lève une erreur. Avec
`handle_parsing_errors=True`, l'AgentExecutor renvoie le message d'erreur au LLM
comme observation, lui donnant une chance de se corriger au lieu de crasher.

### max_iterations

Nombre maximum de cycles Thought→Action→Observation avant que l'AgentExecutor
force l'arrêt. Protection essentielle : sans elle, un agent peut boucler
indéfiniment. `max_iterations=8` est un bon défaut ; à 3 l'agent n'a pas le temps
de faire une tâche complexe multi-étapes.

### Agent autonome

Un agent qui enchaîne plusieurs requêtes en séquence, en accumulant le contexte
via la mémoire. Dans ai-hirekit, `run_autonomous_agent(scenario)` prend une liste
de requêtes et les exécute l'une après l'autre sans intervention humaine.

---

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — Définir les 4 outils avec @tool (25 min)

**Objectif** : créer les 4 outils que l'agent pourra appeler.

**Indices (Build)** :
- Fichier à compléter : `ateliers/atelier-04-agents-tools/exercice.py` (TODO 1)
- Importer `get_all_tools` depuis `hirekit.agent.tools`
- Les 4 outils sont déjà définis dans `hirekit/agent/tools.py` :
  ```python
  from hirekit.agent.tools import get_all_tools

  tools = get_all_tools()
  for t in tools:
      print(f"  - {t.name}: {t.description[:60]}...")
  ```
- Ouvre `hirekit/agent/tools.py` et lis chaque docstring — c'est ce que le LLM voit
- Vérifie que les 4 outils sont des `BaseTool` :
  ```python
  from langchain_core.tools import BaseTool
  assert all(isinstance(t, BaseTool) for t in tools)
  ```

**Les 4 outils** :
1. `search_cvs` — recherche RAG dans les CVs (FAISS, AT03)
2. `match_candidate` — matching CV↔offre (chaîne LCEL, AT02)
3. `web_search` — recherche web simulée (réputation en ligne)
4. `python_repl` — exécution de code Python (calcul de score composite)

**Observation attendue** : les 4 outils s'affichent avec leur nom et description.
La description de chaque outil indique clairement quand l'utiliser — c'est crucial
pour que le LLM fasse le bon choix.

**C'est le moment de dire** : "Chaque outil est une boîte noire pour le LLM. Il ne
voit que le name et la description. Si la docstring est ambiguë, l'agent appellera
le mauvais outil. La qualité de la docstring = qualité de la sélection d'outils."

✋ **Checkpoint 1** — `pytest tests/test_agent/test_tools.py::TestGetAllTools -v`

---

### Mini-lab — Observer le cycle Thought→Action→Observation (15 min)

Avant d'assembler l'agent complet, observons le cycle ReAct sur un seul outil.

Lance ce snippet dans un notebook ou un script :
```python
from hirekit.agent.tools import web_search_tool

result = web_search_tool.invoke({"query": "Marie Dubois développeur React"})
print(result)
```

Puis essaie `python_repl` :
```python
from hirekit.agent.tools import python_repl_tool

result = python_repl_tool.invoke({"code": "score = 0.8 * 0.5 + 0.7 * 0.3 + 0.6 * 0.2; print(f'Score composite: {score}')"})
print(result)
```

| Outil | Input | Sortie observée | Latence |
|---|---|---|---|
| `web_search` | "Marie Dubois développeur React" | ___ | ___s |
| `python_repl` | `score = 0.8*0.5 + 0.7*0.3; print(score)` | ___ | ___s |

**Question** : lequel des deux outils est déterministe ? Lequel peut varier ?

---

### Étape 2 — Assembler l'AgentExecutor (30 min)

**Objectif** : construire l'AgentExecutor ReAct et l'exécuter sur la requête complexe.

**Indices (Build)** :
- Fichier à compléter : `exercice.py` (TODOs 2 et 3)
- Importer `get_agent_executor` depuis `hirekit.agent.react_agent`
- Assembler l'agent :
  ```python
  from hirekit.agent.react_agent import get_agent_executor

  executor = get_agent_executor(tools=tools, max_iterations=8, verbose=True)
  ```
- Lancer la requête complexe :
  ```python
  query = (
      "Trouve les 3 meilleurs profils DevOps, vérifie leur réputation "
      "en ligne, et calcule un score composite (exp * 0.5 + reputation * 0.3 + dispo * 0.2)"
  )
  result = executor.invoke({"input": query})
  print(result["output"])
  ```
- Afficher la trace (TODO 4) :
  ```python
  for i, step in enumerate(result.get("intermediate_steps", []), 1):
      action = step[0]
      observation = step[1]
      print(f"Étape {i}: {action.tool} → {str(observation)[:100]}...")
  ```

**Observation attendue** : avec `verbose=True`, la console affiche chaque cycle
Thought → Action → Action Input → Observation. L'agent commence par `search_cvs`
pour trouver des profils DevOps, puis `web_search` pour vérifier la réputation,
puis `python_repl` pour calculer le score. La `Final Answer` synthétise tout.

**C'est le moment de dire** : "L'agent n'a pas été programmé pour faire search puis
web puis python. Il a décidé tout seul, en lisant les descriptions des outils.
C'est ça la puissance du ReAct : le LLM raisonne sur le prochain outil à appeler."

✋ **Checkpoint 2** — `pytest tests/test_agent/test_react_agent.py::TestGetAgentExecutor -v`

---

### 🐛 Bug Hunt (20 min)

3 bugs à débusquer. Applique chaque patch, observe le comportement, répare, valide.

**Bug v1 — max_iterations=1 (agent bloqué avant la réponse finale)**
```bash
# Simule le bug : édite get_agent_executor() avec max_iterations=1
# puis lance :
pytest tests/test_agent/test_react_agent.py::TestGetAgentExecutor::test_get_agent_executor_max_iterations -v
```
Observe : l'agent n'a qu'un seul cycle. Il appelle un outil puis s'arrête sans
`Final Answer`. Répare : remettre `max_iterations=8`.

**Bug v2 — handle_parsing_errors=False (crash si le LLM se trompe de format)**
```bash
# Simule le bug : édite get_agent_executor() avec handle_parsing_errors=False
# puis pose une question complexe à l'agent
```
Observe : si le LLM produit un format invalide (oubli de `Action Input:`),
l'AgentExecutor lève une exception au lieu de relancer. Répare :
`handle_parsing_errors=True`.

**Bug v3 — Docstring vide sur search_cvs (mauvaise sélection d'outils)**
```bash
# Simule le bug : remplace la docstring de search_cvs_tool par "TODO"
# puis relance la requête complexe
```
Observe : l'agent ne sait pas quand utiliser `search_cvs` — il l'ignore ou
l'utilise au mauvais moment. Répare : restaurer une docstring descriptive.

---

### 📊 Mesure-toi (15 min)

Remplis ce tableau avec tes résultats :

| Métrique | Valeur observée | Cible |
|---|---|---|
| **Nombre d'outils** dans `get_all_tools()` | ___ | 4 |
| **`intermediate_steps`** (requête complexe) | ___ étapes | ≥ 2 |
| **Premier outil choisi** par l'agent | ___ | `search_cvs` |
| **Deuxième outil choisi** | ___ | `web_search` |
| **Troisième outil choisi** | ___ | `python_repl` |
| **`Final Answer` présente** ? | Oui/Non | Oui |
| **Latence totale** (s) | ___s | < 30s |
| **`handle_parsing_errors`** activé ? | Oui/Non | Oui |

✋ **Checkpoint final** — `pytest tests/test_agent/ -v`

---

## ⚡ SPRINT (30 min)

Si score checkpoint < 60% : consolide les 2 concepts fondamentaux.

**Sprint 1 — Cycle ReAct** : ouvre `hirekit/agent/react_agent.py`, lis
`REACT_SYSTEM_PROMPT`. Reproduis à la main (papier) le cycle Thought → Action →
Observation pour la requête *"Trouve les 3 meilleurs profils DevOps"*. Quels
outils l'agent devrait-il appeler, et dans quel ordre ?

**Sprint 2 — Assemblage AgentExecutor** : ouvre `hirekit/agent/react_agent.py`,
lis `get_agent_executor()`. Identifie les 4 paramètres critiques :
`max_iterations`, `handle_parsing_errors`, `return_intermediate_steps`,
`verbose`. Que se passe-t-il si on retire chacun ?

---

## 🏆 BONUS (60-70 min)

### Défi Bonus 1 — Agent autonome multi-scénarios

Utilise `run_autonomous_agent()` pour exécuter un scénario de 3 requêtes en
séquence, sans intervention humaine :
```python
from hirekit.agent.react_agent import run_autonomous_agent

scenario = [
    "Qui a de l'expérience en Kubernetes ?",
    "Vérifie la réputation en ligne de Léa Chen",
    "Calcule un score: 4 * 0.5 + 0.8 * 0.3 + 0.6 * 0.2",
]
results = run_autonomous_agent(scenario)
for r in results:
    print(f"Q: {r['query']}")
    print(f"A: {r['output'][:200]}")
    print(f"Steps: {r['intermediate_steps']}")
```

Observe comment l'agent accumulate le contexte entre les requêtes grâce à la
mémoire `ConversationBufferWindowMemory`. La 3e requête bénéficie-t-elle des
résultats des 2 premières ?

### Défi Bonus 2 — Outil check_availability + planning

Ajoute le 5e outil `check_availability` à l'agent :
```python
from hirekit.agent.tools import get_all_tools_with_availability

tools = get_all_tools_with_availability()  # 5 outils
executor = get_agent_executor(tools=tools, max_iterations=10)
result = executor.invoke({
    "input": "Trouve les candidats DevOps disponibles le 2024-03-15 pour un entretien"
})
```

Vérifie d'abord que le calendrier existe :
```bash
python scripts/generate_availability.py
```

Observe : l'agent peut maintenant non seulement trouver et scorer, mais aussi
proposer des créneaux d'entretien. C'est un agent de bout en bout.

### Défi Bonus 3 — ConversationBufferWindowMemory

Ouvre `hirekit/agent/react_agent.py`, lis `get_agent_executor_with_memory()`.
Compare avec `get_agent_executor()` : quelles différences dans le prompt ?
La variable `history` permet à l'agent de se souvenir des critères du recruteur
entre les échanges.

Teste :
```python
from hirekit.agent.react_agent import get_agent_executor_with_memory

executor = get_agent_executor_with_memory(memory_k=5)
executor.invoke({"input": "Je cherche un profil DevOps senior"})
executor.invoke({"input": "Le budget est 70k€"})
executor.invoke({"input": "Quels candidats correspondent à mes critères ?"})
```

La 3e invocation utilise-t-elle le contexte des 2 premières ?

---

## 🎓 Wrap-up (10 min)

**Quiz oral 10 questions (5 min chrono)** :

1. Qu'est-ce qu'un agent LLM et en quoi diffère-t-il d'une chaîne LCEL ?
2. Que signifie ReAct (Reasoning + Acting) ?
3. Quelles sont les 3 phases du cycle ReAct ?
4. Que fait le décorateur `@tool` ?
5. Pourquoi la docstring d'un outil est-elle cruciale pour l'agent ?
6. Que fait `max_iterations` et que se passe-t-il s'il est trop bas ?
7. À quoi sert `handle_parsing_errors=True` ?
8. Que contient `intermediate_steps` et pourquoi est-ce un audit trail ?
9. Cite les 4 outils de l'agent ai-hirekit et leur rôle.
10. Qu'est-ce qu'un agent autonome et comment diffère-t-il d'un agent mono-requête ?

→ Score ≥ 8/10 : prêt pour AT05 (Chatbot Streamlit).
→ Score < 6/10 : refais le Sprint.

**Ce que je retiens en 3 lignes** :
```
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________
```

---

## 🔗 Pour aller plus loin

**Pont avec AT05** : l'agent ReAct fonctionne en CLI, mais un recruteur veut une
interface conversationnelle. Au prochain atelier, on construira un chatbot
Streamlit qui expose cet agent avec un historique de conversation persistant, des
suggestions de questions, et une UI pour visualiser la trace ReAct en temps réel.
L'agent devient un véritable copilote recruteur accessible dans le navigateur.