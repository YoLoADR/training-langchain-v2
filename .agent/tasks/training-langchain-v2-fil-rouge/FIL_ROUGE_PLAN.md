# Fil Rouge Plan — Training LangChain v2 (ai-hirekit)

> Reverse-engineering du projet ai-hirekit en fil rouge progressif pour la formation
> Ambient IT LangChain (3 jours, 21h). Pattern pédagogique : pre-training-rag (HomeButler).

## 1. Vision produit

**ai-hirekit** est un assistant IA pour recruteurs qui automatise le screening de CVs,
le matching candidat↔offre, la génération de grilles d'entretien et la planification —
accessible via une interface chat (Streamlit) et un bot Telegram (simulé).

Le projet final existe dans `/Users/yohannravino/Factory/ai-hirekit/`. Le but est de le
**découper à l'envers** en 6 ateliers progressifs qui suivent le programme de formation.

## 2. Personas

| Persona | Profil | Besoin |
|---|---|---|
| Sophie, 35 ans | RRH PME, 15 recrutements/an | Screening rapide, pas technique |
| Karim, 28 ans | Tech recruiter ESN, 50 recrutements/an | Matching précis, automatisation |
| Léa, 42 ans | Dirigeante TPE | Assistant simple, mobile (Telegram) |

## 3. User Stories

1. US-01 : Je dépose 10 CVs PDF → je demande "qui a >3 ans d'XP en React ?" → réponse sourcée
2. US-02 : Je soumets une offre + un CV → extraction structurée (Output Parser) + score matching
3. US-03 : Je shortliste un candidat → génération d'une grille d'entretien personnalisée
4. US-04 : Sur 3 sessions, l'assistant se souvient de mes critères (mémoire persistée)
5. US-05 : Via Telegram : "trouve les 3 meilleurs profils DevOps" → agent cherche + matche + répond

## 4. Mapping programme → ateliers (vérifié contre le programme officiel)

### AT01 — J1 matin — LLM + Prompts + Output Parsers

**Programme** : LLMs vs Chat Models, Prompt Templates, sélecteurs d'exemples, Output Parsers

**Mission** : "Prouve qu'un LLM nu hallucine sur des CVs privés. Extrais les infos
structurées d'un CV avec un Output Parser."

**Concepts couverts** :
- LLMs (completion API) vs Chat Models (messages API) — instancier et comparer
- PromptTemplate vs ChatPromptTemplate
- ExampleSelector (sélecteur d'exemples dynamique) — FewShotPromptTemplate
- PydanticOutputParser — extraction CV → `{nom, email, competences[], experiences[]}`
- CommaSeparatedListOutputParser — extraction liste de compétences
- Temperature, max_tokens, system prompt (rappels)

**Livrable** : CLI qui pose 5 questions privées sur des CVs → hallucinations, puis
extrait un CV en JSON structuré via Output Parser.

**Constat pédagogique** : le LLM nu ne connaît pas les CVs → hallucination. L'Output
Parser structure la sortie mais ne résout pas le problème de connaissance. Motivation
pour AT02 (LCEL) et AT03 (RAG).

### AT02 — J1 a.-m. — LCEL + Mémoire conversationnelle

**Programme** : LCEL, Persistence et État, Conversation Memory, chaînes avancées, variables d'état

**Mission** : "Construis une chaîne LCEL de matching CV↔offre qui retourne un score
+ justification. Le recruteur doit pouvoir enchaîner plusieurs matchings sans répéter
ses critères (mémoire persistée)."

**Concepts couverts** :
- LCEL : pipe operator `|`, `RunnablePassthrough`, `RunnableLambda`, `RunnableParallel`
- `RunnablePassthrough.assign()` pour variables d'état
- `RunnableBranch` (routing selon type de question)
- `RunnableWithFallbacks` (fallback si erreur)
- ConversationBufferMemory, ConversationBufferWindowMemory(k=10)
- ConversationSummaryMemory (auto-summarisation)
- **Persistence** : save/load memory en JSON, restauration au redémarrage
- `.batch()` pour traiter 3 CVs en parallèle

**Livrable** : Chaîne LCEL matching + mémoire recruteur persistée entre sessions.
Test : info donnée au tour 1 retrouvée au tour 3 après redémarrage.

### AT03 — J2 matin — RAG sur CVs + offres

**Programme** : Document Loaders, Text Splitters, Vector Stores, Embeddings, Retriever (anti-hallucination)

**Mission** : "Indexe les 30 CVs et 15 offres. Je veux demander 'qui connaît Kubernetes ?'
et recevoir une réponse sourcée avec le nom du candidat et l'extrait du CV. Le retriever
 doit réduire le hallucination rate d'AT01."

**Concepts couverts** :
- Document Loaders : PyMuPDFLoader (CVs PDF), JSONLoader (offres), CSVLoader (skills)
- Text Splitters : RecursiveCharacterTextSplitter, CharacterTextSplitter
- Comparaison chunking : fixed-size vs recursive (Recall@5)
- Embeddings : FastEmbedEmbeddings (sentence-transformers multilingue, 384d)
- Vector Stores : FAISS (CVs), ChromaDB (offres avec métadonnées)
- Retriever : `as_retriever()`, `search_type="mmr"`, `k`, `fetch_k`
- **Objectif anti-hallucination** : Recall@5 ≥ 0.80, 0 hallucination sur questions privées
- Recall@k, faithfulness (mesures)

**Livrable** : RAG pipeline sur CVs + offres, Q&A sourcée, Recall@5 ≥ 0.80.

### AT04 — J2 a.-m. — Agents + Tools

**Programme** : Agent ReAct, Tools (APIs + code execution), recherches web, agents autonomes

**Mission** : "Construis un agent qui, sur 'trouve les 3 meilleurs profils DevOps, vérifie
leur réputation en ligne, et calcule un score composite', orchestre plusieurs outils
dont une recherche web et une exécution de code Python."

**Concepts couverts** :
- Pattern ReAct : Thought → Action → Observation → boucle
- `create_react_agent`, `AgentExecutor`, `max_iterations`
- `@tool` decorator : description et schema critiques
- Deux types d'outils :
  1. Appel d'APIs : search_cvs (RAG), match_candidate (LCEL), check_availability
  2. **Exécution de code** : PythonREPLTool (calcul de score composite)
- **Recherches web** : outil de search (serpapi ou mock simulé) — atelier principal
- **Agents autonomes** : agent qui tourne sur un scénario sans input utilisateur
- `return_intermediate_steps=True` pour audit trail
- `handle_parsing_errors=True`

**Livrable** : Agent ReAct 4+ outils, trace ReAct visible, recherche web fonctionnelle.

### AT05 — J3 matin — Chatbots + Code Analysis + Multimodal

**Programme** : UX Chatbot, compréhension du code (indexation), assistants multimodaux (audio/vocal)

**Mission** : "Déploie l'assistant sur Streamlit ET un bot Telegram simulé. Ajoute un
Code-Reviewer qui indexe un repo Python et répond à 'où est géré l'authentification ?'."

**Concepts couverts** :
- UX Chatbot : Streamlit `st.chat_message`, historique, streaming des tokens
- Bot Telegram simulé (mock local, pas de vrai bot API)
- **Compréhension du code** :
  - Indexer un repo Python comme corpus RAG (RecursiveCharacterTextSplitter sur .py)
  - Q&A sur le code : "où est géré l'auth ?", "que fait la fonction X ?"
  - `GenericLoader` pour fichiers Python
- **Multimodal audio/vocal** :
  - Transcription vocale → texte (Whisper ou mock) → LLM
  - TTS (text-to-speech) pour réponse vocale
  - Introduction (pas approfondissement)

**Livrable** : Streamlit chat + bot Telegram simulé + Code-Reviewer sur repo Python.

### AT06 — J3 a.-m. — Évaluation + Benchmarking + Déploiement

**Programme** : LangSmith, benchmarking (agents + VectorDB), déploiement, monitoring coûts

**Mission** : "Compare les 3 modes (llm_only, rag_only, agent) sur 20 questions. Branche
LangSmith. Déploie avec Docker Compose. Monitor les coûts par requête."

**Concepts couverts** :
- **LangSmith** : tracing des chaînes et agents, évaluation sur dataset
  - `CallbackHandler` LangSmith
  - Dataset de test dans LangSmith
  - Comparaison de runs
- **Benchmarking** :
  - Comparatif des **agents** : ReAct vs RAG seul vs LLM seul (score, latence, coût)
  - Comparatif des **VectorDB** : FAISS vs ChromaDB (Recall@k, latence ingestion)
  - Tableau de métriques chiffrées
- **Déploiement** :
  - FastAPI + Docker Compose (api + streamlit + chromadb)
  - `uvicorn` + `streamlit run`
- **Monitoring des coûts** :
  - Tokens in/out par requête
  - Coût € par requête (Anthropic/OpenAI pricing)
  - Budget par session, alerting seuil
  - `response.usage_metadata`

**Livrable** : Rapport comparatif chiffré + traces LangSmith + Docker Compose + dashboard coûts.

## 5. Structure de chaque atelier (pattern HomeButler)

```
ateliers/atelier-0X-nom/
├── GUIDE-ELEVE.md          # Mission, contraintes, indices, carnet de bord (lexique),
│                           #   mini-lab, bug hunt, checkpoints, sprint/bonus, wrap-up quiz
├── GUIDE-FORMATEUR.md      # Déroulé, timing, points de vigilance, transitions
├── exercice.py             # Squelette à TODOs (NotImplementedError tant que pas complété)
├── solution.py             # Solution de référence (importe depuis hirekit/)
├── bugs/                   # 3 patches git + 3 tests pytest + 3 explications
│   ├── v1.patch
│   ├── test_v1.py
│   ├── v1_explanation.md
│   ├── v2.patch
│   ├── test_v2.py
│   ├── v2_explanation.md
│   ├── v3.patch
│   ├── test_v3.py
│   └── v3_explanation.md
├── checkpoints/            # QCM auto-corrigés
│   ├── check_1.py
│   └── check_final.py
├── .claude/
│   └── CLAUDE.md           # Scope guard (bloquent concepts des ateliers suivants)
└── .cursorrules            # Scope guard pour Cursor
```

## 6. Données simulées

| Donnée | Format | Script | Contenu |
|---|---|---|---|
| 30 CVs | PDF 1-2 pages | `scripts/generate_cvs.py` | Dev React/Python/DevOps, design, marketing, alternance, junior/senior |
| 15 offres | JSON | `scripts/generate_offers.py` | Titre, description, compétences, localisation, salaire |
| Skills taxonomy | CSV | `scripts/generate_skills.py` | 100 compétences × catégorie (frontend, backend, DevOps, soft) |
| QA dataset | JSONL | `scripts/generate_qa_dataset.py` | 150 paires Q/A + sources (pour évaluation) |
| Calendrier | JSON | `scripts/generate_availability.py` | 30 jours de créneaux (pour l'outil planning) |
| Code repo | .py | `scripts/generate_code_repo.py` | 10 fichiers Python (pour Code-Reviewer AT05) |

## 7. TDD

Chaque module du package `hirekit/` est développé en TDD :
1. Écrire le test (pytest) qui définit le comportement attendu
2. Vérifier que le test échoue (RED)
3. Implémenter le code minimal (GREEN)
4. Refactorer

Tests dans `tests/` organisés par module. Sur les branches précoces, les tests des modules
non implémentés sont `@pytest.mark.skip` ou `xfail`.

## 8. Délégation aux équipes d'agents IA

Pattern ai-teams-benchmark v3.1 : 3 équipes, chacune responsable de 2 ateliers.

| Équipe | Stratégie | Modèles | Lot | Ateliers |
|---|---|---|---|---|
| Cuba | Fix + Continue | PO: glm-5.2:cloud, Dev: mistral-large-3, Lead: deepseek-v4-pro | hirekit/llm/ + services/ | AT01 + AT02 |
| Haiti | OpenClaw | PO: glm-5.2:cloud, coding-agent: opencode | hirekit/rag/ + agent/ | AT03 + AT04 |
| Guyane | Direct Coding | PO: glm-5.2:cloud | hirekit/ui/ + eval/ + api/ | AT05 + AT06 |

## 9. Phases d'exécution

| Phase | Action | Durée estimée |
|---|---|---|
| 0 | Sauvegarder le plan dans ai-teams-benchmark/.agent/tasks/ | 15 min |
| 1 | Initialiser repo git + structure de dossiers | 30 min |
| 2 | Rédiger AI-HireKit-Projet-Fil-Rouge.md (doc PO) | 1h |
| 3 | Créer pyproject.toml + .env.example + .gitignore | 15 min |
| 4 | Créer le package hirekit/ (stubs NotImplementedError) | 30 min |
| 5 | Créer les scripts de génération de données | 45 min |
| 6 | Créer les tests/ (TDD scaffolding) | 30 min |
| 7 | Rédiger les 6 GUIDE-ELEVE.md | 3h |
| 8 | Rédiger les 6 GUIDE-FORMATEUR.md | 2h |
| 9 | Créer exercice.py + solution.py × 6 | 2h |
| 10 | Créer bugs/ (3 × 6 = 18 patches + tests) | 3h |
| 11 | Créer checkpoints/ (2 × 6 = 12 QCM) | 1h30 |
| 12 | Créer .claude/ + .cursorrules scope guards × 6 | 1h |
| 13 | Créer les 6 branches git | 30 min |
| 14 | Configurer délégation aux 3 équipes | 1h |
| 15 | Git commit + push à chaque étape | continu |