# AI-HireKit — Projet Fil Rouge

> Formation « Applications d'IA générative avec LangChain » — Ambient IT (3 jours, 21h)
>
 Ce document est la spec produit du fil rouge. Il décrit le projet final tel qu'il
> existe après l'atelier 06. Chaque atelier construit une partie de cette spec.

---

## 1. Vision produit

**ai-hirekit** est un assistant IA pour recruteurs qui automatise le screening de CVs,
le matching candidat↔offre, la génération de grilles d'entretien et la planification —
accessible via une interface chat (Streamlit) et un bot Telegram (simulé).

Le projet final existe dans `/Users/yohannravino/Factory/ai-hirekit/`. Ce fil rouge le
**reverse-engineer** en 6 ateliers progressifs qui suivent le programme de formation.

**Ce que le produit fait (état final après AT06)** :

1. Le recruteur pose une question en langage naturel → l'agent ReAct choisit les bons outils
2. L'agent peut chercher dans la base de CVs (RAG), matcher un candidat, faire une recherche web,
   exécuter du code Python pour calculer un score composite
3. L'assistant se souvient des critères du recruteur entre les sessions (mémoire persistée)
4. Le recruteur peut interagir via Streamlit ou un bot Telegram simulé
5. Toutes les chaînes sont tracées dans LangSmith, les coûts sont monitorés
6. Le tout est déployable via Docker Compose

---

## 2. Personas

| Persona | Profil | Besoin | Usage |
|---|---|---|---|
| **Sophie, 35 ans** | RRH dans une PME, 15 recrutements/an, non technique | Screening rapide de CVs, interface simple | Streamlit sur laptop |
| **Karim, 28 ans** | Tech recruiter en ESN, 50 recrutements/an, à l'aise avec les outils | Matching précis, automatisation, scoring | Bot Telegram en mobilité |
| **Léa, 42 ans** | Dirigeante de TPE, recrute elle-même | Assistant simple, mobile, pas de setup | Bot Telegram uniquement |

---

## 3. User Stories

1. **US-01** : Je dépose 10 CVs PDF → je demande « qui a plus de 3 ans d'expérience en React ? »
   → réponse sourcée avec le nom du candidat et l'extrait du CV → **AT03 (RAG)**

2. **US-02** : Je soumets une offre + un CV → l'assistant extrait les compétences (Output Parser),
   matche le candidat avec l'offre, donne un score + justification → **AT01 + AT02**

3. **US-03** : Je shortliste un candidat → l'agent génère une grille d'entretien personnalisée
   basée sur le CV et l'offre → **AT04 (Agent)**

4. **US-04** : Sur 3 sessions séparées, l'assistant se souvient de mes critères de recrutement
   et des candidats déjà vus → **AT02 (Mémoire persistée)**

5. **US-05** : Via Telegram : « trouve les 3 meilleurs profils DevOps, vérifie leur réputation
   en ligne, et calcule un score composite » → l'agent cherche, matche, recherche web,
   exécute du code → **AT04 + AT05**

---

## 4. Architecture technique (état final)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Interfaces                                                          │
│  ├── Streamlit (chat + dashboard matching + bibliothèque CVs)       │
│  └── Bot Telegram (simulé en local / vrai bot en bonus)             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP / REST
┌──────────────────────────────▼──────────────────────────────────────┐
│  API FastAPI                                                         │
│  /health  /chat  /match  /interview  /search                         │
└──────────┬───────────────────────────────────┬───────────────────────┘
           │                                   │
   ┌───────▼────────┐                   ┌──────▼──────────────┐
   │  Agent ReAct    │                   │   LangSmith         │
   │  (LangChain)    │◄─────────────────┤   (tracing + eval)  │
   │  max_iter=8     │                   └─────────────────────┘
   │  memory_k=10    │
   └───┬────┬────┬───┘
       │    │    │
  ┌────▼─┐ ┌▼───┐ ┌▼──────────────────────────┐
  │ RAG  │ │LCEL│ │  Outils (Tools)            │
  │FAISS │ │Chaî│ │  - search_cvs (RAG)        │
  │+Chro │ │ne  │ │  - match_candidate (LCEL)  │
  │ ma   │ │   │ │  - web_search (recherche)  │
  └──────┘ └───┘ │  - python_repl (code)      │
                    └───────────────────────────┘
```

---

## 5. Stack technique

| Couche | Technologie | Atelier d'introduction |
|---|---|---|
| LLM | Claude (Anthropic) / GPT-4o / Ollama | AT01 |
| Framework | LangChain 0.3+ | AT01 |
| Prompts | PromptTemplate, ChatPromptTemplate, ExampleSelector | AT01 |
| Output Parsers | PydanticOutputParser, CommaSeparatedListOutputParser | AT01 |
| Chaînes | LCEL (pipe, RunnablePassthrough, RunnableParallel) | AT02 |
| Mémoire | ConversationBufferWindowMemory, ConversationSummaryMemory | AT02 |
| RAG | FAISS, ChromaDB, FastEmbedEmbeddings | AT03 |
| Document Loaders | PyMuPDFLoader, JSONLoader, CSVLoader | AT03 |
| Text Splitters | RecursiveCharacterTextSplitter | AT03 |
| Agents | create_react_agent, AgentExecutor | AT04 |
| Tools | @tool, PythonREPLTool, web search | AT04 |
| UI | Streamlit | AT05 |
| Bot | python-telegram-bot (simulé) | AT05 |
| Code Analysis | GenericLoader (Python) + RAG | AT05 |
| Évaluation | LangSmith, Recall@k, MRR | AT06 |
| API | FastAPI | AT05/AT06 |
| Déploiement | Docker Compose | AT06 |

---

## 6. Données simulées

| Donnée | Format | Quantité | Script |
|---|---|---|---|
| CVs fictifs | PDF 1-2 pages | 30 | `scripts/generate_cvs.py` |
| Offres d'emploi | JSON | 15 | `scripts/generate_offers.py` |
| Skills taxonomy | CSV | 100 compétences | `scripts/generate_skills.py` |
| QA dataset | JSONL | 150 paires Q/A | `scripts/generate_qa_dataset.py` |
| Calendrier | JSON | 30 jours | `scripts/generate_availability.py` |
| Code repo | .py | 10 fichiers | `scripts/generate_code_repo.py` |

Profils CV simulés : dev React, dev Python, DevOps, designer, marketing, alternant,
junior fullstack, senior backend, data engineer, PO, etc.

---

## 7. Mapping programme → ateliers

Voir `PROGRAMME-LANGCHAIN.md` pour le mapping détaillé concept par concept.

| Atelier | Demi-journée | Programme | Fonctionnalité construite |
|---|---|---|---|
| AT01 | J1 matin | LLMs, Prompts, ExampleSelector, Output Parsers | LLM nu hallucine + extraction CV→JSON |
| AT02 | J1 a.-m. | LCEL, Mémoire, Persistence, variables d'état | Chaîne matching + mémoire recruteur |
| AT03 | J2 matin | Loaders, Splitters, Vector Stores, Retriever | RAG sur CVs + offres, anti-hallucination |
| AT04 | J2 a.-m. | Agent ReAct, Tools (APIs + code + web) | Agent 4 outils + recherches web |
| AT05 | J3 matin | Chatbot UX, Code Analysis, Multimodal | Streamlit + Telegram + Code-Reviewer |
| AT06 | J3 a.-m. | LangSmith, Benchmarking, Déploiement, Coûts | Éval + Docker + monitoring |

---

## 8. Progression du package hirekit/

Le package `hirekit/` est construit progressivement, un module par atelier :

| Atelier | Modules ajoutés | État après l'atelier |
|---|---|---|
| AT01 | `hirekit/llm/` (provider, prompts, parsers) | LLM fonctionne, extraction CV→JSON |
| AT02 | `hirekit/services/matching.py` | Chaîne LCEL + mémoire |
| AT03 | `hirekit/rag/` (ingestion, chunking, vectorstores, retriever) | RAG fonctionnel |
| AT04 | `hirekit/agent/` (react_agent, tools) + `services/availability.py` | Agent multi-outils |
| AT05 | `hirekit/ui/` (app, telegram_bot, code_reviewer) + `api/` | Interfaces |
| AT06 | `hirekit/eval/` (metrics, tracing) + `docker-compose.yml` | Éval + déploiement |

Sur chaque branche d'atelier, les modules des ateliers **suivants** lèvent
`NotImplementedError`. L'élève les implémente en suivant le GUIDE-ELEVE.md.

---

## 9. Branches git

```
main                              → projet final complet (après AT06)
atelier/01-llm-prompts-parsers    → hirekit/llm/ + config.py
atelier/02-lcel-memoire           → + hirekit/services/matching.py
atelier/03-rag                    → + hirekit/rag/
atelier/04-agents-tools           → + hirekit/agent/ + services/availability.py
atelier/05-chatbot-code-review    → + hirekit/ui/ + api/
atelier/06-eval-benchmark-deploy  → + hirekit/eval/ + docker-compose.yml = main
```

L'élève `git checkout atelier/0X-...` pour passer à l'atelier courant. Les modules
des ateliers suivants sont des stubs `NotImplementedError`.

---

## 10. TDD

Chaque module a ses tests dans `tests/`, organisés par module :

```
tests/
├── conftest.py
├── test_llm/
│   ├── test_provider.py      # AT01
│   ├── test_prompts.py       # AT01
│   └── test_parsers.py       # AT01
├── test_rag/
│   ├── test_ingestion.py      # AT03
│   ├── test_chunking.py       # AT03
│   ├── test_vectorstore.py    # AT03
│   └── test_retriever.py     # AT03
├── test_agent/
│   ├── test_react_agent.py   # AT04
│   └── test_tools.py          # AT04
├── test_services/
│   ├── test_matching.py       # AT02
│   └── test_availability.py   # AT04
├── test_eval/
│   ├── test_metrics.py       # AT06
│   └── test_tracing.py        # AT06
└── test_ui/
    ├── test_telegram_bot.py  # AT05
    └── test_code_reviewer.py # AT05
```

Sur les branches précoces, les tests des modules non implémentés sont
`@pytest.mark.skip` ou `xfail`.

---

## 11. Délégation aux équipes d'agents IA

Le développement de ce fil rouge est délégué à 3 équipes d'agents IA, suivant le
pattern de `ai-teams-benchmark` v3.1 :

| Équipe | Stratégie | Lot | Ateliers |
|---|---|---|---|
| 🇨🇺 Cuba | Fix + Continue | `hirekit/llm/` + `hirekit/services/` | AT01 + AT02 |
| 🇭🇹 Haiti | OpenClaw | `hirekit/rag/` + `hirekit/agent/` | AT03 + AT04 |
| 🇬🇫 Guyane | Direct Coding | `hirekit/ui/` + `hirekit/eval/` + `api/` | AT05 + AT06 |

Chaque équipe reçoit sa spec via GitHub Issue + un canal Telegram dédié. Le scoring
est dans `SCORECARD.md` (dossier tâche ai-teams-benchmark).

---

## 12. Checklist de couverture programme

| Concept du programme | Atelier | Implémenté dans | Testé dans |
|---|---|---|---|
| LLMs vs Chat Models | AT01 | `hirekit/llm/provider.py` | `test_provider.py` |
| Prompt Templates | AT01 | `hirekit/llm/prompts.py` | `test_prompts.py` |
| Sélecteurs d'exemples | AT01 | `hirekit/llm/prompts.py` | `test_prompts.py` |
| Output Parsers | AT01 | `hirekit/llm/parsers.py` | `test_parsers.py` |
| LCEL | AT02 | `hirekit/services/matching.py` | `test_matching.py` |
| Conversation Memory | AT02 | `hirekit/services/matching.py` | `test_matching.py` |
| Persistence et État | AT02 | `hirekit/services/matching.py` | `test_matching.py` |
| Variables d'état | AT02 | `hirekit/services/matching.py` | `test_matching.py` |
| Document Loaders | AT03 | `hirekit/rag/ingestion.py` | `test_ingestion.py` |
| Text Splitters | AT03 | `hirekit/rag/chunking.py` | `test_chunking.py` |
| Vector Stores | AT03 | `hirekit/rag/vectorstore_*.py` | `test_vectorstore.py` |
| Embeddings | AT03 | `hirekit/rag/vectorstore_*.py` | `test_vectorstore.py` |
| Retriever (anti-hallucination) | AT03 | `hirekit/rag/retriever.py` | `test_retriever.py` |
| Agent ReAct | AT04 | `hirekit/agent/react_agent.py` | `test_react_agent.py` |
| Tools (APIs) | AT04 | `hirekit/agent/tools.py` | `test_tools.py` |
| Tools (code execution) | AT04 | `hirekit/agent/tools.py` | `test_tools.py` |
| Recherches web | AT04 | `hirekit/agent/tools.py` | `test_tools.py` |
| Agents autonomes | AT04 | `hirekit/agent/react_agent.py` | `test_react_agent.py` |
| UX Chatbot | AT05 | `hirekit/ui/app.py` | (manuel) |
| Compréhension du code | AT05 | `hirekit/ui/code_reviewer.py` | `test_code_reviewer.py` |
| Multimodal audio/vocal | AT05 | `hirekit/ui/app.py` | (manuel) |
| LangSmith | AT06 | `hirekit/eval/tracing.py` | `test_tracing.py` |
| Benchmarking (agents) | AT06 | `hirekit/eval/metrics.py` | `test_metrics.py` |
| Benchmarking (VectorDB) | AT06 | `hirekit/eval/metrics.py` | `test_metrics.py` |
| Déploiement | AT06 | `docker-compose.yml` | (manuel) |
| Monitoring des coûts | AT06 | `hirekit/eval/metrics.py` | `test_metrics.py` |