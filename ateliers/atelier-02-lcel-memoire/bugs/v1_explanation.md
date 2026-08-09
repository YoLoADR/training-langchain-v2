# Bug v1 — RunnableLambda n'extrait pas la bonne clé

## Symptôme

La chaîne LCEL échoue avec une KeyError quand on essaie d'invoquer le matching.
Le RunnableLambda ne trouve pas la clé "cv" dans le dictionnaire d'entrée.

## Cause

Le RunnableLambda appelle `clean_cv(x)` au lieu de `clean_cv(x["cv"])`.
La fonction `clean_cv` attend une string, pas un dictionnaire.

## Fix

Remplacer `RunnableLambda(clean_cv)` par `RunnableLambda(lambda x: clean_cv(x["cv"]))`.