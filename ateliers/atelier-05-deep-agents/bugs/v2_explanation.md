# Bug v2 — AGENTS.md manquant
#
# ## Ce qui se passe
# Le chemin vers AGENTS.md est modifié: `.agent/memory/AGENTS.md` au lieu de
# `.agent/memory/recruiter/AGENTS.md`. Le fichier n'existe pas à ce chemin,
# donc `AGENTS_MD` est vide.
#
# ## Pourquoi c'est un bug
# Les règles globales (langue française, recadrage hors-sujet, interdiction URLs,
# rôle recruteur) ne sont pas injectées dans le systemPrompt. L'agent peut
# répondre en anglais, parler de la météo, donner des URLs, se comporter comme
# un assistant.
#
# ## Comment le réparer
# Remettre le bon chemin: `AGENT_DIR / "memory" / "recruiter" / "AGENTS.md"`
#
# ## Vrai/Faux
# 1. Le bug est dans `recruiter_agent.py`. V/F
# 2. Sans AGENTS.md, l'agent peut répondre en anglais. V/F
# 3. Le test `test_agents_md_loaded` détecte le bug. V/F