# Programme LangChain — Mapping officiel → Ateliers

> Source : https://www.ambient-it.net/formation/langchain/ (3 jours, 21h)
>
 Ce document mappe chaque concept du programme officiel à son implémentation
> dans le fil rouge ai-hirekit.

---

## Jour 1 — Matin : Architecture et Fondamentaux des LLM

### Programme officiel
- Introduction à LangChain : philosophie, installation et configuration
- Modèles et Prédictions : **LLMs vs Chat Models**
- Prompt Engineering Dynamique : **Prompt Templates** et **sélecteurs d'exemples**
- Gestion des sorties avec les **Output Parsers**
- Atelier pratique : Création d'un premier flux « Prompt + Modèle »

### Implémentation ai-hirekit — AT01

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| Philosophie LangChain | Pourquoi on utilise LangChain (abstraction multi-LLM) | GUIDE-ELEVE.md carnet de bord |
| Installation et configuration | `pyproject.toml`, `.env`, `hirekit/config.py` | Setup projet |
| **LLMs** (completion API) | `get_llm()` → `AnthropicLLM` ou `OpenAI` | `hirekit/llm/provider.py` |
| **Chat Models** (messages API) | `get_chat_model()` → `ChatAnthropic` ou `ChatOpenAI` | `hirekit/llm/provider.py` |
| **Prompt Templates** | `PromptTemplate` pour extraction CV, `ChatPromptTemplate` pour matching | `hirekit/llm/prompts.py` |
| **Sélecteurs d'exemples** | `SemanticSimilarityExampleSelector` pour few-shot matching | `hirekit/llm/prompts.py` |
| **Output Parsers** | `PydanticOutputParser` → CVInfo, `CommaSeparatedListOutputParser` → skills | `hirekit/llm/parsers.py` |
| Atelier pratique | CLI : poser 5 questions privées sur CVs → hallucinations + extraction CV→JSON | `ateliers/atelier-01-.../exercice.py` |

**Constat pédagogique** : le LLM nu ne connaît pas les CVs → hallucination. L'Output
Parser structure la sortie mais ne résout pas le problème de connaissance. Motivation
pour AT02 (LCEL) et AT03 (RAG).

---

## Jour 1 — Après-midi : LCEL et Gestion de la Mémoire

### Programme officiel
- **LangChain Expression Language (LCEL)** : composer des chaînes de manière déclarative
- **Persistence et État** : mise en œuvre de la Conversation Memory
- Chaînes avancées et gestion des **variables d'état**
- Atelier pratique : Développement d'un assistant capable de conserver le contexte

### Implémentation ai-hirekit — AT02

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| **LCEL** (pipe `\|`) | Chaîne matching : `RunnablePassthrough \| prompt \| llm \| parser` | `hirekit/services/matching.py` |
| **RunnablePassthrough** | Passer le CV et l'offre dans la chaîne | `hirekit/services/matching.py` |
| **RunnableLambda** | Prétraitement du CV (nettoyage, troncature) | `hirekit/services/matching.py` |
| **RunnableParallel** | Extraction + matching en parallèle | `hirekit/services/matching.py` |
| **RunnablePassthrough.assign()** | Variables d'état (candidat courant, offre courante) | `hirekit/services/matching.py` |
| **RunnableBranch** | Routing selon type de question | `hirekit/services/matching.py` |
| **RunnableWithFallbacks** | Fallback si erreur LLM | `hirekit/services/matching.py` |
| **ConversationBufferMemory** | Mémoire simple | `hirekit/services/matching.py` |
| **ConversationBufferWindowMemory** | Mémoire fenêtrée k=10 | `hirekit/services/matching.py` |
| **ConversationSummaryMemory** | Auto-summarisation | `hirekit/services/matching.py` |
| **Persistence** | save/load memory en JSON, restauration au redémarrage | `hirekit/services/matching.py` |
| `.batch()` | Traiter 3 CVs en parallèle | `hirekit/services/matching.py` |
| Atelier pratique | Chaîne matching + mémoire recruteur persistée entre sessions | `ateliers/atelier-02-.../exercice.py` |

---

## Jour 2 — Matin : RAG et Gestion des Données (Retrieval)

### Programme officiel
- **Document Loaders** et **Text Splitters**
- **Vector Stores** et **Embeddings** : indexer ses données
- Le **Retriever** : optimiser la récupération pour limiter les hallucinations
- Atelier pratique : Création d'une chaîne de Question-Answering sur documents PDF

### Implémentation ai-hirekit — AT03

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| **Document Loaders** | `PyMuPDFLoader` (CVs PDF), `JSONLoader` (offres), `CSVLoader` (skills) | `hirekit/rag/ingestion.py` |
| **Text Splitters** | `RecursiveCharacterTextSplitter` (recommandé), `CharacterTextSplitter` | `hirekit/rag/chunking.py` |
| Comparaison chunking | Fixed-size vs recursive → Recall@5 | `hirekit/rag/chunking.py` |
| **Embeddings** | `FastEmbedEmbeddings` (multilingue, 384d, CPU) | `hirekit/rag/vectorstore_faiss.py` |
| **Vector Stores** | FAISS (CVs), ChromaDB (offres avec métadonnées) | `hirekit/rag/vectorstore_*.py` |
| **Retriever** | `as_retriever()`, `search_type="mmr"`, `k`, `fetch_k` | `hirekit/rag/retriever.py` |
| **Anti-hallucination** | Recall@5 ≥ 0.80, 0 hallucination sur questions privées | `hirekit/rag/retriever.py` |
| Recall@k, faithfulness | Mesures pour quantifier la qualité | `hirekit/eval/metrics.py` (utilisé en AT03) |
| Atelier pratique | RAG sur 30 CVs PDF + 15 offres, Q&A sourcée | `ateliers/atelier-03-.../exercice.py` |

**Lien avec AT01** : les 5 questions privées d'AT01 (qui hallucinaient) sont repassées
avec le RAG → le hallucination rate doit chuter à 0%.

---

## Jour 2 — Après-midi : Agents et Autonomie

### Programme officiel
- Concept d'**Agent** : raisonnement (ReAct) et cycle de l'Agent Executor
- **Outils (Tools)** : permettre à l'IA d'appeler des APIs ou **d'exécuter du code**
- **Agents autonomes** et simulations
- Atelier pratique : Construction d'un agent capable d'effectuer des **recherches web**

### Implémentation ai-hirekit — AT04

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| **Pattern ReAct** | Thought → Action → Observation → boucle | `hirekit/agent/react_agent.py` |
| `create_react_agent` | Assemblage de l'agent | `hirekit/agent/react_agent.py` |
| `AgentExecutor` | Orchestration + `max_iterations` | `hirekit/agent/react_agent.py` |
| **Tools — appel d'APIs** | `search_cvs` (RAG), `match_candidate` (LCEL), `check_availability` | `hirekit/agent/tools.py` |
| **Tools — exécution de code** | `PythonREPLTool` (calcul de score composite) | `hirekit/agent/tools.py` |
| **Recherches web** | Outil de search (simulé ou serpapi) — **atelier principal** | `hirekit/agent/tools.py` |
| `@tool` decorator | Définition des outils avec description + schema | `hirekit/agent/tools.py` |
| **Agents autonomes** | Agent qui tourne sur un scénario sans input utilisateur | `hirekit/agent/react_agent.py` |
| `return_intermediate_steps` | Audit trail de la trace ReAct | `hirekit/agent/react_agent.py` |
| `handle_parsing_errors` | Robustesse | `hirekit/agent/react_agent.py` |
| Mémoire agent | `ConversationBufferWindowMemory(k=10)` | `hirekit/agent/react_agent.py` |
| Atelier pratique | Agent qui cherche des profils + recherche web + exécute du code | `ateliers/atelier-04-.../exercice.py` |

---

## Jour 3 — Matin : Cas d'usage : Chatbots et Analyse de Code

### Programme officiel
- **UX Chatbot** : recréer une expérience de type ChatGPT
- **Compréhension du code** : indexation et assistant d'aide au développement
- Introduction aux assistants **multimodaux (audio/vocal)**
- Atelier pratique : Développement d'un « Code-Reviewer » intelligent

### Implémentation ai-hirekit — AT05

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| **UX Chatbot** | Streamlit `st.chat_message`, historique, streaming des tokens | `hirekit/ui/app.py` |
| Multi-pages | Chat, Dashboard matching, Bibliothèque CVs | `hirekit/ui/app.py` |
| Bot Telegram | Bot simulé (mock local) + vrai bot (bonus) | `hirekit/ui/telegram_bot.py` |
| **Compréhension du code** | Indexer un repo Python comme corpus RAG | `hirekit/ui/code_reviewer.py` |
| Code indexing | `GenericLoader` pour fichiers .py, `RecursiveCharacterTextSplitter` | `hirekit/ui/code_reviewer.py` |
| Q&A sur code | « Où est géré l'authentification ? », « Que fait la fonction X ? » | `hirekit/ui/code_reviewer.py` |
| **Multimodal audio/vocal** | Transcription vocale → texte (Whisper/mock) → LLM | `hirekit/ui/app.py` |
| TTS | Text-to-speech pour réponse vocale (introduction) | `hirekit/ui/app.py` |
| API REST | FastAPI `/chat`, `/match` | `api/main.py` |
| Atelier pratique | Code-Reviewer intelligent sur repo Python | `ateliers/atelier-05-.../exercice.py` |

---

## Jour 3 — Après-midi : Évaluation, Benchmarking et Déploiement

### Programme officiel
- Évaluation des chaînes et utilisation de **LangSmith**
- **Benchmarking** : analyse comparative des **agents** et **VectorDB**
- **Déploiement** et **monitoring des coûts** en production
- Atelier pratique : Audit de performance et test de robustesse sur dataset

### Implémentation ai-hirekit — AT06

| Concept du programme | Implémentation | Fichier |
|---|---|---|
| **LangSmith** | `CallbackHandler` pour tracer chaînes et agents | `hirekit/eval/tracing.py` |
| Dataset LangSmith | 20 questions de test dans LangSmith | `hirekit/eval/tracing.py` |
| Comparaison de runs | Évaluer llm_only vs rag_only vs agent | `hirekit/eval/metrics.py` |
| **Benchmarking — agents** | ReAct vs RAG seul vs LLM seul (score, latence, coût) | `hirekit/eval/metrics.py` |
| **Benchmarking — VectorDB** | FAISS vs ChromaDB (Recall@k, latence ingestion) | `hirekit/eval/metrics.py` |
| Recall@k, MRR | Métriques de retrieval | `hirekit/eval/metrics.py` |
| **Déploiement** | FastAPI + Docker Compose (api + streamlit + chromadb) | `docker-compose.yml` |
| `uvicorn` | Serveur ASGI pour FastAPI | `api/main.py` |
| **Monitoring des coûts** | Tokens in/out, coût € par requête, budget par session | `hirekit/eval/metrics.py` |
| `response.usage_metadata` | Extraction des tokens consommés | `hirekit/eval/metrics.py` |
| Atelier pratique | Audit de performance + robustesse sur 20 questions | `ateliers/atelier-06-.../exercice.py` |

---

## Récapitulatif de couverture

| Demi-journée | Concepts du programme | Tous couverts ? |
|---|---|---|
| J1 matin | LLMs vs Chat, Prompt Templates, ExampleSelector, Output Parsers | ✅ AT01 |
| J1 a.-m. | LCEL, Persistence, Conversation Memory, variables d'état | ✅ AT02 |
| J2 matin | Document Loaders, Text Splitters, Vector Stores, Embeddings, Retriever | ✅ AT03 |
| J2 a.-m. | Agent ReAct, Tools (APIs + code), recherches web, agents autonomes | ✅ AT04 |
| J3 matin | UX Chatbot, Code Analysis, Multimodal audio/vocal | ✅ AT05 |
| J3 a.-m. | LangSmith, Benchmarking (agents + VectorDB), Déploiement, Coûts | ✅ AT06 |