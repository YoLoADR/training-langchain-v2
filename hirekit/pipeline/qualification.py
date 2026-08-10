"""Questions de qualification et constantes de pipeline.

Inspiration: sellkit/src/pipeline/qualification-questions.ts

6 champs de qualification dans l'ordre:
  name → experience → availability → location → revenueGoal → riskAppetite
"""

from __future__ import annotations

FIELD_QUESTIONS: dict[str, str] = {
    "name": "Comment vous appelez-vous ?",
    "experience": (
        "Quelle est votre expérience en développement, ou un autre domaine ? "
        "Pas d'inquiétude si vous n'en avez pas, on forme aussi."
    ),
    "availability": "Vous êtes disponible pour commencer quand ?",
    "location": "Vous êtes dans quel secteur ?",
    "riskAppetite": (
        "Vous êtes à l'aise avec le fait qu'on soit une startup qui opère "
        "dans des zones grises ? Notre modèle juridique est en cours de validation."
    ),
    "revenueGoal": "Vous visez combien par mois ? Un complément ou un vrai revenu ?",
}

FIELD_LABELS_FR: dict[str, str] = {
    "name": "Nom",
    "experience": "Expérience",
    "availability": "Disponibilité",
    "location": "Lieu",
    "revenueGoal": "Revenu visé",
    "riskAppetite": "Risque",
}

QUALIFICATION_ORDER: list[str] = [
    "name",
    "experience",
    "availability",
    "location",
    "revenueGoal",
    "riskAppetite",
]

CLOSING_STAGES: list[str] = ["interested", "qualified", "closed_won", "closed_lost"]
