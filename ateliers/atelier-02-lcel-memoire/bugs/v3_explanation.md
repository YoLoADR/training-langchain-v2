# Bug v3 — Parser manquant dans la chaîne LCEL

## Symptôme

La chaîne LCEL retourne une string brute au lieu d'un objet MatchResult.
Le `score`, `justification` etc. ne sont pas accessibles.

## Cause

La chaîne est `prompt | llm` sans le parser à la fin. Le PydanticOutputParser
est manquant, donc la sortie reste du texte brut.

## Fix

Ajouter le parser à la fin de la chaîne : `prompt | llm | parser`
ou utiliser `get_matching_chain()` qui inclut le parser.