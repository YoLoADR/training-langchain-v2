# Bug v1 — Skills inversés
#
# ## Ce qui se passe
# Le patch inverse les conditions de `read_skill_for_context()`.
# Avec le patch, qual_count=0 charge `phase-reformulation` au lieu de `phase-first-contact`.
#
# ## Pourquoi c'est un bug
# Le middleware beforeModel charge le mauvais SKILL.md. Le recruteur va commencer
# la conversation en mode "reformulation" (résumé des infos) au lieu de mode
# "premier contact" (recadrage + démarrage qualification).
#
# ## Comment le réparer
# Remettre les conditions dans le bon ordre :
# - qual_count >= 6 → phase-reformulation
# - qual_count > 0 → phase-qualification
# - sinon → phase-first-contact
#
# ## Vrai/Faux
# 1. Le bug est dans `read_skill_for_context()`. V/F
# 2. Le bug affecte uniquement qual_count=0. V/F
# 3. Le test `test_first_contact_skill_when_qual_count_0` détecte le bug. V/F