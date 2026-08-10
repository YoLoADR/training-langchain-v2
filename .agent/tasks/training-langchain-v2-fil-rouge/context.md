# Context — Training LangChain v2 (Fil Rouge ai-hirekit)

> Suite de pre-training-rag (HomeButler AI). v2 : fil rouge basé sur ai-hirekit, en TDD, bot Telegram simulé.
> Développement délégué à des équipes d'agents IA (pattern ai-teams-benchmark).

## Goal

Reverse-engineer le projet ai-hirekit en un fil rouge progressif pour la formation
"Applications d'IA générative avec LangChain" (Ambient IT, 3 jours, 21h).

Le projet final (ai-hirekit) existe déjà. Le but est de le **découper à l'envers** en 6 ateliers
progressifs (un par demi-journée du programme), en suivant le pattern pédagogique de
pre-training-rag (HomeButler AI).

## Sources d'inspiration

| Source | Rôle |
|---|---|
| `pre-training-rag/` | Pattern pédagogique : GUIDE-ELEVE.md, GUIDE-FORMATEUR.md, exercice.py, solution.py, bugs/, checkpoints/, .claude/ scope guards. 6 ateliers + 3 avancés. Package `homebutler/` construit progressivement. |
| `ai-hirekit/` | Projet final à reverse-engineer. Kit de publication d'offres d'emploi (Hermes + Playwright). Le thème métier = recrutement/hiring. |
| `training-langchain/` | Embryon de formation LangChain (pycode/ + tchat/ + slides .md). Base de départ. |
| `ai-teams-benchmark/` | Pattern de délégation à des équipes d'agents IA (3 équipes, Telegram, GitHub Issues, scoring). |
| https://www.ambient-it.net/formation/langchain/ | Programme officiel de formation (3 jours, 6 demi-journées). |

## Programme officiel Ambient IT (3 jours)

### Jour 1 — Matin : Architecture et Fondamentaux des LLM
- Introduction à LangChain : philosophie, installation et configuration
- Modèles et Prédictions : **LLMs vs Chat Models**
- Prompt Engineering Dynamique : **Prompt Templates** et **sélecteurs d'exemples**
- Gestion des sorties avec les **Output Parsers**
- Atelier pratique : Création d'un premier flux « Prompt + Modèle »

### Jour 1 — Après-midi : LCEL et Gestion de la Mémoire
- **LangChain Expression Language (LCEL)** : composer des chaînes de manière déclarative
- **Persistence et État** : mise en œuvre de la Conversation Memory
- Chaînes avancées et gestion des **variables d'état**
- Atelier pratique : Développement d'un assistant capable de conserver le contexte

### Jour 2 — Matin : RAG et Gestion des Données (Retrieval)
- **Document Loaders** et **Text Splitters**
- **Vector Stores** et **Embeddings** : indexer ses données
- Le **Retriever** : optimiser la récupération pour limiter les hallucinations
- Atelier pratique : Création d'une chaîne de Question-Answering sur documents PDF

### Jour 2 — Après-midi : Agents et Autonomie
- Concept d'**Agent** : raisonnement (ReAct) et cycle de l'Agent Executor
- **Outils (Tools)** : permettre à l'IA d'appeler des APIs ou **d'exécuter du code**
- **Agents autonomes** et simulations
- Atelier pratique : Construction d'un agent capable d'effectuer des **recherches web**

### Jour 3 — Matin : Cas d'usage : Chatbots et Analyse de Code
- **UX Chatbot** : recréer une expérience de type ChatGPT
- **Compréhension du code** : indexation et assistant d'aide au développement
- Introduction aux assistants **multimodaux (audio/vocal)**
- Atelier pratique : Développement d'un « Code-Reviewer » intelligent

### Jour 3 — Après-midi : Évaluation, Benchmarking et Déploiement
- Évaluation des chaînes et utilisation de **LangSmith**
- **Benchmarking** : analyse comparative des **agents** et **VectorDB**
- **Déploiement** et **monitoring des coûts** en production
- Atelier pratique : Audit de performance et test de robustesse sur dataset

## Découpage en 6 ateliers

| Atelier | Demi-journée | Concepts LangChain | Fonctionnalité ai-hirekit |
|---|---|---|---|
| AT01 | J1 matin | LLMs vs Chat Models, Prompt Templates, ExampleSelector, Output Parsers | LLM nu hallucine sur CVs privés ; extraction structurée CV→JSON |
| AT02 | J1 a.-m. | LCEL (pipe, RunnablePassthrough, RunnableParallel), Conversation Memory, Persistence, variables d'état | Chaîne matching CV↔offre + mémoire recruteur persistée |
| AT03 | J2 matin | Document Loaders, Text Splitters, Vector Stores, Embeddings, Retriever (anti-hallucination) | RAG sur 30 CVs PDF + 15 offres JSON, Q&A sourcée |
| AT04 | J2 a.-m. | Agent ReAct, Tools (APIs + code execution), recherches web, agents autonomes | Agent 4 outils : search_cvs, match, web_search, python_repl |
| AT05 | J3 matin | UX Chatbot (Streamlit), compréhension du code (indexation), multimodal audio/vocal | Chatbot Streamlit + bot Telegram simulé + Code-Reviewer |
| AT06 | J3 a.-m. | LangSmith, benchmarking (agents + VectorDB), déploiement, monitoring coûts | Éval + benchmark FAISS vs Chroma + Docker Compose + cost monitoring |

## Architecture cible

```
training-langchain-v2/
├── AI-HireKit-Projet-Fil-Rouge.md   # Spec produit (doc Product Owner)
├── PROGRAMME-LANGCHAIN.md           # Mapping programme → ateliers
├── pyproject.toml                   # Config package (hirekit + deps)
├── .env.example                     # Template variables d'env
├── .gitignore
├── hirekit/                         # Package principal (construit progressivement)
│   ├── __init__.py
│   ├── config.py
│   ├── llm/                          # AT01
│   │   ├── provider.py              # get_llm() — LLMs vs Chat Models
│   │   ├── prompts.py               # PromptTemplates + ExampleSelector
│   │   └── parsers.py               # OutputParsers (Pydantic)
│   ├── rag/                          # AT03
│   │   ├── ingestion.py             # Document Loaders
│   │   ├── chunking.py              # Text Splitters
│   │   ├── vectorstore_faiss.py     # FAISS
│   │   ├── vectorstore_chroma.py    # ChromaDB
│   │   └── retriever.py            # Retriever + MMR
│   ├── agent/                        # AT04
│   │   ├── react_agent.py           # AgentExecutor ReAct
│   │   └── tools.py                 # @tool (search, match, web, python_repl)
│   ├── services/                     # AT02 + AT04
│   │   ├── matching.py              # Chaîne LCEL matching
│   │   └── availability.py          # Calendrier fictif
│   ├── eval/                         # AT06
│   │   ├── metrics.py               # Recall@k, MRR, cost monitoring
│   │   └── tracing.py               # LangSmith callbacks
│   └── ui/                           # AT05
│       ├── app.py                   # Streamlit multi-pages
│       ├── telegram_bot.py          # Bot Telegram simulé
│       └── code_reviewer.py         # Indexation code + Q&A
├── ateliers/
│   ├── atelier-01-llm-prompts-parsers/
│   ├── atelier-02-lcel-memoire/
│   ├── atelier-03-rag/
│   ├── atelier-04-agents-tools/
│   ├── atelier-05-chatbot-code-review/
│   └── atelier-06-eval-benchmark-deploy/
├── api/                             # FastAPI (AT05 + AT06)
│   └── main.py
├── scripts/
│   ├── generate_cvs.py              # 30 CVs PDF fictifs
│   ├── generate_offers.py          # 15 offres JSON
│   ├── generate_qa_dataset.py      # 150 paires Q/A
│   ├── generate_availability.py    # Calendrier fictif
│   └── check_atelier_ready.sh      # Pré-vol par atelier
├── data/
│   ├── cvs/                         # 30 CVs PDF
│   ├── offers/                      # 15 offres JSON
│   ├── skills.csv                   # Taxonomie 100 compétences
│   ├── qa_dataset.jsonl             # 150 paires Q/A
│   └── availability.json            # Calendrier 30 jours
├── tests/                           # TDD
│   ├── conftest.py
│   ├── test_llm/
│   ├── test_rag/
│   ├── test_agent/
│   └── test_services/
├── notebooks/
│   ├── 01_llm_basics.ipynb
│   └── 02_rag_demo.ipynb
└── docker-compose.yml               # AT06
```

## Branches git

```
main                              → projet final complet
atelier/01-llm-prompts-parsers    → hirekit/llm/ + config.py
atelier/02-lcel-memoire           → + hirekit/services/matching.py
atelier/03-rag                    → + hirekit/rag/
atelier/04-agents-tools           → + hirekit/agent/ + services/availability.py
atelier/05-chatbot-code-review    → + hirekit/ui/ + api/
atelier/06-eval-benchmark-deploy  → + hirekit/eval/ + docker-compose.yml = final
```

## Délégation aux équipes d'agents IA

Inspiré de ai-teams-benchmark v3.1 :

| Équipe | Stratégie | Lot | Ateliers |
|---|---|---|---|
| Cuba | Fix + Continue | hirekit/llm/ + hirekit/services/ | AT01 + AT02 |
| Haiti | OpenClaw | hirekit/rag/ + hirekit/agent/ | AT03 + AT04 |
| Guyane | Direct Coding | hirekit/ui/ + hirekit/eval/ + api/ | AT05 + AT06 |

## Fichiers liés

- Plan détaillé : `FIL_ROUGE_PLAN.md` (ce dossier)
- Tâches : `todos.md` (ce dossier)
- Journal : `insights.md` (ce dossier)
- Scoring : `SCORECARD.md` (ce dossier)
- Projet cible : `/Users/yohannravino/Factory/training-langchain-v2/`
- Projet source (pattern) : `/Users/yohannravino/Factory/pre-training-rag/`
- Projet source (thème) : `/Users/yohannravino/Factory/ai-hirekit/`
- Benchmark (délegation) : `/Users/yohannravino/Factory/ai-teams-benchmark/`