# Bug v2 — Mémoire non persistée (k=0)

## Symptôme

La mémoire recruteur ne retient aucun message. À chaque redémarrage,
l'historique est vide.

## Cause

`ConversationBufferWindowMemory` est initialisée avec `k=0`, ce qui
désactive la fenêtre glissante. Aucun message n'est conservé.

## Fix

Remplacer `k=0` par `k=10` (ou une valeur raisonnable) dans
`get_recruiter_memory()`.