📝 Slide 1 : Programme de la formation — 3 jours pour maîtriser LangChain et les Deep Agents

POURQUOI avoir une vue d'ensemble avant de plonger dans les détails ?

Une formation de 3 jours sur LangChain et les LLM peut rapidement donner l'impression de nager dans un océan de concepts. Ce slide est votre carte : à chaque instant, vous saurez où vous en êtes et pourquoi l'étape du moment est nécessaire pour la suivante. Chaque demi-journée construit une brique d'un projet réel.

| Jour | Titre | Ce que vous saurez faire |
|------|-------|--------------------------|
| 1 matin | Architecture et Fondamentaux des LLM | Comprendre comment "parle" à un LLM, structurer ses prompts, obtenir des réponses exploitables |
| 1 ap.-m. | Composer des chaînes avec LCEL | Enchaîner plusieurs étapes LLM de façon lisible, donner une mémoire à votre assistant |
| 2 matin | RAG — Connecter le LLM à vos données | Indexer vos documents (PDFs, JSON, CSV), poser des questions sourcées sans hallucination |
| 2 ap.-m. | Agents et Autonomie | Donner à l'IA la capacité de choisir ses outils, chercher sur le web, exécuter du code |
| 3 matin | Deep Agents — La nouvelle génération | Créer un agent qui planifie, adapte son comportement selon la phase, persiste sa mémoire |
| 3 matin | Chatbots, Code Review et Multimodal | Connecter l'agent à Telegram, suivre un pipeline en CRM, analyser du code, gérer la voix |
| 3 ap.-m. | Évaluation et Déploiement | Tracer chaque appel, mesurer la qualité, tester bout en bout, déployer avec Docker |

Fil rouge : tout au long des 3 jours, vous construisez un assistant de recrutement intelligent — du premier prompt hallucinant au Deep Agent autonome connecté à Telegram avec CRM et tests de bout en bout.

> 💡 60 % du temps est en pratique. La théorie sert à comprendre pourquoi on fait tel choix — pas à mémoriser des noms de classes.


📝 Slide 2 : Historique — de LangChain 0.1 aux Deep Agents (2022-2026)

POURQUOI retracer l'histoire avant de coder ?

Les outils que vous allez utiliser n'existent que depuis quelques années. Chacun est né en réponse à un problème concret rencontré par les développeurs. Comprendre cette succession de problèmes → solutions vous aide à comprendre pourquoi l'API a cette forme aujourd'hui, et pourquoi certains vieux tutoriels ne marchent plus.

| Année | Événement | Problème résolu |
|-------|-----------|----------------|
| 2022 oct | LangChain 0.1 (Harrison Chase) | Chaque projet LLM réécrivait sa propre glue code |
| 2022 nov | ChatGPT — 100 M utilisateurs en 2 mois | L'IA de langage devient grand public du jour au lendemain |
| 2023 | Explosion de l'écosystème (LlamaIndex, Haystack, Pinecone…) | Besoin d'indexer ses données → naissance du RAG grand public |
| 2023 | LangSmith — observabilité native | Impossible de débugger un LLM sans voir le prompt envoyé |
| 2023-2024 | LangChain 0.3 + LCEL | L'ancienne API (classes legacy) était trop verbeuse → pipe `|` déclaratif |
| 2024 | Deep Agents library | Les agents ReAct ne savaient ni planifier ni adapter leur comportement |
| 2025-2026 | Convergence LCEL + LangGraph + Deep Agents | Un seul framework couvre du prompt simple à l'agent long-horizon |

> 💡 LangChain a été lancé une semaine avant ChatGPT. Il a surfé sur la vague pour devenir le framework LLM le plus utilisé au monde. Mais sa jeunesse explique les nombreux changements d'API — d'où l'importance de suivre la version 0.3+ (LCEL).


📝 Slide 3 : Comparatifs et tendances 2026 — où en est l'écosystème ?

POURQUOI s'intéresser aux tendances avant de commencer ?

L'écosystème LLM évolue tous les 3 à 6 mois. Les tutoriels de 2023 utilisent souvent une API dépréciée. Ce slide vous donne les repères pour savoir ce qui est actuel et ce qui ne l'est plus — et orienter vos choix quand vous quitterez la formation.

**Trois frameworks, trois philosophies**

| Framework | Idée centrale | Quand le choisir |
|-----------|---------------|------------------|
| LangChain 0.3 + Deep Agents | Tout faire : prompts, chaînes, agents, RAG, déploiement | Par défaut — polyvalent, grande communauté |
| LlamaIndex | RAG d'abord : indexer et interroger ses données | Si votre projet est 90 % du RAG pur |
| Haystack | Pipelines NLP d'entreprise | Si vous venez du monde NLP traditionnel |

**Tendances 2026 à connaître**

| Tendance | En une phrase | |
|----------|---------------|---|
| LCEL déclaratif | On compose les étapes avec un pipe `|`, comme un pipeline Unix | Fini les classes verbeuses |
| Deep Agents | Les agents savent maintenant planifier et adapter leur comportement | C'est le sujet du jour 3 |
| LangSmith natif | Le tracing est automatique, sans écrire une ligne de code | Indispensable en production |
| Tests E2E | On valide le système entier en simulant un vrai utilisateur | Le standard qualité 2026 |

⚠️ **Point de vigilance** — Si vous suivez un tutoriel qui utilise `LLMChain` ou `SequentialChain`, c'est l'ancienne API. En 2026, on utilise LCEL (le pipe `|`). Les deux coexistent mais ne se mélangent pas dans un même projet.

---

Chapitre 1 : Architecture et Fondamentaux des LLM — Jour 1 matin


🎯 Objectif du chapitre

Comprendre ce qu'est un LLM et pourquoi il a tout changé en 3 ans, apprendre à lui parler correctement (prompts structurés), lui faire produire des données exploitables (JSON structuré), prendre conscience de ses limites (hallucination sur vos données privées), et découvrir le projet fil rouge que vous construirez pendant 3 jours.


📝 Slide 1 : L'explosion des LLM — pourquoi maintenant ?

POURQUOI parle-t-on autant d'IA depuis 2022 ?

Pendant des décennies, les programmes informatiques faisaient exactement ce qu'on leur disait — ni plus, ni moins. Un LLM, lui, peut rédiger un email, corriger du code, résumer un contrat, traduire un texte — sans qu'on lui écrive la moindre règle. Il a "appris" ces capacités en lisant des milliards de textes. C'est un changement de paradigme, pas une évolution.

| Avant 2022 | Après ChatGPT (nov 2022) |
|------------|--------------------------|
| L'IA de langage était réservée aux chercheurs | 100 millions d'utilisateurs en 2 mois |
| Chaque tâche nécessitait un modèle spécialisé | Un seul modèle fait tout : code, traduction, résumé, Q&A |
| Il fallait fine-tuner pour chaque usage | Le few-shot prompting remplace souvent le fine-tuning |
| Les modèles open-source étaient loin en qualité | Llama 3 et Mistral rivalisent avec les modèles fermés |

> 💡 Analogie : le LLM est à la programmation ce que le tableur a été au calcul. Avant, il fallait coder une fonction pour chaque opération. Maintenant, on "demande" en langage naturel.

⚠️ **Idée reçue** — "Plus grand = meilleur" : un modèle de 1,3 milliard de paramètres bien aligné (InstructGPT) surpasse un modèle de 175 milliards non aligné (GPT-3). La façon dont on entraîne compte autant que la taille.


📝 Slide 2 : Comment "parler" à un LLM ? — Prompts et messages

POURQUOI la façon de poser la question change-t-elle tout ?

Un LLM ne "comprend" pas votre intention — il prédit le prochain token le plus probable. La façon dont vous formulez votre question (le "prompt") détermine donc la qualité de la réponse. Un prompt flou donne une réponse floue. Un prompt structuré avec un rôle, un contexte et une consigne claire donne une réponse exploitable.

| Style de prompt | Exemple | Résultat |
|----------------|---------|----------|
| Flou | "Parle-moi de Docker" | Article générique de blog |
| Avec rôle | "Tu es expert DevOps. Explique Docker à un junior" | Pédagogique, structuré |
| Avec consigne de format | "Réponds en JSON avec les clés 'concept' et 'exemple'" | Données exploitables |
| Avec contexte | "Voici le CV de Marie… Voici l'offre… Évalue la correspondance" | Analyse personnalisée |

Dans LangChain, on ne tape pas le prompt à la main à chaque appel. On crée un **Prompt Template** — un modèle avec des "trous" qu'on remplit dynamiquement : *"Évalue la correspondance entre ce CV : {cv_text} et cette offre : {offer_text}"*. Le template est validé, réutilisable, et s'intègre dans les chaînes.

> 💡 La règle d'or du prompting : **Rôle + Contexte + Consigne + Format**. Si vous oubliez un de ces 4 éléments, la qualité se dégrade. Un bon prompt fait 80 % du travail — le LLM fait les 20 % restants.


📝 Slide 3 : Prompt Templates — ne plus jamais écrire un prompt à la main

POURQUOI utiliser un template plutôt qu'une simple f-string ?

Un f-string concatène les variables à la volée mais ne valide rien, ne se réutilise pas proprement, et ne s'intègre pas dans les chaînes LangChain. Un `PromptTemplate` valide les variables à la compilation, supporte l'application partielle, et se branche nativement dans le pipeline. Pour un script jetable, l'un ou l'autre suffit. Pour un projet qui vit, le template devient indispensable.

| Type de template | Quand l'utiliser | Exemple |
|------------------|------------------|---------|
| `PromptTemplate` | Un simple texte avec variables | "Résume ce document : {text}" |
| `ChatPromptTemplate` | Vous voulez des rôles (système, utilisateur, assistant) | Système : "Tu es expert" + Human : "{question}" |
| `MessagesPlaceholder` | L'historique de conversation est variable | La mémoire grandit au fil des messages |

Le `ChatPromptTemplate` est le standard en 2026 : il permet de donner un rôle au modèle (message "system"), de poser la question (message "human"), et d'injecter l'historique (placeholder). C'est l'équivalent d'une fiche de briefing avant un entretien.

> 💡 Think of it as a form: le template est le formulaire, les variables sont les champs à remplir, le LLM est la personne qui lit le formulaire rempli et répond. Vous ne réécrivez pas le formulaire à chaque fois — vous remplissez juste les champs.


📝 Slide 4 : Few-shot — montrer des exemples plutôt qu'expliquer

POURQUOI montrer 2-3 exemples vaut-il mieux qu'une longue explication ?

Les LLM sont excellents pour imiter des patterns. Plutôt que d'expliquer en 5 phrases ce que vous attendez, montrez 2-3 exemples de "question → réponse attendue". Le modèle reproduira le pattern. C'est le few-shot prompting, et c'est la technique la plus efficace pour améliorer la qualité sans toucher au modèle.

| Approche | Prompt | Qualité |
|----------|--------|---------|
| Zero-shot | "Évalue ce CV pour cette offre" | Correct mais variable |
| Few-shot statique | 3 exemples fixes + la question | Bonne, mais consomme des tokens |
| Few-shot dynamique | 3 exemples choisis par similarité avec la question | Excellente, tokens optimisés |

LangChain va plus loin avec les **ExampleSelectors** : au lieu de mettre les mêmes 3 exemples partout, le selector choisit dynamiquement les exemples les plus pertinents pour la requête courante, en calculant la similarité sémantique. Le prompt reste court et ciblé.

> 💡 Analogie : un few-shot statique, c'est donner les mêmes 3 exemples à tous vos candidats. Un few-shot dynamique, c'est donner les 3 exemples les plus proches de leur situation. Le deuxième est évidemment plus efficace.


📝 Slide 5 : Output Parsers — transformer du texte en données

POURQUOI le LLM retourne-t-il du texte libre alors qu'on veut du JSON ?

Un LLM génère du texte — c'est sa nature. Mais une application a besoin de données structurées : un score, une liste de compétences, un objet typé. Sans parser, on se retrouve à écrire des expressions régulières fragiles pour extraire l'information du texte. Un Output Parser force le LLM à produire une sortie conforme à un schéma.

| Parser | Ce qu'il force | Usage typique |
|--------|---------------|---------------|
| `PydanticOutputParser` | Un objet Python typé et validé | Extraire un CV en objet `CVInfo` (nom, email, skills, expérience) |
| `CommaSeparatedListOutputParser` | Une liste Python | Extraire les compétences d'un texte |
| `JsonOutputParser` | Un dictionnaire JSON | Sortie générique sans schéma strict |

Le parser génère automatiquement des instructions de format dans le prompt — le LLM sait qu'il doit répondre en JSON. C'est transparent pour le développeur : le prompt, le modèle et le parser s'enchaînent comme un pipeline.

> 💡 Le pattern le plus courant en LangChain : **Template → Modèle → Parser**. Vous donnez une question structurée, le modèle répond, le parser transforme la réponse en objet Python. Vous n'avez plus à toucher au texte libre.


📝 Slide 6 : Le grand écosystème LLM — qui fait quoi ?

POURQUOI y a-t-il autant d'outils et comment s'y retrouver ?

L'écosystème LLM Python compte des centaines de bibliothèques. Sans carte mentale, on installe des outils redondants et on résout les mauvais problèmes avec les mauvais outils. Voici les 4 couches fonctionnelles à retenir :

| Couche | À quoi ça sert | Outils représentatifs |
|--------|---------------|----------------------|
| 1. Modèles | Accéder au LLM (local ou cloud) | Anthropic API, OpenAI, Ollama (local), HuggingFace |
| 2. Orchestration | Enchaîner les appels, gérer la mémoire, les agents | **LangChain**, LlamaIndex, Haystack |
| 3. Vector stores | Stocker et rechercher dans vos documents | FAISS (local), ChromaDB (persistant), Pinecone (cloud) |
| 4. Observabilité | Tracer, débugger, mesurer | LangSmith, Langfuse, MLflow |

Pendant cette formation, on utilise LangChain (couche 2) car il couvre tout : prompts, chaînes, RAG, agents, deep agents, observabilité. On ne bricole pas avec un outil par couche — on reste dans un framework cohérent.

> 💡 La règle : choisir l'outil le plus simple qui résout le problème. Un appel API direct surpasse LangChain pour un usage ponctuel. LangChain devient pertinent dès qu'il y a au moins deux étapes à composer.


📝 Slide 7 : Modèles open-source vs fermés — quelle conséquence sur votre projet ?

POURQUOI le choix du modèle engage toute l'architecture ?

Choisir entre un modèle fermé (Claude, GPT-4o) et un modèle open-source (Mistral, Llama 3) n'est pas une question de goût. C'est une décision qui impacte le coût, la confidentialité, la maintenance et la souveraineté de votre projet pour des années.

| Critère | Open-source (Mistral, Llama 3) | Fermé (Claude, GPT-4o) |
|---------|-------------------------------|------------------------|
| Confidentialité | Vos données restent chez vous | Données envoyées chez le provider |
| Coût | Hébergement propre (fixe) | $0,01 à $0,06 par 1 000 tokens |
| Performance | Très proche en 2026 | Légèrement supérieure |
| Mise en place | Infra à gérer (GPU, Ollama) | Une clé API, c'est tout |
| Hors-ligne | Oui | Non |

L'avantage de LangChain : le code applicatif ne change pas quand on switch de modèle. On change une variable d'environnement, et le reste du pipeline continue de fonctionner. C'est le principal bénéfice de l'abstraction.

⚠️ **Piège classique** — Choisir open-source par principe sans GPU disponible : un modèle 7B sur CPU peut prendre 20 à 60 secondes par réponse. C'est inutilisable en production. Toujours estimer l'infrastructure avant de choisir.


📝 Slide 8 : L'hallucination — pourquoi le LLM invente avec assurance

POURQUOI un LLM donne-t-il des réponses fausses avec autant de confiance ?

Un LLM ne "sait" rien. Il prédit le token le plus probable selon les patterns statistiques de son entraînement. Si vous lui demandez "Marie Dubois maîtrise-t-elle Docker ?", il ne va pas dire "je ne sais pas" — il va prédire une réponse plausible ("Oui, Marie a une bonne maîtrise de Docker") même s'il n'a jamais vu le CV de Marie. C'est l'hallucination, et elle est systémique.

| Question sur vos données privées | LLM seul (sans vos données) | LLM + RAG (avec vos données indexées) |
|----------------------------------|------------------------------|--------------------------------------|
| "Quel est le niveau de Docker de Marie ?" | "Niveau avancé" (inventé, plausible) | "Niveau avancé — source : cv_003, page 2" |
| "Karim a-t-il travaillé chez AWS ?" | "Oui, 2019-2021" (inventé) | "Non — il était chez OVH 2020-2023, source : cv_007" |
| "Quelle école a fait Sophie ?" | "Polytechnique" (inventé) | "Centrale Lyon — source : cv_012, page 1" |

Le constat est clair : sans vos données, le LLM hallucine dans 80 à 100 % des cas sur des informations privées. C'est ce constat qui motive le RAG (Jour 2) — indexer vos documents pour que le LLM réponde à partir de faits réels, avec des sources citées.

> 💡 Le LLM ne "ment" pas — il n'a pas de notion de vérité. "Marie Dubois" est un nom français, "Docker" est une compétence tech : la combinaison est statistiquement probable. Le LLM fait son travail (prédire), mais il prédit à partir de rien.


📝 Slide 9 : 5 idées reçues à démystifier avant de coder

POURQUOI ces idées reçues génèrent-elles des erreurs de conception coûteuses ?

Ces 5 idées reviennent systématiquement dans les projets. Chacune conduit à des décisions d'architecture défectueuses ou à des attentes irréalistes envers les modèles. Les connaître avant de coder vous fait gagner des semaines.

| Idée reçue | Réalité |
|-----------|---------|
| "Plus grand = meilleur" | Un modèle de 1,3 B bien aligné surpasse un modèle de 175 B non aligné |
| "Les LLM comprennent le langage" | Non — ils prédisent le token suivant. Pas de modèle du monde. |
| "Un bon prompt suffit" | Sans vos données indexées, le LLM invente 80-100 % sur vos infos privées |
| "Les LLM sont déterministes" | Même à temperature=0, les APIs peuvent varier légèrement |
| "Les hallucinations sont rares" | 8 à 42 % sans RAG sur des domaines techniques — 80-100 % sur vos données privées |

⚠️ **Risque réel** — Exposer un LLM en production sans mesurer l'hallucination : plusieurs entreprises ont subi des incidents publics (réponses incorrectes présentées avec assurance) dont le coût réputationnel a dépassé le coût de développement.


📝 Slide 10 : Le projet fil rouge — un assistant de recrutement intelligent

POURQUOI construire une vraie application de bout en bout plutôt que des snippets isolés ?

Les snippets isolés enseignent un concept mais ne montrent pas comment les pièces s'assemblent — ni quels pièges surviennent à l'intégration. Pendant 3 jours, vous construisez un assistant de recrutement : un système qui parle aux candidats, lit leurs CVs, évalue leur correspondance aux offres, et suit le pipeline de recrutement.

| Brique | Ce qu'elle fait | Construit pendant |
|--------|----------------|-------------------|
| Prompts + Parsers | Structurer les échanges avec le LLM | Jour 1 matin |
| Chaînes LCEL + Mémoire | Enchaîner les étapes, garder le contexte | Jour 1 ap.-m. |
| RAG sur CVs et offres | Répondre à partir des vrais documents, avec sources | Jour 2 matin |
| Agent ReAct | Choisir ses outils (recherche, web, code) | Jour 2 ap.-m. |
| Deep Agent | Planifier, adapter son comportement selon la phase | Jour 3 matin |
| Telegram + CRM | Parler aux candidats, suivre le pipeline | Jour 3 matin |
| Tests + Déploiement | Prouver que ça marche, déployer avec Docker | Jour 3 ap.-m. |

Architecture cible : Candidat → Telegram → Agent intelligent → RAG + Outils → Réponse + Suivi CRM

> 💡 Chaque demi-journée construit une couche. À la fin du Jour 3, vous avez un système complet de bout en bout — du premier prompt à un agent autonome déployé en production.


🎓 Ce que vous devez retenir — Chapitre 1

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| LLM = prédiction de token | Comprendre ça explique l'hallucination et la sensibilité au prompt |
| Rôle + Contexte + Consigne + Format | La structure d'un bon prompt — 80 % du travail |
| PromptTemplate | Ne plus jamais écrire un prompt à la main — valider, réutiliser, composer |
| Few-shot dynamique | Montrer 2-3 exemples pertinents > expliquer en 5 phrases |
| Output Parser | Transformer du texte libre en données exploitables (JSON, objets typés) |
| 4 couches de l'écosystème | Modèles / Orchestration / Vector stores / Observabilité — choisir le bon outil |
| Open-source vs fermé | Décision d'architecture : coût, confidentialité, maintenance |
| Hallucination 80-100 % | Sans vos données, le LLM invente — le RAG est indispensable |
| 5 idées reçues | Les connaître prévient 80 % des erreurs de conception |
| Projet fil rouge | 7 briques, du premier prompt à l'agent déployé en production |


➡️ Prochain chapitre

Vous savez maintenant parler à un LLM et structurer ses réponses. On passe à l'orchestration : pourquoi utiliser un framework plutôt que des appels API directs, comment enchaîner plusieurs étapes de façon lisible avec le pipe `|`, et comment donner une mémoire à votre assistant pour qu'il se souvienne de la conversation.

---

Chapitre 2 : Composer des chaînes avec LCEL — Jour 1 après-midi


🎯 Objectif du chapitre

Comprendre pourquoi un framework d'orchestration devient indispensable dès qu'on a 2+ étapes, apprendre à composer des pipelines avec le pipe `|` (LCEL), donner une mémoire à votre assistant pour qu'il se souvienne de la conversation entre deux sessions, et paralléliser plusieurs traitements.


📝 Slide 1 : Pourquoi un framework ? Appels API directs vs orchestration

POURQUOI ne pas simplement appeler l'API d'Anthropic ou d'Ollama directement ?

Pour un appel unique sans contexte, l'API directe est parfaite. Mais dès qu'on ajoute une deuxième étape (récupérer des documents, garder la mémoire, appeler un outil, changer de modèle), le code "artisanal" devient spaghetti. Les frameworks d'orchestration existent pour résoudre ce problème de composition.

| Critère | Appel API direct | Framework (LangChain) |
|---------|------------------|----------------------|
| Changer de modèle (Claude → Mistral) | Réécrire le code d'appel | Changer une variable d'environnement |
| Enchaîner 3 étapes | 200 lignes de glue code | 3 lignes avec le pipe `|` |
| Mémoire conversationnelle | À coder from scratch | Intégrée, prête à l'emploi |
| Traçabilité des appels | Logs custom à écrire | Automatique via LangSmith |
| Gestion d'erreurs | try/except partout | Fallback natif |

⚠️ **Quand NE PAS utiliser LangChain** — Pour un simple appel LLM sans chaîne ni mémoire : on ajoute une dépendance lourde pour aucun bénéfice. La règle : un framework se justifie dès qu'il y a au moins deux étapes à composer.


📝 Slide 2 : LCEL — le pipe `|` qui change tout

POURQUOI LCEL a-t-il remplacé l'ancienne API LangChain ?

Avant LCEL, LangChain utilisait des classes comme `LLMChain`, `SequentialChain`, `ConversationChain` — verbeuses, non streamables, difficiles à debugger. LCEL (LangChain Expression Language) introduit le pipe `|` : chaque étape est un "Runnable", et on les enchaîne comme un pipeline Unix. Le code devient lisible, testable, et parallélisable.

| Avant (legacy, déprécié) | Après (LCEL, moderne) |
|--------------------------|----------------------|
| `LLMChain(llm=model, prompt=prompt)` | `prompt \| model` |
| `SequentialChain(chains=[c1, c2])` | `c1 \| c2` |
| 15 lignes pour une chaîne simple | 1 ligne : `prompt \| model \| parser` |

L'idée : chaque composant (prompt, modèle, parser, outil custom) parle la même langue. On les branche avec `|` comme on branche des tuyaux. Ce qui sort de l'un entre dans le suivant.

> 💡 Analogie : LCEL, c'est comme un pipeline Unix (`cat file | grep pattern | sort | head`). Chaque étape prend l'entrée de la précédente, fait son travail, et passe le résultat à la suivante. Pas de glue code, pas de variable intermédiaire.


📝 Slide 3 : Les briques LCEL — que passe-t-on dans le pipe ?

POURQUOI parler de "Runnable" plutôt que de "composant" ?

Dans LCEL, tout est un `Runnable` — un objet avec une interface unifiée (`.invoke()`, `.batch()`, `.stream()`). Que ce soit un prompt, un modèle, un parser ou une fonction Python, tous parlent la même langue. C'est ce qui permet de les brancher indifféremment avec le pipe.

| Brique | Rôle en une phrase | Analogie |
|--------|-------------------|----------|
| `ChatPromptTemplate` | Prépare la question avec des variables | Un formulaire à remplir |
| `ChatAnthropic` / `ChatOpenAI` | Envoie la question au LLM, reçoit la réponse | L'expert qui répond |
| `PydanticOutputParser` | Transforme la réponse en objet typé | Le secrétaire qui met en forme |
| `RunnablePassthrough` | Transmet l'entrée telle quelle | Un simple tuyau |
| `RunnableLambda` | Enveloppe une fonction Python quelconque | Un adaptateur custom |
| `RunnableParallel` | Lance plusieurs Runnables en parallèle | Un embranchement qui se rejoint |

> 💡 Pas besoin de tout mémoriser maintenant. Le pattern le plus courant est `prompt | model | parser` — on l'utilisera toute la formation. Les autres briques s'ajoutent quand le besoin apparaît.


📝 Slide 4 : Enrichir le pipeline — garder des variables en route

POURQUOI a-t-on parfois besoin de garder des données à côté du pipeline ?

Dans un pipeline simple (`prompt | model | parser`), l'entrée est un dictionnaire, et chaque étape ne reçoit que la sortie de la précédente. Mais en pratique, on veut souvent enrichir le contexte au fil du pipeline : ajouter l'offre d'emploi à côté du CV, injecter l'historique de conversation, etc. C'est le rôle de `.assign()`.

| Pattern | Ce qu'il fait | Quand l'utiliser |
|---------|--------------|-----------------|
| `RunnablePassthrough` | Transmet l'entrée telle quelle | Conserver le contexte original |
| `.assign(offer=...)` | Ajoute une clé au dictionnaire en cours | Enrichir le contexte avant le prompt |
| `RunnableLambda(clean)` | Applique une fonction Python custom | Nettoyer, tronquer, transformer |

En pratique, le pipeline ressemble à : `données → .assign() → .assign() → prompt → model → parser`. Chaque `.assign()` ajoute une variable au contexte, le prompt utilise toutes les variables, le modèle répond, le parser structure.

> 💡 Think of it as assembling a dossier : vous commencez avec le CV du candidat, vous ajoutez l'offre d'emploi, vous ajoutez l'historique des échanges, puis vous soumettez le dossier complet au LLM. `.assign()` ajoute une pièce au dossier.


📝 Slide 5 : Paralléliser et router — quand le pipeline se divise

POURQUOI vouloir faire plusieurs choses en même temps ?

Certaines étapes sont indépendantes : extraire les infos du CV et matcher l'offre n'ont pas besoin de s'attendre. Les lancer en parallèle divise la latence par 2. D'autres fois, on veut router : si le score est > 0.8, on shortliste ; si < 0.3, on rejette. Le pipeline s'adapte selon le résultat.

| Pattern | Ce qu'il fait | Gain |
|---------|--------------|------|
| `RunnableParallel` | Lance N branches en parallèle | Latence divisée par N |
| `RunnableBranch` | Route vers la bonne branche selon une condition | Adaptation dynamique |
| `.with_fallbacks()` | Si une étape échoue, bascule vers un plan B | Robustesse |

> 💡 Le parallélisme est gratuit en LCEL : `RunnableParallel(extraction=..., matching=...)` lance les deux branches en même temps. Sans LCEL, il faudrait écrire `asyncio.gather()` à la main — avec gestion d'erreurs, de timeouts, de rate limiting. LCEL gère tout ça nativement.


📝 Slide 6 : La mémoire conversationnelle — pourquoi le LLM oublie

POURQUOI un LLM oublie-t-il ce qu'on lui a dit 2 messages plus tôt ?

Un LLM est sans état : chaque appel est indépendant. Il ne "se souvient" de rien entre deux appels. Pour avoir une conversation, il faut donc renvoyer l'historique à chaque appel. Mais si la conversation fait 50 messages, le prompt explose en tokens — et en coût. C'est là qu'interviennent les stratégies de mémoire.

| Stratégie | Principe | Quand l'utiliser |
|-----------|----------|------------------|
| Tout garder (Buffer) | Renvoyer tout l'historique à chaque appel | Conversations courtes (< 10 messages) |
| Fenêtre glissante (Window k=10) | Ne garder que les k derniers échanges | La plupart des cas — bon compromis |
| Résumé automatique (Summary) | Le LLM résume l'historique périodiquement | Conversations longues (> 50 messages) |

> 💡 Analogie : la mémoire fenêtre, c'est comme une conversation à un cocktail — vous vous souvenez des 10 dernières phrases, mais pas du début de la soirée. La mémoire résumé, c'est un journal intime — vous gardez l'essentiel, pas chaque mot.


📝 Slide 7 : Persister la mémoire — survivre au redémarrage

POURQUOI sauvegarder la mémoire sur disque ?

Un assistant qui oublie tout au redémarrage est inutilisable en production. Le recruteur qui ferme son ordinateur le soir doit retrouver le contexte de ses entretiens le lendemain matin. LangChain permet de sérialiser la mémoire en JSON et de la recharger au prochain démarrage.

| Étape | Ce qu'on fait |
|------|--------------|
| Pendant la conversation | La mémoire vit en RAM (Window k=10) |
| À la fin de la session | On sauvegarde sur disque (JSON) |
| Au prochain démarrage | On recharge la mémoire depuis le disque |

⚠️ **Piège fréquent** — Utiliser un chemin relatif (`memory.json`) : selon le répertoire d'où l'app est lancée, le fichier n'est pas retrouvé. Toujours utiliser un chemin absolu (`Path(__file__).parent / "memory.json"`).


📝 Slide 8 : .batch() — traiter plusieurs entrées en parallèle

POURQUOI .batch() surpasse-t-il une boucle de .invoke() ?

Traiter 30 CVs un par un envoie 30 requêtes API l'une après l'autre — latence = 30 × temps d'un appel. Avec `.batch()`, LangChain envoie les 30 requêtes en parallèle — latence ≈ 3 × temps d'un appel. Sur un batch de 30, le gain est de 10×.

| Méthode | 30 éléments | Implémentation |
|---------|-------------|----------------|
| Boucle `.invoke()` | 30 × latence ≈ 90s | `for cv in cvs: chain.invoke(cv)` |
| `.batch()` | ~3 × latence ≈ 9s | `chain.batch(cvs)` |

> 💡 `.batch()` gère automatiquement le rate limiting et les retries. Pas besoin de coder `asyncio.gather()` manuellement — LangChain fait le travail.


📝 Slide 9 : Erreurs fréquentes en LCEL

POURQUOI les débutants en LCEL tombent-ils toujours sur les mêmes pièges ?

LCEL est élégant mais a ses règles. Ignorer l'une d'elles conduit à des erreurs obscures. Voici les 5 pièges les plus fréquents :

| Piège | Symptôme | Solution |
|------|----------|----------|
| Fonction Python brute dans le pipe | `TypeError: not a Runnable` | Envelopper avec `RunnableLambda()` |
| Mélanger LCEL et classes legacy | Comportement inattendu | Tout faire en LCEL (pipe `|`) |
| `.batch()` avec un dict au lieu d'une liste | Erreur d'unpacking | Passer une **liste** de dicts |
| Output Parser échoue | `OutputParserException` | `max_tokens` trop faible — JSON tronqué |
| Mémoire perdue au redémarrage | Pas de contexte au redémarrage | Sauvegarder en JSON avec chemin absolu |


📝 Slide 10 : Le chaîne complète — du prompt au résultat structuré

POURQUOI visualiser le pipeline complet avant de coder évite-t-il des refactorings ?

Un pipeline LCEL est un assemblage de briques. Si on comprend le rôle de chacune avant de coder, on évite 80 % des erreurs d'architecture. Voici le pipeline type que vous construirez pendant cette demi-journée :

| Étape | Brique | Rôle |
|------|--------|------|
| 1. Préparation | `.assign()` | Enrichir le contexte (CV + offre) |
| 2. Prompt | `ChatPromptTemplate` | Structurer la question (rôle + contexte + consigne) |
| 3. Modèle | `ChatAnthropic` | Générer la réponse |
| 4. Parsing | `PydanticOutputParser` | Transformer en objet typé (score, justification) |
| 5. Mémoire | `WindowMemory(k=10)` | Garder les 10 derniers échanges |

Le tout s'écrit en une seule expression : `contexte | prompt | model | parser`. Et avec `.batch()`, on traite 30 CVs en parallèle. Et avec la mémoire, l'assistant se souvient de la conversation entre deux sessions.

> 💡 Ce pipeline est le squelette de 90 % des projets LLM. On le réutilisera au Jour 2 (RAG) et au Jour 3 (agents). Le comprendre maintenant, c'est gagner du temps sur tout le reste de la formation.


🎓 Ce que vous devez retenir — Chapitre 2

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| Framework = accélérateur | LangChain surpasse l'API directe dès qu'il y a 2+ étapes |
| LCEL (pipe `\|`) | Syntaxe déclarative — `prompt \| model \| parser` en 1 ligne |
| Tout est Runnable | Prompt, modèle, parser, fonction custom — même interface |
| `.assign()` | Enrichir le contexte au fil du pipeline |
| `RunnableParallel` | Divise la latence par N sur les étapes indépendantes |
| `RunnableBranch` | Route dynamique selon une condition (score > 0.8 → shortlist) |
| Mémoire Window (k=10) | Le compromis par défaut — 10 derniers échanges |
| Mémoire Summary | Pour les conversations longues — résumé auto par LLM |
| Persistance JSON | L'assistant survit au redémarrage |
| `.batch()` | 30 CVs en 9s au lieu de 90s — parallélisme gratuit |


➡️ Prochain chapitre

Vous savez composer des chaînes et donner une mémoire à votre assistant. Mais il hallucine toujours sur vos données privées. On passe maintenant au RAG : indexer vos documents (PDFs, JSON, CSV), retrouver les bons passages automatiquement, et répondre avec des sources citées — 0 % d'hallucination.

---

Chapitre 3 : RAG — Connecter le LLM à vos données — Jour 2 matin


🎯 Objectif du chapitre

Comprendre pourquoi un LLM hallucine sur vos données privées et comment le RAG résout ce problème, maîtriser les 5 étapes d'un pipeline RAG (chargement, découpage, embedding, stockage, récupération + génération), choisir la bonne stratégie de découpage selon le type de document, et mesurer la qualité du retrieval avec Recall@k.


📝 Slide 1 : Le problème — le LLM ne connaît pas vos documents

POURQUOI le LLM invente-t-il quand on lui parle de vos données ?

Un LLM est entraîné sur un corpus public (Internet, livres, code). Il ne connaît ni vos CVs, ni vos contrats, ni vos notices produits, ni vos offres d'emploi. Quand vous lui posez une question sur ces documents, il n'a deux options : dire "je ne sais pas" (rare) ou inventer une réponse plausible (fréquent). C'est l'hallucination, et elle est systémique.

| Sans RAG | Avec RAG |
|----------|----------|
| Le LLM ne connaît pas vos documents | Vos documents sont indexés et retrouvés à la demande |
| Hallucination 80-100 % sur vos données privées | 0 % d'hallucination — le LLM répond à partir des sources |
| Pas de citation possible | Chaque réponse cite sa source (document, page) |
| Mise à jour = réentraîner le modèle (irréaliste) | Mise à jour = réindexer les documents (minutes) |

> 💡 RAG = donner au LLM une bibliothèque à consulter avant de répondre. Le modèle reste gelé — seule la bibliothèque évolue. C'est l'idée du papier fondateur : Lewis et al., "RAG for Knowledge-Intensive NLP Tasks", Meta AI, 2020.


📝 Slide 2 : Les 5 étapes d'un RAG — le flux de bout en bout

POURQUOI comprendre chaque étape avant de copier un tutoriel ?

Les tutoriels RAG donnent l'impression que "ça marche tout seul". En production, les problèmes viennent d'une étape mal configurée — et sans comprendre le rôle de chaque composant, on ne sait pas où chercher. Les 5 étapes se divisent en deux phases très différentes.

| Étape | Ce que ça fait | Phase | Fréquence |
|------|---------------|-------|----------|
| 1. Chargement | Lire vos documents (PDFs, JSON, CSV, web) | Indexation | Une fois |
| 2. Découpage | Diviser en petits segments cohérents | Indexation | Une fois |
| 3. Embedding | Convertir chaque segment en vecteur numérique | Indexation | Une fois |
| 4. Stockage | Indexer les vecteurs pour recherche rapide | Indexation | Une fois |
| 5. Récupération + Génération | Retrouver les bons segments → répondre | Inférence | À chaque question |

> 💡 Les étapes 1 à 4 sont un coût fixe (une fois pour toutes). L'étape 5 est le coût variable (à chaque question). Optimiser 1-4 améliore la qualité ; optimiser 5 réduit la latence.


📝 Slide 3 : Chargement — lire vos documents dans LangChain

POURQUOI LangChain fournit-il des "loaders" spécifiques par format ?

Chaque format a une structure différente : un PDF a des pages, un JSON a des clés, un CSV a des colonnes. Les Document Loaders extraient le contenu ET les métadonnées (source, numéro de page, date) dans un format unifié. Sans loader adapté, on perd les métadonnées qui sont critiques pour citer les sources.

| Loader | Format | Métadonnées extraites |
|-------|--------|----------------------|
| `PyMuPDFLoader` | PDF | page, source |
| `JSONLoader` | JSON | source, structure |
| `CSVLoader` | CSV | source, ligne |
| `GenericLoader` | Code (.py, .js) | file_path, fonction |

⚠️ **Piège connu** — PyMuPDF s'installe avec `pip install pymupdf` mais s'importe avec `import fitz`. Ce nom hérité du projet original est une source de confusion universelle.


📝 Slide 4 : Découpage — l'étape qui fait 80 % de la qualité

POURQUOI la façon de découper détermine-t-elle 80 % de la qualité du RAG ?

Le LLM ne "lit" jamais vos documents entiers. Il reçoit uniquement les petits segments (chunks) que le moteur de recherche a jugés pertinents. Si un chunk coupe une compétence au milieu d'une phrase, le LLM répond à partir d'un contexte incomplet. Si un chunk est trop grand, l'information pertinente est noyée dans du bruit.

| Stratégie | Principe | Idéale pour |
|-----------|---------|-------------|
| Taille fixe | N caractères, overlap M | Données non structurées (logs, CSV) |
| Recursive (recommandée) | Séparateurs hiérarchiques (paragraphe → phrase → mot) | PDFs structurés (CVs, contrats, offres) |
| Sémantique | Découpe aux ruptures de sens | Corpus premium, petits volumes |

**Bonnes pratiques** : 400-512 tokens par chunk, 10-20 % d'overlap, toujours ajouter les métadonnées (source, page), et inspecter visuellement 20 chunks avant d'indexer.

> 💡 Analogie : si vous demandez à quelqu'un de trouver une information dans un livre, la façon dont le livre est découpé en chapitres et paragraphes détermine s'il trouve l'info vite ou jamais. Le chunking, c'est la table des matières de votre RAG.


📝 Slide 5 : Embeddings — transformer du texte en vecteurs

POURQUOI la recherche sémantique surpasse-t-elle la recherche par mots-clés ?

Une recherche par mots-clés échoue sur les synonymes : "développeur" ne matche pas "ingénieur logiciel", "Python" ne matche pas "langage de scripting". Les embeddings convertissent le texte en vecteurs où la distance représente la proximité de sens — pas de mots. "Développeur" et "ingénieur logiciel" sont proches en embedding, même s'ils ne partagent aucun mot.

| Modèle d'embedding | Dimension | Multilingue | Usage |
|---------------------|-----------|-------------|-------|
| paraphrase-multilingual-MiniLM | 384 | ✓ | CPU, multilingue — bon pour débuter |
| BAAI/bge-base-en-v1.5 | 768 | ✗ | Projets anglophones performance |
| text-embedding-ada-002 | 1 536 | ✗ | Production OpenAI (payant) |

> 💡 Un embedding, c'est une coordonnée GPS pour le sens d'un texte. Deux textes proches en sens sont proches en coordonnées. La recherche sémantique calcule la distance entre la question et tous les chunks, et retourne les plus proches.


📝 Slide 6 : Vector stores — où stocker les vecteurs

POURQUOI ne pas stocker les vecteurs dans un simple fichier ?

Pour 100 chunks, un fichier suffit. Pour 100 000 chunks, la recherche brute (calculer la distance avec chaque vecteur) prend des secondes. Les vector stores utilisent des structures d'indexation spécialisées (HNSW, IVF) qui permettent une recherche en quelques millisecondes même sur des millions de vecteurs.

| Vector store | Type | Persistance | Quand l'utiliser |
|-------------|------|-------------|------------------|
| FAISS | Bibliothèque in-memory | Sauvegarde manuelle | Recherche rapide, données qui tiennent en RAM |
| ChromaDB | Base locale persistante | Automatique | Persistance entre sessions + filtrage par métadonnées |
| Pinecone | SaaS cloud | Automatique (cloud) | Production à grande échelle (millions de vecteurs) |

En pratique, beaucoup de projets utilisent **les deux** : FAISS pour la vitesse de recherche et ChromaDB pour la persistance et le filtrage (par source, par date, par catégorie).

> 💡 Le filtrage par métadonnées est un avantage majeur de ChromaDB : "cherche dans les CVs uniquement" ou "cherche dans les offres de plus de 50K€". FAISS ne sait pas faire ça nativement.


📝 Slide 7 : Retrieval — retrouver les bons passages

POURQUOI la recherche par similarité seule ne suffit pas toujours ?

La similarité cosinus retourne les k chunks les plus proches du vecteur question — mais ils peuvent être redondants (le même passage répété en légèrement différent). MMR (Maximal Marginal Relevance) équilibre pertinence et diversité : chaque chunk retourné doit être pertinent ET différent des précédents.

| Méthode | Principe | Quand |
|---------|----------|-------|
| Similarity | Top-k par distance cosinus | Simple, rapide |
| MMR | Pertinence + diversité | Éviter les résultats redondants |
| Score threshold | Filtrer par score minimum | Éliminer le bruit |

> 💡 MMR, c'est comme un buffet : au lieu de prendre 5 fois le même plat (les 5 chunks les plus similaires), vous prenez 5 plats différents mais tous bons. La diversité enrichit le contexte donné au LLM.


📝 Slide 8 : Comment on sait si le RAG est bon ? — Recall@k

POURQUOI "ça marche" n'est pas une métrique ?

Sans métrique objective, on ne peut pas comparer deux configurations de chunking, choisir entre deux modèles d'embedding, ou détecter une régression. La métrique la plus intuitive est le **Recall@k** : sur 10 questions, combien de fois le bon document est-il dans les k premiers résultats ?

| Métrique | Question qu'elle répond | Cible |
|----------|------------------------|-------|
| Recall@5 | Le bon document est-il dans le top 5 ? | ≥ 80 % |
| MRR | À quelle position est le bon document en moyenne ? | ≥ 60 % |
| Taux d'hallucination | Le LLM invente-t-il malgré le contexte ? | 0 % |

> 💡 Le Recall@k, c'est comme demander à un recruteur : "sur 10 candidats, combien de fois le bon candidat était dans les 5 que tu m'as proposés ?" Si c'est 8 fois sur 10, le Recall@5 = 0,80. En dessous de 0,70, le RAG est mauvais et il faut revoir le chunking ou l'embedding.


📝 Slide 9 : Anti-patterns — les 5 erreurs qui tuent un RAG

POURQUOI la majorité des projets RAG échouent-ils sur des détails ?

Le RAG est simple à prototyper (50 lignes) mais difficile à mettre en production. Ces 5 erreurs représentent 80 % des problèmes rencontrés dans les projets réels.

| Anti-pattern | Symptôme | Correction |
|-------------|---------------------|------------|
| Chunks trop petits (50 tokens) | Compétences coupées, contexte incomplet | 400-512 tokens |
| Pas d'overlap | Transitions perdues entre chunks | 10-20 % d'overlap |
| Pas de métadonnées | Impossible de citer la source | Ajouter source + page sur chaque chunk |
| Similarity sans MMR | Résultats redondants | Activer MMR (lambda_mult=0.5) |
| Pas d'évaluation | On ne sait pas si c'est bon ou pas | Mesurer Recall@k sur un jeu de test |

> 💡 Le piège le plus sournois : ne pas évaluer. On a l'impression que "ça marche" parce qu'on teste sur des questions dont on connaît la réponse — c'est un biais de confirmation. Il faut un jeu de test indépendant et des métriques objectives.


📝 Slide 10 : Le RAG en pratique — indexer ses documents, répondre avec sources

POURQUOI ces concepts se traduisent-ils en décisions concrètes ?

Le RAG n'est pas que de la théorie — chaque concept se traduit en un choix d'implémentation. Voici comment on passe de la théorie à la pratique sur un projet type (indexer des CVs et des offres d'emploi) :

| Source | Format | Découpage | Vector store |
|--------|--------|-----------|-------------|
| CVs candidats | PDFs | Recursive, 400 tokens, 50 overlap | FAISS (vitesse) |
| Offres d'emploi | JSON | Recursive, 600 tokens, 100 overlap | ChromaDB (filtrage catégorie/salaire) |
| Skills de référence | CSV | Par ligne | ChromaDB (métadonnées) |

Résultat : chaque réponse cite sa source (`[cv_003, page 2]` ou `[offer_007]`). C'est la traçabilité que le LLM nu ne peut pas fournir — et la raison principale d'utiliser un RAG.

> 💡 La règle d'or : on commence simple (FAISS + recursive splitter + 400 tokens), on mesure le Recall@k, et on ajuste si nécessaire. Ne pas optimiser tant qu'on n'a pas mesuré.


🎓 Ce que vous devez retenir — Chapitre 3

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| RAG = bibliothèque externe | Le LLM reste gelé, seule la bibliothèque évolue |
| 5 étapes : Load → Split → Embed → Store → Retrieve | Indexation = une fois. Retrieval = à chaque question. |
| RecursiveCharacterTextSplitter | Respecte la structure des documents — meilleur que taille fixe |
| 400-512 tokens + 10-20 % overlap | Le consensus pour le meilleur rappel |
| Embedding = coordonnée GPS du sens | Deux textes proches en sens = proches en vecteurs |
| FAISS (vitesse) vs ChromaDB (filtrage) | Souvent les deux ensemble |
| MMR | Pertinence + diversité — évite les chunks redondants |
| Recall@k ≥ 0,80 | La métrique qui dit si votre RAG est bon ou pas |
| Métadonnées sur chaque chunk | Indispensable pour citer les sources |
| 5 anti-patterns | Les connaître évite 80 % des problèmes en production |


➡️ Prochain chapitre

Votre RAG répond avec des sources et 0 % d'hallucination. Mais jusqu'ici, votre pipeline fait toujours la même chose dans le même ordre. On passe maintenant aux agents : donner à l'IA la capacité de **décider** quels outils utiliser, dans quel ordre, et de s'adapter à la question posée.

---

Chapitre 4 : Agents et Autonomie — Jour 2 après-midi


🎯 Objectif du chapitre

Comprendre la différence entre une chaîne fixe et un agent qui décide, maîtriser le pattern ReAct (Thought → Action → Observation), assembler un agent avec des garde-fous (limite d'itérations, gestion d'erreurs), définir des outils avec `@tool`, et comprendre comment un agent peut fonctionner de façon autonome sur un scénario multi-étapes.


📝 Slide 1 : Chaîne vs Agent — de l'exécution fixe à la décision

POURQUOI un agent répond-il mieux qu'une chaîne à une question complexe ?

Une chaîne LCEL fait toujours la même chose dans le même ordre : prompt → modèle → parser. C'est parfait pour une tâche unique. Mais si la question nécessite plusieurs étapes avec des choix ("cherche les CVs DevOps, puis vérifie leur réputation en ligne, puis calcule un score"), une chaîne ne sait pas s'adapter. Un agent, lui, **décide** quoi faire à chaque étape.

| Dimension | Chaîne LCEL | Agent |
|-----------|------------|-------|
| Flux d'exécution | Prédéfini, séquentiel | Dynamique, l'agent décide |
| Outils | Toujours les mêmes | Choisis selon la question |
| Correction d'erreur | Impossible (linéaire) | Peut réessayer autrement |
| Coût | Prévisible | Variable (plus élevé) |
| Cas idéal | Extraction, résumé, matching | Multi-sources, multi-étapes |

> 💡 Analogie : une chaîne, c'est une recette de cuisine — vous suivez les étapes dans l'ordre. Un agent, c'est un cuisinier — il regarde les ingrédients, décide quoi faire, ajuste en cours de route, et peut changer de plat si un ingrédient manque.


📝 Slide 2 : ReAct — le pattern qui rend les agents intelligents

POURQUOI ReAct est-il le pattern d'agent le plus robuste ?

ReAct (Reasoning + Acting, Yao et al. 2022) est un cycle où le LLM alterne entre raisonnement et action : il pense (Thought), agit (Action), observe le résultat (Observation), et recommence jusqu'à avoir assez d'information pour répondre. Cette alternance rend le processus transparent et auto-correcteur.

| Phase | Ce que fait le LLM | Exemple |
|-------|---------------------|---------|
| Thought | Il raisonne | "La question demande les 3 meilleurs DevOps. Je dois chercher dans les CVs." |
| Action | Il appelle un outil | `search_cvs("DevOps")` |
| Observation | Il lit le résultat | "3 CVs trouvés : Marie, Karim, Sophie" |
| Thought | Il raisonne à nouveau | "Je dois vérifier leur réputation en ligne." |
| Action | Il appelle un autre outil | `web_search("Marie Dubois GitHub")` |
| Observation | Il lit le résultat | "Profil GitHub actif, 15 repos" |
| Final Answer | Il répond | "Top 3 DevOps : 1. Marie (score 0.87)…" |

> 💡 Ce qui rend ReAct puissant : si l'observation est inattendue (par exemple, la recherche web ne trouve rien), l'agent peut raisonner à nouveau et essayer une autre approche. Une chaîne ne sait pas faire ça.


📝 Slide 3 : AgentExecutor — le chef d'orchestre

POURQUOI a-t-on besoin d'un orchestrateur autour de l'agent ?

L'agent LLM produit du texte (Thought/Action). Mais qui lit ce texte, exécute l'outil, récupère le résultat, et le réinjecte pour le tour suivant ? C'est le rôle de l'AgentExecutor — une boucle qui orchestre le cycle ReAct jusqu'à la réponse finale ou la limite d'itérations.

| Paramètre | Rôle | Sans lui… |
|-----------|------|----------|
| `max_iterations` | Limite le nombre de tours | Boucle infinie, coût explosif |
| `handle_parsing_errors` | Récupère les erreurs de format | Crash si le LLM dévie du format |
| `verbose` | Affiche la trace ReAct | Debug impossible |
| `memory` | Mémoire entre les tours | L'agent oublie le contexte |

⚠️ **Le piège n°1 des agents** — Oublier `max_iterations` : l'agent peut boucler indéfiniment, surtout avec des modèles open-source qui dévient du format. Toujours fixer `max_iterations=8` et `handle_parsing_errors=True`.


📝 Slide 4 : Les outils — ce que l'agent peut "faire"

POURQUOI les outils sont-ils le cœur de la valeur d'un agent ?

Sans outils, un agent ne fait que réfléchir sans agir. Les outils lui donnent accès au monde : rechercher dans vos documents (RAG), appeler une API, faire une recherche web, exécuter du code Python. Le décorateur `@tool` transforme n'importe quelle fonction Python en outil que l'agent peut appeler.

| Type d'outil | Exemple | Ce que ça donne à l'agent |
|-------------|---------|--------------------------|
| Recherche documentaire | `search_cvs("DevOps")` | Accès à vos données indexées |
| Recherche web | `web_search("Marie Dubois GitHub")` | Accès à l'internet |
| Exécution de code | `python_repl("0.87 * 0.5 + 0.8 * 0.3")` | Calculs exacts |
| Appel d'API | `check_availability("Marie")` | Accès à vos services internes |

⚠️ **Point crucial** — Le **docstring** de l'outil est ce que le LLM voit pour décider quand l'utiliser. Un docstring vide ou vague → l'agent choisit le mauvais outil. Un docstring clair et détaillé → l'agent sélectionne bien.


📝 Slide 5 : PythonREPLTool — quand le LLM a besoin de calculer

POURQUOI donner un interpréteur Python à l'agent ?

Les LLM sont mauvais en calcul exact — ils prédisent des tokens, ils ne calculent pas. Pour un score composite (`0.5 × expérience + 0.3 × réputation + 0.2 × disponibilité`), le LLM va approximer et se tromper. `PythonREPLTool` donne à l'agent un interpréteur Python pour calculer exactement.

| Tâche | LLM seul | LLM + PythonREPLTool |
|------|----------|---------------------|
| "Calcule 0.87×0.5 + 0.8×0.3 + 1.0×0.2" | "Environ 0.85" (approximatif) | `0.835` (exact) |
| "Compte les CVs avec > 5 ans d'expérience" | "Environ 12" (approximatif) | `14` (exact) |
| "Génère un graphique de distribution" | Impossible | Matplotlib → PNG |

⚠️ **Sécurité** — PythonREPLTool exécute du code arbitraire. En production : sandbox, restriction des imports, et jamais d'exposition à des utilisateurs non de confiance.


📝 Slide 6 : Recherche web — connecter l'agent à l'internet

POURQUOI un agent a-t-il besoin d'internet ?

Le RAG indexe vos documents internes, mais ne connaît pas la réputation en ligne de vos candidats (GitHub, publications, présence). La recherche web donne à l'agent l'accès à cette information externe. Combiné avec le RAG, l'agent a accès à la fois à vos données (internes) et au web (externe).

| Source | Outil | Ce que ça apporte |
|--------|-------|-------------------|
| Vos documents | RAG (search_docs) | Compétences, expérience, formation |
| Internet | web_search | GitHub, publications, présence en ligne |
| Calcul | python_repl | Scores composites, statistiques |

> 💡 L'agent combine ces sources intelligemment : il cherche d'abord dans vos CVs (RAG), puis vérifie la réputation en ligne (web), puis calcule un score final (Python). C'est exactement ce que ferait un recruteur humain — mais en quelques secondes.


📝 Slide 7 : Agents autonomes — travailler sans humain

POURQUOI un agent peut-il travailler sans intervention humaine ?

Un agent interactif répond message par message. Un agent autonome reçoit un scénario complet et l'exécute de bout en bout en accumulant le contexte. C'est utile pour les tâches batch : "Trouve les 3 meilleurs DevOps, vérifie leur réputation, calcule le score, et prépare un rapport."

| Étape | Action de l'agent | Outil utilisé |
|------|-------------------|--------------|
| 1 | "Cherche les DevOps" | `search_cvs("DevOps")` |
| 2 | "Vérifie leur réputation" | `web_search(chaque candidat)` |
| 3 | "Calcule le score composite" | `python_repl(formule)` |
| 4 | "Classe et rédige le rapport" | Réponse finale |

> 💡 L'agent enchaîne les 4 étapes en conservant le contexte entre chaque. Les résultats de l'étape 1 alimentent l'étape 2, etc. Pas besoin de supervision humaine entre les étapes — l'agent sait enchaîner.


📝 Slide 8 : Mémoire de l'agent — se souvenir entre les tours

POURQUOI la mémoire d'un agent diffère-t-elle de celle d'une chaîne ?

Une chaîne avec mémoire conserve l'historique conversationnel. Un agent avec mémoire conserve en plus les observations des outils — il se souvient que `search_cvs("DevOps")` a retourné Marie, Karim et Sophie, et peut réutiliser cette info au tour suivant sans ré-appeler l'outil.

| Composant | Mémoire chaîne | Mémoire agent |
|-----------|----------------|---------------|
| Messages | ✓ | ✓ |
| Observations outils | ✗ | ✓ |
| Persistance | JSON | JSON |

> 💡 Sans mémoire, l'agent repose la même question à chaque tour. Avec mémoire, il se souvient des résultats précédents et enchaîne intelligemment. C'est la différence entre un assistant amnésique et un assistant qui suit une conversation.


📝 Slide 9 : Les 5 pièges qui tuent un agent

POURQUOI les débutants en agents tombent-ils toujours sur les mêmes erreurs ?

| Piège | Symptôme | Solution |
|------|----------|----------|
| Pas de `max_iterations` | Boucle infinie, coût explosif | `max_iterations=8` |
| `handle_parsing_errors=False` | Crash si le LLM dévie du format | `=True` |
| Docstring d'outil vide | L'agent choisit le mauvais outil | Docstring clair et détaillé |
| `max_iterations=1` | L'agent est bloqué après 1 tour | Minimum 5-8 |
| Fonction non décorée `@tool` | L'agent ne "voit" pas l'outil | `@tool` sur chaque fonction |

> 💡 Ces 5 pièges représentent 80 % des bugs en atelier. Les connaître avant de coder vous fait gagner 2 heures de debug.


📝 Slide 10 : L'agent en pratique — orchestrer plusieurs outils

POURQUOI l'agent ReAct est-il la bonne architecture pour un projet multi-sources ?

Dans un projet réel, une question peut nécessiter 1 à 4 sources différentes. L'agent décide dynamiquement quels outils interroger, dans quel ordre, avec quelle combinaison — sans que le développeur code tous les cas possibles.

| Outil | Source | Type de retour |
|-------|--------|----------------|
| Recherche documentaire | Vos documents indexés (RAG) | Passages + sources |
| Matching | Chaîne LCEL (score, justification) | Score structuré |
| Recherche web | Internet (GitHub, publications) | Résultats web |
| Exécution code | Python (calculs exacts) | Résultat numérique |

Requête type : *"Trouve les 3 meilleurs profils DevOps, vérifie leur réputation en ligne, et calcule un score composite."*

L'agent exécute : recherche CVs → recherche web (pour chaque CV) → calcul du score → réponse classée. Tout ça en autonomie, avec une trace complète de chaque décision.

> 💡 Le pattern ReAct est la base — mais il a ses limites pour les conversations longues (50+ messages). C'est ce que les Deep Agents (prochain chapitre) viennent résoudre : planning, skills dynamiques, contexte structuré.


🎓 Ce que vous devez retenir — Chapitre 4

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| Chaîne = fixe, Agent = décide | L'agent s'adapte à la question au lieu de suivre un chemin prédéfini |
| ReAct (Thought/Action/Observation) | Le cycle qui rend l'agent transparent et auto-correcteur |
| AgentExecutor | L'orchestrateur qui fait tourner la boucle ReAct |
| `max_iterations=8` | Évite les boucles infinies — le piège n°1 |
| `handle_parsing_errors=True` | Récupère les erreurs de format du LLM |
| `@tool` + docstring | Le docstring est ce que le LLM voit pour choisir l'outil |
| PythonREPLTool | Pour les calculs exacts — le LLM est mauvais en calcul |
| Recherche web | Combine données internes (RAG) + externes (internet) |
| Agent autonome | Scénario multi-étapes sans supervision humaine |
| Mémoire agent | Conserve les observations entre les tours |


➡️ Prochain chapitre

Votre agent ReAct sait choisir ses outils et travailler en autonomie. Mais pour les conversations longues (entretiens de recrutement de 50+ messages), ReAct montre ses limites : pas de planning, pas d'adaptation selon la phase. Les Deep Agents sont la nouvelle génération : planning, skills dynamiques, contexte structuré. C'est le passage de l'agent réactif à l'agent autonome structuré.

---

Chapitre 5 : Deep Agents — Architecture 4 couches — Jour 3 matin


🎯 Objectif du chapitre

Comprendre pourquoi Deep Agents surpasse ReAct pour les agents long-horizon, maîtriser l'architecture 4 couches (identité, règles globales, skills par phase, contexte dynamique), comprendre comment le middleware charge automatiquement le bon "manuel de procédure" selon la phase de conversation, et configurer le harness pour exclure les composants inutiles.


📝 Slide 1 : Pourquoi Deep Agents ? — les limites de ReAct

POURQUOI ReAct ne suffit pas pour les conversations longues ?

ReAct est excellent pour des tâches courtes (3-5 tours) avec des outils simples. Mais pour un entretien de recrutement de 50+ messages, il montre ses limites : pas de planning, pas d'adaptation du comportement selon la phase (premier contact vs closing), pas de contexte structuré. Deep Agents résout ces limitations.

| Ce que ReAct ne sait pas faire | Ce que Deep Agents apporte |
|-------------------------------|---------------------------|
| Planifier un entretien en plusieurs phases | Planning intégré (todo list automatique) |
| Adapter son comportement selon la phase | Skills dynamiques : un "manuel" différent par phase |
| Maintenir un contexte structuré (candidat, champs qualifiés) | contextSchema Pydantic injecté avant chaque appel |
| Rappeler les règles globales à chaque tour | AGENTS.md : règles globales persistantes |
| Déléguer une sous-tâche à un agent spécialisé | Subagents natifs |

> 💡 Deep Agents est un "harness" (un cadre) batteries-incluses : planning, filesystem, subagents, context management — tout est intégré. Au lieu de monter chaque pièce toi-même, tu donnes une spec et le cadre assemble.


📝 Slide 2 : L'architecture 4 couches — la vue d'ensemble

POURQUOI 4 couches et pas un seul gros prompt ?

Un agent de recrutement a besoin de 4 types d'information qui changent à des fréquences différentes : l'identité (jamais), les règles globales (rarement), le comportement par phase (à chaque phase), le contexte courant (à chaque message). Tout mettre dans un seul prompt gigantesque serait impossible à maintenir. Séparer les 4 couches permet de modifier l'une sans toucher les autres.

| Couche | Nom | Fréquence de changement | Analogie |
|--------|-----|------------------------|----------|
| 1 | Identité (systemPrompt) | Jamais | La carte d'identité du recruteur |
| 2 | Règles globales (AGENTS.md) | Rarement | Le manuel de l'entreprise |
| 3 | Skills par phase (SKILL.md) | À chaque phase | La fiche réflexe pour la situation |
| 4 | Contexte dynamique (contextSchema) | À chaque message | La fiche de suivi du candidat |

```
┌─────────────────────────────────────────┐
│  Couche 1 : Identité ("Tu es recruteur") │  Jamais
├─────────────────────────────────────────┤
│  Couche 2 : AGENTS.md (règles globales)  │  Rarement
├─────────────────────────────────────────┤
│  Couche 3 : SKILL.md (comportement phase)│  Dynamique
├─────────────────────────────────────────┤
│  Couche 4 : contextSchema (contexte)     │  Temps réel
└─────────────────────────────────────────┘
```


📝 Slide 3 : Couche 1 — l'identité statique

POURQUOI l'identité ne doit-elle jamais changer ?

L'identité définit QUI est l'agent. Le recruteur reste un recruteur du premier au dernier message. Si l'identité change, l'agent perd sa cohérence. C'est la fondation — tout le reste s'ajoute par-dessus.

| Élément | Exemple |
|---------|---------|
| Rôle | "Tu es un recruteur tech spécialisé en IT" |
| Langue | "Tu parles toujours en français" |
| Ton | "Professionnel mais chaleureux, pas robotique" |
| Mission | "Qualifier les candidats pour des postes tech" |
| Interdits | "Ne donne jamais d'URL, ne promets jamais un poste" |

> 💡 L'identité est le seul élément codé en dur dans l'application. Tout le reste (règles, skills, contexte) est dans des fichiers externes modifiables sans toucher au code.


📝 Slide 4 : Couche 2 — AGENTS.md, les règles globales

POURQUOI séparer les règles globales de l'identité ?

Les règles globales ("recadrer le hors-sujet", "ne jamais donner d'URL", "toujours demander l'email") sont des contraintes qui s'appliquent à toutes les phases. Les mettre dans l'identité la rendrait énorme. Les mettre dans un fichier markdown séparé (AGENTS.md) permet à un chef de recrutement de les modifier sans être développeur.

| Règle | Pourquoi elle existe |
|------|----------------------|
| Langue française obligatoire | Cohérence de communication |
| Recadrer le hors-sujet | Maintenir le focus sur le recrutement |
| Pas d'URL, pas de promesse d'embauche | Protection légale et brand |
| Réponses courtes (2-3 phrases) | Consistance des échanges |
| Procédure de gestion d'objection | "Sur 'trop cher' → reformuler la valeur" |

> 💡 AGENTS.md est lu au démarrage et injecté dans l'identité. C'est un fichier markdown — éditable par un non-développeur. Le chef de recrutement peut ajouter une règle sans passer par un commit.


📝 Slide 5 : Couche 3 — SKILL.md, le comportement par phase

POURQUOI charger un "manuel" différent selon la phase ?

Un entretien de recrutement passe par 4 phases : premier contact, qualification, reformulation, closing. Chaque phase nécessite un comportement différent. Charger le bon SKILL.md au bon moment adapte le comportement de l'agent sans modifier son code.

| Phase | Quand | Comportement attendu |
|-------|-------|---------------------|
| Premier contact | Début (0 question qualif) | Présenter l'offre, demander l'intérêt |
| Qualification | Milieu (1-5 questions) | Poser les questions de qualification |
| Reformulation | Avant la fin (6 questions) | Résumer le profil, confirmer la compréhension |
| Closing | Fin (signal de clôture) | Proposer le test technique + lien |

La fonction `read_skill_for_context()` choisit le bon SKILL.md selon où on en est dans la conversation. C'est automatique — l'agent n'a pas besoin de "savir" quelle phase il est, le middleware s'en charge.

> 💡 Analogie : des fiches réflexes que l'agent sort du tiroir selon la situation. "Premier contact" pour le premier message, "Qualification" pour les questions, "Reformulation" pour le résumé, "Closing" pour la conclusion. L'agent ne choisit pas la fiche — le système la lui donne au bon moment.


📝 Slide 6 : Couche 4 — le contexte dynamique avec contextSchema

POURQUOI un schéma Pydantic plutôt qu'un dictionnaire libre ?

Un dictionnaire libre n'a pas de validation — on peut oublier une clé, mettre un mauvais type, et l'agent se comporte de façon imprévisible. Un contextSchema Pydantic valide les types, garantit la présence des champs, et documente le contexte attendu.

| Champ | Type | Exemple | Rôle |
|-------|------|---------|------|
| `qual_count` | int | 3 | Nombre de questions qualif posées |
| `stage` | str | "contacted" | Étape du pipeline CRM |
| `next_field` | str | "disponibilite" | Prochaine question à poser |
| `objection_key` | str | "trop_cher" | Objection détectée |
| `is_closing` | bool | False | Signal de clôture détecté |

> 💡 Le contextSchema, c'est la fiche de suivi que le manager remplit avant chaque entretien : "Le candidat s'appelle Nathan, il a rempli 3/6 champs, il est au stage 'contacted', la prochaine question est sa disponibilité." Le recruteur n'a plus qu'à conduire l'entretien.


📝 Slide 7 : beforeModel — le middleware qui prépare le terrain

POURQUOI un middleware avant le modèle plutôt que tout dans le prompt ?

Le middleware `beforeModel` s'exécute AVANT chaque appel au LLM. Il regarde le contexte, choisit le bon SKILL.md, construit le briefing dynamique, et l'injecte automatiquement. L'injection est transparente — le code applicatif n'a pas à s'en soucier.

| Étape | Ce que fait le middleware |
|------|--------------------------|
| 1. Lire le contexte | Récupérer le contextSchema courant |
| 2. Choisir le skill | Quel SKILL.md correspond à la phase ? |
| 3. Construire le briefing | Assembler les sections (infos candidat, prochaine question, objection) |
| 4. Injecter | Ajouter le skill + le briefing dans les messages |

> 💡 Analogie : un secrétaire qui prépare le dossier du candidat avant chaque entretien. Il lit la fiche de suivi, sort le bon manuel de procédure (SKILL.md), et prépare le briefing. Le recruteur n'a plus qu'à conduire l'entretien — tout est prêt.


📝 Slide 8 : HarnessProfile — ne pas tout activer par défaut

POURQUOI configurer le harness plutôt que de tout garder activé ?

Deep Agents est batteries-incluses : planning, filesystem, subagents, summarisation, todo list. Mais tous ces composants ne sont pas nécessaires pour un recruteur conversationnel. HarnessProfile permet d'exclure les composants inutiles — moins de complexité, moins de tokens.

| Composant | Activé par défaut | Utile pour un recruteur ? |
|-----------|-------------------|--------------------------|
| Planning (write_todos) | ✓ | ✗ (conversation, pas de plan) |
| SummarizationMiddleware | ✓ | Bonus (longues conversations) |
| Filesystem | ✓ | ✓ (lire AGENTS.md, SKILL.md) |
| beforeModel | ✓ | ✓ (cœur du système) |
| Subagents | ✓ | Bonus (délégation) |

> 💡 Configurer le harness, c'est comme régler une usine : "je ne veux pas de planning automatique, pas de subagents, pas de todo list. Mon agent fait juste de la conversation adaptative." On allume ce dont on a besoin, on éteint le reste.


📝 Slide 9 : Subagents — déléguer pour rester simple

POURQUOI déléguer à des subagents ?

Un agent qui fait tout devient un prompt gigantesque qui perd en qualité. Les subagents permettent de déléguer une sous-tâche à un agent spécialisé : un "screener" pour le screening initial, un "matcher" pour le matching technique. L'agent principal orchestre, les subagents exécutent.

| Subagent | Rôle | Input → Output |
|----------|------|----------------|
| Screener | Screening initial (3 questions filtres) | CV → Go/No-go |
| Matcher | Matching technique | CV + offre → Score |
| Scheduler | Planification d'entretien | Disponibilités → Créneaux |

⚠️ Les subagents augmentent la consommation de tokens (chaque subagent a son propre appel LLM). Ne les activer que si la délégation apporte une valeur mesurée.


📝 Slide 10 : Le Deep Agent en pratique — un recruteur qui s'adapte

POURQUOI l'architecture Deep Agents est-elle la bonne pour un recruteur ?

Le recruteur doit conduire des entretiens longs (50+ messages), adapter son comportement selon la phase, maintenir un contexte structuré, et détecter les objections/closing. ReAct ne sait pas faire tout ça. Deep Agents avec 4 couches le fait nativement.

| Couche | Fichier | Ce qu'elle contient |
|--------|---------|---------------------|
| Identité | Code (systemPrompt) | "Tu es un recruteur tech…" |
| Règles | AGENTS.md (markdown) | Langue, recadrage, interdits, format |
| Skills | SKILL.md × 5 phases | first-contact, qualification, reformulation, closing, test |
| Contexte | contextSchema (Pydantic) | qual_count, stage, next_field, objection_key |

Au début de la conversation, le middleware charge `phase-first-contact`. Après 3 questions, il charge `phase-qualification`. Quand le candidat dit "c'est trop cher", le contexte détecte l'objection, le middleware charge la tactique de gestion d'objection. À la fin, `phase-closing` pour proposer le test technique.

> 💡 L'agent ne "sait" pas qu'il change de phase — le middleware le fait pour lui, automatiquement, en regardant le contexte. C'est ce qui rend le système robuste : l'agent se contente de converser, le système s'occupe de l'adapter.


🎓 Ce que vous devez retenir — Chapitre 5

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| Deep Agents vs ReAct | Planning, skills dynamiques, contexte structuré — le saut qualitatif |
| 4 couches | Identité (statique) + Règles (semi-statique) + Skills (dynamique) + Contexte (temps réel) |
| AGENTS.md | Règles globales éditables par un non-développeur |
| SKILL.md par phase | Le comportement s'adapte sans coder — un fichier markdown par phase |
| contextSchema (Pydantic) | Validation des types + documentation vivante du contexte |
| beforeModel middleware | Injecte skill + contexte avant chaque appel LLM — automatique |
| HarnessProfile | Exclure les composants inutiles — moins de complexité, moins de tokens |
| Subagents | Déléguer une sous-tâche à un agent spécialisé — bonus, pas obligatoire |
| read_skill_for_context() | Choisit le bon SKILL.md selon la phase automatiquement |
| 4 couches = séparation des préoccupations | Modifier une couche sans toucher les autres |


➡️ Prochain chapitre

Le Deep Agent fonctionne en ligne de commande. On passe maintenant à la production : connecter l'agent à Telegram pour qu'il parle aux candidats, construire un CRM pour suivre le pipeline, analyser du code, gérer la voix, et faire le pont entre le prototype et le produit.

---

Chapitre 6 : Chatbots, Code Review et Multimodal — Jour 3 matin


🎯 Objectif du chapitre

Connecter le Deep Agent à Telegram via un handler complet (objection → closing → mémoire → CRM → agent → réponse), construire un CRM pour suivre le pipeline de candidats, créer un dashboard visuel, indexer un repo de code pour un assistant de développement, et introduire l'interaction vocale.


📝 Slide 1 : Du prototype CLI au produit — les 3 briques manquantes

POURQUOI un agent CLI n'est pas un produit ?

Un agent en ligne de commande prouve que la logique marche. Mais un produit doit parler aux utilisateurs (interface), suivre l'état (CRM), et s'observer (logs). Ces 3 briques transforment le prototype en produit utilisable.

| Brique | Ce qu'elle apporte | Sans elle… |
|--------|-------------------|------------|
| Interface candidat (Telegram) | L'utilisateur parle à l'agent dans sa messagerie | L'utilisateur doit ouvrir un terminal |
| Suivi pipeline (CRM) | Le recruteur voit où en est chaque candidat | Impossible de suivre le flux |
| Observabilité (logs structurés) | On sait ce qui s'est passé et quand | Debug impossible en production |


📝 Slide 2 : Interface chatbot — recréer une expérience ChatGPT

POURQUOI l'UX chatbot est-elle différente d'une simple API ?

Un chatbot ne se résume pas à "envoyer un message, recevoir une réponse". L'expérience utilisateur nécessite : historique visible, streaming des tokens en temps réel, indicateurs de frappe, multi-pages. Streamlit fournit ces composants nativement.

| Composant UX | Ce que ça donne à l'utilisateur |
|-------------|--------------------------------|
| Messages avec avatars | On voit qui parle (user vs assistant) |
| Streaming des tokens | La réponse apparaît mot par mot (comme ChatGPT) |
| Historique persistant | On retrouve ses conversations au redémarrage |
| Multi-pages | Chat, Dashboard, Bibliothèque — chacun son usage |

> 💡 Le streaming des tokens est un détail UX qui change tout : sans streaming, l'utilisateur attend 10 secondes devant un écran vide. Avec streaming, il voit la réponse se construire en temps réel — la perception de latence est divisée par 3.


📝 Slide 3 : Bot Telegram — parler aux utilisateurs dans leur messagerie

POURQUOI Telegram plutôt qu'une interface web ?

Les utilisateurs sont déjà sur Telegram — ils n'ont pas besoin d'installer une nouvelle app. Le bot Telegram permet à l'agent de parler directement aux candidats dans leur messagerie quotidienne. Le handler orchestre le flux complet à chaque message.

| Étape du handler | Action |
|------------------|--------|
| 1. Détection objection | Le candidat dit "c'est trop cher" → tactique de recadrage |
| 2. Détection closing | Le candidat dit "je suis intéressé" → passage en phase closing |
| 3. Extraction mémoire | On extrait les infos du message (dispo, salaire attendu) |
| 4. Mise à jour CRM | Le stage du candidat est mis à jour dans le pipeline |
| 5. Deep Agent | L'agent génère la réponse avec le bon skill + le contexte |
| 6. Reply + log | Réponse envoyée sur Telegram + log structuré pour audit |

> 💡 Ce handler est le cœur du produit : il orchestre 6 étapes à chaque message entrant. C'est l'équivalent d'un standardiste qui suit une procédure : identifier, détecter le motif, chercher le dossier, transférer à l'expert, répondre.


📝 Slide 4 : CRM Pipeline — suivre les candidats en temps réel

POURQUOI un CRM SQLite plutôt que PostgreSQL ?

Pour un bot qui traite des dizaines de candidats (pas des millions), SQLite suffit — zéro infrastructure, un fichier, pas de serveur. Le mode WAL (Write-Ahead Logging) permet au dashboard de lire pendant que le bot écrit, sans conflit.

| Stage | Description | Couleur |
|-------|-------------|---------|
| New | Nouveau candidat, pas encore contacté | Gris |
| Contacted | Premier message envoyé | Bleu |
| Interested | Candidat a répondu, intéressé | Vert clair |
| Qualified | Qualification complète | Vert |
| Closed Won | Candidat accepté | Vert foncé |
| Closed Lost | Candidat refusé ou désisté | Rouge |

> 💡 WAL = Write-Ahead Logging. Les écritures vont d'abord dans un journal, puis sont fusionnées. Cela permet à plusieurs processus de lire simultanément sans bloquer les écritures. Parfait pour un bot + un dashboard qui tournent en parallèle.


📝 Slide 5 : Dashboard visuel — le pipeline en un coup d'œil

POURQUOI un dashboard en plus du bot ?

Le bot parle aux candidats. Mais le recruteur a besoin d'une vue d'ensemble : combien de candidats à chaque stage, qui a répondu, qui stagne, qui faut-il relancer. Le dashboard Streamlit affiche le pipeline en colonnes kanban — comme Trello, mais pour le recrutement.

| Page | Usage |
|------|-------|
| Chat | Converser avec l'agent |
| Dashboard pipeline | Vue kanban : candidats par stage, stats globales |
| Bibliothèque CVs | Parcourir, filtrer, prévisualiser les CVs |
| Multimodal | Audio → texte → agent → réponse vocale |

> 💡 Le dashboard est la vue "recruteur" — le bot est la vue "candidat". Deux interfaces pour deux publics, un seul backend (le Deep Agent + le CRM).


📝 Slide 6 : Code Reviewer — interroger son code en langage naturel

POURQUOI indexer du code source comme un corpus RAG ?

Un repo de 50 fichiers est impossible à explorer manuellement pour un nouveau développeur. En indexant le code avec un RAG (même technique que pour les CVs !), on peut poser des questions en langage naturel : "Où est géré l'authentification ?", "Que fait la fonction hash_password ?".

| Question en langage naturel | Réponse du Code Reviewer |
|---------------------------|--------------------------|
| "Où est géré l'authentification ?" | "Dans `auth.py:42`, la fonction `verify_token`…" |
| "Que fait hash_password ?" | "Elle hash avec bcrypt + salt…" (`auth.py:15`) |
| "Quelles sont les classes de modèle DB ?" | "User, Session, AuditLog dans `models.py`" |

> 💡 Le Code Reviewer est l'application directe du RAG à un nouveau type de document : du code source au lieu de CVs. Les principes (chunking, embedding, retrieval) sont identiques — seul le loader change.


📝 Slide 7 : Logs structurés — 14 préfixes pour l'observabilité

POURQUOI 14 préfixes de log plutôt que des print() génériques ?

En production, un bot génère des centaines de logs par heure. Sans structure, impossible de retrouver "quelle objection a été détectée pour quel candidat". Les 14 préfixes permettent de retrouver instantanément l'information et de vérifier que chaque étape du handler a bien été exécutée.

| Préfixe | Quand |
|---------|-------|
| 📥 | Message entrant reçu |
| 📤 | Message sortant envoyé |
| 🟡 | Objection détectée |
| 🟣 | Signal de closing détecté |
| 🧠 | Mémoire extraite et stockée |
| 🤖 | Appel LLM en cours |
| ⚠️ | Erreur LLM |
| 🔗 | Lien de conversion envoyé |
| 📊 | Stage CRM mis à jour |
| ❌ | Refus du candidat |
| ✅ | Qualification complète |
| 📞 | Relance automatique (follow-up) |

> 💡 Ces préfixes ne sont pas que pour les humains — les tests E2E (prochain chapitre) les parsent pour vérifier que le flux complet a été exécuté. Un préfixe manquant = une étape manquée = test en échec.


📝 Slide 8 : Multimodal — l'agent parle et écoute

POURQUOI introduire la voix dans un cours LangChain ?

Les chatbots textuels sont la norme, mais l'interaction vocale devient standard (assistants vocaux, transcription d'entretiens). LangChain s'intègre avec Whisper (transcription) et les APIs TTS (synthèse). Le flux : audio → Whisper → texte → agent → réponse → TTS → audio.

| Étape | Technologie | Direction |
|------|-------------|-----------|
| Transcription (STT) | Whisper | Audio candidat → texte |
| Génération réponse | Deep Agent | Texte → texte |
| Synthèse vocale (TTS) | API TTS | Texte → audio candidat |

> 💡 Le multimodal n'est pas qu'un gadget : pour les recruteurs qui font 50 appels par jour, pouvoir dicter ses notes et entendre les résumés vocaux est un gain de productivité massif.


📝 Slide 9 : Follow-up automatique — relancer sans oublier

POURQUOI automatiser les relances ?

Un candidat qui ne répond pas pendant 48h est probablement perdu. Le follow-up sweep scanne le CRM, identifie les candidats en attente, et envoie automatiquement un message de relance personnalisé. C'est le type de tâche qu'un humain oublie mais qu'un agent fait sans faille.

| Étape | Action |
|------|--------|
| 1. Scan | Lister les candidats en attente > 48h |
| 2. Message | L'agent génère une relance personnalisée |
| 3. Envoi | Message Telegram + log |
| 4. Mise à jour | Stage CRM → "follow_up_sent" |


📝 Slide 10 : L'architecture production — Telegram + CRM + Dashboard

POURQUOI ces 3 composants transforment-ils le prototype en produit ?

Le Deep Agent fonctionne en CLI. Pour le mettre en production, il faut : une interface candidat (Telegram), un suivi recruteur (CRM + dashboard), et l'observabilité (logs). Ces 3 briques font le pont entre la démo technique et le produit utilisable.

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Bot Telegram | python-telegram-bot | Interface candidat |
| CRM SQLite | sqlite3 + WAL | Persistance candidats + messages |
| Dashboard Streamlit | 4 pages | Interface recruteur (kanban, stats) |
| API FastAPI | uvicorn | Exposition REST |
| Logs structurés | 14 préfixes | Observabilité + tests E2E |
| Follow-up sweep | Background / cron | Relance automatique 48h |

> 💡 Le flux complet — de Telegram au CRM en passant par le Deep Agent — est ce qui transforme un agent CLI en produit. C'est le pont entre le chapitre 5 (agent) et le chapitre 7 (déploiement + tests E2E).


🎓 Ce que vous devez retenir — Chapitre 6

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| 3 briques produit | Interface (Telegram) + Suivi (CRM) + Observabilité (logs) |
| UX chatbot | Streaming des tokens + historique + multi-pages |
| Handler Telegram 6 étapes | Objection → closing → mémoire → CRM → agent → reply |
| CRM SQLite + WAL | Pipeline 6 stages, lecture/écriture concurrente |
| Dashboard Streamlit | Vue kanban pour le recruteur — le bot est la vue candidat |
| Code Reviewer | RAG appliqué au code source — mêmes principes, loader différent |
| 14 préfixes de log | Observabilité + parsés par les tests E2E |
| Multimodal | Whisper (STT) + TTS — la voix devient standard |
| Follow-up automatique | Relancer les candidats en attente > 48h |
| FastAPI endpoints | Exposer l'agent en API REST |


➡️ Prochain chapitre

Le bot Telegram et le CRM fonctionnent. On passe maintenant à la validation : tracer chaque appel avec LangSmith, mesurer la qualité du retrieval (Recall@k), comparer les architectures, écrire des tests de bout en bout, et déployer l'ensemble avec Docker.

---

Chapitre 7 : Évaluation, Benchmarking et Déploiement — Jour 3 après-midi


🎯 Objectif du chapitre

Comprendre pourquoi l'évaluation est la dernière étape critique avant la production, tracer chaque appel LLM avec LangSmith, mesurer la qualité du retrieval et le coût par requête, comparer les architectures (LLM seul vs RAG vs Agent vs Deep Agent), écrire des tests de bout en bout, et déployer avec Docker Compose.


📝 Slide 1 : Pourquoi évaluer ? — "ça marche" n'est pas une métrique

POURQUOI l'évaluation est-elle la dernière étape critique ?

"Le bot marche" n'est pas une métrique. En production, les cas-limites et les régressions après mise à jour révèlent les failles au pire moment. L'évaluation objective compare les architectures, détecte les régressions, et donne des chiffres à présenter au décideur.

| Ce qu'on mesure | Avec quoi | Pourquoi |
|-----------------|----------|----------|
| Qualité du retrieval | Recall@k, MRR | Le bon document est-il retrouvé ? |
| Qualité de la réponse | Faithfulness, pertinence | La réponse est-elle fidèle aux sources ? |
| Coût par requête | Tokens in/out × prix | Combien coûte une conversation ? |
| Flux complet | Tests E2E Playwright | Toutes les étapes s'enchaînent-elles ? |
| Performance en production | LangSmith tracing | Où est le goulot ? |


📝 Slide 2 : LangSmith — la boîte noire de votre LLM

POURQUOI un système LLM non tracé est-il impossible à optimiser ?

Sans traçabilité, on ne sait pas quel document a été récupéré pour une réponse incorrecte, quel outil l'agent a appelé en premier, ni combien de tokens coûte chaque requête. LangSmith trace automatiquement chaque appel — zéro code supplémentaire avec LangChain.

| Ce que LangSmith trace | Pourquoi c'est utile |
|----------------------|---------------------|
| Le prompt exact envoyé | Débugger les mauvaises réponses |
| La réponse brute du LLM | Voir les erreurs de parsing |
| Les documents récupérés | Vérifier la qualité du retrieval |
| La latence par étape | Identifier le goulot (retrieval vs LLM) |
| Le coût en tokens | Estimer la facture mensuelle |

> 💡 Activer LangSmith = 2 variables d'environnement (`LANGSMITH_TRACING=true` et `LANGSMITH_API_KEY=...`). C'est tout — LangChain trace automatiquement. Pas une ligne de code à ajouter.


📝 Slide 3 : Benchmarking — comparer les architectures

POURQUOI comparer LLM seul vs RAG vs Agent avant de choisir ?

Chaque architecture a un trade-off : le LLM seul est rapide mais hallucine, le RAG est fiable mais limité à la retrieval, l'agent est flexible mais coûteux. Le benchmark quantifie ces trade-offs sur des données réelles pour décider objectivement.

| Architecture | Qualité | Latence | Coût/req | Hallucination |
|-------------|---------|---------|----------|---------------|
| LLM seul | Variable | 2-3s | €0.01 | 80-100 % |
| RAG seul | 85 % | 3-5s | €0.02 | 0 % |
| Agent ReAct | 92 % | 8-15s | €0.05 | 0 % |
| Deep Agent | 94 % | 10-20s | €0.06 | 0 % |

> 💡 L'agent est 5× plus coûteux que le RAG seul mais 7 % plus précis (multi-outils, correction d'erreur). Le choix dépend du budget et du cas d'usage. Le benchmark donne les chiffres pour décider — pas pour deviner.


📝 Slide 4 : Monitoring des coûts — éviter la facture surprise

POURQUOI surveiller les coûts dès le développement ?

Un agent qui fait 8 itérations consomme 8× plus de tokens qu'un simple appel. Sans monitoring, la facture API peut exploser. La solution : extraire `usage_metadata` de chaque réponse et calculer le coût en temps réel.

| Métrique | Source | Cible |
|----------|--------|-------|
| Tokens input | `usage_metadata["input_tokens"]` | < 5 000 / requête |
| Tokens output | `usage_metadata["output_tokens"]` | < 2 000 / requête |
| Coût € par requête | tokens × prix provider | < €0.10 |
| Budget session | Somme par session | < €5 |

> 💡 Le coût d'un agent ReAct est 5× supérieur à un appel direct — mais il fait 5× plus de choses. Le monitoring permet de voir si le ratio valeur/coût est acceptable pour votre cas d'usage.


📝 Slide 5 : Tests E2E — valider le système entier

POURQUOI des tests E2E "human-in-the-loop" plutôt que des tests automatisés classiques ?

Un LLM est non déterministe : la même question peut produire des réponses différentes. Les tests classiques (`assert result == expected`) ne marchent pas. Les tests E2E human-in-the-loop guident un humain à travers un scénario et vérifient l'état du système (base de données, API, logs) à chaque étape — pas le texte exact de la réponse.

| Ce que le test vérifie | Comment |
|----------------------|---------|
| Le stage CRM a changé | Lecture en base de données |
| Le nombre de messages est correct | Comptage en base |
| Les logs structurés sont présents | Recherche des préfixes (📥 🟡 🧠…) |
| L'API répond | Requête HTTP de health check |
| Le flux complet s'est exécuté | 13 étapes vérifiées une par une |

> 💡 Le test E2E, c'est comme un inspecteur qui suit une checklist de 13 points et coche chaque vérification. Il ne vérifie pas ce que le candidat a dit — il vérifie que le système a bien enregistré, mis à jour, et loggé chaque étape.


📝 Slide 6 : Docker Compose — une commande pour tout lancer

POURQUOI Docker Compose pour déployer ?

Docker Compose définit tous les services dans un seul fichier. Il garantit la reproductibilité entre environnements (Mac, Linux, serveur), isole les dépendances, et permet de démarrer l'application complète avec une seule commande : `docker compose up`.

| Service | Port | Rôle |
|---------|------|------|
| API FastAPI | 8000 | Agent + RAG + services |
| Dashboard Streamlit | 8501 | Interface recruteur |
| ChromaDB | 8001 | Persistance des vector stores |

> 💡 Docker Compose, c'est un chef d'orchestre qui dit "1, 2, 3, partez" et tous les musiciens commencent en même temps. Sans Docker, il faudrait lancer 3 processus manuellement dans 3 terminaux différents — et prier pour que les ports ne collisionnent pas.


📝 Slide 7 : Bonnes pratiques de production

POURQUOI ces pratiques différencient-elles un POC d'un produit maintenu ?

Un POC peut ignorer le cache, les retries, et le monitoring. Un produit en production ne peut pas. Ces 5 pratiques sont le minimum pour passer du prototype au produit.

| Pratique | Pourquoi |
|----------|----------|
| Cache TTL | Réduit la latence et le coût pour les appels fréquents |
| Variables d'environnement | Sécurité + portabilité entre environnements |
| Retry avec backoff | Résistance aux pannes transitoires de l'API |
| Health check endpoint | Monitoring infra + load balancer |
| Graceful degradation | L'app reste utilisable si un service est down |


📝 Slide 8 : Sécurité — 5 risques critiques

POURQUOI sécuriser un LLM est-il différent de sécuriser une API classique ?

Une API classique traite des données structurées avec une logique déterministe. Un LLM traite du texte libre et produit des sorties non déterministes. Un attaquant peut injecter des instructions dans le texte pour modifier le comportement du modèle — ce qui n'existe pas dans une API REST.

| Risque | Description | Mitigation |
|--------|-------------|------------|
| Prompt injection | "Ignore les instructions et…" | Middleware regex avant parsing |
| Exfiltration via RAG | Requête malicieuse récupère des données sensibles | Contrôle d'accès sur les collections |
| Credentials exposés | Token API hardcodé dans le code | `.env` + `.gitignore` |
| Pas de rate limiting | Coût API illimité | 10 req/min par IP |
| Logs insuffisants | Impossible de détecter un abus | 14 préfixes de log structuré |

⚠️ **OWASP Gen AI 2025** — Le prompt injection est le risque #1 dans le Top 10 LLM d'OWASP. Plusieurs entreprises ont vu leurs chatbots divulguer des données internes suite à des injections en 2024.


📝 Slide 9 : Les erreurs de déploiement les plus fréquentes

POURQUOI les déploiements LLM échouent-ils souvent pour des raisons non-ML ?

La plupart des incidents ne viennent pas de la qualité du modèle mais de détails d'intégration : modèle rechargé à chaque requête, CORS mal configuré, package non installé. Ces erreurs sont bêtes mais fréquentes.

| Erreur | Symptôme | Solution |
|--------|----------|----------|
| Modèle rechargé à chaque requête | Latence 10-30s, OOM | Lifespan FastAPI + cache Streamlit |
| CORS mal configuré | Erreur bloquante depuis le frontend | CORSMiddleware avec origins explicites |
| Package non installé | `ModuleNotFoundError` dans Streamlit | `pip install -e .` après requirements |
| Pas de rate limiting | Coût API explosif | SlowAPI ou middleware custom |
| Health check absent | Load balancer ne sait pas si l'app est up | `GET /health` retourne le statut |


📝 Slide 10 : L'architecture finale — du premier prompt au produit déployé

POURQUOI ces 3 jours vous ont mené du prompt au déploiement ?

En 3 jours, vous avez construit un système complet — du premier prompt hallucinant à un agent autonome déployé en production avec tests E2E. Chaque demi-journée a construit une couche de l'architecture finale.

| Couche | Construit pendant | Technologie |
|--------|-------------------|-------------|
| Prompts + Parsers | Jour 1 matin | ChatPromptTemplate + PydanticOutputParser |
| Chaînes + Mémoire | Jour 1 ap.-m. | LCEL (pipe `\|`) + WindowMemory |
| RAG | Jour 2 matin | FAISS + ChromaDB + FastEmbed |
| Agent ReAct | Jour 2 ap.-m. | create_react_agent + 4 outils |
| Deep Agent | Jour 3 matin | 4 couches + beforeModel + skills dynamiques |
| Production | Jour 3 matin | Telegram + CRM SQLite + Streamlit |
| Validation + Déploiement | Jour 3 ap.-m. | LangSmith + Playwright E2E + Docker |

> 💡 Vous repartez avec un projet fil rouge complet que vous pouvez adapter à votre propre domaine. La prochaine étape : l'adapter à votre cas d'usage métier, mesurer les résultats avec LangSmith, et déployer avec Docker. Tout le savoir-faire est dans ces 3 jours.


🎓 Ce que vous devez retenir — Chapitre 7

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| "Ça marche" n'est pas une métrique | Recall@k, MRR, coût/req — les chiffres pour décider |
| LangSmith tracing | Trace prompt + réponse + latence + coût automatiquement |
| Benchmark 4 architectures | LLM seul < RAG (85%) < Agent (92%) < Deep Agent (94%) |
| Monitoring des coûts | Un agent coûte 5× plus qu'un appel direct — surveiller |
| Tests E2E human-in-the-loop | Vérifie l'état du système (DB, API, logs), pas le texte |
| Docker Compose | 1 commande lance API + dashboard + vector store |
| 5 bonnes pratiques prod | Cache, .env, retry, health check, graceful degradation |
| 5 risques sécurité | Prompt injection #1 OWASP — middleware + rate limiting |
| Erreurs de déploiement | Modèle rechargé, CORS, package non installé — bêtes mais fréquentes |
| Architecture finale | 7 couches, du prompt au produit déployé en 3 jours |


➡️ Conclusion de la formation

Félicitations. En 3 jours, vous avez parcouru tout l'écosystème LangChain : des fondamentaux des LLM aux Deep Agents en passant par LCEL, le RAG, les agents ReAct, le multimodal, le déploiement Docker et les tests E2E. Vous repartez avec un projet fil rouge complet que vous pouvez adapter à votre propre domaine. La prochaine étape : l'adapter à votre cas d'usage métier et mesurer les résultats avec LangSmith.