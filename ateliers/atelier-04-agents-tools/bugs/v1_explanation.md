# Bug v1 — Outil sans description (@tool decorator)

## Symptôme

L'agent ne sait pas quand utiliser l'outil `search_cvs` car il n'a pas
assez d'informations sur sa fonction. Il choisit le mauvais outil ou
n'en utilise aucun.

## Cause

Le décorateur `@tool` a été appliqué sans nom explicite et sans description
claire. L'agent ReAct se base sur la description de l'outil pour décider
quand l'utiliser.

## Fix

Ajouter un nom explicite et une description détaillée au décorateur `@tool` :
```python
@tool("search_cvs")
def search_cvs_tool(query: str) -> str:
    """Recherche de candidats dans la base de CVs via RAG FAISS.
    Utilise pour trouver qui a telle compétence ou expérience."""
    ...
```