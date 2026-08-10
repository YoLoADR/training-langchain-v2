# Bug v3 — Index FAISS non chargé avant la recherche

## Symptôme

`search_cvs()` lève une `FileNotFoundError` car l'index FAISS n'existe pas
sur le disque.

## Cause

`search_cvs()` appelle `load_faiss_index()` sans vérifier que l'index a
été construit au préalable. L'utilisateur n'a pas lancé `build_faiss_index()`
avant de faire une recherche.

## Fix

Soit :
1. Construire l'index avant de chercher : `build_faiss_index(chunks, force_rebuild=True)`
2. Ou dans `search_cvs()`, vérifier si l'index existe et le construire si
   nécessaire (lazy initialization).
3. Ou passer le vectorstore explicitement : `search_cvs(query, vectorstore=store)`