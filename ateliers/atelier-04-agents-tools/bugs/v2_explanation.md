# Bug v2 — max_iterations=1 (l'agent ne peut pas terminer)

## Symptôme

L'agent s'arrête après une seule itération. Il ne peut pas terminer son
cycle Thought → Action → Observation → Final Answer.

## Cause

`AgentExecutor` est configuré avec `max_iterations=1`. L'agent fait
un seul appel d'outil, puis s'arrête sans donner de réponse finale.

## Fix

Remplacer `max_iterations=1` par `max_iterations=8` (ou au moins 3-4)
pour permettre à l'agent de faire plusieurs cycles Thought/Action/Observation.