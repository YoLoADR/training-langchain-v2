"""Deep Agents — recruteur IA autonome 4 couches.

Inspiration: sellkit/src/agent/deep-agent.ts

Architecture 4 couches:
  Couche 1: systemPrompt  — Identité statique (nom, entreprise, ton) + AGENTS.md
  Couche 2: memory        — AGENTS.md injecté dans systemPrompt (fs.readFileSync)
  Couche 3: skills        — SKILL.md injecté par middleware beforeModel
  Couche 4: contextSchema  — RecruitmentContext (Pydantic) + contexte dynamique

Docs: https://docs.langchain.com/oss/python/deepagents/overview
"""
