# Insights — Fil Rouge v3 (aligné sellkit)

> Journal de progression du fil rouge LangChain, aligné sur l'architecture sellkit.

## 2026-08-10 — Phase 0 : Sauvegarder le plan

### Décisions prises

1. **Alignement sellkit** : training-langchain-v2 doit ressembler à sellkit sur le plan
   architectural (Deep Agents 4 couches, CRM pipeline, pipeline détection, tests E2E).
   sellkit est TypeScript — training-langchain-v2 est Python. On traduit les concepts,
   on ne copie pas le code.

2. **Nouvel ordre des ateliers** : AT04 ReAct → AT05 Deep Agents → AT06 Chatbots+CRM →
   AT07 Eval+E2E. Le Deep Agents arrive après ReAct (l'élève connaît les agents avant
   de découvrir le harness Deep Agents).

3. **Nouveaux modules** : hirekit/pipeline/ (objections, closing, memory, qualification),
   hirekit/deep_agent/ (recruiter_agent, middleware, harness_profile),
   hirekit/crm/ (types, store SQLite), hirekit/telemetry/ (log structuré),
   .agent/ (AGENTS.md + 5 SKILL.md).

4. **Tests restructurés** : tests/unit/ (purs, pas LLM), tests/integration/ (avec LLM),
   tests/e2e/ (Playwright human-in-the-loop). Pattern inspiré sellkit:
   - step1: 3 échanges → DB + API + logs
   - step5: 13 étapes, 3 scénarios aléatoires, DB + API + logs

5. **Cuba a déjà fait AT01-AT05** (6 ateliers originaux). On garde son travail.
   On ajoute les modules manquants (pipeline, deep_agent, crm, telemetry, .agent)
   et on restructure les ateliers (ajout AT05 Deep Agents, décalage AT06-AT07).

### Ce que sellkit a que training-langchain-v2 doit avoir

| Concept sellkit | Fichier sellkit | Équivalent training-langchain-v2 |
|---|---|---|
| createDeepAgent 4 couches | src/agent/deep-agent.ts:17-88 | hirekit/deep_agent/recruiter_agent.py |
| beforeModel middleware | src/agent/middleware/recruitment-context.ts:138-165 | hirekit/deep_agent/middleware.py |
| HarnessProfile | src/harness-profile.ts:14-37 | hirekit/deep_agent/harness_profile.py |
| AGENTS.md (mémoire) | .agent/memory/recruiter/AGENTS.md | .agent/memory/recruiter/AGENTS.md |
| 5 SKILL.md (skills) | .agent/skills/recruiter/phase-*/SKILL.md | .agent/skills/recruiter/phase-*/SKILL.md |
| Memory extraction LLM | src/pipeline/memory.ts:94-131 | hirekit/pipeline/memory.py |
| Objection detection | src/pipeline/objections.ts:125-155 | hirekit/pipeline/objections.py |
| Closing detection | src/pipeline/closing.ts:89-116 | hirekit/pipeline/closing.py |
| CRM SQLite pipeline | src/crm/store.ts:47-292 | hirekit/crm/store.py |
| Telegram handler | src/telegram/handler.ts:45-226 | hirekit/ui/telegram_bot.py |
| Logs structurés (14) | src/telemetry/log.ts | hirekit/telemetry/log.py |
| Web dashboard | src/web/server.ts:19-94 | hirekit/ui/app.py (Streamlit) |
| Step1 test | tests/step1-human-in-the-loop.test.ts | tests/e2e/test_step1_conversation.py |
| Step5 test | tests/step5-human-in-the-loop.test.ts | tests/e2e/test_step5_full_pipeline.py |

### État Cuba (au 2026-08-10)

Cuba a pushé 4 commits sur origin/main:
- c790bc7: données simulées + PLAN.md + scripts (70 fichiers, 42k lignes)
- 3561ff7: AT01+AT02 implémentation LCEL, Mémoire, Prompts, Parsers + atelier AT02 complet
- 9235e0b: AT03 RAG complet (Document Loaders, Splitters, FAISS+ChromaDB, Retriever MMR)
- 1d6801e: AT04 Agents ReAct + Tools (4 outils, AgentExecutor, agent autonome)
- 8afb329: AT05 Chatbots + Code Analysis + Multimodal (Streamlit, Telegram, Code-Reviewer)

**Manque** : Deep Agents, CRM sellkit-style, pipeline détection, tests E2E Playwright.