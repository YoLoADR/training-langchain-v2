# Bug v3 — python_repl n'attrape pas les erreurs (crash de l'agent)

## Symptôme

L'agent s'arrête brutalement quand `python_repl_tool` exécute du code
qui lève une exception (ex: division par zéro). L'AgentExecutor ne
récupère pas l'erreur.

## Cause

`python_repl_tool` n'a pas de bloc `try/except` autour de l'exécution.
L'exception remonte et crash l'agent.

## Fix

Envelopper l'exécution dans un `try/except` qui retourne le message
d'erreur comme observation (string), au lieu de laisser l'exception
remonter. L'agent peut alors lire l'erreur et ajuster son code.