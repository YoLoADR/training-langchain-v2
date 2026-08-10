# Bug v3 — build_context_prompt opt-out non géré
#
# ## Ce qui se passe
# Le patch supprime la condition `if ctx.refusal` qui gère l'opt-out en priorité absolue.
# Sans cette condition, l'opt-out n'est plus traité différemment des autres contextes.
#
# ## Pourquoi c'est un bug
# Quand un candidat dit "ne me recontactez plus", l'agent doit accepter avec respect
# et ne pas insister. Sans la section OPT-OUT, l'agent va continuer à poser des
# questions de qualification, ignorer l'opt-out, et potentiellement insister.
#
# ## Comment le réparer
# Remettre la condition `if ctx.refusal:` au début de `build_context_prompt()`.
#
# ## Vrai/Faux
# 1. L'opt-out doit être traité en priorité absolue. V/F
# 2. Sans la section OPT-OUT, l'agent continue à qualifier. V/F
# 3. Le test `test_refusal_takes_priority` vérifie que l'opt-out prend priorité. V/F