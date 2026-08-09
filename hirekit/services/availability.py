"""Availability service — calendrier fictif pour la planification.

AT04 — outil de vérification de disponibilités.
"""

from __future__ import annotations


def check_availability(date: str, duration_minutes: int = 60) -> dict:
    """AT04 — vérifie les créneaux disponibles pour une date donnée."""
    raise NotImplementedError(
        "AT04 — implémentez check_availability() dans hirekit/services/availability.py"
    )
