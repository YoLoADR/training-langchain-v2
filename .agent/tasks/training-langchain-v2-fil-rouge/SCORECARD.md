# SCORECARD — Training LangChain v2 (Fil Rouge ai-hirekit)

> Scoring des équipes d'agents IA lors de la délégation du développement.
> Inspiré de ai-teams-benchmark SCORECARD.md.

## Grille de scoring (100 points)

| Critère | Points | Détail |
|---|---|---|
| **Compréhension** | 25 | PLAN.md, US Gherkin, découpage correct, respect du programme |
| **Développement** | 40 | Code fonctionnel, TDD respecté (tests passent), stubs → implémentation |
| **Qualité pédagogique** | 35 | GUIDE-ELEVE.md complet (mission, carnet de bord, bugs, checkpoints, quiz), cohérence avec programme |

## Scores par équipe (à remplir après délégation)

| Équipe | Stratégie | Lot | Compréhension /25 | Développement /40 | Pédagogie /35 | Total /100 |
|---|---|---|---|---|---|---|
| 🇨🇺 Cuba | Fix + Continue | llm/ + services/ (AT01-02) | - | - | - | - |
| 🇭🇹 Haiti | OpenClaw | rag/ + agent/ (AT03-04) | - | - | - | - |
| 🇬🇫 Guyane | Direct Coding | ui/ + eval/ + api/ (AT05-06) | - | - | - | - |

## Critères détaillés par lot

### Cuba (AT01 + AT02) — 100 points

| # | Critère | Points | Preuve attendue |
|---|---|---|---|
| 1 | hirekit/llm/provider.py : get_llm() supporte LLMs + Chat Models | 8 | test_provider.py passe |
| 2 | hirekit/llm/prompts.py : PromptTemplate + ChatPromptTemplate + ExampleSelector | 8 | test_prompts.py passe |
| 3 | hirekit/llm/parsers.py : PydanticOutputParser + CommaSeparatedListOutputParser | 8 | test_parsers.py passe |
| 4 | hirekit/services/matching.py : chaîne LCEL pipe operator | 8 | test_matching.py passe |
| 5 | Conversation Memory + persistence (save/load JSON) | 8 | test memoire 3 tours |
| 6 | AT01 GUIDE-ELEVE.md : mission, carnet de bord, bug hunt, checkpoints, quiz | 17 | complet et cohérent |
| 7 | AT02 GUIDE-ELEVE.md : mission, carnet de bord, bug hunt, checkpoints, quiz | 18 | complet et cohérent |
| 8 | AT01 + AT02 bugs (3×2=6 patches + tests + explications) | 17 | 6 pytest verts |
| 9 | AT01 + AT02 checkpoints (2×2=4 QCM auto-corrigés) | 8 | scripts fonctionnels |

### Haiti (AT03 + AT04) — 100 points

| # | Critère | Points | Preuve attendue |
|---|---|---|---|
| 1 | hirekit/rag/ingestion.py : PyMuPDFLoader, JSONLoader, CSVLoader | 8 | test_ingestion.py passe |
| 2 | hirekit/rag/chunking.py : fixed + recursive + comparaison Recall@5 | 8 | test_chunking.py passe |
| 3 | hirekit/rag/vectorstore_faiss.py + vectorstore_chroma.py | 8 | test_vectorstore.py passe |
| 4 | hirekit/rag/retriever.py : MMR, EnsembleRetriever | 8 | test_retriever.py passe |
| 5 | hirekit/agent/tools.py : @tool (search_cvs, match, web_search, python_repl) | 8 | test_tools.py passe |
| 6 | hirekit/agent/react_agent.py : AgentExecutor + max_iterations + mémoire | 8 | test_react_agent.py passe |
| 7 | AT03 + AT04 GUIDE-ELEVE.md | 17 | complet et cohérent |
| 8 | AT03 + AT04 bugs (6 patches + tests + explications) | 17 | 6 pytest verts |
| 9 | AT03 + AT04 checkpoints (4 QCM) | 8 | scripts fonctionnels |
| 10 | Recherches web fonctionnelles (mock ou serpapi) | 10 | démonstration |

### Guyane (AT05 + AT06) — 100 points

| # | Critère | Points | Preuve attendue |
|---|---|---|---|
| 1 | hirekit/ui/app.py : Streamlit multi-pages (chat, dashboard, library) | 8 | streamlit run fonctionne |
| 2 | hirekit/ui/telegram_bot.py : bot Telegram simulé (mock local) | 8 | tests passent |
| 3 | hirekit/ui/code_reviewer.py : indexation repo Python + Q&A | 8 | test_code_reviewer.py passe |
| 4 | hirekit/eval/metrics.py : Recall@k, MRR, cost monitoring | 8 | test_metrics.py passe |
| 5 | hirekit/eval/tracing.py : LangSmith callbacks | 8 | traces visibles |
| 6 | api/main.py : FastAPI + Docker Compose | 8 | docker compose up |
| 7 | AT05 + AT06 GUIDE-ELEVE.md | 17 | complet et cohérent |
| 8 | AT05 + AT06 bugs (6 patches + tests + explications) | 17 | 6 pytest verts |
| 9 | AT05 + AT06 checkpoints (4 QCM) | 8 | scripts fonctionnels |
| 10 | Multimodal audio/vocal (introduction, mock acceptable) | 10 | démonstration |