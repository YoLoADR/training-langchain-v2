# Bug v1 — format_response ne tronque pas (limite Telegram 4096)

## Symptôme

Le bot Telegram envoie un message trop long qui est rejeté par l'API Telegram
(limite de 4096 caractères par message).

## Cause

`format_response()` utilise un `max_length` de 10000 au lieu de 4096,
ce qui dépasse la limite Telegram. Le message n'est jamais tronqué.

## Fix

Remplacer `max_length=10000` par `max_length=4096` dans `format_response()`.
Le texte doit être tronqué et marqué avec `[...tronqué]` si trop long.