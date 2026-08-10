# Bug v2 — GenericLoader ne charge pas les .py (glob incorrect)

## Symptôme

`load_python_files()` retourne une liste vide même quand le repo contient
des fichiers .py. Le Code-Reviewer ne peut pas indexer le code.

## Cause

Le paramètre `glob` de `GenericLoader` est `"*.txt"` au lieu de `"**/*.py"`.
Le loader cherche des fichiers .txt et ignore les fichiers Python.

## Fix

Remplacer `glob="*.txt"` par `glob="**/*.py"` dans `load_python_files()`.