"""Availability service — calendrier fictif pour la planification.

AT04 — outil de vérification de disponibilités.

Charge le calendrier JSON généré par scripts/generate_availability.py
et permet de vérifier quels candidats sont disponibles à une date donnée.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from hirekit.config import AVAILABILITY_PATH


def load_availability(path: str | Path | None = None) -> dict:
    """AT04 — charge le calendrier de disponibilité depuis le JSON.

    Args:
        path: chemin vers availability.json (défaut: data/availability.json).

    Returns:
        Dictionnaire avec 'candidates' (liste) et 'base_date'.
    """
    file_path = Path(path) if path else AVAILABILITY_PATH
    if not file_path.exists():
        raise FileNotFoundError(
            f"Fichier de disponibilité non trouvé: {file_path}. "
            f"Lancez: python scripts/generate_availability.py"
        )
    return json.loads(file_path.read_text(encoding="utf-8"))


def check_availability(date: str, duration_minutes: int = 60) -> dict:
    """AT04 — vérifie les créneaux disponibles pour une date donnée.

    Parcourt tous les candidats et retourne ceux qui ont au moins un créneau
    disponible à la date spécifiée, avec une durée suffisante.

    Args:
        date: date au format "YYYY-MM-DD".
        duration_minutes: durée minimum requise en minutes (défaut: 60).

    Returns:
        Dictionnaire avec:
        - "date": la date interrogée
        - "available_candidates": liste des candidats disponibles
        - "total_checked": nombre total de candidats vérifiés
    """
    data = load_availability()
    candidates = data.get("candidates", [])

    available_candidates = []
    for candidate in candidates:
        slots = candidate.get("slots", [])
        # Filtrer les créneaux de la date demandée qui sont disponibles
        matching_slots = [
            s for s in slots
            if s["date"] == date and s["available"]
        ]

        if matching_slots:
            # Calculer la durée totale disponible
            total_hours = len(matching_slots)
            available_candidates.append({
                "candidate_id": candidate["candidate_id"],
                "name": candidate["name"],
                "slots": matching_slots,
                "total_available_hours": total_hours,
            })

    return {
        "date": date,
        "available_candidates": available_candidates,
        "total_checked": len(candidates),
        "total_available": len(available_candidates),
    }


def check_candidate_availability(
    candidate_id: str,
    date: str | None = None,
    duration_minutes: int = 60,
) -> dict:
    """AT04 — vérifie la disponibilité d'un candidat spécifique.

    Args:
        candidate_id: identifiant du candidat (ex: "cv_001").
        date: date au format "YYYY-MM-DD" (None = toutes dates).
        duration_minutes: durée minimum en minutes.

    Returns:
        Dictionnaire avec les créneaux disponibles du candidat.
    """
    data = load_availability()
    candidates = data.get("candidates", [])

    for candidate in candidates:
        if candidate["candidate_id"] == candidate_id:
            slots = candidate.get("slots", [])
            if date:
                slots = [s for s in slots if s["date"] == date and s["available"]]
            else:
                slots = [s for s in slots if s["available"]]

            return {
                "candidate_id": candidate_id,
                "name": candidate["name"],
                "date": date or "all",
                "available_slots": slots,
                "total_available": len(slots),
            }

    return {
        "candidate_id": candidate_id,
        "name": "Non trouvé",
        "date": date or "all",
        "available_slots": [],
        "total_available": 0,
    }


def find_best_slots(
    candidate_ids: list[str],
    date: str | None = None,
    min_duration_hours: int = 1,
) -> dict:
    """AT04 — trouve les meilleurs créneaux communs pour plusieurs candidats.

    Utile pour planifier un entretien avec plusieurs candidats simultanément.

    Args:
        candidate_ids: liste d'IDs de candidats.
        date: date au format "YYYY-MM-DD" (None = toutes dates).
        min_duration_hours: durée minimum en heures.

    Returns:
        Dictionnaire avec les créneaux communs disponibles.
    """
    data = load_availability()
    candidates = data.get("candidates", [])

    # Collecter les disponibilités de chaque candidat
    candidate_slots = {}
    for candidate in candidates:
        if candidate["candidate_id"] in candidate_ids:
            slots = candidate.get("slots", [])
            if date:
                slots = [s for s in slots if s["date"] == date and s["available"]]
            else:
                slots = [s for s in slots if s["available"]]

            # Indexer par date+heure pour trouver les créneaux communs
            for slot in slots:
                key = f"{slot['date']}_{slot['start']}"
                if key not in candidate_slots:
                    candidate_slots[key] = {
                        "date": slot["date"],
                        "start": slot["start"],
                        "end": slot["end"],
                        "candidates": [],
                    }
                candidate_slots[key]["candidates"].append(candidate["name"])

    # Filtrer les créneaux où TOUS les candidats sont disponibles
    common_slots = [
        s for s in candidate_slots.values()
        if len(s["candidates"]) == len(candidate_ids)
    ]

    return {
        "candidate_ids": candidate_ids,
        "date": date or "all",
        "common_slots": common_slots,
        "total_common": len(common_slots),
    }