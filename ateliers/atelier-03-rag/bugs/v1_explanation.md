# Bug v1 — Mauvais séparateur dans CharacterTextSplitter

## Symptôme

Les CVs ne sont pas correctement chunkés. CharacterTextSplitter avec un
séparateur trop restrictif produit des chunks gigantesques qui dépassent
largement chunk_size.

## Cause

`CharacterTextSplitter` utilise `separator="\n\n"` au lieu de `separator="\n"`.
Comme les CVs ont peu de doubles sauts de ligne, le splitter ne découpe presque
jamais et produit des chunks entiers au lieu de chunks de 400 caractères.

## Fix

Remplacer `separator="\n\n"` par `separator="\n"` dans `chunk_fixed_size()`,
ou utiliser `chunk_recursive()` qui gère les séparateurs de manière hiérarchique.