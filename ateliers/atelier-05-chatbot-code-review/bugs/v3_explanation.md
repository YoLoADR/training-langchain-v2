# Bug v3 — Code chunking avec séparateurs non adaptés au code

## Symptôme

Les chunks de code coupent les fonctions et classes au milieu, rendant
le Q&A sur le code incohérent. Le retriever retourne des extraits qui
commencent ou finissent au milieu d'une fonction.

## Cause

`chunk_code_documents()` utilise les séparateurs par défaut de
`RecursiveCharacterTextSplitter` (paragraphes, lignes, mots) au lieu
de séparateurs adaptés au code Python (`\nclass `, `\ndef `).

## Fix

Spécifier des séparateurs adaptés au code dans le splitter :
```python
separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]
```
Cela préserve les blocs de fonctions et classes lors du chunking.