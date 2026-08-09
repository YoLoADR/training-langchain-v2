# AI-HireKit — Projet Fil Rouge

> Formation "Applications d'IA générative avec LangChain" (Ambient IT, 3 jours, 21h)
>
> Ce repo est le fil rouge v2 de la formation LangChain. Il reverse-engineer le projet
> ai-hirekit (assistant IA pour recruteurs) en 6 ateliers progressifs.

## Programme

| Jour | Demi-journée | Atelier | Thème |
|---|---|---|---|
| J1 | Matin | AT01 | LLM + Prompts + Output Parsers |
| J1 | Après-midi | AT02 | LCEL + Mémoire conversationnelle |
| J2 | Matin | AT03 | RAG (Document Loaders, Vector Stores, Retriever) |
| J2 | Après-midi | AT04 | Agents ReAct + Tools (recherches web, code) |
| J3 | Matin | AT05 | Chatbots + Code Analysis + Multimodal |
| J3 | Après-midi | AT06 | Évaluation + Benchmarking + Déploiement |

## Démarrage rapide

```bash
# Cloner
git clone <repo-url>
cd training-langchain-v2

# Environnement
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Config
cp .env.example .env
# Éditer .env avec votre ANTHROPIC_API_KEY

# Données simulées
python scripts/generate_cvs.py
python scripts/generate_offers.py
python scripts/generate_qa_dataset.py

# Vérifier qu'un atelier est prêt
bash scripts/check_atelier_ready.sh 01
```

## Structure

```
training-langchain-v2/
├── AI-HireKit-Projet-Fil-Rouge.md   # Spec produit complet
├── PROGRAMME-LANGCHAIN.md            # Mapping programme → ateliers
├── hirekit/                         # Package principal (construit progressivement)
├── ateliers/                         # 6 ateliers (GUIDE-ELEVE, exercice, bugs, checkpoints)
├── api/                              # FastAPI (AT05-AT06)
├── scripts/                          # Génération de données + utilitaires
├── data/                             # Données simulées (CVs, offres, QA)
├── tests/                            # Tests TDD
└── docker-compose.yml                # Déploiement (AT06)
```

## Branches git

Chaque atelier a sa branche. Checkout la branche de l'atelier courant :

```bash
git checkout atelier/01-llm-prompts-parsers   # J1 matin
git checkout atelier/02-lcel-memoire           # J1 après-midi
git checkout atelier/03-rag                     # J2 matin
git checkout atelier/04-agents-tools           # J2 après-midi
git checkout atelier/05-chatbot-code-review    # J3 matin
git checkout atelier/06-eval-benchmark-deploy  # J3 après-midi (= main)
```

## Documentation

- [Spec produit](AI-HireKit-Projet-Fil-Rouge.md) — vision, personas, user stories, architecture
- [Mapping programme](PROGRAMME-LANGCHAIN.md) — correspondance concept par concept
- [Ateliers](ateliers/) — GUIDE-ELEVE.md par atelier