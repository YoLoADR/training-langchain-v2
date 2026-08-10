# Bug v2 — Retriever avec k=0 (aucun résultat)

## Symptôme

Le retriever ne retourne aucun document. La chaîne RAG répond toujours
"Je n'ai pas cette information dans les CVs disponibles."

## Cause

Le retriever est configuré avec `k=0`, ce qui signifie qu'il ne retourne
aucun document. La chaîne RAG reçoit un contexte vide et ne peut pas répondre.

## Fix

Remplacer `k=0` par `k=4` (ou une valeur raisonnable comme 5) dans
`get_cv_retriever()`. Le paramètre k contrôle le nombre de documents
récupérés par le retriever.